FROM python:3.11-slim

# Install wkhtmltopdf
RUN apt-get update && \
    apt-get install -y wkhtmltopdf && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
