FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

ENV OPENAI_API_KEY=""

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.run:app", "--host", "0.0.0.0", "--port", "8000"]