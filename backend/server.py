# This file acts as a controller to route API requests

import datetime
import json
import uuid

import globals
from code_generation import get_fake_data, implement_plan_lock_step
from flask import Flask, jsonify, request
from planning import get_design_hypothesis, get_plan
from utils import create_and_write_file, create_folder, read_file

# Initializing flask app
app = Flask(__name__)

@app.route("/generate_fake_data", methods=["POST"])
def generate_fake_data():
    print("calling generate_fake_data...")
    data = request.json
    globals.data_model = data["data_model"]
    data = get_fake_data(globals.data_model)
    return jsonify({"message": "Generated code", "fake_data": data}), 200


@app.route("/save_faked_data", methods=["POST"])
def save_faked_data():
    print("calling save_faked_data...")
    data = request.json
    globals.faked_data = data["faked_data"]
    create_and_write_file(f"{globals.folder_path}/{globals.FAKED_DATA_FILE_NAME}", globals.faked_data)
    return jsonify({"message": "Saved faked data", "data": globals.faked_data}), 200


@app.route("/generate_design_hypothesis", methods=["POST"])
def generate_design_hypothesis():
    print("calling generate_design_hypothesis...")
    data = request.json
    globals.prompt = data["prompt"]
    globals.design_hypothesis = get_design_hypothesis(globals.prompt, globals.data_model)
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    globals.folder_path = (
        f"{globals.GENERATED_FOLDER_PATH}/generations_{date_time}_{uuid.uuid4()}"
    )
    create_folder(globals.folder_path)
    return (
        jsonify(
            {"message": "Generated design hypothesis", "hypothesis": globals.design_hypothesis}
        ),
        200,
    )


@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    print("calling generate_plan...")
    stringified_plan = get_plan(globals.design_hypothesis)
    globals.plan = json.loads(stringified_plan)
    return jsonify({"message": "Generated Plan", "plan": stringified_plan}), 200

# Run curl http://127.0.0.1:5000/generate_code
@app.route("/generate_code", methods=["GET"])
def generate_code():
    print("calling generate_code...")
    file_path = implement_plan_lock_step(
        globals.design_hypothesis, globals.plan, globals.faked_data, globals.folder_path
    )
    # file_path = implement_plan(globals.prompt, globals.plan, globals.faked_data, globals.design_hypothesis, globals.folder_path)
    code = read_file(file_path)
    return jsonify({"message": "Generated code", "code": code}), 200


# For testing only. Run curl http://127.0.0.1:5000/set_globals_for_debug
@app.route("/set_globals_for_debug", methods=["GET"])
def set_globals_for_debug():
    print("calling set_globals_for_debug...")
    globals.folder_path = f"{globals.GENERATED_FOLDER_PATH}/generations_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{uuid.uuid4()}"
    globals.prompt = "i want a UI that will visualize the grocery inventory i have. i want it to be gmail and table-like."
    globals.data_model = {
        "title": "Brown eggs",
        "type": "dairy",
        "description": "Raw organic brown eggs in a basket",
        "quantity": 200,
        "price": 28.1,
        "rating": 4
    }
    globals.faked_data = [
        {
            "title": "Brown eggs",
            "type": "dairy",
            "description": "Raw organic brown eggs in a basket",
            "quantity": 200,
            "price": 28.1,
            "rating": 4
        },
        {
            "title": "White eggs",
            "type": "dairy",
            "description": "Raw organic white eggs in a carton",
            "quantity": 300,
            "price": 30.2,
            "rating": 4.1
        },
        {
            "title": "Jumbo eggs",
            "type": "dairy",
            "description": "Large raw organic eggs in a container",
            "quantity": 150,
            "price": 35.5,
            "rating": 4.8
        },
        {
            "title": "Organic milk",
            "type": "dairy",
            "description": "Fresh organic whole milk in a bottle",
            "quantity": 500,
            "price": 22.2,
            "rating": 4.6
        },
        {
            "title": "Butter",
            "type": "dairy",
            "description": "Creamy organic unsalted butter",
            "quantity": 250,
            "price": 20.1,
            "rating": 4.3
        },
        {
            "title": "Cheese",
            "type": "dairy",
            "description": "White cheddar cheese block",
            "quantity": 120,
            "price": 33.2,
            "rating": 4.7
        },
        {
            "title": "Yogurt",
            "type": "dairy",
            "description": "Greek yogurt in a tub",
            "quantity": 400,
            "price": 15.5,
            "rating": 4.2
        },
        {
            "title": "Cream",
            "type": "dairy",
            "description": "Heavy cream in a carton",
            "quantity": 325,
            "price": 26.6,
            "rating": 4.4
        },
        {
            "title": "Sour cream",
            "type": "dairy",
            "description": "Sour cream in a tub",
            "quantity": 210,
            "price": 18,
            "rating": 3.9
        },
        {
            "title": "Cottage cheese",
            "type": "dairy",
            "description": "Low-fat cottage cheese in a tub",
            "quantity": 175,
            "price": 21.3,
            "rating": 3.8
        }
    ]
    globals.design_hypothesis = "The UI will be designed as a table, resembling Gmail, featuring columns like 'Item name', 'Quantity', 'Expiration Date', and 'Category'. Users can add, delete and update items. Clicking a row will open a detailed view of the item, including its nutritional information. A search bar, at the top, allows users to quickly find specific items."
    globals.plan = [
        {
            "task_id": 1,
            "task": "Create the basic HTML structure",
            "dep": []
        },
        {
            "task_id": 2,
            "task": "Implement the table with labeled columns for 'Item name', 'Quantity', 'Expiration Date', and 'Category'",
            "dep": [1]
        },
        {
            "task_id": 3,
            "task": "Create a form with fields corresponding to the table columns to add new items",
            "dep": [1]
        },
        {
            "task_id": 4,
            "task": "Create a search bar and design it to filter table items",
            "dep": [2]
        },
        {
            "task_id": 5,
            "task": "Create the detailed view window for the item that appears on a click event on a table row",
            "dep": [2]
        },
        {
            "task_id": 6,
            "task": "Implement the item delete and update functionalities",
            "dep": [2,3]
        }
    ]
    return jsonify({"message": "Successfully set global fields"}), 200

# Running app
if __name__ == "__main__":
    app.run(debug=True)
