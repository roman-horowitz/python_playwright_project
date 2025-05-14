FROM mcr.microsoft.com/playwright/python:v1.52.0-noble

WORKDIR /app

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy rest of the project
COPY . .

RUN pip install .

# Ensure the entrypoint script is executable
RUN chmod +x run.sh

ENTRYPOINT ["pytest"]
