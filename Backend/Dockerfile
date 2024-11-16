# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project
COPY . /app/

# Run migrations and collect static files
RUN python manage.py collectstatic --noinput && python manage.py migrate

# Expose port 8080 (your custom port)
EXPOSE 8080

# Run the Django server on port 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
