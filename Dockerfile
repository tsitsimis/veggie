FROM python:3.11.4-slim

# Install git
RUN apt-get update && apt-get install -y git

# Install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /
COPY . .

ENV PYTHONPATH=.
