# This file acts as a controller to route API requests

import datetime
import json
import uuid

import globals
from config_generation import generate_config as get_generated_config
from flask import Flask, jsonify, request
from matrix import brainstorm_inputs as brainstorm_generated_inputs
from matrix import get_context_from_other_inputs
from run_simulation import find_folder_path, get_next_run_id
from utils import create_and_write_file, create_folder, file_exists, read_file

# Initializing flask app
app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response


@app.route("/get_problem", methods=["GET"])
def get_problem():
    print("calling get_problem...")
    print(globals.problem)
    return (
        jsonify({"message": "getting user problem", "problem": globals.problem}),
        200,
    )


@app.route("/save_problem", methods=["POST"])
def save_problem():
    print("calling save_problem...")
    globals.problem = request.json["problem"]
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if globals.folder_path is None:
        globals.folder_path = (
            f"{globals.GENERATED_FOLDER_NAME}/generations_{date_time}_{uuid.uuid4()}"
        )
        create_folder(globals.folder_path)
    create_and_write_file(
        f"{globals.folder_path}/{globals.PROBLEM_FILE_NAME}",
        globals.problem,
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.MATRIX_FILE_NAME}",
        json.dumps(globals.matrix),
    )
    return jsonify({"message": "Saved problem"}), 200


@app.route("/brainstorm_inputs", methods=["GET"])
def brainstorm_inputs():
    print("calling brainstorm_inputs...")
    category = request.args.get("category")
    iteration = request.args.get("iteration")
    existing_brainstorms = request.args.get("brainstorms")
    context = get_context_from_other_inputs(globals.problem, None, globals.matrix)
    brainstorms = brainstorm_generated_inputs(
        category, context, existing_brainstorms, iteration
    )
    return (
        jsonify({"message": "Generated brainstorm_inputs", "brainstorms": brainstorms}),
        200,
    )


@app.route("/get_input", methods=["GET"])
def get_input():
    print("calling get_input...")
    category = request.args.get("category")
    print(globals.matrix[category])
    return (
        jsonify({"message": "getting input", "input": globals.matrix[category]}),
        200,
    )


@app.route("/update_input", methods=["POST"])
def update_input():
    print("calling update_input...")
    globals.matrix[request.json["category"]] = request.json["input"]
    create_and_write_file(
        f"{globals.folder_path}/{globals.MATRIX_FILE_NAME}",
        json.dumps(globals.matrix),
    )
    return jsonify({"message": "Updated input"}), 200


@app.route("/explore_prototype", methods=["POST"])
def explore_prototype():
    print("calling explore_prototype...")
    prototype = request.json["prototype"]
    print(f"hi jenny {prototype}")
    globals.current_prototype = prototype
    globals.prototypes.append(prototype)
    create_and_write_file(
        f"{globals.folder_path}/{globals.PROTOTYPES}",
        json.dumps(globals.prototypes),
    )
    folder_path = f"{globals.folder_path}/{prototype}"
    create_folder(f"{folder_path}")
    create_and_write_file(
        f"{folder_path}/{globals.MATRIX_FILE_NAME}", json.dumps(globals.matrix)
    )
    return jsonify({"message": "Saved prototype"}), 200


@app.route("/get_prototypes", methods=["GET"])
def get_prototypes():
    print("calling get_prototypes...")
    return (
        jsonify(
            {"message": "Generated get_prototypes", "prototypes": globals.prototypes}
        ),
        200,
    )


@app.route("/set_current_prototype", methods=["POST"])
def set_current_prototype():
    print("calling set_current_prototype...")
    data = request.json
    globals.current_prototype = data["current_prototype"]
    globals.matrix = json.loads(
        read_file(
            f"{globals.folder_path}/{globals.current_prototype}/{globals.MATRIX_FILE_NAME}"
        )
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.MATRIX_FILE_NAME}",
        json.dumps(globals.matrix),
    )
    if file_exists(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_FILE_NAME}"
    ):
        globals.config = json.loads(
            read_file(
                f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_FILE_NAME}"
            )
        )
        create_and_write_file(
            f"{globals.folder_path}/{globals.CONFIG_FILE_NAME}",
            json.dumps(globals.config),
        )
    return (
        jsonify(
            {
                "message": "Set current prototype",
            }
        ),
        200,
    )


@app.route("/generate_config", methods=["POST"])
def generate_config():
    print("calling generate_config...")
    problem = globals.problem

    globals.config = get_generated_config(problem, globals.matrix)

    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_FILE_NAME}",
        globals.config,
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.CONFIG_FILE_NAME}",
        globals.config,
    )

    globals.run_tree = {}
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}",
        globals.run_tree,
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}",
        globals.run_tree,
    )

    return jsonify({"message": "Generated config"}), 200


# TASK - needs to see if updated or initial config is being saved and needs run id
@app.route("/save_config", methods=["POST"])
def save_config():
    print("calling save_config...")
    globals.config = request.json["config"]
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_FILE_NAME}",
        globals.config,
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.CONFIG_FILE_NAME}",
        globals.config,
    )
    return jsonify({"message": "Saved config"}), 200


@app.route("/get_config", methods=["GET"])
def get_config():
    print("calling get_config...")
    config = read_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_FILE_NAME}"
    )
    return (
        jsonify({"message": "getting config", "config": config}),
        200,
    )


# TASK - update run tree


# TASK - set current run id
@app.route("/set_current_run_id", methods=["POST"])
def set_current_run_id():
    print("calling set_current_run_id...")
    data = request.json
    globals.run_id = data["current_run_id"]
    if globals.run_id == "0":
        run_id_path = f"{globals.folder_path}/{globals.current_prototype}"
        if file_exists(f"{run_id_path}/{globals.CONFIG_FILE_NAME}"):
            globals.config = json.loads(
                read_file(
                    f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_FILE_NAME}"
                )
            )
            create_and_write_file(
                f"{globals.folder_path}/{globals.CONFIG_FILE_NAME}",
                json.dumps(globals.config),
            )
            return (
                jsonify(
                    {
                        "message": "Set current run_id",
                    }
                ),
                200,
            )

    run_id_path = find_folder_path(
        globals.run_id,
        f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_ITERATIONS_FOLDER_NAME}",
    )
    print("hi jenny " + globals.run_id + " " + run_id_path)
    if file_exists(f"{run_id_path}/{globals.INITIAL_CONFIG_FILE}"):
        globals.config = json.loads(
            read_file(f"{run_id_path}/{globals.INITIAL_CONFIG_FILE}")
        )
        create_and_write_file(
            f"{run_id_path}/{globals.INITIAL_CONFIG_FILE}",
            json.dumps(globals.config),
        )
    return (
        jsonify(
            {
                "message": "Set current run_id",
            }
        ),
        200,
    )


@app.route("/run_config", methods=["POST"])
def run_config():
    print("calling run_config...")
    data = request.json
    run_id = data["run_id"]
    next_run_id, globals.run_tree = get_next_run_id(run_id, globals.run_tree)
    config_iterations_folder_path = f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_ITERATIONS_FOLDER_NAME}"
    current_run_id_folder_path = find_folder_path(run_id, config_iterations_folder_path)
    if run_id == "0":
        config_to_run_file_path = f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_FILE_NAME}"
    else:
        config_to_run_file_path = (
            f"{current_run_id_folder_path}/{globals.UPDATED_CONFIG}"
        )
    config_to_run = read_file(config_to_run_file_path)
    print(config_to_run_file_path + " config_to_run_file_path")
    # create_folder(f"{current_run_id_folder_path}/{next_run_id})
    create_and_write_file(
        f"{current_run_id_folder_path}/{next_run_id}/{globals.UPDATED_CONFIG}",
        config_to_run,
    )
    return (
        jsonify(
            {
                "message": "running config",
                "config": config_to_run,
                "new_run_id": next_run_id,
            }
        ),
        200,
    )


# TASK - reflect and update config
# TASK - stop simulation
#####################################################################################################################################################################################
# For testing only. Run curl http://127.0.0.1:5000/set_globals_for_uuid/uuid
@app.route("/set_globals_for_uuid/<generated_uuid>", methods=["GET"])
def set_globals_for_uuid(generated_uuid):
    print("calling set_globals_for_uuid")
    globals.folder_path = f"{globals.GENERATED_FOLDER_NAME}/{generated_uuid}"
    globals.prototypes = (
        json.loads(read_file(f"{globals.folder_path}/{globals.PROTOTYPES}"))
        if file_exists(f"{globals.folder_path}/{globals.PROTOTYPES}")
        else []
    )
    globals.matrix = json.loads(
        read_file(f"{globals.folder_path}/{globals.MATRIX_FILE_NAME}")
    )
    # globals.matrix = json.loads(
    #     read_file(f"{globals.folder_path}/{globals.RUN_TREE}")
    # )
    globals.problem = read_file(f"{globals.folder_path}/{globals.PROBLEM_FILE_NAME}")
    return jsonify({"message": "Successfully set global fields"}), 200


#####################################################################################################################################################################################

# Running app
if __name__ == "__main__":
    app.run()
