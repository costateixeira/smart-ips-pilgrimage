import json
import os
import sys
import tarfile
import urllib.request
import requests
import time
from pathlib import Path


def debug_log(message):
    print(f"[DEBUG] {message}")


def download_fhir_package(url, output_path):
    """
    Downloads the FHIR package tarball from a given URL and saves it to output_path.
    """
    print(f"Downloading FHIR package from {url}...")
    urllib.request.urlretrieve(url, output_path)
    print(f"Downloaded FHIR package to {output_path}")

def extract_fhir_resources(package_tar, mode, extract_dir):
    """
    Extracts FHIR resources from the specified package tarball based on the mode,
    excluding a single ImplementationGuide resource if present.
    """
    with tarfile.open(package_tar, "r:gz") as tar:
        tar.extractall(extract_dir)
    
    package_path = Path(extract_dir) / "package"
    folders = []
    
    if mode in ("CONFORMANCE", "ALL"):
        folders.append(package_path)
    if mode in ("EXAMPLE", "ALL"):
        folders.append(package_path / "example")
    
    resources = []
    implementation_guide_count = 0
    
    for folder in folders:
        if folder.exists() and folder.is_dir():
            for file in folder.glob("*.json"):
                with open(file, "r", encoding="utf-8") as f:
                    resource = json.load(f)
                    if resource.get("resourceType") == "ImplementationGuide":
                        implementation_guide_count += 1
                        continue  # Skip if there's only one IG
                    if "resourceType" in resource and "id" in resource:
                        resource_url = f"{resource['resourceType']}/{resource['id']}"
                        resources.append({
                            "request": {
                                "method": "PUT",
                                "url": resource_url
                            },
                            "resource": resource
                        })
    
    return resources if implementation_guide_count <= 1 else resources

def create_transaction_bundle(resources):
    """
    Creates a FHIR transaction Bundle containing the extracted resources.
    """
    return {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": resources
    }

def wait_for_fhir_server(fhir_server_url, timeout=120, interval=10):
    """
    Waits for the FHIR server to become available before posting the Bundle.
    """
    print(f"Waiting for FHIR server at {fhir_server_url} to become available...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{fhir_server_url}/metadata", timeout=5)
            if response.status_code == 200:
                print("FHIR server is available.")
                return True
        except requests.RequestException:
            pass
        print("FHIR server not ready, retrying...")
        time.sleep(interval)
    print("Timeout reached, FHIR server not available.")
    return False

def post_bundle_to_fhir_server(bundle, fhir_server_url):
    """
    Posts the FHIR transaction Bundle to the specified FHIR server.
    """
    headers = {
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json"
    }
    response = requests.post(fhir_server_url, json=bundle, headers=headers)
    print(f"FHIR server response: {response.status_code} {response.text}")

def main():
    debug_log(f"Command-line arguments: {sys.argv}")
    package_source = sys.argv[1] if len(sys.argv) > 1 else None
    mode = sys.argv[2].upper() if len(sys.argv) > 2 else "EXAMPLE"
    fhir_server_url = sys.argv[3] if len(sys.argv) > 3 else None
    timeout = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 120
    
    debug_log(f"Parsed arguments - package_source: {package_source}, mode: {mode}, fhir_server_url: {fhir_server_url}, timeout: {timeout}")
    
    if not package_source:
        print("Usage: python script.py <FHIR_PACKAGE_TAR_OR_URL> [MODE] [FHIR_SERVER_URL] [TIMEOUT]")
        print("MODE defaults to: EXAMPLE. Available options: CONFORMANCE, EXAMPLE, ALL")
        sys.exit(1)
    
    extract_dir = Path("extracted_package")
    extract_dir.mkdir(exist_ok=True)
    
    package_tar = Path("fhir_package.tgz")
    
    if package_source.startswith("http://") or package_source.startswith("https://"):
        download_fhir_package(package_source, package_tar)
    else:
        package_tar = Path(package_source)
    
    if mode not in {"CONFORMANCE", "EXAMPLE", "ALL"}:
        print("Invalid mode. Choose from: CONFORMANCE, EXAMPLE, or ALL")
        sys.exit(1)
    
    resources = extract_fhir_resources(package_tar, mode, extract_dir)
    bundle = create_transaction_bundle(resources)
    
    output_file = Path(extract_dir) / "fhir_transaction_bundle.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)
    
    debug_log(f"FHIR transaction Bundle saved to {output_file}")
    
    if fhir_server_url:
        debug_log(f"Waiting for FHIR server: {fhir_server_url}")
        if wait_for_fhir_server(fhir_server_url, timeout):
            debug_log(f"Posting Bundle to FHIR server: {fhir_server_url}")
            post_bundle_to_fhir_server(bundle, fhir_server_url)
        else:
            debug_log("Skipping upload: FHIR server is not available.")

if __name__ == "__main__":
    main()
