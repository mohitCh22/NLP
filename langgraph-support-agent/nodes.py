from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from state import SupportState
from tools import all_tools

from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the OpenAI LLM with the API key from the .env file
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    # model_name="gpt-4o-mini",
    temperature=0
)

# Bind our tools to the model for the Account Specialist Agent
llm_with_tools = llm.bind_tools(all_tools)

# =====================================================================
# 1. TRIAGE NODE (Intent Categorization)
# =====================================================================
def traiage_node(state: SupportState) -> dict:
    """
    Analyzes the user's latest message and identify the intent.
    This acts as a receptionist / front desk agent.
    """
    # Extract the latest user message from the state
    latest_message = state["messages"][-1].content.lower()

    if "refund" in latest_message or "money back" in latest_message or "return" in latest_message or "charge" in latest_message:
        category = "refund"

    elif "account" in latest_message or "balance" in latest_message or "status" in latest_message:
        category = "account"

    else:
        category = "general"

    print(f"[TRIAGE NODE] Categorized user intent as: {category}")
    return {"issue_category": category}

# =====================================================================
# 2. GENERAL SUPPORT NODE
# =====================================================================
def general_support_node(state: SupportState) -> dict:
    """
    Handles general customer support queries that do not require tools or database access.
    """
    print("--- [General Support Node] Generating response ---")

    system_message = SystemMessage(
        content="You are a helpful customer support agent. Provide clear and concise answers to user queries."
    )
    response = llm.invoke([system_message] + state["messages"])
    return {"messages": [response]}

# =====================================================================
# 3. ACCOUNT SPECIALIST NODE
# =====================================================================
def account_specialist_agent(state:SupportState) -> dict:
    """
    Handles user account lookups. Has access to the check_user_balance tool for retrieving account information.
    """
    print("--- [Account Specialist Node] Processing request ---")
    system_message = SystemMessage(
        content="You are an Account Specialist Agent. Use the provided tools to assist users with account inquiries."
    )
    response = llm_with_tools.invoke([system_message] + state["messages"])
    return {"messages": [response]}

# =====================================================================
# 4. REFUND PREPARATION NODE (Human-in-the-Loop Setup)
# =====================================================================
def prepare_refund_node(state:SupportState) -> dict:
    """
    Prepares a refund for the user. This node simulates a human-in-the-loop process where a manager approves the refund.
    """
    print("--- [Refund Preparation Node] Setting up refund parameters ---")
    # Simulate refund preparation logic
    refund_amount = 50.00  # Example fixed refund amount for demonstration
    msg = AIMessage(
        content=f"Refund of ${refund_amount:.2f} has been prepared for user {state['user_id']}. Awaiting manager approval."
    )
    return {
        "refund_amount": refund_amount,
        "messages": [msg]
    }

# =====================================================================
# 5. PROCESS REFUND NODE (Runs AFTER Human Approval)
# =====================================================================
def process_refund_node(state:SupportState) -> dict:
    """
    Processes the refund after manager approval. This node simulates the final step in the refund workflow.
    """
    print("--- [Process Refund Node] Finalizing refund ---")
    amount = state.get("refund_amount", 0.0)
    msg = AIMessage(
        content=f"Refund of ${amount:.2f} has been successfully processed for user {state['user_id']}."
    )
    return {
        "refund_approved": True,
        "messages": [msg]
        }