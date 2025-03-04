from fabric import Connection, task, Config, Group
from fabric.exceptions import GroupException
import os

# --- Configuration ---
SERVER_HOST = "your_server_ip_or_hostname"      # Replace with your server IP or hostname (e.g., your_server_public_ip)
SERVER_USER = "your_server_username"            # Replace with your SSH username on the server
SSH_PRIVATE_KEY_PATH = "~/.ssh/id_rsa"         # **IMPORTANT:** Replace with the path to your private key file!
DEPLOY_PATH = "/path/to/your/deploy/directory" # Replace with deployment directory path on the server (e.g., /home/your_user/python_project) - MUST EXIST ON SERVER
GIT_REPO_URL = "git@github.com:your_username/python_project.git" # **IMPORTANT:** Replace with your GitHub repo URL for 'python_project'
BRANCH = "main"                                 # Branch to deploy
REQUIREMENTS_FILE = "requirements.txt"          # Name of requirements file
APP_RUN_COMMAND = "python app.py"               # Command to run your Flask app (in foreground for simple test)
APP_RESTART_COMMAND = "" # We'll run app directly for test, so no restart needed in this simplified version

# --- Fabric Configuration ---
config = Config(
    overrides={
        'sudo': {},
        'connect_kwargs': {
            'key_filename': [SSH_PRIVATE_KEY_PATH]
        }
    }
)
group = Group(SERVER_HOST, user=SERVER_USER, config=config)

# --- Fabric Tasks ---

@task
def deploy(c):
    print(f"Deploying 'python_project' to server {SERVER_HOST}...")

    with c.cd(DEPLOY_PATH):
        git_pull(c)
        install_dependencies(c)
        configure_app(c) # Keep this task for future configuration if needed
        run_app(c)        # Run the application directly after deployment

    print("'python_project' deployment and run completed! Access your app at http://{SERVER_HOST}:5000/ in your browser (if port 5000 is exposed)")


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
    # --- CUSTOMIZE THIS TASK (Optional for now, keep for future config) ---
    print("--- Configuring 'python_project' Application (CUSTOMIZE THIS TASK if needed in future) ---")
    print("configure_app task is currently minimal. Customize it for specific configuration steps if your app requires them.")
    pass # Add any configuration steps here in future if required

@task
def run_app(c):
    print("Running 'python_project' application...")
    with c.cd(DEPLOY_PATH): # Ensure we are in the deploy directory when running app
        c.run(APP_RUN_COMMAND) # Run the Flask app in foreground for testing

@task
def restart_app(c): # Restart task is not used in this simplified version, but kept for potential future use
    # --- CUSTOMIZE THIS TASK if you want to use a proper restart command later ---
    print("--- Restarting 'python_project' Application (CUSTOMIZE THIS TASK if needed in future for background process) ---")
    print("restart_app task is currently minimal. Customize it for proper application restart command (e.g., using systemd, supervisor, etc.) if needed for background running.")
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
