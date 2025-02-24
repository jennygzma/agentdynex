# This file handles saving mocked data, generating, and cleaning up the code based on the task list
import os

from globals import call_llm

# HOW CODE GENERATION FOLDER WORKS
# - They will all rest in generated/generations_[timestamp]_[uuid]
# - They will all have a faked_data.json file

# - for lock step
# [code_folder_path]/index.html - main code that is changed and updated constantly
# [code_folder_path]/checked.html - after all the steps, the final checked code
# [code_folder_path]/cleaned.html - after all the steps, the final cleaned code
# [code_folder_path]/[task_id]/merged.html - initial generated code per task_id
# [code_folder_path]/[task_id]/checked.html - checked generated code per task_id - currently not being used
# [code_folder_path]/[task_id]/cleaned.html - cleaned generated code per task_id

# for one shot
# index.html - main code that is changed and updated constantly
# initial.html - initial code
# checked.html - checked code
# cleaned.html - cleaned code

openai_api_key = os.getenv("OPENAI_API_KEY")

annotated_config_example = """
{
    "world_name": "Clasroom Scenario NO-P - One Room",
    "locations": [
        {
            "name": "Classroom",
            "description": "The classroom is where students and the professor are and interact with one another. The professor makes announcements to the class - including of the late policy and of assignments."  // the location's description should have be short and concise and describe what an agent or multiple agents will do in there. it should also describe WHERE each agent should go
        }
    ],
    "agents": [
        {
            "first_name": "Professor",
            "private_bio": "",  // the private bio is short but will describe the personality of the agent. in this case, since the professor doesn't really need to have a personality.
            "public_bio": "The professor is carrying out a semester of instruction of a course. Her late policy involves not accepting any late assignments. Any assignment submitted late will not receive any credit.", // the public bio should be vague and not reveal the inherent personality of the agent. it can also refer to what the agent will do that the other agents should be aware of.
            "directives": [ // based on the personality, general and short directives are created for each agent relevant to the simulation. the directives can indicate how an agent will act based on the scenario (in this case, what happens when assignments are assigned), who they will interact with primarily, etc.
                "Maintain a good relationship will all students.",
                "Announce the assignment of five assignments at a regular intervals. Assignments should have due dates after one another.",
                "Assignments should be simple - do not provide descriptions of them, simply tell students that you have an assignment to announce.", // the directive does not ask the students to submit a real assignment, but instead, a proxie of a simple assignment, because it knows that the students are agents in a multi-agent simulation
                "Engage with students when they ask questions or address the Professor.",
                "The late policy should be clearly announced to all students.",
            ],
            "initial_plan": {
                "description": "Announce her late assignment policy to her students and assign five assignments over the course of the semester.", // the descrpition is short and describes what the agent must do. it has nothing to do with the personality of the agent.
                "stop_condition": "The professor has announced five assignments over the course of the semester.", // the stop condition is objective and declares the state of the simulation to be over. it has nothing to do with the personality of the agent.
                "location": "Classroom" // everyone starts off at the same location so the professor can announce the late policy
            }
        },
        {
            "first_name": "Alice",
            "private_bio": "Alice is a procrastinator, often giving herself too little time to finish assignments.",  // the private bio is short but will describe the personality of the agent.
            "public_bio": "Alice is a student in the Professor's class.", // the public bio should be vague and not reveal the inherent personality of the agent.
            "directives": [ // based on the personality, general and short directives are created for each agent relevant to the simulation. the directives can indicate how an agent will act based on the scenario (in this case, what happens when assignments are assigned), who they will interact with primarily, etc.
                "Recognize the Professor's late policy and work on assignments accordingly.",
                "Try to still get a good grade in the class despite penalties for late assignments. Try to submit assignments on time when possible.",
                "Decide whether or not she will need to turn in each assignment late. Share with the Professor whether or not she will be submitting as assignment late, as well as when she submits it.",
                "While working on assignments, Alice can speak to her classmates (Bob and Casey) or the Professor.",
                "Each time a Professor assigns a new assignment, identify all previous assignments that Alice is still working on and has not yet turned in. Prioritize assignments based on their due dates."
            ],
            "initial_plan": {
                "description": "Listen to the Professor's announcements of assignments in the classroom. Work on the assignments as appropriate.", // the descrpition is short and describes what the agent must do. it has nothing to do with the personality of the agent.
                "stop_condition": "There are no more assignments left to complete in the semetser.", // the stop condition is objective and declares the state of the simulation to be over. it has nothing to do with the personality of the agent.
                "location": "Classroom" // everyone starts off at the same location so the professor can announce the late policy
            }
        },
        {
            "first_name": "Bob",
            "private_bio": "Bob is an overachiever - his only focus is getting a good grade, even if it means sacrificing on sleep or fun activities.",  // the private bio is short but will describe the personality of the agent.
            "public_bio": "Bob is a student in the Professor's class.", // the public bio should be vague and not reveal the inherent personality of the agent.
            "directives": [ // based on the personality, general and short directives are created for each agent relevant to the simulation. the directives can indicate how an agent will act based on the scenario (in this case, what happens when assignments are assigned), who they will interact with primarily, etc.
                "Recognize the Professor's late policy and work on assignments accordingly. Try to submit assignments on time when possible.",
                "Try to still get a good grade in the class despite penalties for late assignments.",
                "Decide whether or not he will need to turn in each assignment late. Share with the Professor whether or not he will be submitting as assignment late, as well as when he submits it.",
                "While working on assignments, Bob can speak to his classmates (Alice and Casey) or the Professor.",
                "Each time a Professor assigns a new assignment, identify all previous assignments that Bob is still working on and has not yet turned in. Prioritize assignments based on their due dates."
            ],
            "initial_plan": {
                "description": "Listen to the Professor's announcements of assignments in the classroom. Work on the assignments as appropriate.", // the descrpition is short and describes what the agent must do. it has nothing to do with the personality of the agent.
                "stop_condition": "There are no more assignments left to complete in the semetser.", // the stop condition is objective and declares the state of the simulation to be over. it has nothing to do with the personality of the agent.
                "location": "Classroom" // everyone starts off at the same location so the professor can announce the late policy
            }
        },
        {
            "first_name": "Casey",
            "private_bio": "Casey places a large amount of importance on work life balance. Despite wanting to do well, Casey will not overwork herself to finish an assignment on time.", // the private bio is short but will describe the personality of the agent.
            "public_bio": "Casey is a student in the Professor's class.", // the public bio should be vague and not reveal the inherent personality of the agent.
            "directives": [ // based on the personality, general and short directives are created for each agent relevant to the simulation. the directives can indicate how an agent will act based on the scenario (in this case, what happens when assignments are assigned), who they will interact with primarily, etc.
                "Recognize the Professor's late policy and work on assignments accordingly. Try to submit assignments on time when possible.",
                "Try to still get a good grade in the class despite penalties for late assignments.",
                "Decide whether or not she will need to turn in each assignment late. Share with the Professor whether or not she will be submitting as assignment late, as well as when she submits it.",
                "While working on assignments, Casey can speak to her classmates (Bob and Alice) or the Professor.",
                "Each time a Professor assigns a new assignment, identify all previous assignments that Casey is still working on and has not yet turned in. Prioritize assignments based on their due dates."
            ],
            "initial_plan": {
                "description": "Listen to the Professor's announcements of assignments in the classroom. Work on the assignments as appropriate.", // the descrpition is short and describes what the agent must do. it has nothing to do with the personality of the agent.
                "stop_condition": "There are no more assignments left to complete in the semetser.", // the stop condition is objective and declares the state of the simulation to be over. it has nothing to do with the personality of the agent.
                "location": "Classroom" // everyone starts off at the same location so the professor can announce the late policy
            }
        }
    ]
}
"""

config_rules = """
Please follow these rules while creating the JSON
        1. Please only return the JSON and nothing else.
        2. Do not specify any date or time in the config. For example, do not say “wait for 5 minutes”, or “submit before March 16”, or “submit a day early”.
        3. Everything in the action column (ActionsXIdea, ActionsXGrounding) should be incorporated in the directives for each agent. If it has to do with when the simulation stops, it should be in the stop condition.
        """


def get_matrix_description(matrix):
    print("get_matrix_description...")
    description = ""

    if matrix["AgentsXIdea"]:
        description += f"\nIt is for {matrix['AgentsXIdea']}."
        if matrix["AgentsXGrounding"]:
            description += f" For more details: {matrix['AgentsXGrounding']}"

    if matrix["ActionsXIdea"]:
        description += f"\nThe approach should be: {matrix['ActionsXIdea']}."
        if matrix["ActionsXGrounding"]:
            description += f" For more details: {matrix['ActionsXGrounding']}"

    if matrix["WorldXIdea"]:
        description += f"\nThe interaction paradigm shown in the interface should be {matrix['WorldXIdea']}."
        if matrix["WorldXGrounding"]:
            description += f" For more details: {matrix['WorldXGrounding']}"

    return description.strip()


def generate_config(problem, matrix):
    print("calling LLM for generate_config...")
    print(matrix)
    # print(json.load(matrix))
    matrix_description = get_matrix_description(matrix)
    system_message = f"""
    Based on this context, generate a config.
        {matrix_description}
      This is the format the config should be in:
        {annotated_config_example}
    Follow these rules when generating the config:
    {config_rules}
    """
    user_message = f"Please generate a config given this problem: {problem}"
    res = call_llm(system_message, user_message)
    print("sucessfully called LLM for generate_config", res)
    return res
