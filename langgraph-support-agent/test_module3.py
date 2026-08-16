# test_module3.py

from langchain_core.messages import HumanMessage
from graph import base_app

if __name__ == "__main__":
    print("=== TEST 1: General Query Route ===")
    query1 = {"messages": [HumanMessage(content="What are your support operating hours?")], "user_id": "USR_101"}
    for event in base_app.stream(query1):
        for node, output in event.items():
            print(f"-> Node Executed: [{node}]")

    print("\n" + "="*50 + "\n")

    print("=== TEST 2: Account Tool Call Route ===")
    query2 = {"messages": [HumanMessage(content="Check my account balance please. ID is USR_101")], "user_id": "USR_101"}
    for event in base_app.stream(query2):
        for node, output in event.items():
            print(f"-> Node Executed: [{node}]")
            if "messages" in output:
                latest = output["messages"][-1]
                if hasattr(latest, "tool_calls") and latest.tool_calls:
                    print(f"   [Tool Call Triggered]: {latest.tool_calls[0]['name']}")
                else:
                    print(f"   [Response Snippet]: {latest.content[:80]}...")