# Dockerfile for github action
FROM python:3.11-slim
WORKDIR /action
# Copy all repository files into the container
COPY . .
# Install dependencies & the package
RUN pip install --no-cache-dir -r requirements.txt -e .