# Use the official HAPI FHIR image
FROM hapiproject/hapi:latest

# Set working directory
WORKDIR /app

# Install required dependencies
RUN pip install pyyaml requests

# Copy the existing application.yml into the image
COPY conf/application.yml /app/config/application.yml

# Define entrypoint correctly
CMD java --class-path /app/main.war \
    -Dloader.path=main.war!/WEB-INF/classes/,main.war!/WEB-INF/,/app/extra-classes \
    -Dspring.config.location=file:///app/config/application.yml \
    org.springframework.boot.loader.PropertiesLauncher
