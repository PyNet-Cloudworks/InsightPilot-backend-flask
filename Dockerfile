# Use official Python image
FROM python:3.10

# Install dependencies (e.g., OpenCV)
RUN apt-get update && apt-get install -y libgl1

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Default command
CMD ["python", "run.py"]
