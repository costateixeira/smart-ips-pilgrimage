# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the script into the container
COPY packinstall.py /app/packinstall.py
COPY entrypoint.sh /app/entrypoint.sh

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Install required Python dependencies
RUN pip install requests

# Define the command to run the script
#ENTRYPOINT ["python", "/app/packinstall.py"]

# Use the entrypoint script to ensure correct execution
ENTRYPOINT ["/app/entrypoint.sh"]
