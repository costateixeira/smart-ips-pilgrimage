import os
import json
import tarfile
import urllib.request
import yaml
from pathlib import Path

PACKAGE_URL = os.getenv("PACKAGE_URL", "https://costateixeira.github.io/smart-ips-pilgrimage/package.tgz")
CONFIG_PATH = Path("/app/config")
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
    """Modify application.yml inside the Docker build."""
    yaml_key = package_name.replace(".", "__").replace("-", "__")  # Convert for YAML compatibility

    # Read the existing application.yml.template
    application_yaml_template = CONFIG_PATH / "application.yml.template"
    if not application_yaml_template.exists():
        raise FileNotFoundError("[ERROR] application.yml.template not found!")

    with open(application_yaml_template, "r", encoding="utf-8") as f:
        yaml_content = f.read()

    # Replace placeholders
    yaml_content = yaml_content.replace("{{PACKAGE_URL}}", PACKAGE_URL)
    yaml_content = yaml_content.replace("{{PACKAGE_NAME}}", package_name)
    yaml_content = yaml_content.replace("{{PACKAGE_VERSION}}", package_version)
    yaml_content = yaml_content.replace("{{PACKAGE_KEY}}", yaml_key)

    # Write back the updated YAML
    with open(APPLICATION_YAML_PATH, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    print(f"[INFO] Updated application.yml stored at {APPLICATION_YAML_PATH}")

def main():
    print("[INFO] Starting package preparation...")
    download_package()
    package_name, package_version = get_package_metadata()
    update_application_yaml(package_name, package_version)
    
    print("[INFO] Preparation complete. application.yml is updated.")

if __name__ == "__main__":
    main()
