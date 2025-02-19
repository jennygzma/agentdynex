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
    Only return and a brief one-sentence description of it, including what task the agent will do when interacting in the world.
    Each agent should play a specific role in the simulation. If one of the agents can take on the role of another agent then it should do so and eliminate the redundant agent.
    Avoid redundancy and any unnecessary agents.""",

    "ActionsXIdea": """Within the actions section and the idea subsection we think about how the agents should act in the simulation.
    What are the one or two actions agents need to do in order to complete the simulation? Are they contributing money? Are they submitting an assignment?""",

    "ActionsXGrounding": """Within the actions section and the grounding subsection, we focus on the tangible details of making the action feasible within the simulation.
    We keep it as simple as possible. Should the agent verbally declare that they submitted an assignment? Should the agent submit an assignment in a particular room?""",

    "WorldXIdea": """Within the world section and the idea subsection we contemplate the general design of the simulation.
    How should the simulated world look? How many rooms should there be in this world?""",

    "WorldXGrounding": """Within the world section and the grounding subsection, we delve into the specifics of each room:
    What will the agent do in each room? What is the purpose of each room?
    Only return the location and A ONE SENTENCE DESCRIPTION MAXIMUM OF 100 CHARACTERS.
    Only describe how agents will interact in this room and what they will do.
    Do not describe anything else about the room.
    """,
}

PAAW_EXAMPLES = """
Here are some examples:

OKCupid -
PersonXIdea: Single person
PersonXGrounding: - Difficulty in finding potential partners who meet specific criteria like race, religion, age, or occupation. \n - Challenges in efficiently filtering through dating apps to locate compatible matches. \n - Need for an application that streamlines the process by allowing users to set precise criteria and receive curated suggestions.
ApproachXIdea: Searchable Database to allow people to search for people based on specified criteria
ApproachXGrounding: - Ensure the database includes comprehensive filters such as age, gender, sex, religion, and occupation to meet users' specific search criteria. \n - Develop a robust and scalable search algorithm that efficiently handles large datasets and returns accurate results based on the selected filters. \n - Implement user-friendly search and filtering interfaces that make it easy for users to apply multiple criteria and refine their search results.
InteractionXIdea: Faceted Browsing
InteractionXGrounding: - Provide users with multiple facet filters, including age, gender, religion, occupation, and location, to refine their search effectively. \n - Ensure the UI dynamically updates search results in real-time as users adjust their facet filters, offering immediate feedback. \n - Design intuitive navigation with clear options to reset filters, switch criteria, and save searches, using checkboxes, sliders, and dropdowns for ease of use.

Tinder:
PersonXIdea: Single person
PersonXGrounding: - Users often struggle to find matches that meet their physical preferences quickly and efficiently. \n - The abundance of profiles makes it challenging to identify those that align with specific looks or appearances. \n - A streamlined approach to swiping and filtering by appearance would help users connect with potential matches faster, focusing on visual attraction.
ApproachXIdea: Lower the cognitive load by providing less information, making it easier to judge potential matches quickly
ApproachXGrounding: - Limit the displayed information to essential details, such as a single profile photo and a brief tagline, to encourage snap judgments. \n - Focus on visual appeal as the primary matching criterion, reducing the need for users to sift through extensive profiles. \n - Use an algorithm to prioritize matches based on visual preferences and minimal data inputs, streamlining the matching process.
InteractionXIdea: Card Swipe
InteractionXGrounding: - Each card should prominently feature a large profile photo, as visual appeal is the primary factor in this interaction. \n - Include minimal text, such as the person’s name, age, and a short tagline or fun fact, to provide just enough context without overwhelming the user. \n - Add simple icons or buttons for actions like "Like" or "Pass," ensuring that users can quickly swipe or tap to make their choice.

Coffee Meets Bagel:
PersonXIdea: Single person
PersonXGrounding: - Users who are looking for serious relationships prefer fewer, high-quality matches over endless swiping. \n - The overwhelming number of potential matches on other apps can make it difficult to focus on finding a meaningful connection.\n - An app designed for serious dating should streamline the process by offering a curated selection of potential partners, reducing time spent on the app.
ApproachXIdea: Lower the cognitive load by having less matches to make more intentional judgements
ApproachXGrounding: - Present a select number of potential matches each day to prevent decision fatigue and promote thoughtful consideration.\n - Display key information like shared interests, compatibility indicators, and mutual friends to aid decision-making without overwhelming the user. \n - Prioritize quality over quantity, ensuring that each match is relevant to the user’s preferences and relationship goals.
InteractionXIdea: Feed with 5 options to date
InteractionXGrounding: - The daily message should include a concise profile summary for each of the five matches, highlighting essential details such as name, age, occupation, and a short personal note or shared interest. \n - Include compatibility scores or commonalities (e.g., mutual friends, hobbies) to help users quickly assess each match’s potential. \n - Provide clear action buttons within the message to either like, pass, or start a conversation, making it easy for users to engage with their daily options.
"""

AGENTSXIDEA_EXAMPLES = """Person ideas focus on who the target user of the application is.
For example, if the idea is "learn chinese", some examples of users are "30 year old english-speaking student" or or "busy professional who only has 30 minutes a day to learn chinese"
If the idea is "journaling app", some examples of users are "someone struggling with depression" or "someone going through a breakup". If the idea is "finding a nail salon", some examples are "celebrity assistant looking for personalized nail salon" or "female teenager looking for affordable nail salons". For OkCupid, the PersonXIdea is "Single person looking for a partner." For Tinder, the PersonXIdea is "Single person looking for hookups." For CoffeeMeetsBagel, the PersonXIdea is "Single person looking for a serious life partner".
"""
AGENTSXGROUNDING_EXAMPLES = """Person Grounding focuses on the goal of the application and what problem it's trying to solve for the person.
For example, if the idea is to "learn chinese" for "a 30 year old english-speaking student", some example goals of the application could be "gain vocabulary to travel to China for a week and learn Chinese in 3 weeks", versus "learn grammar".
If the idea is "finding a nail salon" for "a female teenager", the goal of the application could be to "explore a all the nail salons in NYC to formulate where to go when I visit", or "go to a nail salon ASAP for prom".
For OkCupid, where the PersonXIdea is "Single person looking for a partner.":  - Difficulty in finding potential partners who meet specific criteria like race, religion, age, or occupation. \n - Challenges in efficiently filtering through dating apps to locate compatible matches. \n - Need for an application that streamlines the process by allowing users to set precise criteria and receive curated suggestions.
For Tinder, where the PersonXIdea is "Single person looking for hookups.": - Users often struggle to find matches that meet their physical preferences quickly and efficiently. \n - The abundance of profiles makes it challenging to identify those that align with specific looks or appearances. \n - A streamlined approach to swiping and filtering by appearance would help users connect with potential matches faster, focusing on visual attraction.
For CoffeeMeetsBagel, where the PersonXIdea is "Single person looking for a serious life partner": - Users who are looking for serious relationships prefer fewer, high-quality matches over endless swiping. \n - The overwhelming number of potential matches on other apps can make it difficult to focus on finding a meaningful connection.\n - An app designed for serious dating should streamline the process by offering a curated selection of potential partners, reducing time spent on the app.
"""

ACTIONSXIDEA_EXAMPLES = """Approach ideas focus more on what ideas should be implemented as the core logic (backend) of the application based on person context on what the problem is.
It could be a theory within a domain the app will be built in like spaced repetition for learning apps, subjective expected utility for recommendation or search apps, CBT or ACT for mental health apps, gamification, or CLT for decisionmaking.
It could be an app solution, such as a rules-based system to generate outfit recommendations based off rules, Uber for X to match users with homes (airBnb is uber for homes), marketplace system to shop for used cars, workflow system to develop a joke iteratively, database (logging or reading) system to search for grocery stores, social network
When answering, provide the general approach and a short sentence as to how this would help solve the problem.
For OkCupid: Searchable Database to allow people to search for people based on specified criteria
For Tinder: Lower the cognitive load by providing less information, making it easier to judge potential matches quickly
For CoffeeMeetsBagel: Lower the cognitive load by having less matches to make more intentional judgements
"""

ACTIONSXGROUDING_EXAMPLES = """Approach Grounding should focus on how exactly the approach idea should be implemented, while factoring in other context such as the Person and problem context.
Ensure that you understand what the approach idea is exactly before thinking about how you would ground it.
This section should NOT focus on what the use interaction or interface should be. It is only figuing out how to implement the ApproachXIdea, given the other context for the problem.
DO NOT TAKE A RANDOM IDEA AND GROUND IT. IF THE APPROACHXIDEA IS GENERATION AND ELABORATION, FIGURE OUT HOW TO GROUND IT. DO NOT SUDDENLY COME UP WITH SPACED REPETITION.
For OkCupid, where the ApproachXIdea is "Searchable database to allow people to search for people based on specific critera", the ApproachXGrounding is: - Ensure the database includes comprehensive filters such as age, gender, sex, religion, and occupation to meet users' specific search criteria. \n - Develop a robust and scalable search algorithm that efficiently handles large datasets and returns accurate results based on the selected filters. \n - Implement user-friendly search and filtering interfaces that make it easy for users to apply multiple criteria and refine their search results.
For Tinder, where the ApproachXIdea is "Lower the cognitive load by providing less information, making it easier to judge potential matches quickly", the ApproachXGrounding is: - Limit the displayed information to essential details, such as a single profile photo and a brief tagline, to encourage snap judgments. \n - Focus on visual appeal as the primary matching criterion, reducing the need for users to sift through extensive profiles. \n - Use an algorithm to prioritize matches based on visual preferences and minimal data inputs, streamlining the matching process.
For CoffeeMeetsBagel, where the ApproachXIdea is "Lower the cognitive load by providing less information, making it easier to judge potential matches quickly", the ApproachXGrounding is: - Present a select number of potential matches each day to prevent decision fatigue and promote thoughtful consideration.\n - Display key information like shared interests, compatibility indicators, and mutual friends to aid decision-making without overwhelming the user. \n - Prioritize quality over quantity, ensuring that each match is relevant to the user’s preferences and relationship goals.
"""

WORLDXIDEA_EXAMPLES = """The Interaction ideas focuses on the UI Paradigm in the front end, such as the layout and interactoin paradigms.
Examples include chatbot (messaging), cardswipe (tinder), feed (facebook, tiktok, twitter, news), faceted browsing, table (gmail).
Approaches generally have a simple basic for UI which people gravitate towards. For example, a searchable database can easily have a table-like UI, but pairing approaches with non-obvious UIs is interesting, such as Card-Swipe UI.
The InteractionXIdea should also brainstorm some nonobvious InteractionXIdeas.
The application is a UI app. Do not recommend a mobile app. The app cannot suggest any carousels, since it is a UI. For example, if the prompt suggests a swiping interface, in the UI the "swipe" would be done by clicking, since it is not a mobile interface.
For OkCupid: Faceted Browsing
For Tinder: Card Swipe
For CoffeeMeetsBagel: Feed with 5 options to date
"""

WORLDXGROUNDING_EXAMPLES = """Interaction Grounding should focus on how exactly the interaction idea of the UI Paradigm should be implemented, while factoring in other context.
Keep in mind that we do not have the capacity to build a super fancy application. KEEP THE APPLICATION IN SCOPE TO THE USER PROBLEM AND THEORY AS MUCH AS POSSIBLE BECAUSE THERE IS LIMITED CODE WE CAN WRITE. For example, if this is the prompt: "Create a web UI based on this idea: learn chinese, for users: Retired person seeking a mentally stimulating hobby and a way to connect with their cultural heritage, where the application goal is: To gain conversational fluency to communicate with family members and explore ancestral roots. Use the theory of Spaced Repetition (Reviewing information at optimal intervals reinforces memory and aids long-term retention of the language.), which with interaction pattern Interactive storytelling (A narrative-driven approach with dialogues and scenarios, reinforcing vocabulary and phrases through an engaging story with spaced repetition of key elements.) to guide the design.", we should focus on implementing the spaced repetition part - unnecessary features like a social community feature, or working with multiple different stories is overly complex, as is is multiple decks, a setting bar, a profile page.
Only brainstorm interactions that are based in web UI. We cannot support mobile interfaces - so carousel, or push notifications, maps view, cannot be supported.
For OkCupid, where the InteractionXIdea is "Faceted Browsing", the InteractionXGrounding is: - Provide users with multiple facet filters, including age, gender, religion, occupation, and location, to refine their search effectively. \n - Ensure the UI dynamically updates search results in real-time as users adjust their facet filters, offering immediate feedback. \n - Design intuitive navigation with clear options to reset filters, switch criteria, and save searches, using checkboxes, sliders, and dropdowns for ease of use.
For Tinder, where the InteractionXIdea is "Card Swipe", the InteractionXGrounding is: - Limit the displayed information to essential details, such as a single profile photo and a brief tagline, to encourage snap judgments. \n - Focus on visual appeal as the primary matching criterion, reducing the need for users to sift through extensive profiles. \n - Use an algorithm to prioritize matches based on visual preferences and minimal data inputs, streamlining the matching process.
For CoffeeMeetsBagel, where the InteractionXIdea is "Feed with 5 options to date", the InteractionXGrounding is: - The daily message should include a concise profile summary for each of the five matches, highlighting essential details such as name, age, occupation, and a short personal note or shared interest. \n - Include compatibility scores or commonalities (e.g., mutual friends, hobbies) to help users quickly assess each match’s potential. \n - Provide clear action buttons within the message to either like, pass, or start a conversation, making it easy for users to engage with their daily options.
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
    system_message = f"""
    You are a helpful assistant that helps brainstorm specification answers for a category to narrow down inputs.
    {MATRIX_DESCRIPTION}
    {PAAW_EXAMPLES}
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