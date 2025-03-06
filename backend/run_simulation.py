import os

from backend.utils import create_and_write_file

# HOW SIMULATION FOLDER WORKS
# each generation rests in generated/generations_[timestamp]_[uuid]
# each generation has a global config.txt and matrix.txt and config_iteration.txt and config_iterations folder
    # config_iteration.txt stores the user's current iteration they are working on in the simulation, ie: run-1-1 (we need to parse this)

# IN THE CONFIG ITERATION FOLDER
# navigate the folders by going to: config_iterations/[run-id], ie: config_iterations/1/1
# The folder contains
# config_iterations/initial_config.txt - the initially generated config from the design matrix
# config_iterations/1 - the folder that stores the information and result of the first run of initial_config.txt
    # config_iterations/1/initial_config_run-1.txt - stores initial_config.txt
    # config_iterations/1/improvements_run-1.txt - stores improvements
    # config_iterations/1/results_run-1.txt - stores results
    # config_iterations/1/updated_config_run-1 - stores the updated_config based on reflection/improvments 
    # config_iterations/1/1 - references the first time we run updated_config_run-1
        # config_iterations/1/1/initial_config_run-1-1.txt - stores initial_config_run-1.txt from parent folder
        # config_iterations/1/1/improvements_run-1-1.txt - stores improvements
        # config_iterations/1/1/results_run-1-1.txt - stores results
        # config_iterations/1/1/updated_config_run-1-1 - stores the updated_config based on reflection/improvments 
        # config_iterations/1/1/1 - references the first time we run updated_config_run-1-1
    # config_iterations/1/2 - references the second time we run updated_config_run-1
        # config_iterations/1/2/initial_config_run-1-2.txt - stores initial_config_run-1.txt from parent folder
        # config_iterations/1/2/improvements_run-1-2.txt - stores improvements
        # config_iterations/1/2/results_run-1-2.txt - stores results
        # config_iterations/1/2/updated_config_run-1-2 - stores the updated_config based on reflection/improvments 
        # config_iterations/1/2/1 - references the first time we run updated_config_run-1-1
# config_iterations/1 - the folder that stores the information and result of the second run of initial_config.txt

# user needs to fill this out themselves
GPTEAM_PATH = "/Users/jennyma/Projects/GPTeam"
CONFIG_FILE_NAME = "config.txt"

# returns the config_iterations/1/1 path, for example (not the entire code generation)
def get_relative_folder_path_from_run_id(run_id):
    print(f"calling get_relative_folder_path_from_run_id for run_id {run_id}...")
    parts = run_id.split("-")  
    if len(parts) < 2 or parts[0] != "run":
        raise ValueError("Invalid run ID format. Expected format: run-X[-Y[-Z[...]]]")
    numbers = parts[1:] 
    folder_path = "config_iterations/" + "/".join(numbers)
    print(f"relative folder path is: {folder_path}...")
    return folder_path

def get_run_id_from_relative_folder_path(folder_path):
    print(f"calling get_run_id_from_relative_folder_path for folder_path {folder_path}...")
    parts = folder_path.split(os.sep)
    try:
        idx = parts.index("config_iterations")
    except ValueError:
        raise ValueError("Invalid folder path: 'config_iterations' not found")
    numbers = parts[idx + 1:]
    if not numbers:
        raise ValueError("Invalid folder path: No numbers found after 'config_iterations'")
    run_id = "run-" + "-".join(numbers)
    print(f"relative run id is: {run_id}...")
    return run_id

# function to set config
def set_config(config):
    config_path = f"{GPTEAM_PATH}/{CONFIG_FILE_NAME}"
    create_and_write_file(config_path, config)

# function to run simulation
def run_simulation(run_iteration, config):
    set_config(config)
    log_file = "/tmp/world_logs.txt"  # Change path as needed

    # Choose terminal based on OS
    if os.name == "nt":  # Windows
        cmd = f'start cmd /k "poetry run world > {log_file} 2>&1"'
    else:  # macOS / Linux
        cmd = f'gnome-terminal -- bash -c "poetry run world > {log_file} 2>&1; exec bash"'

    subprocess.Popen(cmd, shell=True)
    return log_file


# function to stop simulation

# function to grab logs

