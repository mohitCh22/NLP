from state import SupportState

def route_triage(state:SupportState) -> str:
    """
    Router function that inspects the issue_category in the state and 
    returns a string label pointing to the next destination node in the graph.
    """
    category = state.get("issue_category", "general")

    if category == "account":
        return "account_specialist_agent"
    elif category == "refund":
        return "prepare_refund_node"
    else:
        return "general_support_node"