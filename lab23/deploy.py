from fabric import Connection, task, Config, Group
from fabric.exceptions import GroupException
import os

# --- Configuration ---
SERVER_HOST = "your_server_ip_or_hostname"      # Replace with your server IP or hostname
SERVER_USER = "your_server_username"            # Replace with your SSH username on the server
SERVER_PASSWORD = "your_server_password"        # **DO NOT store password directly in script! See "Security" below**
DEPLOY_PATH = "/path/to/your/deploy/directory" # Replace with deployment directory path on the server (e.g., /var/www/python_project)
GIT_REPO_URL = "git@github.com:your_username/python_project.git" # **IMPORTANT:** Replace with your GitHub repository URL for 'python_project'
BRANCH = "main"                                 # Branch to deploy (e.g., main, master, develop)
REQUIREMENTS_FILE = "requirements.txt"          # Name of your requirements file (if any)
APP_RESTART_COMMAND = "sudo systemctl restart python_project_service" # Command to restart your web app (systemd service example - customize!)

# --- Fabric Configuration (Optional but Recommended) ---
config = Config(overrides={'sudo': {'password': SERVER_PASSWORD}}) # If using sudo and need password
group = Group(SERVER_HOST, user=SERVER_USER, config=config) # Group of servers (can add more servers to this group if needed)

# --- Fabric Tasks ---

@task
def deploy(c): # 'c' is the Connection object, representing the SSH connection
    print(f"Deploying 'python_project' to server {SERVER_HOST}...")

    with c.cd(DEPLOY_PATH): # Change directory on the server
        git_pull(c)
        install_dependencies(c)
        configure_app(c) # Customize this task for your 'python_project' configuration
        restart_app(c)   # Customize this task for your 'python_project' restart

    print("'python_project' deployment completed successfully!")


@task
def git_pull(c):
    print("Updating code from GitHub repository...")
    c.run(f"git fetch origin {BRANCH}") # Fetch latest branch info
    c.run(f"git checkout {BRANCH}")    # Switch to the deployment branch (if needed)
    c.run(f"git reset --hard origin/{BRANCH}") # Update to the latest code, discarding local changes (use with caution!)

@task
def install_dependencies(c):
    if REQUIREMENTS_FILE and os.path.exists(REQUIREMENTS_FILE): # Check if requirements.txt exists
        print("Installing Python dependencies...")
        c.run(f"pip install -r {REQUIREMENTS_FILE}")
    else:
        print("requirements.txt not found, skipping dependency installation.")


@task
def configure_app(c):
    # --- CUSTOMIZE THIS TASK! ---
    # Implement configuration steps specific to your 'python_project'
    # Examples:
    # - Create or update configuration files (settings.ini, .env, etc.)
    # - Set environment variables
    # - Migrate database (if applicable)
    print("--- Configuring 'python_project' Application (CUSTOMIZE THIS TASK!) ---")
    print("You need to customize the 'configure_app' task to perform specific configuration steps for your 'python_project'.")
    # Example (Illustrative - adapt to your needs):
    # c.run("cp config_template.ini app_config.ini") # Copy config template
    # c.run("sed -i 's/PLACEHOLDER_VALUE/actual_value/g' app_config.ini") # Replace placeholders

@task
def restart_app(c):
    # --- CUSTOMIZE THIS TASK! ---
    # Implement the command to restart your 'python_project' web server/application
    # Examples:
    # - Restart systemd service: c.sudo("systemctl restart python_project_service") (most common for production)
    # - Restart Supervisor process: c.run("supervisorctl restart python_project_process")
    # - Restart Gunicorn/uWSGI process directly (less recommended for production)
    print("--- Restarting 'python_project' Application (CUSTOMIZE THIS TASK!) ---")
    print("You need to customize the 'restart_app' task to execute the correct restart command for your 'python_project'.")
    if APP_RESTART_COMMAND:
        print(f"Executing restart command: '{APP_RESTART_COMMAND}'")
        c.sudo(APP_RESTART_COMMAND) # Use sudo if admin privileges are needed to restart the service
    else:
        print("APP_RESTART_COMMAND is not configured, skipping application restart.")


# --- Run the script ---
if __name__ == "__main__":
    try:
        group.run(deploy) # Run the 'deploy' task on the server group (currently just one server)
    except GroupException as e:
        print("Error during deployment to one or more servers:")
        print(e)
        exit(1)
