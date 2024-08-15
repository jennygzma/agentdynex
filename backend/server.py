# This file acts as a controller to route API requests

import datetime
import json
import uuid

import globals
from code_generation import get_fake_data as get_generated_fake_data
from code_generation import (
    get_iterate_code,
    implement_plan_lock_step,
    test_code_per_lock_step,
    wipeout_code,
)
from flask import Flask, jsonify, request
from matrix import brainstorm_answers
from matrix import brainstorm_inputs as brainstorm_generated_inputs
from matrix import brainstorm_questions, get_context_from_other_inputs
from matrix import get_needs_specification as check_needs_specification
from matrix import summarize_input_from_context
from planning import get_design_hypothesis as get_generated_design_hypothesis
from planning import get_plan as get_generated_plan
from planning import get_plan_from_task_map
from utils import (
    create_and_write_file,
    create_folder,
    file_exists,
    folder_exists,
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
            f"{globals.GENERATED_FOLDER_PATH}/generations_{date_time}_{uuid.uuid4()}"
        )
        create_folder(globals.folder_path)
        create_folder(f"{globals.folder_path}/{globals.MATRIX_FOLDER_NAME}")
    create_and_write_file(
        f"{globals.folder_path}/{globals.PROBLEM_FILE_NAME}",
        globals.problem,
    )
    # globals.matrix = categorize_problem(globals.problem)
    create_and_write_file(
        f"{globals.folder_path}/{globals.MATRIX_FILE_NAME}",
        json.dumps(globals.matrix),
    )
    return jsonify({"message": "Saved problem"}), 200


@app.route("/get_needs_specification", methods=["GET"])
def get_needs_specification():
    print("calling get_needs_specification...")
    category = request.args.get("category")
    needs_specification = check_needs_specification(category, globals.matrix[category])
    return (
        jsonify(
            {
                "message": "getting user problem",
                "needs_specification": needs_specification,
            }
        ),
        200,
    )


@app.route("/brainstorm_inputs", methods=["GET"])
def brainstorm_inputs():
    print("calling brainstorm_inputs...")
    category = request.args.get("category")
    context = get_context_from_other_inputs(globals.problem, None, globals.matrix)
    brainstorms = brainstorm_generated_inputs(category, context)
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


@app.route("/get_questions", methods=["GET"])
def get_questions():
    print("calling get_questions...")
    category = request.args.get("category")
    context = get_context_from_other_inputs(globals.problem, category, globals.matrix)
    questions = brainstorm_questions(category, globals.matrix[category], context)
    return (
        jsonify({"message": "Generated get_questions", "questions": questions}),
        200,
    )


@app.route("/get_brainstorms", methods=["GET"])
def get_brainstorms():
    print("calling get_brainstorms...")
    category = request.args.get("category")
    question = request.args.get("question")
    context = get_context_from_other_inputs(globals.problem, None, globals.matrix)
    brainstorms = brainstorm_answers(category, question, context)
    return (
        jsonify({"message": "Generated get_brainstorms", "brainstorms": brainstorms}),
        200,
    )


@app.route("/update_specifications", methods=["POST"])
def update_specifications():
    print("calling update_specifications...")
    category = request.json["category"]
    print(request.json["specifications"])
    specifications = request.json["specifications"]
    text = ""
    for spec in specifications:
        question = spec.get("question", "")
        answer = spec.get("answer", "")
        if answer.strip():
            text += f"{question}{answer}\n"
    category_input = summarize_input_from_context(
        category, globals.matrix[category], text
    )
    globals.matrix[category] = category_input
    create_and_write_file(
        f"{globals.folder_path}/{globals.MATRIX_FOLDER_NAME}/{globals.CATEGORY_FILE_NAME[category]}",
        text,
    )
    create_and_write_file(
        f"{globals.folder_path}/{globals.MATRIX_FILE_NAME}",
        json.dumps(globals.matrix),
    )
    return jsonify({"message": "Saved goal"}), 200


@app.route("/explore_prototype", methods=["POST"])
def explore_prototype():
    print("calling explore_prototype...")
    prototype = request.json["prototype"]
    globals.prototypes.append(prototype)
    create_and_write_file(
        f"{globals.folder_path}/{globals.PROTOTYPES}",
        json.dumps(globals.prototypes),
    )
    folder_path = f"{globals.folder_path}/{prototype}"
    create_folder(f"{folder_path}")
    context = get_context_from_other_inputs(globals.problem, None, globals.matrix)
    prompt = f"Create a web UI based on this: {context}. "
    create_and_write_file(f"{folder_path}/{globals.PROMPT_FILE_NAME}", prompt)
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
    return (
        jsonify(
            {
                "message": "Set current prototype",
            }
        ),
        200,
    )


@app.route("/get_prompt", methods=["GET"])
def get_prompt():
    print("calling get_prompt...")
    prompt = read_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.PROMPT_FILE_NAME}"
    )
    return (
        jsonify(
            {
                "message": "getting prompt for theory",
                "prompt": prompt,
            }
        ),
        200,
    )


@app.route("/save_prompt", methods=["POST"])
def save_prompt():
    print("calling save_prompt...")
    prompt = request.json["prompt"]
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    create_and_write_file(
        f"{folder_path}/{globals.PROMPT_FILE_NAME}",
        prompt,
    )
    task_map_json = (
        json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
        if file_exists(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}")
        else {}
    )
    task_map = {int(key): value for key, value in task_map_json.items()}
    if folder_exists(f"{folder_path}/1"):
        wipeout_code(folder_path, 1, task_map, globals.current_prototype)
    create_and_write_file(
        f"{folder_path}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}",
        "",
    )
    create_and_write_file(
        f"{folder_path}/{globals.FAKED_DATA_FILE_NAME}",
        "",
    )
    create_and_write_file(
        f"{folder_path}/{globals.TASK_MAP_FILE_NAME}",
        "",
    )
    return jsonify({"message": "Saved prompt"}), 200


@app.route("/generate_fake_data", methods=["POST"])
def generate_fake_data():
    print("calling generate_fake_data...")
    user_iteration = request.json["user_iteration"]
    design_hypothesis = read_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}"
    )
    data = get_generated_fake_data(design_hypothesis, user_iteration)
    faked_data = data
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.FAKED_DATA_FILE_NAME}",
        faked_data,
    )
    return jsonify({"message": "Generated data"}), 200


@app.route("/save_faked_data", methods=["POST"])
def save_faked_data():
    print("calling save_faked_data...")
    faked_data = request.json["faked_data"]
    create_and_write_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.FAKED_DATA_FILE_NAME}",
        faked_data,
    )
    return jsonify({"message": "Saved faked data"}), 200


@app.route("/get_faked_data", methods=["GET"])
def get_faked_data():
    print("calling get_faked_data...")
    faked_data = read_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.FAKED_DATA_FILE_NAME}"
    )
    return (
        jsonify({"message": "getting faked data", "faked_data": faked_data}),
        200,
    )


@app.route("/generate_design_hypothesis", methods=["POST"])
def generate_design_hypothesis():
    print("calling generate_design_hypothesis...")
    prompt = read_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.PROMPT_FILE_NAME}"
    )
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    faked_data = read_file(f"{folder_path}/{globals.FAKED_DATA_FILE_NAME}")
    design_hypothesis = get_generated_design_hypothesis(prompt, faked_data)
    task_map_json = (
        json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
        if file_exists(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}")
        else {}
    )
    task_map = {int(key): value for key, value in task_map_json.items()}
    if folder_exists(f"{folder_path}/1"):
        wipeout_code(folder_path, 1, task_map, globals.current_prototype)
    create_and_write_file(
        f"{folder_path}/{globals.PROMPT_FILE_NAME}",
        prompt,
    )
    create_and_write_file(
        f"{folder_path}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}",
        design_hypothesis,
    )
    return (
        jsonify(
            {
                "message": "Generated design hypothesis",
                "hypothesis": design_hypothesis,
            }
        ),
        200,
    )


@app.route("/save_design_hypothesis", methods=["POST"])
def save_design_hypothesis():
    print("calling save_design_hypothesis...")
    data = request.json
    design_hypothesis = data["design_hypothesis"]
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_map_json = (
        json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
        if file_exists(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}")
        else {}
    )
    task_map = {int(key): value for key, value in task_map_json.items()}
    if folder_exists(f"{folder_path}/1"):
        wipeout_code(folder_path, 1, task_map, globals.current_prototype)
    create_and_write_file(
        f"{folder_path}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}",
        design_hypothesis,
    )
    return (
        jsonify({"message": "Saved design hypothesis", "data": design_hypothesis}),
        200,
    )


@app.route("/get_design_hypothesis", methods=["GET"])
def get_design_hypothesis():
    print("calling get_design_hypothesis...")
    design_hypothesis = read_file(
        f"{globals.folder_path}/{globals.current_prototype}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}"
    )
    return (
        jsonify(
            {
                "message": "getting design hypothesis",
                "design_hypothesis": design_hypothesis,
            }
        ),
        200,
    )


@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    print("calling generate_plan...")
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    design_hypothesis = read_file(
        f"{folder_path}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}"
    )
    plan = get_generated_plan(design_hypothesis)
    task_map_json = (
        json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
        if file_exists(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}")
        else {}
    )
    task_map = {int(key): value for key, value in task_map_json.items()}
    if folder_exists(f"{folder_path}/1"):
        wipeout_code(folder_path, 1, task_map, globals.current_prototype)
    task_map = {
        int(task["task_id"]): {
            "task": task["task"],
            globals.CURRENT_DEBUG_ITERATION: 0,
            globals.DEBUG_ITERATION_MAP: {},
        }
        for task in plan
    }
    create_and_write_file(
        f"{folder_path}/{globals.TASK_MAP_FILE_NAME}",
        json.dumps(task_map),
    )
    print(task_map)
    return jsonify({"message": "Generated Plan", "plan": plan}), 200


@app.route("/get_plan", methods=["GET"])
def get_plan():
    print("calling get_plan...")
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    plan = get_plan_from_task_map(folder_path)
    return jsonify({"message": "getting plan", "plan": plan}), 200


@app.route("/update_step_in_plan", methods=["POST"])
def update_step_in_plan():
    print("calling update_step_in_plan")
    data = request.json
    task_id = int(data["task_id"])
    new_task_description = data["task_description"]
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_map_json = json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
    task_map = {int(key): value for key, value in task_map_json.items()}
    task_map[task_id]["task"] = new_task_description
    if folder_exists(f"{folder_path}/{task_id}"):
        wipeout_code(folder_path, task_id, task_map, globals.current_prototype)
    create_and_write_file(
        f"{folder_path}/{globals.TASK_MAP_FILE_NAME}",
        json.dumps(task_map),
    )
    plan = json.loads(get_plan_from_task_map(folder_path))
    return (
        jsonify({"message": f"Updated step in plan for {task_id}", "data": plan}),
        200,
    )


@app.route("/add_step_in_plan", methods=["POST"])
def add_step_in_plan():
    print("calling add_step_in_plan")
    data = request.json
    curr_task_id = int(data["current_task_id"])
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    new_task_id = curr_task_id + 1
    new_task_description = data["new_task_description"]
    task_map_json = json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
    task_map = {int(key): value for key, value in task_map_json.items()}
    keys_to_shift = sorted(
        [key for key in task_map if key >= new_task_id], reverse=True
    )
    for key in keys_to_shift:
        task_map[key + 1] = task_map.pop(key)
    task_map[new_task_id] = {
        "task": new_task_description,
        globals.CURRENT_DEBUG_ITERATION: 0,
        globals.DEBUG_ITERATION_MAP: {},
    }
    task_map = {key: task_map[key] for key in sorted(task_map)}
    if folder_exists(f"{folder_path}/{new_task_id}"):
        wipeout_code(folder_path, new_task_id, task_map, globals.current_prototype)
    create_and_write_file(
        f"{folder_path}/{globals.TASK_MAP_FILE_NAME}",
        json.dumps(task_map),
    )
    plan = json.loads(get_plan_from_task_map(folder_path))
    return (
        jsonify({"message": f"Added step in plan for {new_task_id}", "data": plan}),
        200,
    )


@app.route("/remove_step_in_plan", methods=["POST"])
def remove_step_in_plan():
    print("calling remove_step_in_plan")
    data = request.json
    task_id = int(data["task_id"])
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_map_json = json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
    task_map = {int(key): value for key, value in task_map_json.items()}
    task_map.pop(task_id)
    keys_to_shift = sorted([key for key in task_map if key > task_id])
    for key in keys_to_shift:
        task_map[key - 1] = task_map.pop(key)
    if folder_exists(f"{folder_path}/{task_id}"):
        wipeout_code(folder_path, task_id, task_map, globals.current_prototype)
    create_and_write_file(
        f"{folder_path}/{globals.TASK_MAP_FILE_NAME}",
        json.dumps(task_map),
    )
    plan = json.loads(get_plan_from_task_map(folder_path))
    return (
        jsonify({"message": f"Removed step in plan for {task_id}", "data": plan}),
        200,
    )


# For testing only. Run curl http://127.0.0.1:5000/generate_code
@app.route("/generate_code", methods=["POST"])
def generate_code():
    print("calling generate_code...")
    data = request.json
    task_id = int(data["task_id"])
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_code_folder_path = f"{folder_path}/{task_id}"
    design_hypothesis = read_file(
        f"{folder_path}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}"
    )
    task_map_json = json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
    task_map = {int(key): value for key, value in task_map_json.items()}
    if folder_exists(task_code_folder_path):
        wipeout_code(folder_path, task_id, task_map, globals.current_prototype)
    faked_data = read_file(f"{folder_path}/{globals.FAKED_DATA_FILE_NAME}")
    plan = json.loads(get_plan_from_task_map(folder_path))
    implement_plan_lock_step(design_hypothesis, plan, folder_path, task_id, faked_data)
    task_main_code_folder_path = (
        f"{folder_path}/{task_id}/{globals.MAIN_CODE_FILE_NAME}"
    )
    code = read_file(task_main_code_folder_path)
    return jsonify({"message": "Generated code", "code": code}), 200


@app.route("/get_code_per_step", methods=["GET"])
def get_code_per_step():
    print("calling get_code_per_step...")
    task_id = request.args.get("task_id")
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_main_code_folder_path = (
        f"{folder_path}/{task_id}/{globals.MAIN_CODE_FILE_NAME}"
    )
    code = read_file(task_main_code_folder_path) or ""
    return jsonify({"message": f"grabbed code for {task_id}", "code": code}), 200


@app.route("/get_iteration_map_per_step", methods=["GET"])
def get_iteration_map_per_step():
    print("calling get_iteration_map_per_step...")
    task_id = int(request.args.get("task_id"))
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_map_json = json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
    task_map = {int(key): value for key, value in task_map_json.items()}
    print(task_map[task_id][globals.DEBUG_ITERATION_MAP])
    return (
        jsonify(
            {
                "message": f"grabbed iteration_map for {task_id}",
                "iterations": task_map[task_id][globals.DEBUG_ITERATION_MAP],
            }
        ),
        200,
    )


@app.route("/get_code_per_step_per_iteration", methods=["GET"])
def get_code_per_step_per_iteration():
    print("calling get_code_per_step_per_iteration...")
    task_id = request.args.get("task_id")
    iteration = request.args.get("iteration")
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    code_folder_path = ""
    if iteration == "0":
        code_folder_path = f"{folder_path}/{task_id}/{globals.CLEANED_CODE_FILE_NAME}"
    else:
        code_folder_path = f"{folder_path}/{task_id}/{globals.ITERATION_FOLDER_NAME}/{iteration}/{globals.ITERATION_CLEANED_FILE_NAME}"
    code = read_file(code_folder_path) or ""
    create_and_write_file(
        f"{folder_path}/{task_id}/{globals.MAIN_CODE_FILE_NAME}", code
    )
    return (
        jsonify(
            {
                "message": f"grabbed code for {task_id} and iteration {iteration}",
                "code": code,
            }
        ),
        200,
    )


@app.route("/delete_code_per_step_per_iteration", methods=["POST"])
def delete_code_per_step_per_iteration():
    print("calling delete_code_per_step_per_iteration...")
    data = request.json
    task_id = int(data["task_id"])
    iteration = data["iteration"]
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_map_json = json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
    task_map = {int(key): value for key, value in task_map_json.items()}
    print(
        f"deleting {iteration} {task_map[task_id][globals.DEBUG_ITERATION_MAP][str(iteration)]}"
    )
    task_map[task_id][globals.DEBUG_ITERATION_MAP].pop(str(iteration), None)
    print(
        f"after, task id {task_id} iteration {iteration}, {task_map[task_id][globals.DEBUG_ITERATION_MAP]}"
    )
    create_and_write_file(
        f"{folder_path}/{globals.TASK_MAP_FILE_NAME}",
        json.dumps(task_map),
    )
    return jsonify({"message": f"deleted iteration for {task_id} {iteration}"}), 200


@app.route("/save_code_per_step", methods=["POST"])
def save_code_per_step():
    print("calling get_code_per_step...")
    data = request.json
    task_id = data["task_id"]
    code = data["code"]
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_main_code_folder_path = (
        f"{folder_path}/{task_id}/{globals.MAIN_CODE_FILE_NAME}"
    )
    create_and_write_file(task_main_code_folder_path, code)
    print(code)
    return jsonify({"message": f"Grabbed code for {task_id}", "code": code}), 200


@app.route("/iterate_code", methods=["POST"])
def iterate_code():
    print("calling iterate_code...")
    data = request.json
    task_id = data["task_id"]
    problem = data["problem"]
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    task_map_json = json.loads(read_file(f"{folder_path}/{globals.TASK_MAP_FILE_NAME}"))
    task_map = {int(key): value for key, value in task_map_json.items()}
    task_map[task_id][globals.CURRENT_DEBUG_ITERATION] = (
        task_map[task_id][globals.CURRENT_DEBUG_ITERATION] + 1
    )
    faked_data = read_file(
        f"{folder_path}/{globals.FAKED_DATA_FILE_NAME}",
    )
    current_debug_iteration = task_map[task_id][globals.CURRENT_DEBUG_ITERATION]
    task_map[task_id][globals.DEBUG_ITERATION_MAP][
        str(current_debug_iteration)
    ] = problem
    print(task_map)
    create_and_write_file(
        f"{folder_path}/{globals.TASK_MAP_FILE_NAME}",
        json.dumps(task_map),
    )
    task = task_map[task_id]["task"]
    task_code_folder_path = f"{folder_path}/{task_id}"
    current_iteration_folder_path = f"{task_code_folder_path}/{globals.ITERATION_FOLDER_NAME}/{current_debug_iteration}"
    create_folder(current_iteration_folder_path)
    design_hypothesis = read_file(
        f"{folder_path}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}"
    )
    get_iterate_code(
        problem,
        task,
        task_code_folder_path,
        current_iteration_folder_path,
        design_hypothesis,
        faked_data,
    )
    return (
        jsonify(
            {
                "message": "Debugged and regenerated code",
                "current_iteration": task_map[task_id][globals.CURRENT_DEBUG_ITERATION],
            }
        ),
        200,
    )


@app.route("/get_test_cases_per_lock_step", methods=["GET"])
def get_test_cases_per_lock_step():
    print("calling get_test_cases_per_lock_step...")
    task_id = int(request.args.get("task_id"))
    folder_path = f"{globals.folder_path}/{globals.current_prototype}"
    index = task_id - 1
    plan = json.loads(read_file(f"{folder_path}/{globals.PLAN_FILE_NAME}"))
    task = plan[index]["task"]
    design_hypothesis = read_file(
        f"{folder_path}/{globals.DESIGN_HYPOTHESIS_FILE_NAME}"
    )
    test_cases = test_code_per_lock_step(task, design_hypothesis)
    return (
        jsonify(
            {
                "message": f"Grabbed test cases for {task_id} {task}",
                "test_cases": json.loads(test_cases),
            }
        ),
        200,
    )


# For testing only. Run curl http://127.0.0.1:5000/set_globals_for_uuid/uuid
@app.route("/set_globals_for_uuid/<generated_uuid>", methods=["GET"])
def set_globals_for_uuid(generated_uuid):
    print("calling set_globals_for_uuid")
    globals.folder_path = f"{globals.GENERATED_FOLDER_PATH}/{generated_uuid}"
    globals.prototypes = json.loads(
        read_file(f"{globals.folder_path}/{globals.PROTOTYPES}")
    )
    globals.matrix = json.loads(
        read_file(f"{globals.folder_path}/{globals.MATRIX_FILE_NAME}")
    )
    globals.problem = read_file(f"{globals.folder_path}/{globals.PROBLEM_FILE_NAME}")
    return jsonify({"message": "Successfully set global fields"}), 200


# Running app
if __name__ == "__main__":
    app.run(debug=True)
