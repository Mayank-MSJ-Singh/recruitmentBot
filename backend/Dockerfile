# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/app

# Set work directory
WORKDIR $WORKDIR

# Install system dependencies (build-essential needed for compiling certain packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt $WORKDIR/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code
COPY . $WORKDIR/

# Expose port 8000
EXPOSE 8000

# Run the app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
