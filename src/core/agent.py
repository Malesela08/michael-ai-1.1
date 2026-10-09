import json
import ollama

from src.core.config import DEFAULT_MODEL

def read_system_status(component: str) -> str:
    """Retrieves status of a system component."""
    status_db = {
        "can_bus": "ONLINE - 0 dropped packets",
        "engine": "TEMP 92°C - Normal operating parameters",
        "perimeter": "ALERT - Unidentified movement detected on North Node"
    }
    return status_db.get(component.lower(), f"Unknown component: {component}")

def run_diagnostic_action(action_type: str) -> str:
    """Executes a diagnostic action on a system node."""
    return f"Action '{action_type}' executed successfully on local node."

tool_map = {
    "read_system_status": read_system_status,
    "run_diagnostic_action": run_diagnostic_action
}

def run_agent(user_prompt: str):
    messages = [
        {"role": "system", "content": "You are an autonomous AI Agent. Use your available tools to gather information and execute tasks before providing a final report."},
        {"role": "user", "content": user_prompt}
    ]

    print(f"\n[USER GOAL]: {user_prompt}\n" + "-"*50)

    while True:
        response = ollama.chat(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=[read_system_status, run_diagnostic_action]
        )
        
        messages.append(response.message)

        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = tool_call.function.arguments

                print(f"[AGENT TOOL CALL]: Invoking '{fn_name}' with args {fn_args}")

                if fn_name in tool_map:
                    tool_output = tool_map[fn_name](**fn_args)
                    print(f"[TOOL RESULT]: {tool_output}")

                    messages.append({
                        "role": "tool",
                        "tool_name": fn_name,
                        "content": str(tool_output)
                    })
        else:
            print(f"\n[AGENT FINAL ANSWER]:\n{response.message.content}")
            break

if __name__ == "__main__":
    run_agent("Check the status of the perimeter and run a reset action if needed.")
