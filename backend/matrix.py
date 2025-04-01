import json

from globals import call_llm

PAAW_DESCRIPTION = """When we create a simulation based on a particular problem, we define it with a 6x2 problem matrix.
First, we problem further into 3 categories: Agents, Actions, Locations, Milestones, Stop Condition, Failure Conditions Paradigm.
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

    "LocationsXIdea": """Within the locations section and the idea subsection we contemplate the general design of the simulation.
    How should the simulated locations look? How many rooms should there be in this location?""",

    "LocationsXGrounding": """Within the locations section and the grounding subsection, we delve into the specifics of each room:
    What will the agent do in each room? What is the purpose of each room?""",

    "MilestonesXIdea": """Within the milestones section and the idea subsection we contemplate the chronological milestones of the simulation to ensure that it is progressing
    What are the 3-5 milestones?""",

    "MilestonesXGrounding": """Within the milestones section and the grounding subsection, we delve into the specifics of each milestone.
    Specifically, what must have happened for the agents to have reached each milestone?""",

    "StopConditionXIdea": """Within the stop condition section and the idea subsection we contemplate the stop condition of the simulation.
    When should the simulation stop?""",

    "StopConditionXGrounding": """Within the stop condition section and the grounding subsection, we delve into the specifics of the stop condition:
    Specifically, in what state should each agent and location be in for there to be a stop?""",

    "FailureConditionXIdea": """Within the failure condition section and the idea subsection we contemplate in what state we should consider the simulation as a failure.
    When should the simulation fail?""",

    "FailureConditionXGrounding": """Within the failure condition section and the grounding subsection, we delve into the specifics of the failure condition:
    Specifically, what are the details that show that the simulation has failed with no point of return?
    """,
}

PAAW_EXAMPLES = """
Here are some examples:

Idea: Landlord implementing no-smoking policy
AgentsXIdea: 1 strict landlord agent who hates smoking, 1 young smoking tenant,  2 non-smoking rule-follower tenants
AgentsXGrounding:
Sophia: landlord who does not want tenants to smoke. She will evict them if necessary.
Nishaad: a young newly college-graduate student who is addicted to his vape. He wants to continue living in the apartment because it is embarrassing if he is evicted.
Mohan: a young married man who has no smoking addiction and is a stickler for rules. He wants to continue living in the apartment and finds it embarrassing that he might be evicted.
Tejas: an older man who has lived in the apartment for 10 years. He is seen as the father figure to Nishaad and Mohan. He wants everyone to get along and finds it embarrassing that he might be evicted.
ActionsXIdea: landlord announces no smoking policy, tenants talk amongst each other only after the landlord leaves, tenants talk to the landlord privately in the landlord room.
ActionsXGrounding:
The landlord agent will announce the no smoking policy to all the tenants
The tenant agents will interact with one another and sometimes talk to the landlord agent.
The tenant agents will continue to “smoke” if they want to
LocationXGrounding: 1 landlord’s room, 1 tenant’s room
LocationXIdea:
Landlord’s Room: where the landlord goes to wait after speaking to the tenants once in a while. The tenant agents can come into the room if they so please to talk to the landlord.
Waiting Room: where the agents interact with one another and “live” together. The landlord agent will periodically come in here to chat with the tenants. All agents start off in this room so the landlord can tell everyone about the no smoking policy. All agents should end in this room when the Landlord tells them about if the lease can be renewed or not based on the tenant’s behavior for the no-smoking policy.
MilestonesXIdea:
Landlord announces no smoking policy to tenants
Tenants continue smoking or don’t continue smoking
Tenants accept or reject the new lease
MilestonesXGrounding:
Landlord announces no smoking policy to tenants - the first milestone is when the landlord announces the new policy to the tenants. This should jumpstart the tenants beginning to talk to each other about the new policy
Tenants continue smoking or don’t continue smoking - the second milestone is when the tenants choose what and what not to do after having discussed with each other and sufficiently had time to process their reactions
Landlord or Tenants accept or reject the new lease - the final milestone should be when the tenants accept or reject the new lease after they have had some interaction with each other and with the landlord and decided if they smoked or not
StopConditionXIdea: landlord or tenants cancel or extend the lease
StopConditionXGrounding:
Either the landlord agent tells all the tenants in the waiting room the new modified or unmodified lease they have to sign, and the tenant agents either reject or accept the new leases,
Or the tenant agents decide they don’t want to continue the lease.
The tenant agents should have had sufficient time discussing amongst themselves what they want to do (they are free to do anything), and also time to talk to the landlord.
FailureConditionXIdea: indefinite waiting periods where tenants and landlord wait for a responses from each other, tenants do not discuss with each other, tenants do not discuss with landlord, tenants do not decide if they want to accept or reject the new lease
FailureConditionXGrounding:
The simulation is a failure if it gets stuck in an indefinite waiting loop, if, for example, the agents are all waiting for response from eachother or not
The simulation is a failure if the tenants don’t discuss with eachother or the landlord, because then no dynamics are being captured as to the new smoking policy
The simulation is a failure if they have no reaction to accept or reject the lease

Idea: Simulating people buying a house for a homeowner who really cares about the home but also cares about monetary value
AgentsXIdea: 1 sentimental real estate agent, 1 genuine home-buyer agents, 2 rich home-buyer agents
AgentsXGrounding:
Debbie: 1 real estate agent to facilitate the selling of the home. Really wants to find a genuine, kind home owner, but he might get fired if the home is not sold for a high enough price.
Alice: first-time home buyer who is not as wealthy but will resort to emotional plea to seller to create an emotional connection. She desperately wants a home to live in.
Bob: aggressive buyer who will offer significantly above the asking price who needs to buy a house as soon as possible.
Charlie: strategic buyer who will offer a lot of cash who needs to buy a home as soon as possible.
ActionsXIdea: real estate agent conducting the bidding, home-buyer agents making bids
ActionsXGrounding:
The real estate agent will declare the price of the home
The real estate agent will verbally ask agents to bid
The agents will not talk to each other. They will only speak to the real-estate agent when they are making their offers.
LocationXIdea: 1 bidding room, 1 rooms for the agents to wait in
LocationXGrounding:
Bidding Room: where the home-buyer agents will travel here to speak to the real estate agent regarding their home bid. Home-buyer agents should come into this room whenever they want to make an offer or speak to the real-estate agent. Only one home-buyer agent is allowed in here at a time.
Waiting Room: where each agent will return to. They cannot speak to each other. This is where they will reflect and make their next move. All agents will start off in the waiting room and the bidding agent will declare the price of the home, then the bidding agent will move to the bidding room.
MilestonesXIdea:
The real estate agent declares the price of the home
All of the homebuyers have declared interest in buying the home
Some homebuyers have employed other methods to try to buy the home
The real estate agent declares the agent who is the new homeowner
MilestonesXGrounding:
The real estate agent declares the price of the home - The real estate agent needs to declare the price of the home
All of the homebuyers have declared interest in buying the home - the home buyers need to have declared interest in buying the home by showing the amount of money they want to pay
Some homebuyers have employed other methods to try to buy the home - after the initial declaration of interaction and talking to the real estate agents, the homebuyers may try to provide emotional pleas or more to buy a home
The real estate agent has decided who will buy the home.
StopConditionXIdea: landlord decides who will get the home and home-buyer agrees
StopConditionXGrounding:
The landlord agent tells the home-buyer agent that they get the house and the final cost, and the home-buyer agent agrees to pay the amount. Otherwise, they can reject it. The landlord agent can then ask their next pick until there is a mutual agreement.
FailureConditionXIdea: the people try to submit their home-decisions through a portal or pdf instead of verbally declaring it, they enter indefinite waiting loops waiting for eachother
FailureConditionXGrounding:
The simulation fails if there are EOF errors or if people are trying to submit their home-decisions through a portal
The simulation fails if there are indefinite waiting periods of no action from a logical error, such as when an agent doesn’t respond to anyone or everyone is waiting for an acknowledgement and no acknowledgement of actions is coming.
"""

AGENTSXIDEA_EXAMPLES = """Agents Ideas focus on the amount and type of agents we need.
Consider different TYPES of agents.
For example if simulating a house-bidding situation where people cannot hear or see what fellow competitors are bidding.
Each response in the response array can only contain 1 TYPE of agent:
["1 logical real estate agent", "1 wealthy home bidder", "4 middle-class but genuine home bidders", "3 wealthy home bidders"]. We need different types of agents so the user can decide what they want.
If there are no types of agents required, return different quantities as well like ["3 shopper agents parked far away", "1 shopper agent with a child", "5 shopper agents parked close"]
The user can then check off which types of agents they want in the simulation.
DO NOT RETURN STUFF LIKE "1 home bidder and 1 real estate agent"... KEEP ALL THE TYPES OF AGENTS SEPARATED.
"""

AGENTSXGROUNDING_EXAMPLES = """Agents Grounding focuses on the personality of each agent and a brief description of the agent.
Make sure to explicitly write a "stake", such as they will be embarrassed if X doesn't happen or they will be happy if Y happens, or they urgently need X, or they don't care either way.
Be very clear about the stakes of the situation for each of them.
For example, if the scenario is to simulate prom pairings, some example groundings are:
"- Alice is a socialite student who cares EXTREMELY about her personal image. You secretly have a crush on George and hope he will ask you to prom. You are jealous, conniving, and selfish. It will be EXTREMELY embarassing to not have a date to the PROM at all and you think everyone will think you're a loser. You will do WHATEVER it takes to get a date to the prom, especially if it is George, because you are DESPERATE to not go alone.
\n - Bob is a charismatic and outgoing student who is well-liked by his peers and isn't afraid to make the first move. You hope to ask Alice to prom but are nervous about her response. You HATE feeling like a back-up option and absolutely do not tolerate rejection well. It will be EXTREMELY embarrassing to not have a date to the PROM at all and you think everyone will think you're a loser."
\n - Charlie is known for his athletic abilities, he's not very socially proactive and prefers others to approach him first. It will be EXTREMELY embarrassing to not have a date to the PROM at all and you think everyone will think you're a loser.
\n - Danielle is an artistic and creative student who values unique and non-conventional ideas and connections. You secretly admire Eric's analytical mind and think you would complement each other well.It will be EXTREMELY embarrassing to not have a date to the PROM at all and you think everyone will think you're a loser.
\n - Eric is a serious and diligent student who often takes a strategic approach to social situations. You find Danielle's creative perspective intriguing and are considering asking her to prom. It will be EXTREMELY embarrassing to not have a date to the PROM at all and you think everyone will think you're a loser.
\n - Felicia is an outgoing cheerleader who is both popular and well-liked by a majority of the students. It will be EXTREMELY embarrassing to not have a date to the PROM at all and you think everyone will think you're a loser.
\n - George is a selfish, backstabby student who wants people to think he is extremely cool and way above them socially. You just want to milk your popularity and don’t care about other people’s feelings. It will be EXTREMELY embarrassing to not have a date to the PROM at all and you think everyone will think you're a loser."

For example, if the idea is to "simulate the tragedy of the commons" for "3 agents with varying degrees of social influence/peer pressure influencing their choices", some example goals of the application could be:
"- Alice: an agent that is highly influenced by others. She desperately craves social approval
\n - Bob: an agent that is neutral. Bob doesn't care about what happens.
\n - Charlie: an agent who is a non-conformist. Charlie really values being different and innovative"
If the idea is to "simulate the tragedy of the commons" for "3 agents simulating a hoarder/sharer dynamic", some examples can include:
"- Alice: an agent who is a hoarder. She hates giving away things.
 \n - Bob: an agent who is a sharer. He loves sharing things
 \n - Charlie: is opportunistic, adjusting behavior based on the others. Charlie craves the validation of others."
Only return and a brief one-sentence description of it, including what task the agent will do when interacting in the location.
Each agent should play a specific role in the simulation. If one of the agents can take on the role of another agent then it should do so and eliminate the redundant agent.
Avoid redundancy and any unnecessary agents.

We just want to raise the stakes of each agent so that it's clear what is valuable to them.
For example, in a competition, we could say that "he will feel very embarrassed if he loses," or "he will feel embarrassed if he is rejected" or "he will feel embarrassed if he has no partner" depending on their personality. They could also not care -- and in that case, the stakes are neutral. We just need to exaggerate the stakes based on their personality.
"""

ACTIONSXIDEA_EXAMPLES = """Action ideas focus on what each type of agent need to do in the location.
Make sure there are actions that span all the types of agents.
Every action should consist of the agent communicating that they have completed a task.
Agents can complete a task by simply saying they have completed a task.
For example, if the idea is to "simulate the tragedy of the commons", some examples of the actions are "agents should verbally stating the money they have consumed"
For example, if there are two types of agents, an example idea could be "mediator agents should announce whose turn it is" and "mediator agent announces the bet each round" and "agents should verbally state to mediator the money they have consumed"
If agents are voting in a simulation, they can just verbally declare it without having to cast a ballot or upload their vote. If an agent is counting the votes, they should NOT have to read any files. They should either just observer or count via verbal vote.
Try to keep the array oragnized by agent. For example, the first 3 actions in the list are for the real estate agent, the next couple actions are for the home buyer agent. Here is an example:
[
    "Professor announces the submission due date",
    "Professor gives extensions to students when requested",
    "Professor schedules a meeting with students submitting work late frequently",
    "Professor agent provides feedback to student agents",
    "Student agents declare they submitted the assignment",
    "Student agents declare they submitted the assignment late",
    "Students can can discuss homework with eachothen when they are working on the assignment"ß
]

IF THERE IS MENTION OF DISCUSSION, THERE MUST BE MENTION OF WHEN THE DISCUSSION OCCURS.
FOR EXAMPLE, "STUDNETS DICSUSS WITH ONE ANOtHER IN BETWEEN DEBATES." "STUDENTS LISTEN DURING DEBATES"
DO NOT RETURN STUFF LIKE "Studnets should discuss amongst eachother". It is obvious that all the agents will discuss with eachother.
Instead, create rules about WHEN the agents can discuss, for example: "Students can only discuss about the assignment to eachother when they are working".
Or, "Students can only speak after the debate is over."

DO NOT RETURN OBVIOUS THINGS THAT THE AGNETS WILL DO, SUCH AS
"Agents will declare interest" -- THAT IS OBVIOUS
"React to invitations" -- THAT IS OBVIOUS
What is not obvious is declaring the FINAL pairing, or the FINAL result -- so that can be an action.
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

LOCATIONSXIDEA_EXAMPLES = """The Locations ideas focuses on the location in which the agents exist in and how they perform their action.
Return a result for each room.
Examples include "1 classroom", "1 dorm room", "community meeting room", "bunker".
The location should factor in how exactly the agents will perform their action -- for example, if they need to move to another room, when voting, then we need two rooms: one to wait and one to vote in.
Do not create unnecessary rooms. For example, if students are verbally declaring their tasks, there is no need to create another room.
Only brainstorm room ideas that exist in the physical world -- for example, do not brainstorm "submission portal"
"""

LOCATIONSXGROUNDING_EXAMPLES = """The Locations Grounding should focus on how exactly the locations idea should be implemented, while factoring in the context of how the agent needs to perform the action.
DO NOT ADD ANY NEW ROOMS NOT SPECIFIED BY LOCATIONSXIDEA. IT SHOULD BE EXACTLY THE SAME AS LOCATIONSXIDEA.
Consider who can enter each room -- for example, can only a certain type of agent be in the office room, but all agents can be in the common room? Explicitly state out who can be in each room. If only certain agents can speak to one another, be specific about that too.
Also, consider exactly where each agent should start out. If there is an initial announcement that needs to be made, all agents should start off in the same room.
For the idea "simulate the tragedy of the commons", the location idea could be "A single room", and the grounding can be:
"A single room that acts like a “bunker”. The room has a single water dispenser with a visible gauge that shows the water level. Parties can take turns using the water dispenser one by one. The dispenser refills slowly because of limited water resources from an underground reservoir. So if family overuse, the refill rate will decrease and risk complete depletion."
Only return a description for each of the locations. Each description should contain A ONE SENTENCE DESCRIPTION MAXIMUM OF 100 CHARACTERS.
Only describe how agents will interact in this room and what they will do.
DO NOT DESCRIBE ANYTHING ELSE.
"""

MILESTONESXIDEA_EXAMPLES = """
The milestones ideas focus on the chronological order in which the simulation should proceed.
It also provides a way for the user to quantitatively measure things.

Some of the milestones are obvious -- for example, for a professor simulating how students will respond to a late policy, something we can quantitatively measure is how many students will turn assignments on time?
Thus, the milestones should reflect this, and we can guide the simulation towards assignments. The milstones will then be:
For example:
1. Late policy is announced
2. Assignment 1 has been completed
3. Assignment 2 has been completed
4. Assignment 3 has been completed

For example, if a coach is implementing a new practice schedule, something quantitative we can measure is how many agents will attend practice given the new policy. Some milestones that you can consider can be:
1. Coach declares new practice schedule
2. Practice 1 starts
3. Practice 1 is completed
4. Practice 2 starts
5. Practice 2 is completed.

If the simulation idea is to test to see how a friend group reacts to a breakup, the quantitative things you can measure can be:
1)  how many people know about the breakup after X amount of time?
In this case, the miletsones will be:
1. X and Y announce breakup to 1 person
2. 1/2 of the friends know
3. all of the friends know
2) how many people subgroups form after X amount of time?
1. X and Y announce breakup to the group
2. One school day passes
3. Another school day passes.

The response should include ALL of these options.

Essentially, we want you to just come up with logical "milestones" that the simulation should go through.
There should be 3-8 milestones per simulation.
Each milestone should be no more than 10 words.
"""

MILESTONESXGROUNDING_EXAMPLES = """The Milestones Grounding should focus on the specifics of the milestone
What should have occured for each milestone?
For example:
1. Assignment 1 has been completed - all student agents have submitted assignment 1
2. Assignment 2 has been completed - all student agents have submitted assignment 2
3. Assignment 3 has been completed - all student agents have submitted assignment 3

The numbers shold be labled so they are in chronological order.
"""

STOPCONDITIONXIDEA_EXAMPLES = """The Stop condition ideas focus on in what state the simulation can stop.
Examples include "an agreement has been made between agent A and agent B", "there are no more funds", "3 rounds are completed".
Keep it simple. Do not brainstorm anythign that is overly complex.
"""

STOPCONDITIONXGROUNDING_EXAMPLES = """The Stop Condition Grounding should focus on the specifics of the stop condition.
What room should the stop condition be in? What should have the agents been able to do before the simulation is over?
It should clarify the exact state in which the simulatoin will stop.
"""

FAILURECONDITIONXIDEA_EXAMPLES = """The failure condition ideas focus on some scenarios in which we know the simulation has derailed.
Examples include "agents wait for acknowledgements for something they say indefinitely", "agents try to do an impossible action rooted in physical world",
and "agents wait indefinitely to submit their assignments.
"""

FAILURECONDITIONXGROUNDING_EXAMPLES = """The Failure Condition Grounding should focus on the specifics of the failure condition.
What exactly does each failure condition mean to fail? What logic has gone wrong?
"""

MATRIX_EXAMPLES = {
    "AgentsXIdea": AGENTSXIDEA_EXAMPLES,
    "AgentsXGrounding": AGENTSXGROUNDING_EXAMPLES,
    "ActionsXIdea": ACTIONSXIDEA_EXAMPLES,
    "ActionsXGrounding": ACTIONSXGROUDING_EXAMPLES,
    "LocationsXIdea": LOCATIONSXIDEA_EXAMPLES,
    "LocationsXGrounding": LOCATIONSXGROUNDING_EXAMPLES,
    "MilestonesXIdea": MILESTONESXIDEA_EXAMPLES,
    "MilestonesXGrounding": MILESTONESXGROUNDING_EXAMPLES,
    "StopConditionXIdea": STOPCONDITIONXIDEA_EXAMPLES,
    "StopConditionXGrounding": STOPCONDITIONXGROUNDING_EXAMPLES,
    "FailureConditionXIdea": FAILURECONDITIONXIDEA_EXAMPLES,
    "FailureConditionXGrounding": FAILURECONDITIONXGROUNDING_EXAMPLES,
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
    # is_action = "Actions" in category
    print(f"category {category} is_grounding {is_grounding}")
    iteration_message = f"The user would also like you to factor this into the brainstormed answer: {iteration}" if iteration != "" else ""
    user_message = f"""This is the category you are brainstorming for: {category}. {iteration_message}.
    Make sure not to repeat brainstorms from this list: {existing_brainstorms}
    """
    if not is_grounding:
        response_format = """
            The answers SHOULD BE 10-15 words WORDS that specify what exactly the idea is. ALL THE ANSWERS MUST BE VERY DIFFERENT FROM ONE ANOTHER.
            Format the the responses in an array like so: ["home-buyer agents declare their bid", "home-owner agents can only speak to the real-estate agent", "simulation ends when real-estate agent picks a buyer"]
            The array should have size 10 maximum. The inputsa must all be different from one another.
            IF THE TYPE IS A STOP CONDITION, THE ARRAY CAN ONLY HAVE 3 SIZES MAXIMUM. USE THE MILESTONES CONTEXT TO INFORM HOW YOU WILL RETURN THE STOP CONDITION.
            """
    elif is_grounding:
        response_format = """
            The answers should be as specific as possible, but do not be overly verbose in your response. USE AS LITTLE WORDS AS POSSIBLE. Do not repeat what is said in the corresponding idea section.
            The answer should be 50-100 words.
        RETURN THE ANSWER AS A STRING WITH BULLETED LIST. THERHE SHOULD BE A BULLET POINT FOR EACH BOX CHECKED IN THE IDEA SECTION:
        example:
            - The daily message should include a concise profile summary for each of the five matches, highlighting essential details such as name, age, occupation, and a short personal note or shared interest.
            - Include compatibility scores or commonalities (e.g., mutual friends, hobbies) to help users quickly assess each match’s potential.
            - Provide clear action buttons within the message to either like, pass, or start a conversation, making it easy for users to engage with their daily options.
            DO NOT RETURN A PARAGRAPH.
        """
    # else:
    #     response_format = """
    #         The answers SHOULD BE 10-15 words WORDS that specify what exactly the idea is. ALL THE ANSWERS MUST BE VERY DIFFERENT FROM ONE ANOTHER.
    #         Format the the responses in an array like so: ["1 professor and 2 students", "3 shoppers"]
    #         The array should have size 3 maximum.
    #     """

    system_message = f"""
    You are a helpful assistant that helps brainstorm specification answers for a category to narrow down inputs.
    {MATRIX_DESCRIPTION}
    {PAAW_EXAMPLES}
    Here is the context for this problem: {context}
    {MATRIX_EXAMPLES[category]}
    {response_format}
    """
    res = call_llm(system_message, user_message)
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
    res = call_llm(system_message, user_message)
    print("sucessfully called LLM for cleanup_brainstorms", res)
    cleaned = res
    try:
        cleaned_json = json.loads(cleaned)
        return cleaned_json
    except json.JSONDecodeError:
        print("Error decoding JSON, retrying...")
        return cleanup_array(brainstorms)