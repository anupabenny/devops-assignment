# Use an official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the main.py file into the working directory
COPY main.py /app/

# Install necessary Python libraries
RUN pip install fastapi uvicorn psutil prometheus_client

# Expose port 8000 for the application
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]