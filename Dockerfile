# Use a minimal base image for Python
FROM python:3.9-slim

# Set a working directory inside the container
WORKDIR /app

# Copy your ETL script into the container
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt

# Command to run your ETL script
CMD ["python", "food_insights_etl_script.py"]
