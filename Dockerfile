# Use the official Python image from Docker Hub
FROM python:3.13.1

# Set environment variables to prevent Python from writing pyc files and to avoid buffering of output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (needed for PostgreSQL and building dependencies)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose the port the app runs on (default for Django is 8000)
EXPOSE 7500

# Start the Django development server (or replace with a production-ready WSGI server like Gunicorn)
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:7500"]
