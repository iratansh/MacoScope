# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
# Install dependencies for mysqlclient
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project
COPY . /app/

# Create the directory for static files
RUN mkdir -p /app/staticfiles

# Run migrations and collect static files
RUN python manage.py collectstatic --noinput && python manage.py migrate

# Expose port 8080 (your custom port)
EXPOSE 8080

# Run the Django server on port 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
