# This file handles brainstorming the spec and creating the task list.
import json

from globals import call_llm

PAAW_DESCRIPTION = """When we create a simulation based on a particular problem, we define it with a 3x2 problem matrix.
First, we problem further into 3 categories: Agents, Actions, and World Paradigm.
Within each category, there are 2 more sub-categories: idea and grounding.

Specifically we will use this matrix to create a configuration file for a multi-agent system, GPTeams.
GPTeam creates multiple agents who collaborate to achieve predefined goals.
GPTeam employs separate agents, each equipped with a memory, that interact with one another using communication as a tool.
Agents move around the world and perform tasks in different locations, depending on what they are doing and where other agents are located.
They can speak to each other and collaborate on tasks, working in parallel towards common goals.

"""

MATRIX_DESCRIPTIONS = {
    "AgentsXIdea": """Within the agents section, the idea subsection identifies who the necessary agents are in the simulation. It defines the different types of agents.
    Do you need mediators, students, professors, rich people, poor people?""",

    "AgentsXGrounding": """Within the agents section and the grounding subsection, we dig deeper into understanding each agent's personality and context.
    Specifically: What is each agent's driving personality? Identify the agents that will exist in the simulation. Keep it very simple.
    """,

    "ActionsXIdea": """Within the actions section and the idea subsection we think about how the agents should act in the simulation.
    What are the one or two actions agents need to do in order to complete the simulation? Are they contributing money? Are they submitting an assignment?""",

    "ActionsXGrounding": """Within the actions section and the grounding subsection, we focus on the tangible details of making the action feasible within the simulation.
    We keep it as simple as possible. Should the agent verbally declare that they submitted an assignment? Should the agent submit an assignment in a particular room?""",

    "WorldXIdea": """Within the world section and the idea subsection we contemplate the general design of the simulation.
    How should the simulated world look? How many rooms should there be in this world?""",

    "WorldXGrounding": """Within the world section and the grounding subsection, we delve into the specifics of each room:
    What will the agent do in each room? What is the purpose of each room?""",

    "StopConditionXIdea": """Within the stop condition section and the idea subsection we contemplate the stop condition of the simulation.
    When should the simulation stop?""",

    "StopConditionXGrounding": """Within the stop condition section and the grounding subsection, we delve into the specifics of the stop condition:
    Specifically, in what state should each agent and world be in for there to be a stop?
    """,
}

PAAW_EXAMPLES = """
Here are some examples:

Problem: Simulating people buying a house for a homeowner who really cares about the home but also cares about monetary value
AgentsXIdea: 1 real estate agent, 3 home-buyer agents
AgentsXGrounding:
Debbie: 1 real estate agent to facilitate the selling of the home. Does not care as much about financial gain as a good buyer who will love the home
Alice: first-time home buyer who is not as wealthy but will resort to emotional plea to seller to create an emotional connection
Bob: aggressive buyer who will offer significantly above the asking price
Charlie: strategic buyer who will offer a lot of cash
ActionsXIdea: real estate agent conducting the bidding, home-buyer agents making bids
ActionsXGrounding:
The real estate agent will declare the price of the home
The real estate agent will verbally ask agents to bid
The agents will not talk to each other. They will only speak to the real-estate agent when they are making their offers.
WorldXIdea: 1 bidding room, 1 waiting room for each agent to stay in
WorldXGrounding:
Bidding Room: where the home-buyer agents will travel here to speak to the real estate agent regarding their home bid. Home-buyer agents should come into this room whenever they want to make an offer or speak to the real-estate agent. Only one home-buyer agent is allowed in here at a time.
Waiting Room: where each agent will return to. They cannot speak to each other. This is where they will reflect and make their next move. All agents will start off in the waiting room and the bidding agent will declare the price of the home, then the bidding agent will move to the bidding room.
StopConditionXIdea: landlord or tenants cancel or extend the lease
StopConditionXGrounding:
Either the landlord agent tells all the tenants in the waiting room the new modified or unmodified lease they have to sign, and the tenant agents either reject or accept the new leases,
Or the tenant agents decide they don’t want to continue the lease.
The tenant agents should have had sufficient time discussing amongst themselves what they want to do (they are free to do anything), and also time to talk to the landlord.

Idea: Landlord implementing no-smoking policy
AgentsXIdea: 1 landlord agent, 3 tenant agents
AgentsXGrounding:
Sophia: landlord who does not want tenants to smoke
Nishaad: a young newly college-graduate student who is addicted to his vape. He wants to continue living in the apartment.
Mohan: a young married man who has no smoking addiction and is a stickler for rules. He wants to continue living in the apartment.
Tejas: an older man who has lived in the apartment for 10 years. He is seen as the father figure to Nishaad and Mohan.
ActionsXIdea: landlord announces no smoking policy
ActionsXGrounding:
The landlord agent will announce the no smoking policy
The tenant agents will interact with one another and sometimes talk to the landlord agent.
WorldXIdea: 1 landlord’s room, 1 tenant’s room
WorldXGrounding:
Landlord’s Room: where the landlord goes to wait after speaking to the tenants once in a while. Only the landlord is allowed in this room.
Waiting Room: where the agents interact with one another and “live” together. The landlord agent will periodically come in here to chat with the tenants. All agents start off in this room so the landlord can tell everyone about the no smoking policy. All agents should end in this room when the Landlord tells them about if the lease can be renewed or not based on the tenant’s behavior for the no-smoking policy.
StopConditionXIdea: landlord decides who will get the home and home-buyer agrees
StopConditionXGrounding:
The landlord agent tells the home-buyer agent that they get the house and the final cost, and the home-buyer agent agrees to pay the amount. Otherwise, they can reject it. The landlord agent can then ask their next pick until there is a mutual agreement.
"""

AGENTSXIDEA_EXAMPLES = """Agents Ideas focus on the amount and type of agents we need.
Consider different TYPES of agents.
For example if simulating a house-bidding situation where people cannot hear or see what fellow competitors are bidding, a good idea could be "1 real estate agent, and 2 home bidders", because we need someone to facillitate the bidding.
However, a simple simulation of people returning shopping carts could just have "3 shopper agents".
One response should return 3 agents maximum. Another shoudl return 5 agents maximum. Another should return 7 agents maximum.
"""
AGENTSXGROUNDING_EXAMPLES = """Agents Grounding focuses on the personality of each agent and a brief description of the agent.
For example, if the idea is to "simulate the tragedy of the commons" for "3 agents with varying degrees of social influence/peer pressure influencing their choices", some example goals of the application could be:
"- Alice: an agent that is highly influenced by others \n - Bob: an agent that is neutral \n - Charlie: an agent who is a non-conformist".
If the idea is to "simulate the tragedy of the commons" for "3 agents simulating a hoarder/sharer dynamic", some examples can include:
"- Alice: an agent who is a hoarder \n - Bob: an agent who is a sharer \n - Charlie: is opportunistic, adjusting behavior based on the others."
Only return and a brief one-sentence description of it, including what task the agent will do when interacting in the world.
Each agent should play a specific role in the simulation. If one of the agents can take on the role of another agent then it should do so and eliminate the redundant agent.
Avoid redundancy and any unnecessary agents.
"""

ACTIONSXIDEA_EXAMPLES = """Action ideas focus on what each type of agent need to do in the world and when they can exit the simulation (the stop condition).
Make sure there are actions that span all the types of agents, as well as stop conditions for each agent.
Every action should consist of the agent communicating that they have completed a task. Agents can complete a task by simply saying they have completed a task.
For example, if the idea is to "simulate the tragedy of the commons", some examples of the actions are "agents should verbally stating the money they have consumed", "the simulation stops when the pot is empty"
For example, if there are two types of agents, an example idea could be "mediator agents should announce whose turn it is" and "mediator agent announces the bet each round" and "agents should verbally state to mediator the money they have consumed" and "simulation stops when there is no more money" and "simulation stops when 3 rounds are over."
If agents are voting in a simulation, they can just verbally declare it without having to cast a ballot or upload their vote. If an agent is counting the votes, they should NOT have to read any files. They should either just observer or count via verbal vote.
Try to keep the array oragnized by agent. For example, the first 3 actions in the list are for the real estate agent, the next couple actions are for the home buyer agent, last couple actions shows the stop condition(s)). Here is an example:
[
    "Professor announces the submission due date",
    "Professor gives extensions to students when requested",
    "Professor schedules a meeting with students submitting work late frequently",
     "Professor agent provides feedback to student agents",
    "Student agents declare they submitted the assignment",
    "Student agents declare they submitted the assignment late",
    "Simulation ends when professor finishes meetings with all students",
    "Simulation ends when all assignments have been submitted",
    "Simulation ends when all meetings have ended",
    "Simulation ends after feedback from professor is provided to all students"
]
"""

ACTIONSXGROUDING_EXAMPLES = """Action Grounding should focus on how the LOGISTICS of the actions will play out in the simulation. It should really work on specifying what the actions will do.
There should be a description for EACH ACTION checked off.
For example, here are some things you should consider if running a classroom simulation:
- If the professors must announce the assignment, when should it be announced?
- What type of assignment should it be? (hint, the assignment should be announced at the beginning of class, it should be a research proposal that does not require a PDF).
- How many assignments should there be? (3 assignments)
- When are the due dates? (should not be specific dates, should just be sequentially announced one after another, due approximately minutes after one another because it is a simulation)
- If the students verbally declare they submitted the assignmnet, what do they say?
Make sure the explanations for how to complete the action are NOT AT ALL RELATED TO THE AGENT'S PERSONALITY. IT SHOULD REMAIN EXTREMELY OBJECTIVE.
Remember that agents are JUST agents. They cannot do actions like submitting PDFS, uploading files, accessing portals, etc. Everything should be verbal or pretend or proxies of normal human behavior.
So agents don't have to actually complete an assignment, they can just verbally say they did it. The professor doesn't have to ask for a PDF or research project, they just verbally state an assignment is due and the student pretends to complete it.
Explicitly ensure that actions are simple and based in a simulation-like world.
"""

WORLDXIDEA_EXAMPLES = """The World ideas focuses on the world in which the agents exist in and how they perform their action.
Examples include "1 classroom", "1 dorm room", "1 classroom and 1 dorm room", "community meeting room", "bunker".
The world should factor in how exactly the agents will perform their action -- for example, if they need to move to another room, when voting, then we need two rooms: one to wait and one to vote in.
Do not create unnecessary rooms. For example, if students are verbally declaring their tasks, there is no need to create another room.
Only brainstorm room ideas that exist in the physical world -- for example, do not brainstorm "submission portal"
"""

WORLDXGROUNDING_EXAMPLES = """The World Grounding should focus on how exactly the world idea should be implemented, while factoring in the context of how the agent needs to perform the action.
DO NOT ADD ANY NEW ROOMS NOT SPECIFIED BY WORLDXIDEA. IT SHOULD BE EXACTLY THE SAME AS WORLDXIDEA.
Consider who can enter each room -- for example, can only a certain type of agent be in the office room, but all agents can be in the common room? Explicitly state out who can be in each room. If only certain agents can speak to one another, be specific about that too.
Also, consider exactly where each agent should start out. If there is an initial announcement that needs to be made, all agents should start off in the same room.
For the idea "simulate the tragedy of the commons", the world idea could be "A single room", and the grounding can be:
"A single room that acts like a “bunker”. The room has a single water dispenser with a visible gauge that shows the water level. Parties can take turns using the water dispenser one by one. The dispenser refills slowly because of limited water resources from an underground reservoir. So if family overuse, the refill rate will decrease and risk complete depletion."
Only return the location and A ONE SENTENCE DESCRIPTION MAXIMUM OF 100 CHARACTERS.
Only describe how agents will interact in this room and what they will do.
DO NOT DESCRIBE ANYTHING ELSE.
"""

STOPCONDITIONXIDEA_EXAMPLES = """The Stop condition ideas focus on in what state the simulation can stop.
Examples include "an agreement has been made between agent A and agent B", "there are no more funds", "3 rounds are completed".
Keep it simple. Do not brainstorm anythign that is overly complex.
"""

STOPCONDITIONXGROUNDING_EXAMPLES = """The Stop Condition Grounding should focus on the specifics of the stop condition.
What room should the stop condition be in? What should have the agents been able to do before the simulation is over?
It should clarify the exact state in which the simulatoin will stop.
"""

MATRIX_EXAMPLES = {
    "AgentsXIdea": AGENTSXIDEA_EXAMPLES,
    "AgentsXGrounding": AGENTSXGROUNDING_EXAMPLES,
    "ActionsXIdea": ACTIONSXIDEA_EXAMPLES,
    "ActionsXGrounding": ACTIONSXGROUDING_EXAMPLES,
    "WorldXIdea": WORLDXIDEA_EXAMPLES,
    "WorldXGrounding": WORLDXGROUNDING_EXAMPLES,
    "StopConditionXIdea": STOPCONDITIONXIDEA_EXAMPLES,
    "StopConditionXGrounding": STOPCONDITIONXGROUNDING_EXAMPLES,
}

MATRIX_DESCRIPTION = f"{PAAW_DESCRIPTION} + {" ".join(MATRIX_DESCRIPTIONS.values())}"

def get_context_from_other_inputs(problem, category, matrix):
    print(matrix)
    compiled_text = f"{problem}\n"
    if category is not None and "Idea" in category:
        skipped = category.replace("Idea", "Grounding")
    else:
        skipped = ""

    for key, value in matrix.items():
        if key == category:
            continue
        if not value:
            continue
        if category is not None and "Idea" in category and key == skipped:
            continue
        else:
            compiled_text += f"For the {key} section, the input is: {value}\n"
    return compiled_text

def brainstorm_inputs(category, context, existing_brainstorms, iteration):
    print("calling LLM for brainstorm_inputs...")
    is_grounding = "Grounding" in category
    is_action = "Actions" in category
    print(f"category {category} is_grounding {is_grounding}")
    iteration_message = f"The user would also like you to factor this into the brainstormed answer: {iteration}" if iteration != "" else ""
    user_message = f"""This is the category you are brainstorming for: {category}. {iteration_message}.
    Make sure not to repeat brainstorms from this list: {existing_brainstorms}
    """
    if is_action and not is_grounding:
        response_format = """
            The answers SHOULD BE 10-15 words WORDS that specify what exactly the idea is. ALL THE ANSWERS MUST BE VERY DIFFERENT FROM ONE ANOTHER.
            Format the the responses in an array like so: ["home-buyer agents declare their bid", "home-owner agents can only speak to the real-estate agent", "simulation ends when real-estate agent picks a buyer"]
            The array should have size 10 maximum. The actions must all be different from one another."""
    elif is_grounding:
        response_format = """
            The answers should be as specific as possible, but do not be overly verbose in your response. USE AS LITTLE WORDS AS POSSIBLE. Do not repeat what is said in the corresponding idea section.
            The answer should be 50-100 words.
        RETURN THE ANSWER AS A STRING WITH BULLETED LIST. LIMIT TO 3 OR 4 BULLET POINTS IN THE LIST:
        example:
            - The daily message should include a concise profile summary for each of the five matches, highlighting essential details such as name, age, occupation, and a short personal note or shared interest.
            - Include compatibility scores or commonalities (e.g., mutual friends, hobbies) to help users quickly assess each match’s potential.
            - Provide clear action buttons within the message to either like, pass, or start a conversation, making it easy for users to engage with their daily options.
            DO NOT RETURN A PARAGRAPH.
        """
    else:
        response_format = """
            The answers SHOULD BE 10-15 words WORDS that specify what exactly the idea is. ALL THE ANSWERS MUST BE VERY DIFFERENT FROM ONE ANOTHER.
            Format the the responses in an array like so: ["1 professor and 2 students", "3 shoppers"]
            The array should have size 3 maximum.
        """

    system_message = f"""
    You are a helpful assistant that helps brainstorm specification answers for a category to narrow down inputs.
    {MATRIX_DESCRIPTION}
    {PAAW_EXAMPLES}
    Here is the context for this problem: {context}
    {MATRIX_EXAMPLES[category]}
    {response_format}
    """
    res = call_llm(system_message, user_message, llm="openai")
    brainstorms = res if is_grounding else cleanup_array("here are the users: " + res)
    print("sucessfully called LLM for brainstorm_inputs", res)
    return brainstorms

def cleanup_array(brainstorms):
    print("calling LLM for cleanup_array...")
    user_message = f"Please clean up the response so it only returns the array. This is the response: {brainstorms}"
    system_message = """You are an assistant to clean up GPT responses into an array.
			The response should be as formatted: [
                "a", "b", "c"
            ]
            Only the array should be returned. NOTHING OUTSIDE OF THE ARRAY SHOULD BE RETURNED.
            """
    res = call_llm(system_message, user_message, llm="openai")
    print("sucessfully called LLM for cleanup_brainstorms", res)
    cleaned = res
    try:
        cleaned_json = json.loads(cleaned)
        return cleaned_json
    except json.JSONDecodeError:
        print("Error decoding JSON, retrying...")
        return cleanup_array(brainstorms)