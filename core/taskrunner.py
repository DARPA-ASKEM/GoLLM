import json
import signal
import sys
import concurrent.futures
import argparse
from core.utils import escape_newlines

class TaskRunnerInterface:
    def __init__(self, description: str):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--input_pipe', type=str, required=True, help='The name of the input pipe')
        parser.add_argument('--output_pipe', type=str, required=True, help='The name of the output pipe')
        args = parser.parse_args()
        self.input_pipe = args.input_pipe
        self.output_pipe = args.input_pipe

    def read_input(self) -> dict :
        with open(self.input_pipe, 'rb') as f:
            line = f.readline().strip()
            return json.loads(line.decode())

    def read_input_with_timeout(self, timeout_seconds: int = 30):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.read_input)
            try:
                return future.result(timeout=timeout_seconds)
            except concurrent.futures.TimeoutError:
                raise TimeoutError('Reading from input pipe timed out')

    def write_output(self, output: dict):
        bs = (escape_newlines(json.dumps(output)) + "\n").encode()
        with open(self.output_pipe, 'wb') as f_out:
            f_out.write(bs)
            return

    def write_output_with_timeout(self, output: dict, timeout_seconds: int = 30):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.write_output, output)
            try:
                return future.result(timeout=timeout_seconds)
            except concurrent.futures.TimeoutError:
                raise TimeoutError('Writing to output pipe timed out')

    def on_cancellation(self, func : function):
        def signal_handler(sig, frame):
            func()
            sys.exit(1)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
