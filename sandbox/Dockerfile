# Stage 1: Use Python to process package.json and generate application.yml
FROM python:3.10-slim AS prep

# Set working directory
WORKDIR /app

# Install required dependencies for processing package.json
RUN pip install pyyaml requests

# Copy the application.yml template
COPY conf/application.yml.template /app/config/application.yml.template

# Copy the package processing script
COPY entrypoint.py /app/entrypoint.py

# Define build-time argument for PACKAGE_URL
ARG PACKAGE_URL
ENV PACKAGE_URL=${PACKAGE_URL}

# Run the Python script to process package.json and generate application.yml
RUN if [ -z "$PACKAGE_URL" ]; then echo "[ERROR] PACKAGE_URL is empty!"; exit 1; fi \
    && python /app/entrypoint.py

# Copy entrypoint script and set correct permissions in the prep stage
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && ls -l /app/entrypoint.sh && cat -A /app/entrypoint.sh

# Stage 2: Build the final HAPI FHIR server image
FROM hapiproject/hapi:latest

# Set working directory
WORKDIR /app

# Copy the modified application.yml from the first stage
COPY --from=prep /app/config/application.yml /app/config/application.yml

# Copy the already-executable entrypoint script
COPY --from=prep /app/entrypoint.sh /app/entrypoint.sh

# Use ENTRYPOINT with exec to avoid needing a shell
ENTRYPOINT ["/app/entrypoint.sh"]
