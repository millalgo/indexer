# Use official Python image
FROM python:3.12-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install client and build tools
RUN apt-get update && \
    apt-get install -y \
      postgresql-client \
      libpq-dev \
      gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Run entrypoint script to init. database
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
