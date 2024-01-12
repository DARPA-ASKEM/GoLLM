FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

ENV OPENAI_API_KEY=""

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code
COPY . .

# Set the command to run your script
ENTRYPOINT ["python", "./config_from_paper.py"]