#!/bin/sh
set -e

# Ensure all variables have valid defaults
FHIR_PACKAGE_URL=${FHIR_PACKAGE_URL:-"https://costateixeira.github.io/smart-ips-pilgrimage/package.tgz"}
MODE=${MODE:-"EXAMPLE"}
FHIR_SERVER_URL=${FHIR_SERVER_URL:-""}
TIMEOUT=${TIMEOUT:-120}

echo "[DEBUG] Running script with: $FHIR_PACKAGE_URL $MODE $FHIR_SERVER_URL $TIMEOUT"

exec python /app/packinstall.py "$FHIR_PACKAGE_URL" "$MODE" "$FHIR_SERVER_URL" "$TIMEOUT"