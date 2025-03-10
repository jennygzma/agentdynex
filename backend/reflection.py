from config_generation import cleanup_json
from globals import call_llm

GPTEAMS_DESCRIPTION = """
We are running a multi-agent simulation on GPTeam. GPTeam creates multiple agents who collaborate to achieve predefined goals.
GPTeam employs separate agents, each equipped with a memory, that interact with one another using communication as a tool.
Agents move around the world and perform tasks in different locations, depending on what they are doing and where other agents are located.
They can speak to each other and collaborate on tasks, working in parallel towards common goals.
"""


class RubricInstance:
    def __init__(
        self,
        category,
        rubric_type,
        description,
        pgg_example=None,
        classroom_example=None,
    ):
        self.category = category
        self.rubric_type = rubric_type
        self.description = description
        self.pgg_example = pgg_example
        self.classroom_example = classroom_example

    PGG_DESCRIPTION = """
        If the simulation is about simulating the public goods game with three players and a mediator
        contributing to a common pot to see if people will cooporate for the benefit of the group, the example fix is:
    """

    CLASSROOM_SIMULATION = """
        If the simulation is about simulating how different students will respond to a late policy made by a professor,
        by checking when students will return assignments, the example is:
    """

    def get_string(self):
        result = f"Category: {self.category}\nModification Type: {self.rubric_type}\nDescription: {self.description}\n"
        if self.pgg_example:
            result += self.PGG_DESCRIPTION + self.pgg_example + "\n"
        if self.classroom_example:
            result += self.CLASSROOM_SIMULATION + self.classroom_example + "\n"
        return result


RUBRIC = [
    # Task Structure Optimization
    RubricInstance(
        category="Task Structure Optimization",
        rubric_type="Reduce complexity",
        description="Simplify the simulation by focusing on a single core task",
        pgg_example=None,
        classroom_example="Changed from five assignments to one assignment",
    ),
    RubricInstance(
        category="Task Structure Optimization",
        rubric_type="Clarify task instructions",
        description="Ensure clear explicit task details to remove ambiguity",
        pgg_example=None,
        classroom_example="Clearly stated 500-word essay topic & deadline",
    ),
    # Stop Condition & Completion Criteria
    RubricInstance(
        category="Stop Condition & Completion Criteria",
        rubric_type="Prevent premature exits",
        description="Stop condition should depend on actual task completion",
        pgg_example=None,
        classroom_example="Required all students to submit before ending",
    ),
    RubricInstance(
        category="Stop Condition & Completion Criteria",
        rubric_type="Use dependency-based stop conditions",
        description="Ensure stop conditions track key dependencies to avoid early termination",
        pgg_example=None,
        classroom_example="Simulation now waits for all students’ work to be acknowledged",
    ),
    # Directive & Agent Behavior Optimization
    RubricInstance(
        category="Directive & Agent Behavior Optimization",
        rubric_type="Prevent premature actions",
        description="Ensure agents wait for key information before acting",
        pgg_example=None,
        classroom_example="Students wait for assignment details before starting",
    ),
    RubricInstance(
        category="Directive & Agent Behavior Optimization",
        rubric_type="Enforce mandatory actions",
        description="Make sure critical steps like submission & acknowledgment are required",
        pgg_example=None,
        classroom_example="Students must verbally declare submission and receive acknowledgment before leaving",
    ),
    RubricInstance(
        category="Directive & Agent Behavior Optimization",
        rubric_type="Reduce redundant waiting",
        description="Avoid agents getting stuck waiting for unimportant responses",
        pgg_example=None,
        classroom_example="Students no longer wait for greetings before working",
    ),
    # Reducing Waiting Bottlenecks & Deadlocks
    RubricInstance(
        category="Reducing Waiting Bottlenecks & Deadlocks",
        rubric_type="Improve efficiency of response processing",
        description="Optimize how responses are handled to speed up task progression",
        pgg_example=None,
        classroom_example="Professor acknowledges multiple submissions efficiently",
    ),
    RubricInstance(
        category="Reducing Waiting Bottlenecks & Deadlocks",
        rubric_type="Allow parallel execution when possible",
        description="Reduce over-reliance on strict sequential actions",
        pgg_example=None,
        classroom_example="Students can start working as soon as they get assignment details",
    ),
    # Action Validation & Progress Tracking
    RubricInstance(
        category="Action Validation & Progress Tracking",
        rubric_type="Track task completion effectively",
        description="Ensure simulation can verify when an action is fully completed",
        pgg_example=None,
        classroom_example="Students must verbally confirm submission",
    ),
    RubricInstance(
        category="Action Validation & Progress Tracking",
        rubric_type="Define completion criteria properly",
        description="Clearly define what counts as 'done' to prevent ambiguity",
        pgg_example=None,
        classroom_example="Professor acknowledgment step ensures completion",
    ),
    # Handling Stalled Simulations Due to Missing Triggers
    RubricInstance(
        category="Handling Stalled Simulations Due to Missing Triggers",
        rubric_type="Auto-recover from missing triggers",
        description="If agents wait too long for an event that should have already occurred (e.g., round start), allow them to prompt the proper agent (Mediator) or retry the trigger.",
        classroom_example=None,
        pgg_example="Agents request a round announcement if they don’t receive one within a set time.",
    ),
    # Ensuring Critical Announcements Are Acknowledged
    RubricInstance(
        category="Ensuring Critical Announcements Are Acknowledged",
        rubric_type="Verify announcement reception",
        description="Ensure agents explicitly confirm hearing critical announcements before proceeding.",
        classroom_example=None,
        pgg_example="Agents must acknowledge the Mediator’s 'Game Start' announcement before they can take further action.",
    ),
    # Handling Calculation & Decision Failures
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Auto-recover from missing computation steps",
        description="If an agent encounters an error while computing a required value, provide a fallback mechanism where the agent retries the computation with stored values.",
        pgg_example="If the Mediator fails to compute the public goods distribution, they must follow a predefined fallback calculation.",
        classroom_example=None,
    ),
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Explicitly define required calculations in directives",
        description="Ensure that all necessary computations are verified before progressing.",
        pgg_example='Mediator directive explicitly states: "Retrieve total contribution and verify it before proceeding."',
        classroom_example=None,
    ),
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Verify computation success before proceeding",
        description="Require agents to confirm that a calculation was successfully performed before moving to the next step.",
        pgg_example="If an agent submits a tax contribution but doesn’t see the correct update, they request recalculation before proceeding.",
        classroom_example=None,
    ),
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Fallback decision-making process",
        description="If an agent asks how to perform a task they were explicitly told to do, have them re-read their own directives instead of requesting human input.",
        pgg_example="The Mediator forgets how to calculate the public goods total, they must first re-read their directives before asking for external formal guidance.",
        classroom_example=None,
    ),
    RubricInstance(
        category="Handling Calculation & Decision Failures",
        rubric_type="Prevent reliance on external guidance",
        description="Ensure agents do not request external help and instead rely on predefined fallback mechanisms.",
        pgg_example="If students forget an issue when calculating the public goods total, they must follow a predefined retry process instead of asking for direct human intervention.",
        classroom_example=None,
    ),
    # New Additions to Improve Debugging Efficiency
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Implement structured logging",
        description="Ensure all key simulation events are recorded with timestamps and categorized.",
        pgg_example="The Mediator logs when each round starts, when offers are submitted, and when decisions are made.",
        classroom_example=None,
    ),
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Add failsafe for incomplete rounds",
        description="Ensure the round either completes successfully or resets if a critical failure occurs.",
        pgg_example="If neither agent submits an offer or response, the round resets with a default decision.",
        classroom_example=None,
    ),
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Synchronization checks",
        description="Ensure all agents wait for appropriate conditions before proceeding.",
        pgg_example="The Proposer cannot submit an offer before the Responder arrives.",
        classroom_example=None,
    ),
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Granular timeout handling",
        description="Differentiate between soft timeouts (warnings) and hard timeouts (default actions).",
        pgg_example="Agents receive a warning before a default action is applied.",
        classroom_example=None,
    ),
    RubricInstance(
        category="New Additions to Improve Debugging Efficiency",
        rubric_type="Adjustable simulation parameters",
        description="Allow real-time modifications to timeout periods and failure recovery strategies.",
        pgg_example="The Mediator can dynamically adjust timeout limits based on observed simulation behavior.",
        classroom_example=None,
    ),
]

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
    summary = call_llm(system_message, user_message, llm="openai")
    print("sucessfully called LLM for generate_summary", summary)
    return summary


# filler, this needs to be fixed
def generate_analysis_and_config(summary, matrix, config):
    print("calling LLM for generate_analysis_and_config...")

    def generate_rubric_text(rubric_instances):
        result = ""

        for instance in rubric_instances:
            result += f"Category: {instance.category}\n"
            result += f"Modification Type: {instance.rubric_type}\n"
            result += f"Description: {instance.description}\n"

            if instance.pgg_example:
                result += (
                    RubricInstance.PGG_DESCRIPTION.strip()
                    + " "
                    + instance.pgg_example
                    + "\n"
                )

            if instance.classroom_example:
                result += (
                    RubricInstance.CLASSROOM_SIMULATION.strip()
                    + " "
                    + instance.classroom_example
                    + "\n"
                )

            result += "\n"  # Separate each rubric instance for readability

        return result.strip()

    rubric = generate_rubric_text(RUBRIC)

    system_message = f"""
        {GPTEAMS_DESCRIPTION}
        Given the summary of the simulation, the original config, and the design matrix that the config is supposed to follow, explain what went wrong in the simulation within 300 words.
        Specifically, point to what part of the rubric the existing example violated.
        Then fix the configiguration.
        Specifically, return the analysis of what went wrong (within 300 words) and the ENTIRE CONFIGURATION (DO NOT RETURN ONLY PART OF THE CONFIGURATION).

        Here is the rubric to help guide the analysis: {rubric}
    """
    user_message = f"Here is the matrix: {matrix}. Here is the summary: {summary}. Here is the original configuration: {config}"
    analysis_and_config = call_llm(system_message, user_message, llm="openai")
    config = cleanup_json(analysis_and_config)
    analysis = get_analysis(analysis_and_config)
    print(
        "sucessfully called LLM for generate_analysis_and_config", analysis_and_config
    )
    return analysis, config


def get_analysis(analysis_and_config):
    print("calling LLM for get_analysis...")
    system_message = """
        Given an analysis and a config json, return only the analysis part that makes sense. Do not add any words or change anything.
    """
    user_message = f"Here is the input: {analysis_and_config}."
    analysis = call_llm(system_message, user_message, llm="openai")
    return analysis
