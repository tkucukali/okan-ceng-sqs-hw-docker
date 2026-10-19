# 1. Pinned base image
FROM python:3.11-slim

WORKDIR /app

# 2. Cache-friendly order: Copy and install requirements before code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# 3. Non-root user: Create an unprivileged user for security
RUN useradd --create-home --uid 10000 appuser
USER appuser

# Configuration via Environment Variables
ENV AUTHOR_NAME="Tolgahan"
ENV PORT=8080

EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]