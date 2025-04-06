import os
import subprocess
import json
import sys

def find_json_key(directory):
    """Find the first .json file in the specified directory."""
    try:
        for file in os.listdir(directory):
            if file.endswith(".json"):
                return os.path.join(directory, file)
        raise FileNotFoundError("No .json file found in the directory.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

def load_json(json_path):
    """Load the JSON file to validate it."""
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

def install_gcloud_sdk():
    """Install Google Cloud SDK."""
    print("Installing Google Cloud SDK...")
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run([
        "sudo", "apt", "install", "-y", "apt-transport-https", "ca-certificates", "gnupg"
    ], check=True)
    subprocess.run([
        "curl", "https://packages.cloud.google.com/apt/doc/apt-key.gpg", "|",
        "sudo", "tee", "/usr/share/keyrings/cloud.google.gpg"
    ], shell=True, check=True)
    subprocess.run([
        "echo", "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list"
    ], shell=True, check=True)
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt", "install", "-y", "google-cloud-sdk"], check=True)

def set_application_credentials(json_path):
    """Set the GOOGLE_APPLICATION_CREDENTIALS environment variable."""
    print(f"Setting GOOGLE_APPLICATION_CREDENTIALS to {json_path}")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
    # Optionally export it for future terminal sessions
    with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
        bashrc.write(f'\nexport GOOGLE_APPLICATION_CREDENTIALS="{json_path}"\n')

def activate_service_account(json_path):
    """Activate Google Cloud Service Account."""
    print("Activating service account...")
    subprocess.run([
        "gcloud", "auth", "activate-service-account", "--key-file", json_path
    ], check=True)

def set_project(project_id):
    """Set the default Google Cloud project."""
    print(f"Setting default project to {project_id}...")
    subprocess.run([
        "gcloud", "config", "set", "project", project_id
    ], check=True)

def main():
    key_directory = "/path/to/keys"  # Replace with the actual directory containing your JSON key
    print(f"Searching for .json key file in {key_directory}...")

    # Find the JSON key file
    json_path = find_json_key(key_directory)
    print(f"Found key file: {json_path}")

    # Validate the JSON key
    config = load_json(json_path)

    # Install Google Cloud SDK if not already installed
    try:
        subprocess.run(["gcloud", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Google Cloud SDK is already installed.")
    except FileNotFoundError:
        install_gcloud_sdk()

    # Set the environment variable for the key
    set_application_credentials(json_path)

    # Authenticate using the service account key
    activate_service_account(json_path)

    # Optionally set the project if it's specified in the JSON
    project_id = config.get("project_id", None)
    if project_id:
        set_project(project_id)

    print("Google Cloud environment setup completed successfully.")

if __name__ == "__main__":
    main()
