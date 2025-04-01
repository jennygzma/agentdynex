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

config_example = """
{
    "world_name": "Ultimatum Game",
    "locations": [
        {
            "name": "Negotiation Room",
            "description": "A shared space where the Proposer and Responder interact to make and respond to offers."
        },
        {
            "name": "Proposer's Room",
            "description": "A private space where the Proposer deliberates on the offer before submitting it."
        },
        {
            "name": "Responder's Room",
            "description": "A private space where the Responder deliberates on whether to accept or reject an offer."
        }
    ],
    "agents": [
        {
            "first_name": "Mediator",
            "private_bio": "",
            "public_bio": "The Mediator facilitates the Ultimatum Game, ensures smooth interactions between the Proposer and Responder, enforces rules, and announces the results.",
            "directives": [
                "Announce the start of the Ultimatum Game. If no announcement is detected within 10 seconds, retry until confirmation.",
                "Ensure both Proposer and Responder arrive in the Negotiation Room before starting the round.",
                "Before processing payouts, verify that a valid total sum was retrieved. If not, prompt the Proposer to provide it.",
                "If the total sum is missing and cannot be retrieved, assume a default total sum of 100 units.",
                "Explicitly confirm that the total sum has been announced and acknowledged by the Proposer and Responder before proceeding.",
                "If the Proposer does not submit an offer within 30 seconds, assign a default minimum offer.",
                "If the Responder does not respond within 30 seconds, assume rejection and proceed.",
                "Retrieve and store the total sum, compute Proposer and Responder payouts, and confirm the final amounts before announcing.",
                "Announce whether the offer was accepted or rejected.",
                "If accepted, allocate the proposed split to both players and announce the payout.",
                "If rejected, announce that both players receive nothing.",
                "Ensure all actions are completed before moving to the next round.",
                "Do not finalize the round until all payout calculations have been confirmed.",
                "Declare the end of the simulation after the predetermined number of rounds."
            ],
            "initial_plan": {
                "description": "Facilitate the Ultimatum Game by enforcing offer submission, response deadlines, and payout calculations.",
                "stop_condition": "Final round has been completed, and all payouts have been successfully confirmed.",
                "location": "Negotiation Room"
            }
        },
        {
            "first_name": "Proposer",
            "private_bio": "",
            "public_bio": "The Proposer makes an offer on how to split a given sum with the Responder.",
            "directives": [
                "At the start of each round, move to the Negotiation Room.",
                "Retrieve the total sum available for distribution before submitting an offer. If the total sum is unknown, request clarification from the Mediator.",
                "Confirm receipt of the total sum announcement from the Mediator before proceeding.",
                "Select and submit an offer within 30 seconds, regardless of whether the Responder has arrived.",
                "If no offer is submitted within 30 seconds, default to a predefined minimum offer.",
                "Confirm receipt of the offer by the Mediator. If not acknowledged, resend until confirmation.",
                "Wait for the Mediator to announce the Responder’s decision.",
                "If the offer is accepted, receive the allocated amount.",
                "If the offer is rejected, receive nothing and prepare for the next round.",
                "Return to the Proposer’s Room between rounds to deliberate on the next offer.",
                "Do not request human input for total sum verification. Use stored values or predefined defaults."
            ],
            "initial_plan": {
                "description": "Participate in the Ultimatum Game by making and submitting offers in each round.",
                "stop_condition": "Final round has been completed or timeout occurs for submission.",
                "location": "Negotiation Room"
            }
        },
        {
            "first_name": "Responder",
            "private_bio": "",
            "public_bio": "The Responder decides whether to accept or reject the Proposer’s offer.",
            "directives": [
                "At the start of each round, move to the Negotiation Room.",
                "Wait up to 30 seconds for an offer to arrive.",
                "If no offer is received within 30 seconds, assume a zero offer and reject it.",
                "Submit an accept/reject decision within 30 seconds.",
                "If the Mediator does not acknowledge receipt of the response, resend it until confirmation.",
                "If the offer is accepted, receive the allocated amount.",
                "If the offer is rejected, receive nothing and prepare for the next round.",
                "Return to the Responder’s Room between rounds to deliberate on the next response strategy."
            ],
            "initial_plan": {
                "description": "Participate in the Ultimatum Game by reviewing and responding to offers when prompted.",
                "stop_condition": "Final round has been completed or timeout occurs for response submission.",
                "location": "Negotiation Room"
            }
        }
    ]
}
"""
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
        2. EXPLICITLY STATE THAT AGENTS CANNOT DISCUSS FOR MORE THAN 3 ROUNDS WITH OTHER AGENTS BEFORE MOVING ON.THEY MUST GET THEIR POINT ACROSS BY THEN.
        3. IF THERE ARE MULTIPLE LOCATIONS, ENSURE THAT AGENTS KNOW THEY CAN MOVE TO CERTAIN LOCATIONS AND TELL THEM THE RULES OF THAT LOCATION.
        4. Do not specify any date or time in the config. ONLY SPEAK BY ROUNDS For example, do not say “wait for 5 minutes”, or “submit before March 16”, or “submit a day early”.
        5. Everything in the action column (ActionsXIdea, ActionsXGrounding) should be incorporated in the directives for each agent. If it has to do with when the simulation stops, it should be in the stop condition.
"""
# 2. For every simulation, create an agent called "Overseer". The overseer will be a neutral force in the simulation that PLAYS NO ROLE IN THE SIMULATION except to keep the simulation on track. Specifically, the overseer will ensure that:
#             - The primary job of the overseer is to make sure the simulation runs smoothly and properly defines the simulation. It can act as a mediator, it can act as a clock, or an enforcer. It is essentially an invisible presence that forces the simulation to move foward and that the agents are acting in logicaly sound ways.
#             - THE OVERSEER NEEDS TO UNDERSTAND THE PROGRESS OF THE SIMULATION ACCURATELY.
#             - IN ALMOST ALL CASES, THE OVERSEER CANNOT TALK TO ANY AGENT UNLESS THE AGENT IS DOING SOMETHING ALONG THE LINES OF A FAILURE CONDITION OR A LOGISTICAL FAILURE.
#             - THE OVERSEER CANNOT "ENCOURAGE" ANYONE, THEY CANNOT "GIVE PEP TALKS", THEY CANNOT RANDOMLY HOP INTO A CONVERSATION IF THE SIMULATION IS GOIGN WELL.
#             - THE OVERSEER CAN ONLY SAY VERY NEUTRAL PHRASES TO PUSH SIMULATION FORWARD.
#             - The overseer will also fill in-place any sort of logistic that wasn't covered. It essentially fills in the logical gaps of the simulation
#                 - For example, if votes need to be counted but there is no agent available for vote coutning, the overseer can take that role.
#             - The overseer wil enforce the rules of the simulation. For example, if only a certain amount of agents can be in a location, they can enforce this.
#             - THE OVERSEER CANNOT INFLUENCE THE BEHAVIOR OF THE AGENTS. THEY CANNOT TALK TO THE AGENTS UNLESS IT IS ABOUT SOMETHING LOGISTICAL THAT IS GOING WRONG TO GUIDE THE AGENTS IN THE RIGHT DIRECTION AGAIN.
#                 - For example, when conducting a simulation regarding agents going to swim practice, the overseer cannot tell the swimmers they should go to practice and they need to calm down. They can only talk to the swimmer if the swimmer themselves has declared they will go to practice but are still stuck in the team room, because that is a logical problem with the simulation.
#                 - For example, when conducting a simulation where people need to go to prom, the overseer cannot influence how the agents ask eachother or who they want to ask. Hoewver, they can interfere if Bob agrees to go with Alice but Bob has already agreed to go with Jenny, to tell Bob he has already committed to a date and needs to reject one of them because that is a logical error of the simulation.
#             - THE AGENTS CANNOT TALK TO THE OVERSEER. BUT THEY MUST LISTEN TO THE OVERSEER TO ACKNOWLEDGE IT. THEY CANNOT GO INTO DISCUSSION WITH THE OVERSEER. If the overseer speaks to an agent that means they have done something logically insensible.
#                 - f agents try to do something within the failure-conditions list, then the overseer will redirect the agent.
#             - ensure that agents cannot speak to the OVERSEER, unlses the OVERSEER talks to them first. And if they do speak to the overseer, it is just to respond to the overseer to get the simulation moving. THIS MUST BE DEFINED IN EACH AGENT'S DIRECTIVE.
#             - If there is a really long stall in the simulation where milestones are not being completed, the overseer must intervene to keep the simulation on track and finish at a reasonable time. If the agents are stuck in a waiting loop, the overseer can intervene
#                 - For example, when conducting a simulation where people need to find partners for prom, if after 5 rounds of discussion Felicia is still "waiting" or not making a decision, the Overseer can remind everyone that prom is coming soon and they have to make a decision soon.
#             - Agents stay on track in completing each milestone, so the milestones must be FULLY EMBEDDED INTO THE OVERSEER AGENT'S DIRECTIVES.
#             - Agents in the simulation defined by the user CANNOT TALK TO THE OVERSEER, but must LISTEN TO THE OVERSEER if the overseer speaks to them because there is something logically wrong with what the agent is doing.


def get_matrix_description(matrix):
    print("get_matrix_description...")
    description = ""

    if matrix["AgentsXIdea"]:
        description += f"\nThe agenst will be {matrix['AgentsXIdea']}."
        if matrix["AgentsXGrounding"]:
            description += f" For more details: {matrix['AgentsXGrounding']}"

    if matrix["ActionsXIdea"]:
        description += f"\nThe actions the different agents can take will be: {matrix['ActionsXIdea']}."
        if matrix["ActionsXGrounding"]:
            description += f" For more details: {matrix['ActionsXGrounding']}"

    if matrix["LocationsXIdea"]:
        description += f"\nThe locations that the simulation will exist in should be {matrix['LocationsXIdea']}."
        if matrix["LocationsXGrounding"]:
            description += f" For more details: {matrix['LocationsXGrounding']}"

    if matrix["MilestonesXIdea"]:
        description += f"\nThe chronological milestones in the simulation should be {matrix['MilestonesXIdea']}."
        if matrix["MilestonesXGrounding"]:
            description += f" For more details: {matrix['MilestonesXGrounding']}"

    if matrix["StopConditionXIdea"]:
        description += f"\nThe stop condition for when the simulation is over should be {matrix['StopConditionXIdea']}."
        if matrix["StopConditionXGrounding"]:
            description += f" For more details: {matrix['StopConditionXGrounding']}"

    if matrix["FailureConditionXIdea"]:
        description += f"\nIndications that the simulation has gone awry are {matrix['FailureConditionXIdea']}."
        if matrix["FailureConditionXGrounding"]:
            description += f" For more details: {matrix['FailureConditionXGrounding']}"

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
    res = "Here is the config " + call_llm(system_message, user_message)
    json = cleanup_json(res)
    print("sucessfully called LLM for generate_config", json)
    return json


def cleanup_json(json):
    print("calling LLM for cleanup_json...")
    user_message = f"This is the JSON: \n {json}"
    system_message = f"""
        You are cleaning up a JSON file to ensure that it runs on first try.
        If the code runs on first try, return the code.
        DO NOT DELETE ANY CODE. Only remove natural language. The goal is to have the code compile. Comments are okay.
        This is an EXAMPLE of a result: {config_example}.
    """
    cleaned_json = call_llm(system_message, user_message)
    print("successfully called LLM for cleanup_json: " + cleaned_json)
    return cleaned_json
