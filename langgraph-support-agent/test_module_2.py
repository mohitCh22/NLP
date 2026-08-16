from langchain_core.messages import HumanMessage
from nodes import traiage_node, prepare_refund_node

if __name__ == "__main__":
    # Simulate a user message
    user_message = HumanMessage(content="I want to return my recent purchase and get a refund.")

    # Initialize the state with the user's message
    state = {
        "messages": [user_message],
        "issue_category": "",
        "user_id": "user_123",
        "refund_amount": 0.0,
        "refund_approved": False,
    }

    # Run the triage node to categorize the issue
    triage_result = traiage_node(state)
    state.update(triage_result)

    # If the issue is categorized as a refund, prepare the refund
    if state["issue_category"] == "refund":
        refund_result = prepare_refund_node(state)
        state.update(refund_result)

    # Print the final state after processing
    print("Final State:", state)