#!/bin/sh
set -e

echo "[INFO] Checking if application.yml is present..."
if [ ! -f /app/config/application.yml ]; then
    echo "[INFO] No prebuilt application.yml found. Processing at runtime..."
    
    TMP_DIR="/tmp/package"
    mkdir -p "$TMP_DIR"
    cd "$TMP_DIR"

    # Download the package
    wget -q "${PACKAGE_URL}" -O package.tgz

    # Extract the tarball
    tar -xzf package.tgz

    # Locate package.json inside the extracted folder
    PACKAGE_JSON=$(find . -name package.json | head -n 1)

    if [ -z "$PACKAGE_JSON" ]; then
        echo "[ERROR] package.json not found in package!"
        exit 1
    fi

    # Extract name and version from package.json
    PACKAGE_NAME=$(jq -r '.name' "$PACKAGE_JSON")
    PACKAGE_VERSION=$(jq -r '.version' "$PACKAGE_JSON")

    if [ -z "$PACKAGE_NAME" ] || [ -z "$PACKAGE_VERSION" ]; then
        echo "[ERROR] Missing name or version in package.json!"
        exit 1
    fi

    # Convert PACKAGE_NAME to a YAML-compatible key
    PACKAGE_KEY=$(echo "$PACKAGE_NAME" | sed 's/[.-]/__/g')

    echo "[INFO] Package Name: $PACKAGE_NAME"
    echo "[INFO] Package Version: $PACKAGE_VERSION"
    echo "[INFO] YAML Key: $PACKAGE_KEY"

    # Replace placeholders in application.yml.template and generate application.yml
    export PACKAGE_URL PACKAGE_NAME PACKAGE_VERSION PACKAGE_KEY
    envsubst < /app/config/application.yml.template > /app/config/application.yml
fi

echo "[INFO] Starting FHIR server..."
exec java --class-path /app/main.war \
    -Dloader.path=main.war!/WEB-INF/classes/,main.war!/WEB-INF/,/app/extra-classes \
    -Dspring.config.location=file:///app/config/application.yml \
    org.springframework.boot.loader.PropertiesLauncher
