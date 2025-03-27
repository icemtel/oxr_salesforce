FROM python:3.11-slim

WORKDIR /action

# Copy all repository files into the container
COPY . .
RUN ls
# Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt

# Run the update script
#CMD ["python", "update_exchange_rates.py"]