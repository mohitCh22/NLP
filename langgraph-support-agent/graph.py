from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from state import SupportState
from edges import route_triage
from tools import all_tools
from nodes import (
    general_support_node,
    account_specialist_agent,
    traiage_node,
    prepare_refund_node,
    process_refund_node
)

# 1. INITIALIZE THE GRAPH BUILDER WITH STATE SCHEMA
builder = StateGraph(SupportState)

# 2. DEFINE NODES
builder.add_node("triage_node", traiage_node)
builder.add_node("general_support_node", general_support_node)
builder.add_node("account_specialist_agent", account_specialist_agent)
builder.add_node("prepare_refund_node", prepare_refund_node)
builder.add_node("process_refund_node", process_refund_node)
builder.add_node("tools",ToolNode(all_tools))  # Prebuilt tool execution node

# 3. CONNECT NODES WITH EDGES
builder.add_edge(START, "triage_node")
builder.add_conditional_edges(
    "triage_node",
    route_triage,
    {
        "general_support_node": "general_support_node",
        "account_specialist_agent": "account_specialist_agent",
        "prepare_refund_node": "prepare_refund_node"
    }

)

# 4. ADD STANDARD COMPLETION PATHS

builder.add_edge("general_support_node", END)
builder.add_edge("prepare_refund_node", "process_refund_node")
builder.add_edge("process_refund_node", END)

# 5. ADD REACT TOOL LOOP FOR ACCOUNT AGENT
builder.add_conditional_edges(
    "account_specialist_agent",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END
    }
)
builder.add_edge("tools","account_specialist_agent")  # Loop back to account agent after tool execution 

# 6. COMPILE UNCHECKPOINTED GRAPH (For Basic Routing Testing)
base_app = builder.compile()