FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install required dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . /app/

# Copy Firebase credentials
COPY firebase-key.json /app/firebase-key.json

# Copy the .env file (this includes GOOGLE_APPLICATION_CREDENTIALS)
COPY .env /app/.env

# Expose the port Flask runs on
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app.main:app"]
