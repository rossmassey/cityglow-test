# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install Python dependencies including Django and uvicorn
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir \
        django>=5.2.0 \
        uvicorn[standard]>=0.24.0 \
        gunicorn>=21.0.0

# Copy project files
COPY . .

# Create directory for static files
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Run database migrations
RUN python manage.py migrate

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Expose port
EXPOSE $PORT

# Command to run the application
CMD exec uvicorn api.asgi:application --host 0.0.0.0 --port $PORT --workers 1 