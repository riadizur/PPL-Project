# Use the official Python 3.8 image from DockerHub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . /

# Install the necessary Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary port (optional, depending on your application)
EXPOSE 8000

# Run the app (replace 'app.py' with your app entry point)
CMD ["python", "app.py"]