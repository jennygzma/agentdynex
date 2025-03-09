from globals import call_llm


def generate_summary(logs):
    print("calling LLM for generate_summary...")
    example = """
    Simulation Summary:
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
    system_message = f"""
        We are running a multi-agent simulation on GPTeam. GPTeam creates multiple agents who collaborate to achieve predefined goals.
        GPTeam employs separate agents, each equipped with a memory, that interact with one another using communication as a tool.
        Agents move around the world and perform tasks in different locations, depending on what they are doing and where other agents are located.
        They can speak to each other and collaborate on tasks, working in parallel towards common goals.

        Given some logs of the simulation, get some key points and summary. Return only the necessary information and keep the words under 300 words.
        Here is an example of a summary: {example}
    """
    user_message = f"Here are the logs: {logs}"
    summary = call_llm(system_message, user_message, llm="openai")
    print("sucessfully called LLM for generate_summary", summary)
    return summary


# filler, this needs to be fixed
def generate_analysis(logs):
    print("calling LLM for generate_analysis...")
    example = """
    Simulation Summary:
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
    system_message = f"""
        We are running a multi-agent simulation on GPTeam. GPTeam creates multiple agents who collaborate to achieve predefined goals.
        GPTeam employs separate agents, each equipped with a memory, that interact with one another using communication as a tool.
        Agents move around the world and perform tasks in different locations, depending on what they are doing and where other agents are located.
        They can speak to each other and collaborate on tasks, working in parallel towards common goals.

        Given some logs of the simulation, get some key points and summary. Return only the necessary information and keep the words under 300 words.
        Here is an example of a summary: {example}
    """
    user_message = f"Here are the logs: {logs}"
    analysis = call_llm(system_message, user_message, llm="openai")
    print("sucessfully called LLM for generate_analysis", analysis)
    return analysis
