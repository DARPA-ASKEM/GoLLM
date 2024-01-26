import json
import signal
import sys
import concurrent.futures
import argparse
import os
import time
import threading
from typing import Callable
from core.utils import escape_newlines

def self_destruct(delay: int):
    # if for whatever reason this process is still around, do our best to self destruct
    time.sleep(delay)
    os.kill(os.getpid(), signal.SIGKILL)  # Send the SIGTERM signal to the current process

class TaskRunnerInterface:
    def __init__(self, description: str):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--id', type=str, required=True, help='The id of the request')
        parser.add_argument('--input', type=str, required=False, help='The name of the input pipe')
        parser.add_argument('--input_pipe', type=str, required=False, help='The name of the input pipe')
        parser.add_argument('--output_pipe', type=str, required=False, help='The name of the output pipe')
        parser.add_argument('--self_destruct_timeout_seconds', type=int, default=60*60*24, required=False, help='Process self destruct timeout in seconds')
        args = parser.parse_args()
        self.id = args.id
        self.input = args.input
        self.input_pipe = args.input_pipe
        self.output_pipe = args.input_pipe

        if self.input is None and self.input_pipe is None:
            raise ValueError('Either `input` or `input_pipe` must be specified')

        # Start the self destruct timer
        threading.Thread(target=self_destruct, args=(args.seld_destruct_timeout_seconds)).start()

    def read_input_with_timeout(self, timeout_seconds: int = 30):

        def read_input() -> dict :
            with open(self.input_pipe, 'rb') as f:
                line = f.readline().strip()
                return json.loads(line.decode())

        if self.input is not None:
            return json.loads(self.input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(read_input)
            try:
                return future.result(timeout=timeout_seconds)
            except concurrent.futures.TimeoutError:
                raise TimeoutError('Reading from input pipe timed out')

    def write_output_with_timeout(self, output: dict, timeout_seconds: int = 30):

        def write_output(output: dict):
            bs = (escape_newlines(json.dumps(output)) + "\n").encode()
            with open(self.output_pipe, 'wb') as f_out:
                f_out.write(bs)
                return

        # if no output pipe is specified, just print the output to stdout
        if self.output_pipe is None:
            print(json.dumps(output))
            return

        # otherwise use the output pipe
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(write_output, output)
            try:
                return future.result(timeout=timeout_seconds)
            except concurrent.futures.TimeoutError:
                raise TimeoutError('Writing to output pipe timed out')

    def on_cancellation(self, func : Callable):
        def signal_handler(sig, frame):
            func()
            sys.exit(1)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
