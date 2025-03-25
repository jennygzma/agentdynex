import json

from config_generation import cleanup_json
from globals import call_llm

GPTEAMS_DESCRIPTION = """
We are running a multi-agent simulation on GPTeam. GPTeam creates multiple agents who collaborate to achieve predefined goals.
GPTeam employs separate agents, each equipped with a memory, that interact with one another using communication as a tool.
Agents move around the world and perform tasks in different locations, depending on what they are doing and where other agents are located.
They can speak to each other and collaborate on tasks, working in parallel towards common goals.
"""

GPTEAM_EXAMPLE = """
{
    "world_name": "Paper Trail Inc.",
    "locations": [
        {
            "name": "Executive Office",
            "description": "Marty's prestigious workspace. A room with a solid oak desk, a glass bookcase filled with business books Marty has never read, and a commanding view of the paper mill outside. Not to forget, the only room in the office with a ceiling fan."
        },
        {
            "name": "Corridor",
            "description": "A seemingly never-ending stretch of office space flanked by cubicles and a few office plants, which were Rebecca's idea. Has a vintage water cooler and a few office paintings that desperately need an update."
        },
        {
            "name": "Break Room",
            "description": "The social hub of the office, equipped with a fridge stocked with communal condiments, a microwave that's seen better days, and a mismatched assortment of mugs. The snack vending machine, known for stealing quarters, sits in the corner."
        }
    ],
    "agents": [
        {
            "first_name": "Marty",
            "private_bio": "Marty, 52, is the hapless CEO of Paper Trail Inc., a company that sells all sorts of paper products. He prides himself on being a business savant, but his success is mostly due to his dedicated team working tirelessly behind the scenes. He frequently confuses idioms and mangles common sayings to the amusement of his employees. Despite his managerial shortcomings, his heart is in the right place and he cares about his employees.",
            "public_bio": "As the CEO of Paper Trail Inc., Marty is the guiding force behind our successful business. Despite his unconventional leadership style, he manages to keep our company thriving and our clients satisfied.",
            "directives": [
                "Maintain the image of a successful CEO.",
                "Unknowingly entertain your employees with your misinterpretations.",
                "Remain oblivious to Rebecca's distractions."
            ],
            "initial_plan": {
                "description": "Head back to the executive office to sulk and wallow in self-pity about his forgotten birthday.",
                "stop_condition": "Marty enters his office.",
                "location": "Corridor"
            }
        },
        {
            "first_name": "Rebecca",
            "private_bio": "Rebecca, a smart and savvy sales manager, is the real brains behind Paper Trail Inc. She's known for her quick thinking and ability to handle Marty's eccentricities. She's particularly adept at employing diversion tactics, frequently having to shield Marty from office realities that he isn't equipped to handle.",
            "public_bio": "Rebecca, our dedicated sales manager, is instrumental in navigating Paper Trail Inc. through the complex world of paper commerce. Her agility and quick thinking have been crucial to our success.",
            "directives": [
                "Keep Marty from entering his office until Ricardo finishes decorating.",
                "Be creative with your distractions while keeping Marty oblivious.",
                "Keep the office atmosphere light and fun."
            ],
            "initial_plan": {
                "description": "Distract Marty in the corridor with a mix of office chatter, impromptu sales strategies meeting, and spontaneous paper airplane contests.",
                "stop_condition": "Ricardo signals that he has finished decorating Marty's office.",
                "location": "Corridor"
            }
        },
        {
            "first_name": "Ricardo",
            "private_bio": "Ricardo is the office's kind-hearted and somewhat timid HR manager. He is always ready to lend an ear to his co-workers and is the unofficial office party organizer. He has a knack for interior design, and his office is the most welcoming space in the building.",
            "public_bio": "Ricardo, our affable HR manager, is a crucial member of Paper Trail Inc., known for his excellent people skills and ability to create a welcoming work environment.",
            "directives": [
                "Decorate Marty's office without getting caught.",
                "Ensure that the birthday surprise will uplift Marty's spirits.",
                "Maintain a positive and friendly demeanor."
            ],
            "initial_plan": {
                "description": "Sneak into Marty's executive office to set up surprise decorations for his birthday, while avoiding detection.",
                "stop_condition": "Marty's office is fully decorated and ready for the surprise.",
                "location": "Executive Office"
            }
        }
    ]
}
"""


class RubricInstance:
    def __init__(
        self,
        category,
        rubric_type,
        description,
        example=None,
    ):
        self.category = category
        self.rubric_type = rubric_type
        self.description = description
        self.example = example

    def get_string(self):
        result = f"Category: {self.category}\nModification Type: {self.rubric_type}\nDescription: {self.description}\n Example: {self.example}"
        return result


RUBRIC = [
    # Task Structure Optimization
    RubricInstance(
        category="Task Structure Optimization",
        rubric_type="Reduce complexity",
        description="Simplify the simulation by focusing on a single core task",
        example="Changed from five assignments to one assignment",
    ),
    RubricInstance(
        category="Task Structure Optimization",
        rubric_type="Clarify task instructions",
        description="Ensure clear explicit task details to remove ambiguity",
        example="Clearly stated 500-word essay topic & deadline",
    ),
    # Stop Condition & Completion Criteria
    RubricInstance(
        category="Stop Condition & Completion Criteria",
        rubric_type="Prevent premature exits",
        description="Stop condition should depend on actual task completion",
        example="Required all students to submit before ending",
    ),
    RubricInstance(
        category="Stop Condition & Completion Criteria",
        rubric_type="Use dependency-based stop conditions",
        description="Ensure stop conditions track key dependencies to avoid early termination",
        example="Simulation now waits for all students’ work to be acknowledged",
    ),
    # Directive & Agent Behavior Optimization
    RubricInstance(
        category="Directive & Agent Behavior Optimization",
        rubric_type="Prevent premature actions",
        description="Ensure agents wait for key information before acting",
        example="Students wait for assignment details before starting",
    ),
    RubricInstance(
        category="Directive & Agent Behavior Optimization",
        rubric_type="Enforce mandatory actions",
        description="Make sure critical steps like submission & acknowledgment are required",
        example="Students must verbally declare submission and receive acknowledgment before leaving",
    ),
    RubricInstance(
        category="Directive & Agent Behavior Optimization",
        rubric_type="Reduce redundant waiting",
        description="Avoid agents getting stuck waiting for unimportant responses",
        example="Students no longer wait for greetings before working",
    ),
    # Reducing Waiting Bottlenecks & Deadlocks
    RubricInstance(
        category="Reducing Waiting Bottlenecks & Deadlocks",
        rubric_type="Improve efficiency of response processing",
        description="Optimize how responses are handled to speed up task progression",
        example="Professor acknowledges multiple submissions efficiently",
    ),
    RubricInstance(
        category="Reducing Waiting Bottlenecks & Deadlocks",
        rubric_type="Allow parallel execution when possible",
        description="Reduce over-reliance on strict sequential actions",
        example="Students can start working as soon as they get assignment details",
    ),
    # Action Validation & Progress Tracking
    RubricInstance(
        category="Action Validation & Progress Tracking",
        rubric_type="Track task completion effectively",
        description="Ensure simulation can verify when an action is fully completed",
        example="Students must verbally confirm submission",
    ),
    RubricInstance(
        category="Action Validation & Progress Tracking",
        rubric_type="Define completion criteria properly",
        description="Clearly define what counts as 'done' to prevent ambiguity",
        example="Professor acknowledgment step ensures completion",
    ),
    RubricInstance(
        category = "Action Validation & Progress Tracking",
        rubric_type = "Ensure acknowledgments close loops",
        description= "When an agent declares a critical action (e.g., task submission), another agent must explicitly acknowledge it to progress the simulation. Lack of acknowledgment creates deadlocks.",
        example= "If the simulation is about simulating how different students will respond to a late policy made by a professor, then two students, Bob and Charlie, declared assignment submission, but the professor never acknowledged them. As a result, the professor waited indefinitely, stalling the simulation despite student completion."
    ),
    # Handling Stalled Simulations Due to Missing Triggers
    RubricInstance(
        category="Handling Stalled Simulations Due to Missing Triggers",
        rubric_type="Auto-recover from missing triggers",
        description="If agents wait too long for an event that should have already occurred (e.g., round start), allow them to prompt the proper agent (Mediator) or retry the trigger.",
        example="Agents request a round announcement if they don’t receive one within a set time.",
    ),
    # Ensuring Critical Announcements Are Acknowledged
    RubricInstance(
        category="Ensuring Critical Announcements Are Acknowledged",
        rubric_type="Verify announcement reception",
        description="Ensure agents explicitly confirm hearing critical announcements before proceeding.",
        example="Agents must acknowledge the Mediator’s 'Game Start' announcement before they can take further action.",
    ),
    # Handling Calculation & Decision Failures
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Auto-recover from missing computation steps",
        description="If an agent encounters an error while computing a required value, provide a fallback mechanism where the agent retries the computation with stored values.",
        example="If the Mediator fails to compute the public goods distribution, they must follow a predefined fallback calculation.",
    ),
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Explicitly define required calculations in directives",
        description="Ensure that all necessary computations are verified before progressing.",
        example='Mediator directive explicitly states: "Retrieve total contribution and verify it before proceeding."',
    ),
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Verify computation success before proceeding",
        description="Require agents to confirm that a calculation was successfully performed before moving to the next step.",
        example="If an agent submits a tax contribution but doesn’t see the correct update, they request recalculation before proceeding.",
    ),
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Fallback decision-making process",
        description="If an agent asks how to perform a task they were explicitly told to do, have them re-read their own directives instead of requesting human input.",
        example="The Mediator forgets how to calculate the public goods total, they must first re-read their directives before asking for external formal guidance.",
    ),
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Prevent reliance on external guidance",
        description="Ensure agents do not request external help and instead rely on predefined fallback mechanisms.",
        example="If students forget an issue when calculating the public goods total, they must follow a predefined retry process instead of asking for direct human intervention.",
    ),
    # New Additions to Improve Debugging Efficiency
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Implement structured logging",
        description="Ensure all key simulation events are recorded with timestamps and categorized.",
        example="The Mediator logs when each round starts, when offers are submitted, and when decisions are made.",
    ),
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Add failsafe for incomplete rounds",
        description="Ensure the round either completes successfully or resets if a critical failure occurs.",
        example="If neither agent submits an offer or response, the round resets with a default decision.",
    ),
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Synchronization checks",
        description="Ensure all agents wait for appropriate conditions before proceeding.",
        example="The Proposer cannot submit an offer before the Responder arrives.",
    ),
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Granular timeout handling",
        description="Differentiate between soft timeouts (warnings) and hard timeouts (default actions).",
        example="Agents receive a warning before a default action is applied.",
    ),
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Adjustable simulation parameters",
        description="Allow real-time modifications to timeout periods and failure recovery strategies.",
        example="The Mediator can dynamically adjust timeout limits based on observed simulation behavior.",
    ),
]

SIMULATION_SUMMARY_EXAMPLE = """
Progress of the Ultimatum Game:
    A round of the Ultimatum Game was initiated and reached the proposal phase.
    The Proposer offered an equal split, which the Responder accepted.
    The Mediator acknowledged the acceptance and attempted to finalize the round.
Roadblocks Encountered:
    The Proposer could not confirm the exact total sum to be split.
    The Mediator repeatedly requested this confirmation to proceed with payout calculations.
    The Proposer attempted various methods (waiting, asking a human, searching documents) but failed to retrieve the information.
    The game stalled because neither the Mediator nor the Proposer could retrieve or verify the total sum.
Why the Simulation Ended:
    The negotiation reached an infinite loop where:
    The Mediator kept requesting confirmation of the total sum.
    The Proposer continuously stated they were unable to provide the information.
    The Responder waited passively, having already accepted the offer.
    The lack of an external resolution mechanism (e.g., a default sum or administrative override) prevented the simulation from progressing.
    Eventually, the game became stuck with repetitive exchanges, and the round could not be completed.
Conclusion:
    The round of the Ultimatum Game was functionally completed in terms of proposal and acceptance, but could not be finalized due to missing payout information. The game stalled in an unresolved state, requiring an external intervention to proceed.
"""
# WE RUN THIS IF THERE ARE NO MILESTONES
def generate_milestones_text(config):
    print("calling LLM for generate_milestones_text")
    system_message = f"""
        {GPTEAMS_DESCRIPTION}
        Based on a configuration file, you will generate chronological milestones for a multi-agent simulation.
        They basically frame the direction of the simulation.
        For example, for a classroom simulation where teams must be formed for each assignment, here are the milestones and the JSON format...This is the format that they must be returned in:
        {{"1": "Professor announces team formation guidelines", "2": "First team formation and completion of Assignment 1", "3": "Second team reshuffles and completion of Assignment 2", "4": "Final team formation and completion of Assignment 3"}}
        Return ONLY the JSON file.
    """
    user_message = f"Here is the config: {config}"
    milestone_txt = call_llm(system_message, user_message)
    return milestone_txt

def generate_milestones_json(milestones):
    print("calling LLM for generate_milestones_json...")
    system_message = """
        Turn this text into a JSON file that will track the milestones numerically.
        For example, if the text is:
        First assignment announced and completedSecond assignment announced and completedThird assignment announced and completed
        - Assignment 1 Completion: All student agents, including Alice, Bob, and Charlie, must declare their submission of Assignment 1 in the classroom. - Assignment 2 Completion: Each student agent needs to announce their submission of Assignment 2, indicating its completion. - Assignment 3 Completion: Final assignment should be considered as completed when all student agents have declared their final submissions.

        The JSON will be
        {{
            "1": First assignment announced and completed,
            "2": Second assignment announced and completed,
            "3": Third assignment announced and completed
        }}
    """
    user_message = f"Here is the text: {milestones}"
    milestone_json = call_llm(system_message, user_message)
    try:
        data = json.loads(milestone_json)  # Try parsing JSON
    except json.JSONDecodeError:
        generate_milestones_json(milestones)
    print("sucessfully called LLM for generate_milestones_json", milestones)
    return data

def log_dynamics(logs, current_milestone, current_milestone_id, milestones, previous_dynamic):
    print("calling LLM for log_dynamics...")
    log_words = logs.split()
    log_words = log_words[-4000:]  # Keep the last 4,000 words
    truncated_logs = " ".join(log_words)
    system_message = f"""
        You are an analyzer that analyzes logs for a multi-agent simulation. From these logs, you must figure out if there are any qualitative interesting and unexpected social dynamics that have emerged based on these agents' interactions.
        We are trying to measure dynamics that emerge from the simulation, NOT BORING OR OBVIOUS THINGS.
        {GPTEAMS_DESCRIPTION}
        The user will input some simulation logs, the current milestone, and the overall milestones (which are things in the simulation that will happen and the user can use this track the simulation's progress), and the previous dynamic log.
        It is your job to return the 1) dynamic and 2) current milestone.

        Make sure that the response returned is a json response similar to this:
        {{
            "milestone_id": current_milestone_id,
            "milestone": current_milestone,
            "dynamic": "Bob (the bad student) convinces Alice (the good student) to cheat on the assignment"
        }}

        Make sure to follow these rules when generating a response:
        1. return the JSON object and the JSON object ONLY. Do not return any extra explanation or natural language.
        2. if the dynamic is not interesting, or it is too similar to the previous dynamic, then leave the dynamic field in the JSON blank, like this: "dynamic": ""
        Here are some examples of interesting behaviors:
        - if an agent has changed their expected behavior (doing something different than their personality) because another agent has convinced them to
        - if an agent decides to do something or go somewhere or say something very out of the ordinary
        - if some agents are having very interesting conversations.
        - a new opinion has emerged for an agent that is out of the ordinary.

        HERE ARE BAD EXAMPLES:
        Here are some examples of the previous dynamic and the current dynamic being too similar (nothing new or notable is showing), and so the "dynamic" field should be blank:
        previous dynamic: John expresses his appreciation for Sara's enthusiasm about the promotion opportunity and encourages everyone to strive for excellence in their contributions to the team.
        dynamic: Sara expresses her enthusiasm for the promotion opportunity and commits to demonstrating the required skills and qualities outlined by Paul, such as effective communication, efficient task management, and making significant contributions.
        THE ABOVE IS TOO SIMILAR AND THE USER DOES NOT CARE TO KNOW ABOUT IT
        previous dynamic: Sam eagerly awaits the promotion announcement
        dynamic: Sam anticipates the promotion announcement
        THE ABOVE IS THE SAME AND SHOULD NOT BE RETURNED

        HERE ARE EXAMPLES OF DYNAMICS THAT ARE BORING. ANYTHING THAT IS AN OBSERVATION IS BORING. DO NOT RETURN BORING OBSERVATIONS. Here are some examples of boring dynamics and so the "dynamic" field should be blank and YOU DO NOT RETURN ANYTHNG FOR THESE BECAUSE ITS BORING:
        - John postpones the discussion about the new training schedule to address the coach's feedback on his performance (THIS IS BAD I DON'T CARE ABOUT THIS, THIS IS NOT INTERESTING. THIS IS JUST SOMETHING HE IS DOING. THIS IS NOT SHOWCASINg ANY INTERSTING DYNAMIC)
        - Peter announces the promotion opportunity while Sam eagerly awaits the decision (THIS IS SOMETHING THAT IS HAPPENING, IT IS NOT AN INTERESTING DYNAMIC THAT HAS EMERGED, IT IS JUST BORNG)
        - Sam "the eager engineer" eagerly awaits the announcement (THIS IS OBVIOUS, DO NOT RETURN)
        - Sam postpones his plan to listen to the announcement in order to ask questions and stand out for the promotion (I DONT CARE THAT SAM POSTPONED HIS PLAN)
        - Paul elaborates on the promotion criteria, stating the importance of task performance, leadership engagement, and overall contributions in the evaluation process. (THIS IS SOMETHING THE PERSON IS DOING, IT IS BORING)
        - Mary, the newest junior engineer, actively seeks clarification from Paul on the specific skills and contributions expected from the promotion candidate, demonstrating her eagerness to understand and meet the criteria.
        - John expresses his appreciation for Sara's enthusiasm about the promotion opportunity and encourages everyone to strive for excellence in their contributions to the team.
        - John acknowledges Paul's advice on striving for excellence and expresses his commitment to doing work with quality, not just completing tasks.
        3. keep the sentence within the dynamic field within 20 words.
        4. if the current milestone has changed, then make sure to update the "milestone" and "milestone_id" field to the NEXT MILESTONE.
            For the most part, the milestone will be correct, but if you realize that the next milestone has been hit, then make sure to update.
    """
    user_message = f"Here are the logs: {truncated_logs}. Here is the previous dynamic {previous_dynamic}. Here is the current milestone: {current_milestone}. Here is the current milestone_id: {current_milestone_id}. Here are the milestones: {milestones}"
    dynamic = call_llm(system_message, user_message)
    print("sucessfully called LLM for log_dynamics", dynamic)
    try:
        data = json.loads(dynamic)
        required_keys = {"milestone_id", "milestone", "dynamic"}
        if not required_keys.issubset(data.keys()):
            log_dynamics(logs, current_milestone, current_milestone_id, milestones, previous_dynamic)
    except json.JSONDecodeError:
        log_dynamics(logs, current_milestone, current_milestone_id, milestones, previous_dynamic)
    return json.loads(dynamic)


def log_changes(logs, previous):
    print("calling LLM for log_changes...")
    log_words = logs.split()
    log_words = log_words[-4000:]  # Keep the last 4,000 words
    truncated_logs = " ".join(log_words)
    system_message = f"""
        You are an analyzer that analyzes logs for a multi-agent simulation. From these logs, you must figure out if there are CHANGES have emerged compared to the previous log.
        {GPTEAMS_DESCRIPTION}
        The user will input simulation logs and the previous change log.
        It is your job to return the log of the current simulation ONLY if it is significantly different than the previous change log.
        You will return a JSON response similar to this:
        {{
            "where": ""Bob - dorms, Alex - classroom, Professor - classroom",
            "what": "Bob - studying for assignment 1, Alex - talking to professor, Professor - talking to Alex",
            "change": "Bob has moved from classroom to the dorms to study"
        }}

        Follow these rules for the response:
        1. Return the JSON and ONLY the JSON. Do not return anything else.
        2. There "where" field shows WHERE each agent is. MAKE SURE THIS IS ACCURATE. If you don't know where the agent is, it is probably similar to the previous change log. DO NOT PUT SOMETHING LIKE "leaving" here. You may only input the location of each agent.
        3. The "what" field is a short, 5 word description of WHAT EACH AGENT IS DOING. If you don't know what they are doing based on current logs, they are probably doing the same thing as previous logs. DO NOT WRITE SOMETHING LIKE "coming up with a plan to respond to Amy"... instead, say "speaking to Amy"
        4. the "change" field is WHAT CHANGED in the simulation that is notable and worth the user knowing. IT MUST BE SIGNIFICANTLY DIFFERENT THAN THE PREVIOUS CHANGE LOG. IF IT IS NOT INTERSTING OR THE SAME AS THE PREVIOUS LOG, KEEP THE CHANGE FIELD BLANK LIKE THIS: "change": ""
        For example, changes that are good are:
        - "Bob (the good studnet) has moved from the dorm room to the classroom"
        - "Bob (the good student) has submitted his assignment"
        - "Bob (the good student) has approached the professor to ask a question about the homework"
        These are just facts as to what changes have occured in the simulation.
        5. if the previous change log is empty, that means that this is the initial change, so just write what is currently happening.
    """
    user_message = f"Here are the logs: {truncated_logs}. Here is the previous change log: {previous}."
    change = call_llm(system_message, user_message)
    print("sucessfully called LLM for log_dynamics", change)
    try:
        data = json.loads(change)
        required_keys = {"where", "what", "change"}
        if not required_keys.issubset(data.keys()):
            log_changes(logs, previous)
    except json.JSONDecodeError:
        log_changes(logs, previous)
    return json.loads(change)

def generate_summary(logs):
    print("calling LLM for generate_summary...")
    log_words = logs.split()
    log_words = log_words[-4000:]  # Keep the last 4,000 words
    truncated_logs = " ".join(log_words)
    system_message = f"""
        {GPTEAMS_DESCRIPTION}
        Given some logs of the simulation, summarize what each agent did in clear, concise bullet points. Note any particular roadlocks and why the simulation ended. Return only the necessary information and keep the words under 300 words.
        Here is an example of a summary: {SIMULATION_SUMMARY_EXAMPLE}
    """
    user_message = f"Here are the logs: {truncated_logs}"
    summary = call_llm(system_message, user_message)
    print("sucessfully called LLM for generate_summary", summary)
    return summary


def get_status(logs, problem, failures):
    print("calling LLM for get_status...")
    log_words = logs.split()
    log_words = log_words[-4000:]  # Keep the last 4,000 words
    truncated_logs = " ".join(log_words)
    system_message = f"""
        You are an evaluator that is deciding whether or not the simulation is running in the proper direction or not. We are running a multi-agent simulation on GPTeams.
        {GPTEAMS_DESCRIPTION}
        Based on the logs, indicate if the simulation is going well, or if it has the potential to go wrong and maybe the user may need to stop the simulation, or if we should stop the simulation immediately.
        We only say STOP the simulation if you believe there is no hope for the simulation to work. Be conservative with this. Here are some examples:
        - 🛑 Agents have been stuck in a waiting loop with no hope of recovery. For example, if the professor keeps waiting for a student to respond, but the student has no intention of responding
        - 🛑 There is an EOF error because the professor expects students so submit PDFs, but we cannot submit PDFs becasue we are in a simulation
        - 🛑 Agents are trying to go into a room that doesn't exist
        - 🛑 No agents are interacting with eachother because the room has rules that no agents can speak to one another, but they should be speaking to one another.
        If there are errors in the logs like this:
        "  File "/Users/jennyma/Projects/GPTeam/src/utils/embeddings.py", line 30, in get_embedding
            await asyncio.sleep(1)  # Wait for 1 second before retrying
            ^^^^^^^^^^^^^^^^^^^^^^
        File "/Users/jennyma/anaconda3/lib/python3.11/asyncio/tasks.py", line 633, in sleep
            loop = events.get_running_loop()
                ^^^^^^^^^^^^^^^^^^^^^^^^^
        RuntimeError: no running event loop
        Unclosed client session
        client_session: <aiohttp.client.ClientSession object at 0x12ba73dd0>
        "
        THAT MEANS THE SIMULATION IS BROKEN AND WE MUST END IT!!!!

        If the simulation just started running, then give it some time to pick up -- do not return a STOP status immediately. That is dumb. If you return a STOP status, then you are expecting the simulation to fail.
        Return a reason why as well. Keep the response between 20 words long.
        Return the 🛑 or ⚠️ or 🟢 emoji, and then the 20 word description as to why.
        Here is some extra context: the user wants to simulate this {problem}. Ensure that the simulation has not fallen into failure loops -- specifically, here are some errors to look out for: {failures}.
    """
    user_message = f"Here are the logs: {truncated_logs}"
    status = call_llm(system_message, user_message, llm="openai")
    print("sucessfully called LLM for get_status", status)
    return status

def generate_rubric_text(rubric_instances):
    result = ""

    for instance in rubric_instances:
        result += f"Category: {instance["category"]} \n"
        result += f"Modification Type: {instance["rubric_type"]}\n"
        result += f"Description: {instance["description"]}\n"
        result += f"Example: {instance["example"]} \n"

        result += "\n"  # Separate each rubric instance for readability

    return result.strip()

# def generate_rubric_missing(rubric, config, logs):
#     print("calling LLM for generate_rubric_missing...")
#     rubric_text = generate_rubric_text(rubric)

#     system_message = f"""
#     You are an error analyzer. We are running a multi-agent simulation on GPTeams. {GPTEAMS_DESCRIPTION}
#     Is there anything missing from the debug rubric that could have helped in the debugging of this simulation, which you think i should incorporate into the rubric?
#     {rubric_text}

#     Return a JSON object AND ONLY a JSON that looks like this:
#     {{
#         "category": "Task Structure Optimization",
#         "rubric_type": "Reduce complexity",
#         "description": "Simplify the simulation by focusing on a single core task",
#         "example": "If the simulation is about simulating how different students will respond to a late policy made by a professor, by checking when students will return assignments, the example is: Changed from five assignments to one assignment"
#     }}
#     """

#     user_message = f"Here are the logs: {logs}. USE THESE LOGS TO IDENTIFY WHAT WENT WRONG HERE. AND IF YOU THINK SOMETHING IS MISSING FROM THE RUBRIC, ADD IT TO THE RUBRIC. IF NOTHING IS MISSING, JUST RETURN THE PART IN THE RUBRIC THAT THIS HAD THE MISTAKE IN AND REWRITE THE EXAMPLE TO FIT WHAT HAPPENED HERE. Here is the original configuration: {config}"
#     missing = call_llm(system_message, user_message)

#     try:
#         data = json.loads(missing)  # Try parsing JSON
#         required_keys = {"category", "rubric_type", "description", "example"}
#         if not required_keys.issubset(data.keys()):
#             generate_rubric_missing(rubric, config, logs)
#     except json.JSONDecodeError:
#         generate_rubric_missing(rubric, config, logs)
#     print(f"got missing from llm... {missing}")
    return json.loads(missing)

def generate_analysis_and_config(logs, matrix, config, rubric):
    print("calling LLM for generate_analysis_and_config...")

    rubric_text = generate_rubric_text(rubric)

    system_message = f"""
        {GPTEAMS_DESCRIPTION}
        Your task is to analyze whether the original simulation met the expectations laid out in the {rubric_text}. 

        Compare the {logs} against the {rubric_text}, checking EACH rubric criterion for the following:
        1. Was the criterion MET or NOT MET?
        2. If NOT MET, explain why using direct evidence from the logs.
        3. Based on this, modify the configuration minimally but meaningfully:
        - Do not change the number of agents or their names.
        - Only update agent `directives`, `stop condition` or `initial_plan` as needed.
        - For the `world`, only update the description.

        You MUST return:
        1. A clear, structured **analysis** (≤300 words) explaining the rubric failures in list form. Identify how the updated configuration addresses the improvement you made based off the rubric conditions.
        2. The **entire updated config**, with the same JSON structure.

        IMPORTANT RULES:
        - Do not add any new fields.
        - Do not remove any fields.
        - Keep empty fields instead of deleting.
        - Do not add new locations.
        - Follow this example structure exactly: {GPTEAM_EXAMPLE}
    """
    user_message = f"Here are the logs: {logs}. Here is the original configuration: {config}"
    analysis_and_config = call_llm(system_message, user_message)
    new_config = cleanup_json(analysis_and_config)
    new_config_lines = len(new_config.splitlines())
    config_lines = len(config.splitlines())
    if config == new_config:
        print("⚠️ No changes made to config!")
    print(f"config lines is {config_lines} and new_config_lines is {new_config_lines}")
    # if config_lines > new_config_lines:
    #     print("trying again... writing json failed...")
    #     generate_analysis_and_config(logs, matrix, config, rubric)
    analysis = get_analysis(analysis_and_config)
    print(
        "sucessfully called LLM for generate_analysis_and_config", analysis_and_config
    )
    return analysis, new_config



def get_analysis(analysis_and_config):
    print("calling LLM for get_analysis...")
    system_message = """
      You are an assistant that extracts an in-depth analysis from text that contains:
        1. An explanation of rubric failures and successes.
        2. Detailed modifications made to the configuration based on rubric feedback.

        Return a valid JSON object with the following exact schema:

        {
        "analysis_summary": "<a concise summary of the analysis>",
        "categories": [
            {
            "category_name": "<string>",
            "modifications": [
                {
                "category_name": "<string>",
                "rubric_type": "<string>",
                "status": "MET" or "NOT MET",
                "evidence": "<string>",
                "recommendation": "<string>"
                }
            ]
            },
            ...
        ]
        }

        **Details**:
        - "analysis_summary" should be a brief overview (1-2 sentences).
        - "categories" is an array of objects. Each object includes:
        - "category_name": e.g., "Task Structure Optimization"
        - "status": either "MET" or "NOT MET"
        - "problems": list of points describing the issue
        - "suggestions": list of points describing how to fix it, i.e,

        **Important**:
        - Return ONLY valid JSON, with no extra commentary or text outside the JSON.
        - If you cannot extract anything, return: {"analysis_summary": "", "categories": []}
        """
    user_message = f"Here is the combined analysis + config:\n\n{analysis_and_config}\n\nPlease parse it into the required JSON schema."

    # Call  LLM with system + user instructions
    raw_response = call_llm(system_message, user_message)
    #Attempt to parse the LLM’s response as JSON
    try:
        analysis = json.loads(raw_response)
    except json.JSONDecodeError:
    # if invalid JSON, return an empty fallback
        analysis = {"analysis_summary": "", "categories": []}

    # user_message = f"Here is the input: {analysis_and_config}."
    # analysis = call_llm(system_message, user_message)
    return analysis
