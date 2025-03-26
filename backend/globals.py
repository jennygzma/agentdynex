import os
import secrets

import globals
from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI

# either anthropic or openai
LLM = "anthropic"

# Load variables from .env file
load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

anthropic_client = Anthropic(api_key=anthropic_api_key)
openai_client = OpenAI(api_key=openai_api_key)


def call_llm(system_message, user_message, llm=globals.LLM):
    if llm == "anthropic":
        temperature = secrets.randbelow(10**6) / 10**6
        message = anthropic_client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=4096,
            temperature=temperature,
            system=system_message,
            messages=[{"role": "user", "content": user_message}],
        )
        return message.content[0].text
    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]
    message = openai_client.chat.completions.create(model="gpt-4", messages=messages)
    return message.choices[0].message.content


PROBLEM_FILE_NAME = "problem.txt"
PROTOTYPES = "prototypes.txt"
MATRIX_FILE_NAME = "matrix.txt"
CONFIG_FILE_NAME = "config.txt"
MILESTONES_FILE_NAME = "milestones.txt"
DYNAMICS_FILE_NAME = "dynamics.json"
CHANGES_FILE_NAME = "changes.json"
STATIC_LIST_FILE_NAME = "static_list.json"
ITERATIVE_LIST_FILE_NAME = "iterative_list.json"
FIXES_TO_APPLY_FILE_NAME = "fixes_to_apply.json"
RUN_TREE = "run_tree.json"

# config iteration logic
INITIAL_CONFIG_FILE = "initial_config.txt"
LOGS_FILE = "logs.txt"
ANALYSIS_FILE = "analysis.txt"
SUMMARY_FILE = "summary.txt"
UPDATED_CONFIG = "updated_config.txt"

GENERATED_FOLDER_NAME = "generated"
CONFIG_ITERATIONS_FOLDER_NAME = "config_iterations"

# matrix fields
problem = None
matrix = {
    "AgentsXIdea": None,
    "AgentsXGrounding": None,
    "ActionsXIdea": None,
    "ActionsXGrounding": None,
    "LocationsXIdea": None,
    "LocationsXGrounding": None,
    "MilestonesXIdea": None,
    "MilestonesXGrounding": None,
    "StopConditionXIdea": None,
    "StopConditionXGrounding": None,
    "FailureConditionXIdea": None,
    "FailureConditionXGrounding": None,
}
run_tree = None
config = None
run_id = None
milestones = None
current_milestone_id = "1"
iterative_list = None
static_list = None
fixes_to_apply = []

# all prototypes to explore
prototypes = []
current_prototype = None
# folder for this code generation, in the form of a UUID
folder_path = None
rubric = None
