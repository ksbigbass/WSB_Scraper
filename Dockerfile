# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system dependencies for Tkinter and GUI backends
RUN apt-get update && apt-get install -y \
    tk8.6 \
    tcl8.6 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Copy and install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for PRAW (pass at runtime for security; do not hardcode)
# ENV REDDIT_CLIENT_ID="FwwowWJjJ3qa2A"
# ENV REDDIT_CLIENT_SECRET="kOGPQcJYvl5Ncu5VPZ7T2yOnbezOFw"
# ENV REDDIT_USER_AGENT=""

# Run the script when the container launches
CMD ["python", "reddit_scraper.py"]