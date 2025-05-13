FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["pytest"]
