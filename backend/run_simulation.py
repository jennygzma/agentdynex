import os
import shutil
import signal
import subprocess

import globals
from utils import create_and_write_file

# HOW SIMULATION FOLDER WORKS
# each generation rests in generated/generations_[timestamp]_[uuid]
# each generation has a global config.txt and matrix.txt and config_iteration.txt and config_iterations folder
# config_iteration.txt stores the user's current iteration they are working on in the simulation, ie: run-1-1 (we need to parse this)

# IN THE CONFIG ITERATION FOLDER
# navigate the folders by going to: generations_[]_[]/[prototype]/config_iterations/[run-id]/...
# The folder contains
# config_iterations/initial_config.txt - the initially generated config from the design matrix
# config_iterations/run-1 - the folder that stores the information and result of the first run of initial_config.txt
# config_iterations/run-1/initial_config.txt - stores initial_config.txt
# config_iterations/run-1/logs.txt - stores the raw logs from the run
# config_iterations/run-1/results.txt - stores results (like a summary of the logs)
# config_iterations/run-1/improvements.txt - stores improvements
# config_iterations/run-1/updated_config - stores the updated_config based on reflection/improvments
# config_iterations/run-1/run-1-1 - references the first time we run updated_config_run-1
# config_iterations/run-1/run-1-1/initial_config.txt - stores initial_config_run-1.txt from parent folder
# config_iterations/run-1/run-1-1/logs.txt - stores the raw logs from the run
# config_iterations/run-1/run-1-1/results.txt - stores results (like a summary of the logs)
# config_iterations/run-1/run-1-1/improvements.txt - stores improvements
# config_iterations/run-1/run-1-1/updated_config.txt - stores the updated_config based on reflection/improvments
# config_iterations/run-1/run-1-1/run-1-1-1 - references the first time we run updated_config_run-1-1
# config_iterations/run-1/run-1-2 - references the second time we run updated_config_run-1
# config_iterations/run-1/run-1-2/initial_config_run.txt - stores initial_config_run-1.txt from parent folder
# config_iterations/run-1/run-1-2/improvements_run.txt - stores improvements
# config_iterations/run-1/run-1-2/results_run.txt - stores results (like a summary of the logs)
# config_iterations/run-1/run-1-2/updated_config_run.txt - stores the updated_config based on reflection/improvments
# config_iterations/run-1/run-1-2/1-2-1 - references the first time we run updated_config_run-1-1
# config_iterations/run-2 - the folder that stores the information and result of the second run of initial_config.txt


# JSON TREE structure
# {
# 	"run-1": {
# 		"run-1-1": {
# 			"run-1-1-1": {},
# 			"run-1-1-2": {}
# 		},
# 		"run-1-2": {
# 			"run-1-2-1": {},
# 			"run-1-2-2": {}
# 		},
# 		"run-1-3": {}
# 	},
# 	"run-2": {
# 		"run-2-1": {
# 			"run-2-1-1": {},
# 			"run-2-1-2": {}
# 		}
# 	}
# }

# user needs to fill this out themselves
GPTEAM_PATH = "/Users/jennyma/Projects/GPTeam"
CONFIG_FILE_NAME = "config.txt"


# config_id will be 0, run-1, run-2, run-1-1. if 0, the new run_id for it will be 0->run-1, run-1->run-1-1 or run-1-2 (if run-1-1 exists then it will be run-1-2(it needs to check the json file))
# it also adds it to the json file in the return statement.
def get_next_run_id(run_id, run_tree):
    def find_node(tree, target):
        """Recursively find the node corresponding to target in the tree."""
        if target in tree:
            return tree[target]
        for _key, subtree in tree.items():
            found = find_node(subtree, target)
            if found is not None:
                return found
        return None

    print(f"calling get_next_run_id for {run_id}...")
    if run_id == "0":
        suffix = 1
        while f"run-{suffix}" in run_tree:
            suffix += 1
        new_run_id = f"run-{suffix}"
        run_tree[new_run_id] = {}
        return new_run_id, run_tree

    parent_node = find_node(run_tree, run_id)

    if parent_node is None:
        raise ValueError(f"Run ID '{run_id}' not found in the tree.")

    # Determine next available suffix
    suffix = 1
    while f"{run_id}-{suffix}" in parent_node:
        suffix += 1

    new_run_id = f"{run_id}-{suffix}"
    parent_node[new_run_id] = {}  # Add as child

    return new_run_id, run_tree


def find_folder_path(run_id, current_prototype_path):
    """
    Given a run_id, finds the corresponding folder path in the config_iterations directory.

    :param run_id: The run identifier (e.g., "run-1-2-1").
    :param base_path: The base directory containing config iterations.
    :return: The absolute path to the folder corresponding to run_id.
    """
    print(f"calling find_folder_path for run_id {run_id}...")
    if run_id == "0" or None:
        return current_prototype_path
    parts = run_id.split("-")
    folder_path = os.path.join(
        f"{current_prototype_path}/{globals.CONFIG_ITERATIONS_FOLDER_NAME}",
        f"run-{parts[1]}",
    )

    for i in range(2, len(parts)):
        sub_run = "-".join(parts[: i + 1])
        folder_path = os.path.join(folder_path, sub_run)

    return folder_path


# function to run simulation
def run_simulation(run_iteration_path, run_id, config):
    print(f"calling run_simulation for run_id {run_id}...")
    config_path = f"{GPTEAM_PATH}/{CONFIG_FILE_NAME}"
    create_and_write_file(config_path, config)

    log_file = f"{run_iteration_path}/{globals.LOGS_FILE}_{run_id}"

    if os.name == "nt":  # Windows
        cmd = [
            "cmd.exe",
            "/c",
            "start",
            "cmd",
            "/k",
            f'poetry run world > "{log_file}" 2>&1',
        ]
    else:  # macOS / Linux (More portable approach)
        terminals = [
            "gnome-terminal",
            "konsole",
            "xfce4-terminal",
            "x-terminal-emulator",
        ]
        terminal_cmd = next((t for t in terminals if shutil.which(t)), None)

        if terminal_cmd:
            cmd = [
                terminal_cmd,
                "--",
                "bash",
                "-c",
                f'poetry run world > "{log_file}" 2>&1; exec bash',
            ]
        else:
            raise RuntimeError("No suitable terminal emulator found.")

    subprocess.Popen(cmd)


# function to stop simulation
def stop_simulation():
    """Stops the currently running simulation."""
    global current_process

    if current_process:
        if os.name == "nt":  # Windows
            subprocess.run(
                ["taskkill", "/F", "/PID", str(current_process.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:  # macOS / Linux
            os.kill(current_process.pid, signal.SIGTERM)  # Send termination signal

        current_process = None  # Reset the global variable
        print("Simulation stopped.")
    else:
        print("No active simulation to stop.")


# function to grab logs
