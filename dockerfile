# Dockerfile for github action
FROM python:3.11-slim
WORKDIR /oxr_salesforce
# Copy all repository files into the container
COPY . .
# Install dependencies & the package
RUN pip install -e .