# This file acts as a controller to route API requests

import datetime
import json
import uuid

import globals
from config_generation import generate_config as get_generated_config
from flask import Flask, jsonify, request
from matrix import brainstorm_inputs as brainstorm_generated_inputs
from matrix import get_context_from_other_inputs
from reflection import (
    generate_milestones_json,
    generate_milestones_text,
    generate_new_specific_problems_and_solutions,
    generate_problems_and_solutions,
)
from reflection import generate_summary as generate_LLM_summary
from reflection import generate_updated_config as generate_updated_config_from_fixes
from reflection import get_status as generate_status
from reflection import (
    log_changes,
    log_dynamics,
)
from run_simulation import (
    delete_child_runs,
    delete_run_and_children,
    find_folder_path,
    get_next_run_id,
)
from run_simulation import run_simulation as run_external_simulation
from run_simulation import stop_simulation as stop_external_simulation
from utils import (
    create_and_write_file,
    create_folder,
    delete_file,
    delete_folder,
    file_exists,
    read_file,
)

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
    globals.current_prototype = prototype
    globals.prototypes.append(prototype)
    create_and_write_file(
        f"{globals.folder_path}/{globals.PROTOTYPES}",
        json.dumps(globals.prototypes),
    )
    folder_path = f"{globals.folder_path}/{prototype}"
    print("hi jenny " + folder_path)
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
    globals.milestones = json.loads(
        read_file(
            f"{globals.folder_path}/{globals.current_prototype}/{globals.MILESTONES_FILE_NAME}"
        )
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.MILESTONES_FILE_NAME}",
        json.dumps(globals.milestones),
    )
    run_tree_path = (
        f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}"
    )

    if file_exists(run_tree_path):
        globals.run_tree = json.loads(read_file(run_tree_path))
    else:
        globals.run_tree = {}
        create_and_write_file(run_tree_path, json.dumps(globals.run_tree))

    create_and_write_file(
        f"{globals.folder_path}/{globals.RUN_TREE}",
        json.dumps(globals.run_tree),
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

    globals.existing_fixes_to_apply = []
    globals.user_specified_fixes_to_apply = []
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
    if globals.run_tree != {}:
        delete_folder(
            f"{globals.folder_path}/{globals.current_prototype}/{globals.CONFIG_ITERATIONS_FOLDER_NAME}"
        )
    globals.run_tree = {}
    globals.run_id = "0"
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}",
        json.dumps(globals.run_tree),
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}",
        json.dumps(globals.run_tree),
    )
    milestones_txt = (
        f"{globals.matrix['MilestonesXIdea']} {globals.matrix['MilestonesXGrounding']}"
        if globals.matrix["MilestonesXIdea"]
        else generate_milestones_text(globals.config)
    )
    milestones_json = generate_milestones_json(milestones_txt)
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.MILESTONES_FILE_NAME}",
        json.dumps(milestones_json),
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.MILESTONES_FILE_NAME}",
        json.dumps(globals.milestones),
    )
    globals.milestones = milestones_json

    if globals.iterative_list is None:
        globals.iterative_list = []
        create_and_write_file(
            f"{globals.folder_path}/{globals.ITERATIVE_LIST_FILE_NAME}",
            json.dumps(globals.iterative_list),
        )

    globals.static_list = json.loads(read_file(globals.STATIC_LIST_FILE_NAME))

    return jsonify({"message": "Generated config"}), 200


@app.route("/save_config", methods=["POST"])
def save_config():
    print("calling save_config...")
    globals.config = request.json["config"]
    config_type = request.json["type"]
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.CONFIG_FILE_NAME}",
        globals.config,
    )
    if config_type == "updated":
        create_and_write_file(
            f"{current_run_id_folder_path}/{globals.UPDATED_CONFIG}",
            globals.config,
        )
    elif config_type == "initial":
        create_and_write_file(
            f"{current_run_id_folder_path}/{globals.INITIAL_CONFIG_FILE}",
            globals.config,
        )
    else:
        create_and_write_file(
            f"{current_prototype_folder_path}/{globals.CONFIG_FILE_NAME}",
            globals.config,
        )

    return jsonify({"message": "Saved config"}), 200


@app.route("/get_config", methods=["GET"])
def get_config():
    print("calling get_config...")
    config_type = request.args.get("type")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    if config_type == "updated":
        config = read_file(f"{current_run_id_folder_path}/{globals.UPDATED_CONFIG}")
    elif config_type == "initial":
        config = read_file(
            f"{current_run_id_folder_path}/{globals.INITIAL_CONFIG_FILE}"
        )
    else:
        config = read_file(
            f"{current_prototype_folder_path}/{globals.CONFIG_FILE_NAME}",
        )
    return (
        jsonify({"message": "getting config", "config": config}),
        200,
    )


@app.route("/set_current_run_id", methods=["POST"])
def set_current_run_id():
    print("calling set_current_run_id...")
    data = request.json
    globals.run_id = data["current_run_id"]
    run_id_path = find_folder_path(
        globals.run_id,
        f"{globals.folder_path}/{globals.current_prototype}",
    )
    if globals.run_id == "0":
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

    if file_exists(f"{run_id_path}/{globals.INITIAL_CONFIG_FILE}"):
        globals.config = json.loads(
            read_file(f"{run_id_path}/{globals.INITIAL_CONFIG_FILE}")
        )
        create_and_write_file(
            f"{run_id_path}/{globals.INITIAL_CONFIG_FILE}",
            json.dumps(globals.config),
        )

    if file_exists(f"{run_id_path}/{globals.EXISTING_FIXES_TO_APPLY_FILE_NAME}"):
        globals.existing_fixes_to_apply = json.loads(
            read_file(f"{run_id_path}/{globals.EXISTING_FIXES_TO_APPLY_FILE_NAME}")
        )
        create_and_write_file(
            f"{globals.folder_path}/{globals.EXISTING_FIXES_TO_APPLY_FILE_NAME}",
            json.dumps(globals.existing_fixes_to_apply),
        )
    else:
        globals.existing_fixes_to_apply = []
    if file_exists(f"{run_id_path}/{globals.USER_SPECIFIED_FIXES_TO_APPLY_FILE_NAME}"):
        globals.user_specified_fixes_to_apply = json.loads(
            read_file(
                f"{run_id_path}/{globals.USER_SPECIFIED_FIXES_TO_APPLY_FILE_NAME}"
            )
        )
        create_and_write_file(
            f"{globals.folder_path}/{globals.USER_SPECIFIED_FIXES_TO_APPLY_FILE_NAME}",
            json.dumps(globals.existing_fixes_to_apply),
        )
    else:
        globals.user_specified_fixes_to_apply = []
    return (
        jsonify(
            {
                "message": "Set current run_id",
            }
        ),
        200,
    )


@app.route("/create_new_run", methods=["POST"])
def create_new_run():
    print("calling create_new_run...")
    next_run_id, globals.run_tree = get_next_run_id(globals.run_id, globals.run_tree)
    create_and_write_file(
        f"{globals.folder_path}/{globals.RUN_TREE}", json.dumps(globals.run_tree)
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}",
        json.dumps(globals.run_tree),
    )

    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    if globals.run_id == "0":
        config_to_run_file_path = (
            f"{current_run_id_folder_path}/{globals.CONFIG_FILE_NAME}"
        )
    else:
        config_to_run_file_path = (
            f"{current_run_id_folder_path}/{globals.UPDATED_CONFIG}"
        )
    config_to_run = read_file(config_to_run_file_path)
    print(config_to_run_file_path + " config_to_run_file_path")
    # create_folder(f"{current_run_id_folder_path}/{next_run_id})
    if globals.run_id == "0":
        create_folder(
            f"{current_run_id_folder_path}/{globals.CONFIG_ITERATIONS_FOLDER_NAME}/{next_run_id}"
        )
        create_and_write_file(
            f"{current_run_id_folder_path}/{globals.CONFIG_ITERATIONS_FOLDER_NAME}/{next_run_id}/{globals.INITIAL_CONFIG_FILE}",
            config_to_run,
        )
    else:
        create_folder(f"{current_run_id_folder_path}/{next_run_id}")
        create_and_write_file(
            f"{current_run_id_folder_path}/{next_run_id}/{globals.INITIAL_CONFIG_FILE}",
            config_to_run,
        )
    globals.run_id = next_run_id
    return (
        jsonify(
            {
                "message": "created new run",
                "new_run_id": next_run_id,
            }
        ),
        200,
    )


@app.route("/get_run_tree", methods=["GET"])
def get_run_tree():
    print("calling get_run_tree...")
    globals.run_tree = json.loads(
        read_file(
            f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}"
        )
    )
    return (
        jsonify(
            {
                "run_tree": globals.run_tree,
            }
        ),
        200,
    )


@app.route("/run_simulation", methods=["POST"])
def run_simulation():
    print("calling run_simulation...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    create_and_write_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}", "")
    create_and_write_file(f"{current_run_id_folder_path}/{globals.SUMMARY_FILE}", "")
    delete_file(f"{current_run_id_folder_path}/{globals.ANALYSIS_FILE}")
    delete_file(f"{current_run_id_folder_path}/{globals.UPDATED_CONFIG}")

    config_to_run_file_path = (
        f"{current_run_id_folder_path}/{globals.INITIAL_CONFIG_FILE}"
    )
    config_to_run = read_file(config_to_run_file_path)

    has_children = (
        bool(globals.run_tree.get(globals.run_id, {}))
        if isinstance(globals.run_tree.get(globals.run_id), dict)
        else False
    )
    print(f"has_children {has_children}, run_id {globals.run_id}")
    if has_children:
        to_delete, globals.run_tree = delete_child_runs(
            globals.run_id, globals.run_tree
        )
        print(f"to_delete {to_delete}")
        print(f"new run tree {globals.run_tree}")
        for curr_run_id in to_delete:
            delete_folder(f"{current_run_id_folder_path}/{curr_run_id}")
        create_and_write_file(
            f"{globals.folder_path}/{globals.RUN_TREE}", json.dumps(globals.run_tree)
        )
        create_and_write_file(
            f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}",
            json.dumps(globals.run_tree),
        )

    run_external_simulation(current_run_id_folder_path, config_to_run)
    return (
        jsonify(
            {
                "message": "running simulation",
            }
        ),
        200,
    )


@app.route("/stop_simulation", methods=["POST"])
def stop_simulation():
    print("calling stop_simulation...")
    stop_external_simulation()
    return (
        jsonify(
            {
                "message": "stopping simulation",
            }
        ),
        200,
    )


@app.route("/delete_run", methods=["POST"])
def delete_run():
    print("calling delete_run...")
    data = request.json
    run_id = data["run_id"]
    globals.run_tree = delete_run_and_children(run_id, globals.run_tree)
    create_and_write_file(
        f"{globals.folder_path}/{globals.RUN_TREE}", json.dumps(globals.run_tree)
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}",
        json.dumps(globals.run_tree),
    )
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    delete_folder(current_run_id_folder_path)
    return (
        jsonify(
            {
                "message": f"deleted {run_id}",
            }
        ),
        200,
    )


@app.route("/get_logs", methods=["GET"])
def get_logs():
    print("calling get_logs...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    logs = read_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}")
    return (
        jsonify(
            {
                "message": "grabbed logs",
                "logs": logs,
            }
        ),
        200,
    )


@app.route("/get_status", methods=["GET"])
def get_status():
    print("calling get_status...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    logs = read_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}")
    problem = read_file(f"{globals.folder_path}/{globals.PROBLEM_FILE_NAME}")
    failures = f"""Here are the failures to look out for: {globals.matrix["FailureConditionXIdea"]}.
    Here are the specifics: {globals.matrix["FailureConditionXGrounding"]}
    """
    status = generate_status(logs, problem, failures)
    return (
        jsonify(
            {
                "message": "generated summary",
                "status": status,
            }
        ),
        200,
    )


@app.route("/generate_summary", methods=["POST"])
def generate_summary():
    print("calling generate_summary...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    logs = read_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}")
    summary = generate_LLM_summary(logs)
    create_and_write_file(
        f"{current_run_id_folder_path}/{globals.SUMMARY_FILE}", summary
    )
    return (
        jsonify(
            {
                "message": "generated summary",
                "summary": summary,
            }
        ),
        200,
    )


@app.route("/get_summary", methods=["GET"])
def get_summary():
    print("calling get_summary...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    summary = read_file(f"{current_run_id_folder_path}/{globals.SUMMARY_FILE}")
    return (
        jsonify(
            {
                "message": "got summary",
                "summary": summary,
            }
        ),
        200,
    )


@app.route("/fetch_dynamics", methods=["GET"])
def fetch_dynamics():
    print("calling fetch_dynamics...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    logs = read_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}")
    if file_exists(f"{current_run_id_folder_path}/{globals.DYNAMICS_FILE_NAME}"):
        dynamics_text = read_file(
            f"{current_run_id_folder_path}/{globals.DYNAMICS_FILE_NAME}"
        )
        dynamics_data = json.loads(dynamics_text)
    else:
        dynamics_data = []
    previous = (
        next((log for log in reversed(dynamics_data) if log.get("dynamic")), "")
        if dynamics_data
        else ""
    )
    dynamic = log_dynamics(
        logs,
        globals.current_milestone_id,
        globals.milestones[globals.current_milestone_id],
        globals.milestones,
        previous,
    )
    if dynamic["milestone_id"] != globals.current_milestone_id:
        globals.current_milestone_id = str(dynamic["milestone_id"])
    if file_exists(f"{current_run_id_folder_path}/{globals.DYNAMICS_FILE_NAME}"):
        dynamics_text = read_file(
            f"{current_run_id_folder_path}/{globals.DYNAMICS_FILE_NAME}"
        )
        dynamics_data = json.loads(dynamics_text)
    else:
        dynamics_data = []
    if dynamic["dynamic"] != "":
        dynamics_data.append(dynamic)
        create_and_write_file(
            f"{current_run_id_folder_path}/{globals.DYNAMICS_FILE_NAME}",
            json.dumps(dynamics_data),
        )

    return (
        jsonify(
            {
                "message": "fetching dynamics",
                "current_milestone_id": globals.current_milestone_id,
                "dynamics_data": dynamics_data,
            }
        ),
        200,
    )


@app.route("/get_dynamics", methods=["GET"])
def get_dynamics():
    print("calling fetch_dynamics...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    dynamics = json.loads(
        read_file(
            f"{current_run_id_folder_path}/{globals.DYNAMICS_FILE_NAME}",
        )
    )
    return (
        jsonify(
            {
                "message": "fetching dynamics",
                "current_milestone_id": globals.current_milestone_id,
                "dynamics_data": dynamics,
            }
        ),
        200,
    )


@app.route("/fetch_changes", methods=["GET"])
def fetch_changes():
    print("calling fetch_changes...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    logs = read_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}")
    if file_exists(f"{current_run_id_folder_path}/{globals.CHANGES_FILE_NAME}"):
        changes_text = read_file(
            f"{current_run_id_folder_path}/{globals.CHANGES_FILE_NAME}"
        )
        changes_data = json.loads(changes_text)
    else:
        changes_data = []
    previous = (
        next((log for log in reversed(changes_data) if log.get("change")), "")
        if changes_data
        else ""
    )

    change = log_changes(logs, previous)
    change_with_milestone = {
        "milestone_id": globals.current_milestone_id,
        "milestone": globals.milestones[str(globals.current_milestone_id)],
        "where": change["where"],
        "what": change["what"],
        "change": change["change"],
    }
    if change["change"] != "":
        changes_data.append(change_with_milestone)
        create_and_write_file(
            f"{current_run_id_folder_path}/{globals.CHANGES_FILE_NAME}",
            json.dumps(changes_data),
        )

    return (
        jsonify(
            {
                "message": "fetching changes",
                "current_milestone_id": globals.current_milestone_id,
                "changes_data": changes_data,
            }
        ),
        200,
    )


@app.route("/get_changes", methods=["GET"])
def get_changes():
    print("calling get_changes...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    changes = json.loads(
        read_file(
            f"{current_run_id_folder_path}/{globals.CHANGES_FILE_NAME}",
        )
    )
    return (
        jsonify(
            {
                "message": "fetching dynamics",
                "current_milestone_id": globals.current_milestone_id,
                "changes_data": changes,
            }
        ),
        200,
    )


@app.route("/get_iterative_list", methods=["GET"])
def get_iterative_list():
    print("calling get_static_list...")
    return (
        jsonify(
            {
                "message": "got iterative list",
                "list": (
                    globals.iterative_list if globals.iterative_list is not None else []
                ),
            }
        ),
        200,
    )


@app.route("/get_static_list", methods=["GET"])
def get_static_list():
    print("calling get_static_list...")
    return (
        jsonify({"message": "got static list", "list": globals.static_list}),
        200,
    )


@app.route("/generate_fixes", methods=["GET"])
def generate_fixes():
    print("calling generate_fixes...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )

    has_children = (
        bool(globals.run_tree.get(globals.run_id, {}))
        if isinstance(globals.run_tree.get(globals.run_id), dict)
        else False
    )
    print(f"has_children {has_children}, run_id {globals.run_id}")
    if has_children:
        to_delete, globals.run_tree = delete_child_runs(
            globals.run_id, globals.run_tree
        )
        print(f"to_delete {to_delete}")
        print(f"new run tree {globals.run_tree}")
        for curr_run_id in to_delete:
            delete_folder(f"{current_run_id_folder_path}/{curr_run_id}")
        create_and_write_file(
            f"{globals.folder_path}/{globals.RUN_TREE}", json.dumps(globals.run_tree)
        )
        create_and_write_file(
            f"{globals.folder_path}/{globals.current_prototype}/{globals.RUN_TREE}",
            json.dumps(globals.run_tree),
        )

    logs = read_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}")
    log_words = logs.split()
    log_words = log_words[-4000:]
    config = read_file(f"{current_prototype_folder_path}/{globals.CONFIG_FILE_NAME}")
    fixes = generate_problems_and_solutions(
        globals.static_list, globals.iterative_list, log_words, config
    )
    print(f"hi jenny all_fixes {fixes}")
    # create_and_write_file(
    #     f"{current_run_id_folder_path}/{globals.ANALYSIS_FILE}", analysis
    # )
    # create_and_write_file(
    #     f"{current_run_id_folder_path}/{globals.UPDATED_CONFIG}",
    #     updated_config,
    # )
    return (
        jsonify(
            {
                "message": "generated fixes",
                "fixes": fixes,
            }
        ),
        200,
    )


@app.route("/identify_new_list_entry", methods=["POST"])
def identify_new_list_entry():
    print("calling identify_new_list_entry...")
    data = request.json
    user_input = data["input"]
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    logs = read_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}")
    log_words = logs.split()
    log_words = log_words[-4000:]
    config = read_file(f"{current_prototype_folder_path}/{globals.CONFIG_FILE_NAME}")
    new_fixes = generate_new_specific_problems_and_solutions(
        user_input, globals.static_list, globals.iterative_list, log_words, config
    )
    return (
        jsonify(
            {
                "message": "generated fixes",
                "new_fixes": new_fixes,
            }
        ),
        200,
    )


@app.route("/set_fixes_to_apply", methods=["POST"])
def set_fixes_to_apply():
    print("calling set_fixes_to_apply...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    data = request.json
    user_specified = data["user_specified"]
    if user_specified:
        globals.user_specified_fixes_to_apply = (
            globals.user_specified_fixes_to_apply
            + json.loads(json.dumps(data["fixes"]))
        )
        create_and_write_file(
            f"{current_run_id_folder_path}/{globals.USER_SPECIFIED_FIXES_TO_APPLY_FILE_NAME}",
            json.dumps(globals.user_specified_fixes_to_apply),
        )
        create_and_write_file(
            f"{globals.folder_path}/{globals.USER_SPECIFIED_FIXES_TO_APPLY_FILE_NAME}",
            json.dumps(globals.user_specified_fixes_to_apply),
        )
    else:
        globals.existing_fixes_to_apply = globals.existing_fixes_to_apply + json.loads(
            json.dumps(data["fixes"])
        )
        create_and_write_file(
            f"{current_run_id_folder_path}/{globals.EXISTING_FIXES_TO_APPLY_FILE_NAME}",
            json.dumps(globals.existing_fixes_to_apply),
        )
        create_and_write_file(
            f"{globals.folder_path}/{globals.EXISTING_FIXES_TO_APPLY_FILE_NAME}",
            json.dumps(globals.existing_fixes_to_apply),
        )
    return (
        jsonify(
            {
                "message": "set fixes to apply",
            }
        ),
        200,
    )


@app.route("/get_fixes_to_apply", methods=["GET"])
def get_fixes_to_apply():
    print("calling get_fixes_to_apply...")
    user_specified = request.args.get("user_specified")
    fixes_to_apply = (
        globals.user_specified_fixes_to_apply
        if user_specified
        else globals.existing_fixes_to_apply
    )
    return (
        jsonify(
            {
                "message": "got fixes to apply",
                "fixes_to_apply": fixes_to_apply,
            }
        ),
        200,
    )


@app.route("/add_to_iterative_list", methods=["POST"])
def add_to_iterative_list():
    print("calling add_to_iterative_list...")
    new_elements = json.loads(json.dumps(request.json["elements"]))
    print(f"hi jenny current iterative list {globals.iterative_list}")
    print(f"hi jenny current new_elements list {new_elements}")
    globals.iterative_list = globals.iterative_list + new_elements
    create_and_write_file(
        f"{globals.folder_path}/{globals.ITERATIVE_LIST_FILE_NAME}",
        json.dumps(globals.iterative_list),
    )
    return (
        jsonify({"message": "added list entry"}),
        200,
    )


@app.route("/generate_updated_config", methods=["POST"])
def generate_updated_config():
    print("calling generate_updated_config...")
    current_prototype_folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    current_run_id_folder_path = find_folder_path(
        globals.run_id, current_prototype_folder_path
    )
    logs = read_file(f"{current_run_id_folder_path}/{globals.LOGS_FILE}")
    log_words = logs.split()
    log_words = log_words[-3000:]
    config = read_file(f"{current_prototype_folder_path}/{globals.CONFIG_FILE_NAME}")
    updated_config = generate_updated_config_from_fixes(
        globals.existing_fixes_to_apply + globals.user_specified_fixes_to_apply,
        logs,
        config,
    )
    create_and_write_file(
        f"{current_run_id_folder_path}/{globals.UPDATED_CONFIG}",
        updated_config,
    )
    return (
        jsonify({"message": "added list entry", "updated_config": updated_config}),
        200,
    )


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
    globals.run_tree = json.loads(
        read_file(f"{globals.folder_path}/{globals.RUN_TREE}")
        if file_exists(f"{globals.folder_path}/{globals.RUN_TREE}")
        else {}
    )
    globals.iterative_list = (
        json.loads(
            read_file(f"{globals.folder_path}/{globals.ITERATIVE_LIST_FILE_NAME}")
        )
        if file_exists(f"{globals.folder_path}/{globals.ITERATIVE_LIST_FILE_NAME}")
        else None
    )
    globals.static_list = json.loads(read_file(globals.STATIC_LIST_FILE_NAME))
    file_path_milestone = f"{globals.folder_path}/{globals.MILESTONES_FILE_NAME}"
    globals.milestones = (
        json.loads(read_file(file_path_milestone))
        if file_exists(file_path_milestone)
        else {}
    )
    globals.existing_fixes_to_apply = (
        json.loads(
            read_file(
                f"{globals.folder_path}/{globals.EXISTING_FIXES_TO_APPLY_FILE_NAME}"
            )
        )
        if file_exists(
            f"{globals.folder_path}/{globals.EXISTING_FIXES_TO_APPLY_FILE_NAME}"
        )
        else []
    )
    globals.user_specified_fixes_to_apply = (
        json.loads(
            read_file(
                f"{globals.folder_path}/{globals.USER_SPECIFIED_FIXES_TO_APPLY_FILE_NAME}"
            )
        )
        if file_exists(
            f"{globals.folder_path}/{globals.USER_SPECIFIED_FIXES_TO_APPLY_FILE_NAME}"
        )
        else []
    )
    globals.run_id = "0"
    globals.problem = read_file(f"{globals.folder_path}/{globals.PROBLEM_FILE_NAME}")
    return jsonify({"message": "Successfully set global fields"}), 200


#####################################################################################################################################################################################

# Running app
if __name__ == "__main__":
    app.run()
