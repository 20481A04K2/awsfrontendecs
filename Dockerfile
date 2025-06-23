# Use Amazon Public ECR base image to avoid Docker Hub rate limits
FROM public.ecr.aws/docker/library/python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir Flask requests boto3

# Expose port 8080
EXPOSE 8080

# Run the Flask app
CMD ["python3", "app.py"]
