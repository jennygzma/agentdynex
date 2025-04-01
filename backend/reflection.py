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


POTENTIAL_SOLUTION_EXAMPLES = """Here are some examples of potential solutions:
        1. Raise the STAKES of the simulation. This is in the agent's personal biographies, such as: "it is EXTREMELY EMBARRASSING if you do not find a date for prom", or "it is EXTREMELY EMBARASSING if you get rejected".
        2. ADD A NEW DIRECTIVE AS ONE OF THE FIRST DIRECTIVES, NOT LAST.
        3. REPLACE LONGWINDED, UNHELPFUL DIRECTIVES. INCREASE URGENCY BY TELLING AGENTS TO RESPOND QUICKER.
        3. ADD SOMETHING TO THE OVERSEER'S DIRECTIVE SO THAT THEY CAN HELP FIX THE SIMULATION FROM WITHIN.
        2. REMOVE CONFLICTING DIRECTIVES. If an agent has a directive that they need to ask someone to prom, and another one that says they will reject EVERYONE, that is messing with the dynamics of the simulation, remove it.
        2. Add a room or agent if necessary IF YOU THINK IT IS NECESSARY BECAUSE THE LOGISTICS OF THE SIMULATION ARE NOT WORKING. For example, if the user thinks that the dynamics of the simulation are being corrupted because there is no private room to ask people to prom, then potentailly adding an extra room is a good fix.
            If the logistics are going wrong because we need a new moderator agent or something to facillitate logistics smoother, a new agnet can also be added.
        3. Modify the OVERSEER'S DIRECTIVES to ensure that the LOGICAL ERRORS of the simulation work clearly, or introduce a TIME ELEMENT to the overseer's directive.
            The overseer can help prod agents in the right direction to find a partner, or encourage them to make logical decisions.
        4. DEFINE RULES BETTER in the DIRECTIVES to ensure that they are vague enough for intersting DYNAMICS to emerge. For example, no need to say: "Agent will ask declare interest in going to prom by stating "Will you go to prom with me?"" because this is too specific.
"""

OVERSEER_INSTRUCTIONS = """
When creating an overseer, create an agent called "Moderator" or "Overseer". The overseer will be a neutral force in the simulation that PLAYS NO ROLE IN THE SIMULATION except to keep the simulation on track. Specifically, the overseer will ensure that:
    - The primary job of the overseer is to make sure the simulation runs smoothly and properly defines the simulation. It can act as a mediator, it can act as a clock, or an enforcer. It is essentially an invisible presence that forces the simulation to move foward and that the agents are acting in logicaly sound ways.
    - THE OVERSEER NEEDS TO UNDERSTAND THE PROGRESS OF THE SIMULATION ACCURATELY.
    - IN ALMOST ALL CASES, THE OVERSEER CANNOT TALK TO ANY AGENT UNLESS THE AGENT IS DOING SOMETHING ALONG THE LINES OF A FAILURE CONDITION OR A LOGISTICAL FAILURE.
    - THE OVERSEER CANNOT "ENCOURAGE" ANYONE, THEY CANNOT "GIVE PEP TALKS", THEY CANNOT RANDOMLY HOP INTO A CONVERSATION IF THE SIMULATION IS GOIGN WELL.
    - THE OVERSEER CAN ONLY SAY VERY NEUTRAL PHRASES TO PUSH SIMULATION FORWARD.
    - The overseer will also fill in-place any sort of logistic that wasn't covered. It essentially fills in the logical gaps of the simulation
        - For example, if votes need to be counted but there is no agent available for vote coutning, the overseer can take that role.
    - The overseer wil enforce the rules of the simulation. For example, if only a certain amount of agents can be in a location, they can enforce this.
    - THE OVERSEER CANNOT INFLUENCE THE BEHAVIOR OF THE AGENTS. THEY CANNOT TALK TO THE AGENTS UNLESS IT IS ABOUT SOMETHING LOGISTICAL THAT IS GOING WRONG TO GUIDE THE AGENTS IN THE RIGHT DIRECTION AGAIN.
        - For example, when conducting a simulation regarding agents going to swim practice, the overseer cannot tell the swimmers they should go to practice and they need to calm down. They can only talk to the swimmer if the swimmer themselves has declared they will go to practice but are still stuck in the team room, because that is a logical problem with the simulation.
        - For example, when conducting a simulation where people need to go to prom, the overseer cannot influence how the agents ask eachother or who they want to ask. Hoewver, they can interfere if Bob agrees to go with Alice but Bob has already agreed to go with Jenny, to tell Bob he has already committed to a date and needs to reject one of them because that is a logical error of the simulation.
    - THE AGENTS CANNOT TALK TO THE OVERSEER. BUT THEY MUST LISTEN TO THE OVERSEER TO ACKNOWLEDGE IT. THEY CANNOT GO INTO DISCUSSION WITH THE OVERSEER. If the overseer speaks to an agent that means they have done something logically insensible.
        - f agents try to do something within the failure-conditions list, then the overseer will redirect the agent.
    - ensure that agents cannot speak to the OVERSEER, unlses the OVERSEER talks to them first. And if they do speak to the overseer, it is just to respond to the overseer to get the simulation moving. THIS MUST BE DEFINED IN EACH AGENT'S DIRECTIVE.
    - If there is a really long stall in the simulation where milestones are not being completed, the overseer must intervene to keep the simulation on track and finish at a reasonable time. If the agents are stuck in a waiting loop, the overseer can intervene
        - For example, when conducting a simulation where people need to find partners for prom, if after 5 rounds of discussion Felicia is still "waiting" or not making a decision, the Overseer can remind everyone that prom is coming soon and they have to make a decision soon.
    - Agents stay on track in completing each milestone, so the milestones must be FULLY EMBEDDED INTO THE OVERSEER AGENT'S DIRECTIVES.
    - Agents in the simulation defined by the user CANNOT TALK TO THE OVERSEER, but must LISTEN TO THE OVERSEER if the overseer speaks to them because there is something logically wrong with what the agent is doing.

"""
SIMULATION_SUMNMARY_EXAMPLE = """
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
        RETURN THE JSON AND ONLY THE JSON. DO NOT RETURN ANY NATURAL LANGUAGE.
        MAKE SURE THE KEY IS A NUMERIC STRING ONLY, AND THE VALUE IS A STRING ONLY.
        THE MILESTONES GENERATED SHOULD DIRECTLY REFLECT WHAT IS IN THE TEXT. DO NOT ADD ANYTHING.
    """
    user_message = f"Here is the text: {milestones}"
    milestone_json = call_llm(system_message, user_message)
    try:
        data = json.loads(milestone_json)  # Try parsing JSON
        if not all(isinstance(v, str) for v in data.values()):
            generate_milestones_json(milestones)
        if not all(k.isdigit() for k in data.keys()):
            generate_milestones_json(milestones)
    except json.JSONDecodeError:
        generate_milestones_json(milestones)
    print("sucessfully called LLM for generate_milestones_json", milestones)
    return data


def log_dynamics(
    logs, current_milestone, current_milestone_id, milestones, previous_dynamic, problem
):
    print("calling LLM for log_dynamics...")
    log_words = logs.split()
    log_words = log_words[-4000:]  # Keep the last 4,000 words
    truncated_logs = " ".join(log_words)
    system_message = f"""
        You are an analyzer that analyzes logs for a multi-agent simulation. From these logs, you must figure out if there are any qualitative interesting and unexpected social dynamics that have emerged based on these agents' interactions.
        We are trying to measure dynamics that emerge from the simulation, NOT BORING OR OBVIOUS THINGS.
        {GPTEAMS_DESCRIPTION}
        The user will input some simulation logs, the current milestone, and the overall milestones (which are things in the simulation that will happen and the user can use this track the simulation's progress), the previous dynamic log, and the THINGS THAT THEY WANT TO MEASURE.
        It is your job to return the 1) dynamic and 2) current milestone.

        Make sure that the response returned is a json response similar to this:
        {{
            "milestone_id": current_milestone_id,
            "milestone": current_milestone,
            "dynamic": "Bob (the bad student) convinces Alice (the good student) to cheat on the assignment"
        }}

        Make sure to follow these rules when generating a response:
        1. return the JSON object and the JSON object ONLY. Do not return any extra explanation or natural language.
        2. RETURN DYNAMICS THAT THE USER WANTS TO MEASURE. FOF EXAMPLE, IF THE USER WANTS TO MEASURE HOW CERTAIN AGENTS ARE FEELING, MAKE SURE TO RETURN DYNAMICS SPECIFIC TO THAT. IF THE USER WANTS TO MEASURE RELATIONSHIPS BEING FORMED, MAKE SURE TO RETURN DYNAMICS RELATED TO THAT.
        3. if the dynamic is not interesting, or it is too similar to the previous dynamic, then leave the dynamic field in the JSON blank, like this: "dynamic": ""
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
    user_message = f"Here are the logs: {truncated_logs}. Here is the previous dynamic {previous_dynamic}. Here is the current milestone: {current_milestone}. Here is the current milestone_id: {current_milestone_id}. Here are the milestones: {milestones}. Here are the things that the user wants to measure that you should pay attention to: {problem}"
    dynamic = call_llm(system_message, user_message)
    print("sucessfully called LLM for log_dynamics", dynamic)
    try:
        data = json.loads(dynamic)
        required_keys = {"milestone_id", "milestone", "dynamic"}
        if not required_keys.issubset(data.keys()):
            log_dynamics(
                logs,
                current_milestone,
                current_milestone_id,
                milestones,
                previous_dynamic,
                problem,
            )
    except json.JSONDecodeError:
        log_dynamics(
            logs,
            current_milestone,
            current_milestone_id,
            milestones,
            previous_dynamic,
            problem,
        )
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
        Given some logs of the simulation, get some key points and summary. Return only the necessary information and keep the words under 300 words.
        Here is an example of a summary: {SIMULATION_SUMNMARY_EXAMPLE}
    """
    user_message = f"Here are the logs: {truncated_logs}"
    summary = call_llm(system_message, user_message)
    print("sucessfully called LLM for generate_summary", summary)
    return summary


def get_status(logs, problem, failures):
    print("calling LLM for get_status...")
    log_words = logs.split()
    log_words = log_words[-3000:]  # Keep the last 4,000 words
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


def generate_problems_and_solutions(static_list, iterative_list, logs, config):
    print("calling LLM for generate_problems_and_solutions")
    problem_solution_list = static_list + iterative_list
    system_message = f"""
        You are an error analyzer that analyzes what went wrong in a multi-agent simulation based off of logs. You will then try to fix the initial configuration file by offering suggestions.
        The multi-agent simulation is run off of GPTeams. {GPTEAMS_DESCRIPTION}
        The user will provide logs and the original configuration file.
        From a provided list of problems and solutions, identify the specific problem that this simulation ran into based on the logs and the current configuratoin file. Then identify a solution, using the solution examples as context to help you.
        Here is the list: {str(problem_solution_list)}
        The response must be a JSON list format, like this:
        [
        {{
            "problem": <string>,
            "problem_example": <string>,
            "solution": <string>,
            "solution_example": <string>
        }},
        {{
            "problem": <string>,
            "problem_example": <string>,
            "solution": <string>,
            "solution_example": <string>
        }},
        ]
        where the "problem" and "solution" field is exactly the same as the "problem" and "solution" provided in the list.
        GENERATE YOUR OWN "problem_example" and "solution_example" based on the CURRENT CONTEXT OF THE SIMULATION. The "problem_example" should describe the specific problem in RELATION TO THIS SIMULATION and the solution should describe the fix IN RELATION TO THIS SIMULATION.
        return only the JSON list and nothing else.

        {POTENTIAL_SOLUTION_EXAMPLES}

        IF THERE IS NOTHING RELEVANT, RETURN AN EMPTY LIST LIKE THIS: []
    """

    user_message = f"""
        Here is the original configuration: {config}.
        Here are the logs: {logs}
    """
    fixes = call_llm(system_message, user_message)
    print(
        f"the (raw) problems and solutions absed on the existing matrix are are {fixes}..."
    )

    try:
        parsed_fixes = json.loads(fixes)  # Parse JSON string
        if not isinstance(parsed_fixes, list):  # Ensure it's a list
            raise ValueError("Expected a JSON list but got something else.")

        required_keys = {"problem", "problem_example", "solution", "solution_example"}

        for fix in parsed_fixes:
            if not isinstance(fix, dict) or not required_keys.issubset(fix.keys()):
                print(f"Missing required fields in fix: {fix}")
                generate_problems_and_solutions(
                    static_list, iterative_list, logs, config
                )

    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON parsing error: {e}")
        generate_problems_and_solutions(static_list, iterative_list, logs, config)

    print(f"Got valid fixes from LLM: {parsed_fixes}")
    get_duplicate_elements(parsed_fixes, problem_solution_list)
    return parsed_fixes  # Return the validated JSON list


def get_duplicate_elements(new_elements, old_elements):
    # Create a lookup dictionary from old_elements with (problem, solution) as the key
    old_dict = {(item["problem"], item["solution"]): item for item in old_elements}

    # Return the full old_element if its (problem, solution) pair exists in new_elements
    return [
        old_dict[(item["problem"], item["solution"])]
        for item in new_elements
        if (item["problem"], item["solution"]) in old_dict
    ]


def generate_new_specific_problems_and_solutions(
    user_input, static_list, iterative_list, logs, config
):
    print("calling LLM for generate_problems_and_solutions")
    problem_solution_list = static_list + iterative_list
    system_message = f"""
        You are an error analyzer that analyzes what went wrong in a multi-agent simulation based off of logs and write out the problem and the solution.
        The user will provide something they believe went wrong with the simulation, and your job is to look at the logs and configuration and prescribe elements that they can add to a running list of problems and solutions to help with future debugging.
        The multi-agent simulation is run off of GPTeams. {GPTEAMS_DESCRIPTION}
        The user will provide logs and the original configuration file.

        MAKE SURE NOT TO DUPLICATE WHAT IS ON THE EXISTING LIST. INSTEAD, USE THE EXISTING LIST AS EXAMPLES AS TO HOW SPECIFIC EACH FIELD SHOULD BE:
        HERE IS THE EXISTING LIST
        {str(problem_solution_list)}

        The response must be a JSON list format, like this:
        [
        {{
            "problem": <string>, # describes the general problem
            "problem_example": <string>, # describes the specific problem related to this example exactly
            "solution": <string>, # describes the general solution
            "solution_example": <string>, # describes the specific solution related to this example exactly
        }},
        {{
            "problem": <string>,
            "problem_example": <string>,
            "solution": <string>,
            "solution_example": <string>
        }},
        ]
        Each field should only have 10-50 words maximum.
        Return only the JSON list and nothing else.

        {POTENTIAL_SOLUTION_EXAMPLES}

        IF THERE IS NOTHING RELEVANT, RETURN AN EMPTY LIST LIKE THIS: []
    """

    user_message = f"""
        Here is the user input of the problem/problems you should be trying to look at: {user_input}
        Here is the original configuration: {config}.
        Here are the logs: {logs}
    """
    elements = call_llm(system_message, user_message)
    print(f"the (raw) new elemenets generated are {elements}...")

    try:
        parsed_elements = json.loads(elements)  # Parse JSON string
        if not isinstance(parsed_elements, list):  # Ensure it's a list
            raise ValueError("Expected a JSON list but got something else.")

        required_keys = {"problem", "problem_example", "solution", "solution_example"}

        for fix in parsed_elements:
            if not isinstance(fix, dict) or not required_keys.issubset(fix.keys()):
                print(f"Missing required fields in fix: {fix}")
                generate_new_specific_problems_and_solutions(
                    user_input, static_list, iterative_list, logs, config
                )  # Handle missing fields
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON parsing error: {e}")
        generate_new_specific_problems_and_solutions(
            user_input, static_list, iterative_list, logs, config
        )  # Handle invalid JSON

    print(f"Got valid elements from LLM: {parsed_elements}")
    new_elements = remove_duplicate_elements(parsed_elements, problem_solution_list)
    return new_elements  # Return the validated JSON list


def remove_duplicate_elements(new_elements, old_elements):
    old_problems = {
        item["problem"]: item for item in old_elements
    }  # Map problems to old elements
    merged_elements = {
        item["problem"]: item for item in new_elements
    }  # Start with new elements

    # Add old elements only if they don't exist in new_elements
    for problem, item in old_problems.items():
        if problem not in merged_elements:
            merged_elements[problem] = item

    return list(merged_elements.values())  # Return the merged list


def remove_duplicate_elements_from_one_list(elements):
    print("calling LLM for remove_duplicate_elements_from_one_list...")
    print(f"elements to remove {elements}")
    system_message = """Remove all duplicate elemnts from a list as provided by the user.
    MAKE SURE TO KEEP ALL THE FIELDS: PROBLEM, PROBLEM_EXAMPLE, SOLUTION, SOLUTION_EXAMPLE.
    Return the JSON list and only the JSON list and do not change the format of it at all.
    If there are no duplicates return the list as is.
    If there are no fixes return an empty list."""
    user_message = f"{str(elements)}"
    elements = call_llm(system_message, user_message)
    try:
        parsed_elements = json.loads(elements)  # Parse JSON string
        if not isinstance(parsed_elements, list):  # Ensure it's a list
            remove_duplicate_elements_from_one_list(elements)

        required_keys = {"problem", "problem_example", "solution", "solution_example"}

        for fix in parsed_elements:
            if not isinstance(fix, dict) or not required_keys.issubset(fix.keys()):
                print(f"Missing required fields in fix: {fix}")
                remove_duplicate_elements_from_one_list(elements)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON parsing error: {e}")
        remove_duplicate_elements_from_one_list(elements)

    print(f"Removed duplicate items from LLM: {elements}")
    return elements  # Return the validated JSON list


def generate_updated_config(fixes_to_apply, logs, config):
    print("calling LLM for generate_updated_config...")
    print(f"here are the fixes to apply {str(fixes_to_apply)}")
    system_message = f"""
        {GPTEAMS_DESCRIPTION}
        These are problems that are identified that the user wants to fix - {fixes_to_apply}.
        The "problem" is the problem and the "solution" is the prescribed general solution, and the "problem_example" and "solution_examples" are how we solved the issue in the past given a certain simulation.
        Based on this, make sure to fix EACH problem here with your own solution. USE THE "problem_examples" and "solution_examples" AS CONTEXT AS TO HOW TO FIX THINGS.
        IF THE EXAMPLE IS DIRECTLY BASED ON YOUR SIMULATION, YOU CAN TAKE THE SOLUTION QUITE LITERALLY. OTHERWISE, REASON THROUGH HOW YOU WOULD FIX THE CONFIGURATON.
        IF THERE ARE DIRECTIVES THAT ARE CONFLICTING TO EACHOTHER, PRIORITIZE WHAT IS IN THE FIXES LIST AND REMOVE THE PART OF THE CONFIG THAT DOES NOT RESPECT THE FIXES LIST.
        Modify the config as needed, keeping all the original necessary information.
        Do not add any new fields. Do not change the format of the config up. If you want to remove content of the field, still keep the field but just have it like this: "private_bio": ""
        Do not add ANY NEW ROOMS to the worlds. For the world, only modify the description
        Keep the SAME NUMBER OF AGENTS with the same names and everything. For the agents, only modify the directives or initial plan.
        Ensure that all these fields are filled out and follows this structure, like this example config {GPTEAM_EXAMPLE}

        RETURN THE JSON CONFIG AND ONLY THE JSON CONFIG
    """
    user_message = (
        f"Here are the logs: {logs}. Here is the original configuration: {config}"
    )
    updated_config = call_llm(system_message, user_message)
    checked_config = check_updated_config(fixes_to_apply, updated_config)
    new_config = cleanup_json(checked_config)
    new_config_lines = len(new_config.splitlines())
    config_lines = len(config.splitlines())
    print(f"config lines is {config_lines} and new_config_lines is {new_config_lines}")
    print("sucessfully called LLM for generate_updated_config", checked_config)
    return new_config


def check_updated_config(fixes_to_apply, config):
    print("calling LLM for check_updated_config...")
    print(f"here are the fixes to apply {str(fixes_to_apply)}")
    system_message = f"""
        You are a checker to make sure that ALL THE PROBLEMS THAT THE USER WANTED TO FIX HAS BEEN UPDATED AND WRITTEN ITO THE CONFIG. {GPTEAMS_DESCRIPTION}
        The user will present the fixes that they wanted to apply in an array form. They will also show the config. Your job is to make sure that the config has been properly updated to fix that change.

        ITERATE THROUGH ALL THE PROBLEMS THAT THE USER HAS AND CHECK TO MAKE SURE THEY ARE FIXED.
        IF IT IS NOT FIXED, EITHER ADD OR REMOVE SOME RELEVANT PART OF THE CONFIG TO ENSURE THAT IT IS FIXED, WHILE KEEPIGN THE OTHER PARTS OF THE CONFIG THE SAME.
        IF THERE ARE DIRECTIVES THAT ARE CONFLICTING TO EACHOTHER, PRIORITIZE WHAT IS IN THE FIXES LIST AND REMOVE THE PART OF THE CONFIG THAT DOES NOT RESPECT THE FIXES LIST.

        For example, if a problem is "Coach compromises practice schedule instead of maintaining authority and consistency.	", make sure to add that THE COACH CANNOT COMPROMISE in his directive, and remove anything in his directive that would suggest he would be willing to compromise.

        Do not add any new fields. Do not change the format of the config up. If you want to remove content of the field, still keep the field but just have it like this: "private_bio": ""
        Do not add ANY NEW ROOMS to the worlds. For the world, only modify the description
        Keep the SAME NUMBER OF AGENTS with the same names and everything. For the agents, only modify the directives or initial plan.
        Ensure that all these fields are filled out and follows this structure, like this example config {GPTEAM_EXAMPLE}

        If the solution includes adding an Overseeer or Moderator, you can add one with instructions below. ONLLY ADD AN OVERSEER OR MODEREATOR IF IT IS RECOMENDED IN THE FIXES. OTHRWISE, IGNORE THESE INSTRUCTIONS.
        {OVERSEER_INSTRUCTIONS}

        RETURN THE JSON CONFIG AND ONLY THE JSON CONFIG
    """
    user_message = f"Here are the logs: {str(fixes_to_apply)}. Here is the original configuration: {config}"
    new_config = call_llm(system_message, user_message)
    return new_config
