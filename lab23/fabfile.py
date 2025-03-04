from fabric import Connection, task, Config
import os
import subprocess

# --- Configuration ---
SERVER_HOST = "SERVER_IP"
SERVER_USER = "deploy_user"
SSH_PRIVATE_KEY_PATH = "path-to-ssh-key"
DEPLOY_PATH = "path-to-deploy"
GIT_REPO_URL = "https://github.com/your-username/your-repo.git"  # HTTPS URL
BRANCH = "main"
REQUIREMENTS_FILE = "requirements.txt"
APP_RUN_COMMAND = "python3 app.py"  # Run directly; nohup not strictly needed with PID file
PID_FILE = f"{DEPLOY_PATH}/app.pid" # Define PID_FILE

# --- Fabric Configuration ---
config = Config(
    overrides={
        'sudo': {},
        'connect_kwargs': {
            'key_filename': [SSH_PRIVATE_KEY_PATH],
        },
    }
)

# --- Helper Function for Running Remote Commands ---
def run_remote_command(command):
    """Runs a command on the remote server using subprocess.run."""
    ssh_command = f'"{os.environ["COMSPEC"]}" /c ssh -i "{SSH_PRIVATE_KEY_PATH}" {SERVER_USER}@{SERVER_HOST} "{command}"'
    try:
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True, check=True)
        print(f"  Stdout: {result.stdout.strip()}")
        print(f"  Stderr: {result.stderr.strip()}")
        print(f"  Return Code: {result.returncode}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running remote command: {command}")
        print(f"  Return Code: {e.returncode}")
        print(f"  Stdout: {e.stdout.strip()}")
        print(f"  Stderr: {e.stderr.strip()}")
        return e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return e


# --- Fabric Tasks ---

@task
def git_pull(c):
    print("--- STARTING git_pull ---")
    run_remote_command(f"cd {DEPLOY_PATH} && pwd")
    print(f"Attempting to change to: {DEPLOY_PATH}")
    run_remote_command(f"cd {DEPLOY_PATH} && pwd")
    print("Running: git fetch origin main")
    run_remote_command(f"cd {DEPLOY_PATH} && git fetch origin {BRANCH}")
    run_remote_command(f"cd {DEPLOY_PATH} && git checkout {BRANCH}")
    run_remote_command(f"cd {DEPLOY_PATH} && git reset --hard origin/{BRANCH}")
    print("--- ENDING git_pull ---")

@task
def install_dependencies(c):
    requirements_path = os.path.join(DEPLOY_PATH, REQUIREMENTS_FILE).replace("\\","/")
    print(f"Checking for requirements file at: {requirements_path}")
    requirements_path = os.path.normpath(requirements_path).replace("\\", "/")
    print(f"Normalized requirements path: {requirements_path}")
    if run_remote_command(f"cd {DEPLOY_PATH} && test -f {requirements_path}").returncode == 0:
        print("Installing Python dependencies...")
        run_remote_command(f"cd {DEPLOY_PATH} && pip install -r {REQUIREMENTS_FILE}")
    else:
        print("requirements.txt not found on the server, skipping dependency installation.")

@task
def run_app(c):
    print("Running 'python_project' application...")
    run_remote_command(f"cd {DEPLOY_PATH} && {APP_RUN_COMMAND} > app.log 2>&1 &") # Run in background

@task
def stop_app(c):
    print("Stopping 'python_project' application...")
    if run_remote_command(f"test -f {PID_FILE}").returncode == 0:
        run_remote_command(f"kill -TERM $(cat {PID_FILE})")
        run_remote_command(f"rm -f {PID_FILE}")
    else:
        print("PID file not found.  Application may not be running.")

@task
def deploy(c):
    print(f"Deploying 'python_project' to server {SERVER_HOST}...")

    normalized_deploy_path = os.path.normpath(DEPLOY_PATH).replace("\\", "/")
    print(f"Normalized path: {normalized_deploy_path}")

    # --- Check if the directory exists; create it if it doesn't ---
    if run_remote_command(f"test -d {normalized_deploy_path}").returncode != 0:
        print(f"Directory '{normalized_deploy_path}' does not exist; creating it.")
        run_remote_command(f"mkdir -p {normalized_deploy_path}")

    # --- Check if the repository has been cloned; clone it if it hasn't ---
    if run_remote_command(f"test -d {normalized_deploy_path}/.git").returncode != 0:
        print(f"Repository not found in '{normalized_deploy_path}'; cloning.")
        # --- Remove any existing files/directories within the deploy path ---
        print(f"Removing existing files in '{normalized_deploy_path}'...")
        run_remote_command(f"rm -rf {normalized_deploy_path}/* {normalized_deploy_path}/.[!.]*")
        # --- Capture output during cloning ---
        result = run_remote_command(f"git clone {GIT_REPO_URL} {normalized_deploy_path}")
        print(f"  Clone Stdout: {result.stdout.strip()}")
        print(f"  Clone Stderr: {result.stderr.strip()}")
    else:
        print(f"Repository already cloned in '{normalized_deploy_path}'.")

    run_remote_command(f"cd {normalized_deploy_path}")
    stop_app(c)  # Stop the app before updating
    git_pull(c)
    install_dependencies(c)
    run_app(c)  # Start the app

    print("'python_project' deployment and run completed! ...")

# --- Create a Collection and add tasks ---
from invoke import Collection
ns = Collection(deploy)
ns.add_task(git_pull)
ns.add_task(install_dependencies)
ns.add_task(run_app)
ns.add_task(stop_app) # Add stop_app task
ns.configure(config)
