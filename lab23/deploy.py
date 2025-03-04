from fabric import Connection, task, Config, Group
from fabric.exceptions import GroupException
import os

# --- Configuration ---
SERVER_HOST = "your_server_ip_or_hostname"      # Replace with your server IP or hostname
SERVER_USER = "your_server_username"            # Replace with your SSH username on the server
# SERVER_PASSWORD = "your_server_password"        # REMOVED:  Using private key instead of password
SSH_PRIVATE_KEY_PATH = "~/.ssh/id_rsa"         # **IMPORTANT:** Replace with the path to your private key file! (e.g., ~/.ssh/id_rsa, ~/.ssh/my_deploy_key)
DEPLOY_PATH = "/path/to/your/deploy/directory" # Replace with deployment directory path on the server (e.g., /var/www/python_project)
GIT_REPO_URL = "git@github.com:your_username/python_project.git" # **IMPORTANT:** Replace with your GitHub repository URL for 'python_project'
BRANCH = "main"                                 # Branch to deploy (e.g., main, master, develop)
REQUIREMENTS_FILE = "requirements.txt"          # Name of your requirements file (if any)
APP_RESTART_COMMAND = "sudo systemctl restart python_project_service" # Command to restart your web app (systemd service example - customize!)

# --- Fabric Configuration (Optional but Recommended) ---
config = Config(
    overrides={
        'sudo': {}, # sudo settings - we'll configure password prompt if needed later (less common with keys)
        'connect_kwargs': {
            'key_filename': [SSH_PRIVATE_KEY_PATH]  # Specify private key path for connection
        }
    }
)
group = Group(SERVER_HOST, user=SERVER_USER, config=config) # Group of servers


# --- Fabric Tasks ---

@task
def deploy(c): # 'c' is the Connection object
    print(f"Deploying 'python_project' to server {SERVER_HOST} using private key authentication...")

    with c.cd(DEPLOY_PATH):
        git_pull(c)
        install_dependencies(c)
        configure_app(c)
        restart_app(c)

    print("'python_project' deployment completed successfully!")


@task
def git_pull(c):
    print("Updating code from GitHub repository...")
    c.run(f"git fetch origin {BRANCH}")
    c.run(f"git checkout {BRANCH}")
    c.run(f"git reset --hard origin/{BRANCH}")

@task
def install_dependencies(c):
    if REQUIREMENTS_FILE and os.path.exists(REQUIREMENTS_FILE):
        print("Installing Python dependencies...")
        c.run(f"pip install -r {REQUIREMENTS_FILE}")
    else:
        print("requirements.txt not found, skipping dependency installation.")


@task
def configure_app(c):
    # --- CUSTOMIZE THIS TASK! ---
    print("--- Configuring 'python_project' Application (CUSTOMIZE THIS TASK!) ---")
    print("You need to customize the 'configure_app' task...")
    # ... (your custom configuration steps here) ...

@task
def restart_app(c):
    # --- CUSTOMIZE THIS TASK! ---
    print("--- Restarting 'python_project' Application (CUSTOMIZE THIS TASK!) ---")
    print("You need to customize the 'restart_app' task...")
    if APP_RESTART_COMMAND:
        print(f"Executing restart command: '{APP_RESTART_COMMAND}'")
        c.sudo(APP_RESTART_COMMAND)
    else:
        print("APP_RESTART_COMMAND is not configured, skipping application restart.")


# --- Run the script ---
if __name__ == "__main__":
    try:
        group.run(deploy)
    except GroupException as e:
        print("Error during deployment to one or more servers:")
        print(e)
        exit(1)
