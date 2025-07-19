# Use Python as the base image
FROM python:3.10-slim

# Don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Show logs instantly
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the whole project
COPY . .

# Command to run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
