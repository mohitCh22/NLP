from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class SupportState(TypedDict):
    """
    The central state schema passed between all nodes in the support agent graph.
    """
    # 'add_messages' ensures conversation history accumulates rather than getting overwritten
    messages:Annotated[list, add_messages]

    # Internal routing & execution flags
    issue_category: str # "account", "refund", or "general"
    user_id: str           # User ID extracted or provided by the client
    refund_amount: float   # Prepared refund value for escalation
    refund_approved: bool  # Tracks whether a manager approved the refund
