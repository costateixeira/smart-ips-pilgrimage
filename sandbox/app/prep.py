import os
import json
import tarfile
import urllib.request
import yaml
from pathlib import Path

PACKAGE_URL = os.getenv("PACKAGE_URL", "https://costateixeira.github.io/smart-ips-pilgrimage/package.tgz")
CONFIG_PATH = Path("/app/config")  # Location inside the Docker image
APPLICATION_YAML_PATH = CONFIG_PATH / "application.yml"
PACKAGE_DIR = Path("/tmp/package")

def download_package():
    """Download and extract the package tarball."""
    print(f"[INFO] Fetching package from {PACKAGE_URL}...")
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    tar_path = PACKAGE_DIR / "package.tgz"

    urllib.request.urlretrieve(PACKAGE_URL, tar_path)

    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(PACKAGE_DIR)

    print("[INFO] Package extracted.")

def get_package_metadata():
    """Read name and version from package.json inside the extracted package."""
    package_json_path = PACKAGE_DIR / "package/package.json"

    if not package_json_path.exists():
        raise FileNotFoundError("[ERROR] package.json not found in package!")

    with open(package_json_path, "r", encoding="utf-8") as f:
        package_data = json.load(f)

    package_name = package_data.get("name")
    package_version = package_data.get("version")

    if not package_name or not package_version:
        raise ValueError("[ERROR] Missing name or version in package.json!")

    print(f"[INFO] Package Name: {package_name}")
    print(f"[INFO] Package Version: {package_version}")

    return package_name, package_version

def update_application_yaml(package_name, package_version):
    """Modify application.yml inside the Docker image."""
    yaml_key = package_name.replace(".", "__").replace("-", "__")  # Convert for YAML compatibility

    # Read the existing application.yml
    if not APPLICATION_YAML_PATH.exists():
        raise FileNotFoundError("[ERROR] application.yml not found!")

    with open(APPLICATION_YAML_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Update the implementationguides section dynamically
    if "hapi" not in config:
        config["hapi"] = {}
    if "fhir" not in config["hapi"]:
        config["hapi"]["fhir"] = {}
    if "implementationguides" not in config["hapi"]["fhir"]:
        config["hapi"]["fhir"]["implementationguides"] = {}

    config["hapi"]["fhir"]["implementationguides"][yaml_key] = {
        "packageUrl": PACKAGE_URL,
        "name": package_name,
        "version": package_version,
        "reloadExisting": True,
        "installMode": "STORE_AND_INSTALL",
    }

    # Write back the updated YAML
    with open(APPLICATION_YAML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False)

    print(f"[INFO] Updated application.yml with {yaml_key} stored at {APPLICATION_YAML_PATH}")

def main():
    print("[INFO] Starting package preparation...")
    download_package()
    package_name, package_version = get_package_metadata()
    update_application_yaml(package_name, package_version)
    
    print("[INFO] Preparation complete. application.yml is updated.")

if __name__ == "__main__":
    main()
