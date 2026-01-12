"""
Widget Definitions for Banking MCP Server
Contains all widget data structures
"""

WIDGETS = {
    "account_summary": {
        "name": "account_summary",
        "description": "Displays account summary with balance, account number, and recent transactions",
        "widget_type": "account_summary",
        "data": {
            "title": "Account Summary",
            "accountNumber": "****1234",
            "accountType": "Checking",
            "balance": 12543.67,
            "availableBalance": 12543.67,
            "currency": "USD",
            "recentTransactions": [
                {"date": "2025-01-10", "description": "Salary Deposit", "amount": 5000.00, "type": "credit"},
                {"date": "2025-01-08", "description": "Grocery Store", "amount": -125.43, "type": "debit"},
                {"date": "2025-01-05", "description": "Electric Bill", "amount": -89.50, "type": "debit"},
            ]
        }
    },
    "deposit": {
        "name": "deposit",
        "description": "Displays deposit form for transferring money into the account",
        "widget_type": "deposit",
        "data": {
            "title": "Make a Deposit",
            "description": "Transfer money into your account",
            "fields": [
                {
                    "name": "amount",
                    "label": "Deposit Amount",
                    "type": "number",
                    "placeholder": "0.00",
                    "required": True,
                    "min": 0.01,
                    "step": 0.01
                },
                {
                    "name": "source",
                    "label": "Source Account",
                    "type": "select",
                    "options": [
                        {"value": "external", "label": "External Bank Account"},
                        {"value": "check", "label": "Check Deposit"},
                        {"value": "cash", "label": "Cash Deposit"}
                    ],
                    "required": True
                },
                {
                    "name": "memo",
                    "label": "Memo (Optional)",
                    "type": "text",
                    "placeholder": "Add a note about this deposit",
                    "required": False
                }
            ],
            "submitLabel": "Complete Deposit"
        }
    },
    "withdrawal": {
        "name": "withdrawal",
        "description": "Displays withdrawal form for transferring money out of the account",
        "widget_type": "withdrawal",
        "data": {
            "title": "Make a Withdrawal",
            "description": "Transfer money from your account",
            "fields": [
                {
                    "name": "amount",
                    "label": "Withdrawal Amount",
                    "type": "number",
                    "placeholder": "0.00",
                    "required": True,
                    "min": 0.01,
                    "max": 10000.00,
                    "step": 0.01
                },
                {
                    "name": "destination",
                    "label": "Destination",
                    "type": "select",
                    "options": [
                        {"value": "external", "label": "External Bank Account"},
                        {"value": "atm", "label": "ATM Withdrawal"},
                        {"value": "check", "label": "Check"}
                    ],
                    "required": True
                },
                {
                    "name": "memo",
                    "label": "Memo (Optional)",
                    "type": "text",
                    "placeholder": "Add a note about this withdrawal",
                    "required": False
                }
            ],
            "submitLabel": "Complete Withdrawal"
        }
    },
    "general": {
        "name": "general",
        "description": "General purpose widget for common questions and information display",
        "widget_type": "card",
        "data": {
            "title": "Banking Assistant",
            "content": "I can help you with:\n\n• View account summary\n• Make deposits\n• Process withdrawals\n• Answer banking questions\n\nWhat would you like to do?",
            "actions": [
                {
                    "label": "View Account",
                    "primary": True,
                    "data": {"action": "account_summary"}
                },
                {
                    "label": "Make Deposit",
                    "primary": False,
                    "data": {"action": "deposit"}
                },
                {
                    "label": "Make Withdrawal",
                    "primary": False,
                    "data": {"action": "withdrawal"}
                }
            ]
        }
    }
}

