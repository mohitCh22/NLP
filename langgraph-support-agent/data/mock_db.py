# data/mock_db.py

"""
Mock User Database simulating an internal CRM/Database system.
This serves as our backend source of truth for user accounts and transactions.
"""

MOCK_USER_DB = {
    "USR_101": {
        "name": "Mohit Chimankar",
        "email": "mohit@example.com",
        "balance": 1250.00,
        "account_status": "Active",
        "tier": "Premium"
    },
    "USR_202": {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "balance": 0.00,
        "account_status": "Suspended",
        "tier": "Standard"
    }
}

MOCK_TRANSACTION_DB = {
    "TX_901": {
        "user_id": "USR_101",
        "amount": 50.00,
        "status": "Completed",
        "item": "Monthly Subscription"
    }
}