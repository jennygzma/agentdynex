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
    What will the agent do in each room? What is the purpose of each room?
    """,
}

# PAAW_EXAMPLES = """
# Here are some examples:

# OKCupid -
# PersonXIdea: Single person
# PersonXGrounding: - Difficulty in finding potential partners who meet specific criteria like race, religion, age, or occupation. \n - Challenges in efficiently filtering through dating apps to locate compatible matches. \n - Need for an application that streamlines the process by allowing users to set precise criteria and receive curated suggestions.
# ApproachXIdea: Searchable Database to allow people to search for people based on specified criteria
# ApproachXGrounding: - Ensure the database includes comprehensive filters such as age, gender, sex, religion, and occupation to meet users' specific search criteria. \n - Develop a robust and scalable search algorithm that efficiently handles large datasets and returns accurate results based on the selected filters. \n - Implement user-friendly search and filtering interfaces that make it easy for users to apply multiple criteria and refine their search results.
# InteractionXIdea: Faceted Browsing
# InteractionXGrounding: - Provide users with multiple facet filters, including age, gender, religion, occupation, and location, to refine their search effectively. \n - Ensure the UI dynamically updates search results in real-time as users adjust their facet filters, offering immediate feedback. \n - Design intuitive navigation with clear options to reset filters, switch criteria, and save searches, using checkboxes, sliders, and dropdowns for ease of use.

# Tinder:
# PersonXIdea: Single person
# PersonXGrounding: - Users often struggle to find matches that meet their physical preferences quickly and efficiently. \n - The abundance of profiles makes it challenging to identify those that align with specific looks or appearances. \n - A streamlined approach to swiping and filtering by appearance would help users connect with potential matches faster, focusing on visual attraction.
# ApproachXIdea: Lower the cognitive load by providing less information, making it easier to judge potential matches quickly
# ApproachXGrounding: - Limit the displayed information to essential details, such as a single profile photo and a brief tagline, to encourage snap judgments. \n - Focus on visual appeal as the primary matching criterion, reducing the need for users to sift through extensive profiles. \n - Use an algorithm to prioritize matches based on visual preferences and minimal data inputs, streamlining the matching process.
# InteractionXIdea: Card Swipe
# InteractionXGrounding: - Each card should prominently feature a large profile photo, as visual appeal is the primary factor in this interaction. \n - Include minimal text, such as the person’s name, age, and a short tagline or fun fact, to provide just enough context without overwhelming the user. \n - Add simple icons or buttons for actions like "Like" or "Pass," ensuring that users can quickly swipe or tap to make their choice.

# Coffee Meets Bagel:
# PersonXIdea: Single person
# PersonXGrounding: - Users who are looking for serious relationships prefer fewer, high-quality matches over endless swiping. \n - The overwhelming number of potential matches on other apps can make it difficult to focus on finding a meaningful connection.\n - An app designed for serious dating should streamline the process by offering a curated selection of potential partners, reducing time spent on the app.
# ApproachXIdea: Lower the cognitive load by having less matches to make more intentional judgements
# ApproachXGrounding: - Present a select number of potential matches each day to prevent decision fatigue and promote thoughtful consideration.\n - Display key information like shared interests, compatibility indicators, and mutual friends to aid decision-making without overwhelming the user. \n - Prioritize quality over quantity, ensuring that each match is relevant to the user’s preferences and relationship goals.
# InteractionXIdea: Feed with 5 options to date
# InteractionXGrounding: - The daily message should include a concise profile summary for each of the five matches, highlighting essential details such as name, age, occupation, and a short personal note or shared interest. \n - Include compatibility scores or commonalities (e.g., mutual friends, hobbies) to help users quickly assess each match’s potential. \n - Provide clear action buttons within the message to either like, pass, or start a conversation, making it easy for users to engage with their daily options.
# """

AGENTSXIDEA_EXAMPLES = """Agents Ideas focus on the amount and type of agents we need.
For example, if the idea is "simulating the tragedy of the commons ", some examples of agents are:
"5 agents with varying degrees of social influence/peer pressure influencing their choices" or
"3 agents with different family sizes who need different amounts of the resource that is being shared to survive"
ONLY GIVE 3 AGENTS MAXIMUM.
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
Every action should consist of the agent communicating that they have completed a task. Agents can complete a task by simply saying they have completed a task.
For example, if the idea is to "simulate the tragedy of the commons", some examples of the actions are "verbally stating the money they have consumed, stopping when they all agree or the pot is empty"
Remember that agents are JUST agents. They cannot do actions like submitting PDFS, uploading files, accessing portals, etc. Everything should be verbal or pretend or proxies of normal human behavior.
So agents don't have to actually complete an assignment, they can jsut verbally say they did it. The professor doesn't have to ask for a PDF or research project, they just verbally state an assignment is due and the student pretends to complete it.
If agents are voting in a simulation, they can just verbally declare it without having to cast a ballot or upload their vote. If an agent is counting the votes, they should NOT have to read any files. They should either just observer or count via verbal vote.
"""

ACTIONSXGROUDING_EXAMPLES = """Action Grounding should focus on how exactly the action will be performed by the agents, whether that be declaring verbally when something has happened or physically moving to another room.
Ensure that you focus on the simplist way that the agent will perform the action.
Make sure the explanations for how to complete the action are NOT AT ALL RELATED TO THE AGENT'S PERSONALITY. IT SHOULD REMAIN EXTREMELY OBJECTIVE.
For the idea "simulate the tragedy of the commons", some examples of the actions "declaring the money they have consumed, stopping when they all agree or the pot is empty" can be:
"Agents verbally communicate that they have consumed a resource upon doing so, which will also be supported in the world be the visible depletion of the resource after said consumption. The simulation should either end once all agents verbally declare and agree upon sustainable consumption rates that satisfy the stability of the resource and each parties’ needs, or it should end once all parties declare that the resource has officially depleted."
"""

WORLDXIDEA_EXAMPLES = """The World ideas focuses on the world in which the agents exist in and how they perform their action.
Examples include "1 classroom", "1 dorm room", "1 classroom and 1 dorm room", "community meeting room", "bunker".
The world should factor in how exactly the agents will perform their action -- for example, if they need to move to another room, when voting, then we need two rooms: one to wait and one to vote in.
Only brainstorm room ideas that exist in the physical world -- for example, do not brainstorm "submission portal"
"""

WORLDXGROUNDING_EXAMPLES = """The World Grounding should focus on how exactly the world idea should be implemented, while factoring in the context of how the agent needs to perform the action.
For the idea "simulate the tragedy of the commons", the world idea could be "A single room", and the grounding can be:
"A single room that acts like a “bunker”. The room has a single water dispenser with a visible gauge that shows the water level. Parties can take turns using the water dispenser one by one. The dispenser refills slowly because of limited water resources from an underground reservoir. So if family overuse, the refill rate will decrease and risk complete depletion."
Only return the location and A ONE SENTENCE DESCRIPTION MAXIMUM OF 100 CHARACTERS.
Only describe how agents will interact in this room and what they will do.
Do not describe anything else about the room.
"""

MATRIX_EXAMPLES = {
    "AgentsXIdea": AGENTSXIDEA_EXAMPLES,
    "AgentsXGrounding": AGENTSXGROUNDING_EXAMPLES,
    "ActionsXIdea": ACTIONSXIDEA_EXAMPLES,
    "ActionsXGrounding": ACTIONSXGROUDING_EXAMPLES,
    "WorldXIdea": WORLDXIDEA_EXAMPLES,
    "WorldXGrounding": WORLDXGROUNDING_EXAMPLES,
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
    print(f"category {category} is_grounding {is_grounding}")
    iteration_message = f"The user would also like you to factor this into the brainstormed answer: {iteration}" if iteration != "" else ""
    user_message = f"""This is the category you are brainstorming for: {category}. {iteration_message}.
    Make sure not to repeat brainstorms from this list: {existing_brainstorms}
    """
    grounding_format = """
        The answers should be as specific as possible, but do not be overly verbose in your response. USE AS LITTLE WORDS AS POSSIBLE. Do not repeat what is said in the corresponding idea section.
        The answer should be 50-100 words.
       RETURN THE ANSWER AS A STRING WITH BULLETED LIST. LIMIT TO 3 OR 4 BULLET POINTS IN THE LIST:
       example:
        - The daily message should include a concise profile summary for each of the five matches, highlighting essential details such as name, age, occupation, and a short personal note or shared interest.
        - Include compatibility scores or commonalities (e.g., mutual friends, hobbies) to help users quickly assess each match’s potential.
        - Provide clear action buttons within the message to either like, pass, or start a conversation, making it easy for users to engage with their daily options.
        DO NOT RETURN A PARAGRAPH.
    """ if is_grounding else """
        The answers SHOULD BE 10-15 words WORDS that specify what exactly the idea is. ALL THE ANSWERS MUST BE DIFFERENT FROM ONE ANOTHER.
        Format the the responses in an array like so: ["1 professor and 2 students", "3 shoppers"]
        The array should have size 3 maximum.
    """
    #     {PAAW_EXAMPLES} ADD LATER
    system_message = f"""
    You are a helpful assistant that helps brainstorm specification answers for a category to narrow down inputs.
    {MATRIX_DESCRIPTION}
    Here is the context for this problem: {context}
    {MATRIX_EXAMPLES[category]}
    {grounding_format}
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