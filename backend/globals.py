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
            model="claude-3-sonnet-20240229",
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


MATRIX_FILE_NAME = "matrix.txt"

CONFIG_FILE_NAME = "config.txt"
PROBLEM_FILE_NAME = "problem.txt"
PROTOTYPES = "prototypes.txt"
MATRIX_FOLDER_NAME = "matrix"

GENERATED_FOLDER_PATH = "generated"

# matrix fields
problem = None
matrix = {
    "AgentsXIdea": None,
    "AgentsXGrounding": None,
    "ActionsXIdea": None,
    "ActionsXGrounding": None,
    "WorldXIdea": None,
    "WorldXGrounding": None,
    "StopConditionXIdea": None,
    "StopConditionXGrounding": None,
}
# all prototypes to explore
prototypes = []
current_prototype = None
# folder for this code generation, in the form of a UUID
folder_path = None
