from langchain_core.tools import tool
from data.mock_db import MOCK_USER_DB, MOCK_TRANSACTION_DB

@tool
def check_user_balance(user_id:str):
    """
    Looks up user account information, status, and current balance using the User ID.
    Use this tool whenever a customer asks about their account details or account status.
    """
    user = MOCK_USER_DB.get(user_id)
    if user:
        return (
            f"--- Account Summary for {user['name']} ---\n"
            f"User ID: {user_id}\n"
            f"Status: {user['account_status']}\n"
            f"Current Balance: ${user['balance']:.2f}\n"
            f"Membership Tier: {user['tier']}"
        )
    else:
        return {"error": f"User ID {user_id} not found."}
    
# List of all tools available to our Account Specialist Agent
all_tools = [check_user_balance]