import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is missing from the environment.")

client = OpenAI()


# ---------------------------------------------------------
# Tool implementation
# ---------------------------------------------------------

def get_current_time(timezone: str) -> str:
    """
    Return the current time for an IANA timezone.

    Examples:
        America/New_York
        America/Los_Angeles
        Europe/London
    """
    try:
        current_time = datetime.now(ZoneInfo(timezone))

        return json.dumps(
            {
                "timezone": timezone,
                "datetime": current_time.isoformat(),
            }
        )

    except Exception as exc:
        return json.dumps(
            {
                "error": f"Unable to read timezone: {exc}",
            }
        )


# ---------------------------------------------------------
# Tool descriptions shown to the model
# ---------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current date and time in a specified timezone.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": (
                        "An IANA timezone such as America/New_York "
                        "or Europe/London."
                    ),
                }
            },
            "required": ["timezone"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


# ---------------------------------------------------------
# Tool router
# ---------------------------------------------------------

def execute_tool(tool_name: str, arguments: dict) -> str:
    """
    Route a model-requested tool call to the correct Python function.
    """

    if tool_name == "get_current_time":
        return get_current_time(
            timezone=arguments["timezone"],
        )

    return json.dumps(
        {
            "error": f"Unknown tool: {tool_name}",
        }
    )


# ---------------------------------------------------------
# Agent loop
# ---------------------------------------------------------

def run_agent(user_message: str) -> str:
    """
    Send the user's request to the model and continue processing
    tool calls until the model produces a final response.
    """

    input_items = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    max_iterations = 10

    for iteration in range(max_iterations):
        print(f"\nAgent iteration: {iteration + 1}")

        response = client.responses.create(
            model="gpt-5.5",
            instructions=(
                "You are a helpful AI agent. "
                "Use tools when they are needed. "
                "Do not claim to know the current time without using the tool."
            ),
            tools=TOOLS,
            input=input_items,
        )

        # Preserve everything the model returned.
        input_items.extend(response.output)

        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # No function calls means the model has finished.
        if not function_calls:
            return response.output_text

        # Execute each requested function.
        for function_call in function_calls:
            print(f"Tool requested: {function_call.name}")
            print(f"Arguments: {function_call.arguments}")

            try:
                arguments = json.loads(function_call.arguments)

                result = execute_tool(
                    tool_name=function_call.name,
                    arguments=arguments,
                )

            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                result = json.dumps(
                    {
                        "error": f"Invalid tool arguments: {exc}",
                    }
                )

            print(f"Tool result: {result}")

            # Return the result to the model.
            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": result,
                }
            )

    raise RuntimeError(
        f"Agent exceeded the maximum of {max_iterations} iterations."
    )


# ---------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------

def main() -> None:
    print("Simple AI Agent")
    print("Type 'quit' to exit.")

    while True:
        user_message = input("\nYou: ").strip()

        if not user_message:
            continue

        if user_message.lower() in {"quit", "exit"}:
            break

        try:
            answer = run_agent(user_message)
            print(f"\nAgent: {answer}")

        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    main()