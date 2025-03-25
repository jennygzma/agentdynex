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

def log_dynamics(logs, current_milestone, current_milestone_id, milestones):
    print("calling LLM for log_dynamics...")
    log_words = logs.split()
    log_words = log_words[-4000:]  # Keep the last 4,000 words
    truncated_logs = " ".join(log_words)
    system_message = f"""
        {GPTEAMS_DESCRIPTION}
        Read these logs and say if there are some interesting social dynamics that have emerged from these agent's behavior.
        For example, if some agents have changed their personality because some other agent has convinced them, or some new opinions have emerged, note them down.
        Keep the dynamic within 20 words.
        IT MUST BE INTERESTING. WAITING IS BORING. SOMEONE DOING SOMETHING EXPECTED IS BORING. WE ARE TRYING TO STUDY SOCIAL DYNAMICS. ONLY RETURN SOMETHING IF IT IS INTERESTING.
        Also, the user will provide the list of milestones the simulation will hit chronologically.
        They will also provide the current milestone it is under.
        For the most part, the current milestone will be correct, but if you realize that the next milestone has been hit,
        make sure to update the current milestone to the next one.

        Make sure that the response returned is a json response similar to this:
        {{
            "milestone_id": current_milestone_id,
            "milestone": current_milestone,
            "dynamic": "Bob (the bad student) convinces Alice (the good student) to cheat on the assignment"
        }}
        IF THERE IS NO NOTABLE DYNAMIC, KEEP THE DYNAMIC EMPTY
        ONLY RETURN THE JSON AND NOTHING ELSE!!
    """
    user_message = f"Here are the logs: {truncated_logs}. Here is the current milestone: {current_milestone}. Here is the current milestone_id: {current_milestone_id}. Here are the milestones: {milestones}"
    dynamic = call_llm(system_message, user_message)
    print("sucessfully called LLM for log_dynamics", dynamic)
    try:
        data = json.loads(dynamic)
        required_keys = {"milestone_id", "milestone", "dynamic"}
        if not required_keys.issubset(data.keys()):
            log_dynamics(logs, current_milestone, current_milestone_id, milestones)
    except json.JSONDecodeError:
        log_dynamics(logs, current_milestone, current_milestone_id, milestones)
    return json.loads(dynamic)


def log_changes(logs, previous):
    print("calling LLM for log_changes...")
    log_words = logs.split()
    log_words = log_words[-4000:]  # Keep the last 4,000 words
    truncated_logs = " ".join(log_words)
    system_message = f"""
        {GPTEAMS_DESCRIPTION}
        Read these logs and tell us where each agent is and what they are doing compared to the previous instance.
        The key thing is also to note WHAT CHANGE was made. The user will provide the previous change log. Detect what has changed from that.
        If the previous change log is empty, then that means this is the INITIAL change, so just write what is happening.
        Make sure that the response returned is a json response similar to this:
        {{
            "where": ""Bob - dorms, Alex - classroom, Professor - classroom",
            "what": "Bob - studying for assignment 1, Alex - talking to professor, Professor - talking to Alex",
            "change": "Bob has moved from classroom to the dorms to study"
        }}
        the "where" field should track where each agent is.
        the "what" field should track what each agent is DOING
        the "change" field tracks any notable changes from the previous time, ie: if the agent moved rooms.
        If there is no change, keep the CHANGE field empty.

        ONLY RETURN THE JSON AND NOTHING ELSE!!
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
        Sometimes, simulations get stuck in a loop that cannot be fixed due to some logical error.
        Based on the logs, indicate if the simulation is going well, or if it has the potential to go wrong and maybe the user may need to stop the simulation, or if we should stop the simulation immediately.
        We only say STOP the simulation if you believe there is no hope for the simulation to work. Be conservative with this. Here are some examples:
        - Agents have been stuck in a waiting loop with no hope of recovery. For example, if the professor keeps waiting for a student to respond, but the student has no intention of responding
        - There is an EOF error because the professor expects students so submit PDFs, but we cannot submit PDFs becasue we are in a simulation
        - Agents are trying to go into a room that doesn't exist
        - No agents are interacting with eachother because the room has rules that no agents can speak to one another, but they should be speaking to one another.
        If the simulation just started running, then give it some time to pick up -- do not return a STOP status immediately. That is dumb. If you return a STOP status, then you are expecting the simulation to fail.
        Return a reason why as well. Keep the response between 100 characters long.
        Return the 🛑 or ⚠️ or 🟢 emoji, and then the 100 word description as to why.
        Here is some extra context: the user wants to simulate this {problem}. Ensure that the simulation has not fallen into failure loops -- specifically, here are some errors to look out for: {failures}
    """
    user_message = f"Here are the logs: {truncated_logs}"
    status = call_llm(system_message, user_message)
    print("sucessfully called LLM for get_status", status)
    return status

def get_progress(logs, matrix):
    print("calling LLM for get_progress...")
    log_words = logs.split()
    log_words = log_words[-4000:]  # Keep the last 4,000 words
    truncated_logs = " ".join(log_words)
    system_message = f"""
        You are an evaluator that is deciding whether or not the simulation is running in the proper direction or not.
        We are running a multi-agent simulation on GPTeams.
        {GPTEAMS_DESCRIPTION}
        For each agent as defined in the design matrix, return where in the world they are, and what they are doing.

        Also return a one sentence description of the general state of the simulation.

        For example, here is a response given this matrix:


        Here is some extra context: the user wants to simulate this {matrix}.
    """
    user_message = f"Here are the logs: {truncated_logs}"
    status = call_llm(system_message, user_message)
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
