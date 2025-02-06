FROM hapiproject/hapi:latest

# Copy files directly (they will be created automatically)
COPY conf /data/hapi
COPY web /custom
COPY apps /apps

# Set environment variable for configuration
ENV SPRING_CONFIG_LOCATION=file:///data/hapi/application.yml

# Expose necessary ports
EXPOSE 8080

# Start HAPI server
CMD ["java", "-jar", "/app/hapi-fhir-cli.jar"]
