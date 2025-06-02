FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Install dependencies
RUN pip install Flask requests

# Expose port 8080
EXPOSE 8080

# Run the Flask app
CMD ["python3", "app.py"]
