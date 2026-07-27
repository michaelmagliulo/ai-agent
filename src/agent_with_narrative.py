import json
import os
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from openai import OpenAI


# =============================================================================
# DISPLAY HELPERS
# =============================================================================

def print_banner(title: str) -> None:
    """
    Print a large section heading.

    This does not affect the agent.
    It only makes the terminal output easier to follow.
    """
    print("\n")
    print("=" * 80)
    print(title.center(80))
    print("=" * 80)


def print_json(data: Any) -> None:
    """
    Pretty-print Python dictionaries and lists as formatted JSON.

    default=str prevents printing errors if an object contains a value
    that JSON does not normally understand, such as a datetime.
    """
    print(json.dumps(data, indent=4, default=str))


def print_conversation(input_items: list[Any]) -> None:
    """
    Show everything currently stored in the agent's conversation.

    Some items are ordinary dictionaries that we created.
    Other items are response objects returned by the OpenAI SDK.
    """

    print(f"\nThe conversation contains {len(input_items)} item(s):")

    for index, item in enumerate(input_items, start=1):
        print("\n" + "-" * 80)
        print(f"Conversation item {index}")
        print("-" * 80)

        # OpenAI SDK response objects are Pydantic models.
        # model_dump() converts them into ordinary Python dictionaries.
        if hasattr(item, "model_dump"):
            print_json(item.model_dump())
        else:
            print_json(item)


# =============================================================================
# LOAD CONFIGURATION
# =============================================================================

print_banner("STARTING THE PROGRAM")

print("\nStep 1: Loading variables from the .env file.")

# load_dotenv() searches for a .env file and loads its values
# into the program's environment.
load_dotenv()

print("Step 2: Looking for OPENAI_API_KEY.")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. "
        "Add it to your .env file before running the program."
    )

# Do not print the actual API key.
print("OPENAI_API_KEY was found.")

print("Step 3: Creating the OpenAI client.")

# The OpenAI client reads OPENAI_API_KEY from the environment.
client = OpenAI()

print("OpenAI client created successfully.")


# =============================================================================
# TOOL IMPLEMENTATION
# =============================================================================

def get_current_time(timezone: str) -> str:
    """
    Return the current time for an IANA timezone.

    Examples:
        America/New_York
        America/Los_Angeles
        Europe/London

    Important:
        This is an ordinary Python function.

        The model cannot execute this function directly.
        The model can only ask our Python program to execute it.
    """

    print_banner("PYTHON TOOL: GET CURRENT TIME")

    print("\nThe get_current_time() Python function has started.")
    print(f"Timezone received by the function: {timezone}")

    try:
        print("\nPython is creating a ZoneInfo object.")

        timezone_object = ZoneInfo(timezone)

        print("Python is reading the current time in that timezone.")

        current_time = datetime.now(timezone_object)

        print(f"Current datetime object: {current_time}")

        result = {
            "timezone": timezone,
            "datetime": current_time.isoformat(),
        }

        print("\nThe tool created this result:")
        print_json(result)

        print("\nThe result will be converted into a JSON string.")

        result_json = json.dumps(result)

        print("The get_current_time() tool has finished.")

        return result_json

    except Exception as exc:
        print("\nThe time tool encountered an error.")
        print(f"Python error: {exc}")

        error_result = {
            "error": f"Unable to read timezone: {exc}",
        }

        print("\nThe tool will return this error to the model:")
        print_json(error_result)

        return json.dumps(error_result)


# =============================================================================
# TOOL DEFINITIONS SHOWN TO THE MODEL
# =============================================================================

# This does not execute the function.
#
# It is a description of the function that is sent to the model.
# The description tells the model:
#
#   1. The name of the available tool
#   2. What the tool does
#   3. What arguments the tool requires
#
# The model uses this information to decide whether it wants Python
# to execute the tool.

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
                        "An IANA timezone such as America/New_York, "
                        "America/Los_Angeles, or Europe/London."
                    ),
                }
            },
            "required": ["timezone"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


# =============================================================================
# TOOL ROUTER
# =============================================================================

def execute_tool(tool_name: str, arguments: dict[str, Any]) -> str:
    """
    Route a model-requested tool call to the correct Python function.

    The model returns the name of the tool it wants to use.
    This router matches that name to an actual Python function.
    """

    print_banner("TOOL ROUTER")

    print("\nThe model requested a tool.")
    print(f"Requested tool name: {tool_name}")
    print("Arguments received by the router:")
    print_json(arguments)

    if tool_name == "get_current_time":
        print("\nA matching Python function was found.")
        print("The router is calling get_current_time().")

        return get_current_time(
            timezone=arguments["timezone"],
        )

    print("\nNo matching Python function was found.")

    return json.dumps(
        {
            "error": f"Unknown tool: {tool_name}",
        }
    )


# =============================================================================
# AGENT LOOP
# =============================================================================

def run_agent(user_message: str) -> str:
    """
    Run one complete agent session.

    The loop continues until one of two things happens:

        1. The model returns a final answer without requesting a tool.
        2. The maximum number of iterations is reached.

    Each pass through the loop is one API request.
    """

    print_banner("NEW AGENT RUN")

    print("\nThe user asked:")
    print(user_message)

    print("\nCreating the initial conversation history.")

    # The first item in the conversation is the user's message.
    input_items: list[Any] = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    # This is a safety limit.
    #
    # Without a limit, a badly behaving agent could continue calling tools
    # and making API requests indefinitely.
    max_iterations = 10

    print(f"Maximum permitted iterations: {max_iterations}")

    for iteration in range(max_iterations):
        print_banner(f"AGENT ITERATION {iteration + 1}")

        print_conversation(input_items)

        print_banner("CALLING THE OPENAI API")

        print(
            "\nThis is the point where our Python program sends the following "
            "information to the model:"
        )
        print("  1. The agent instructions")
        print("  2. The available tool descriptions")
        print("  3. The conversation so far")

        print("\nSending the request now...")

        # This is the only place in this program where we call OpenAI.
        #
        # The model receives the conversation and tool definitions.
        # It can either:
        #
        #   1. Return a final answer
        #   2. Request that Python execute a tool
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

        print("\nA response was received from OpenAI.")

        print_banner("RESPONSE SUMMARY")

        print(f"\nResponse ID: {response.id}")
        print(f"Final text currently available: {response.output_text!r}")
        print(f"Number of output items: {len(response.output)}")

        print("\nOutput item types:")

        for index, item in enumerate(response.output, start=1):
            print(f"  Item {index}: {item.type}")

        print_banner("RAW RESPONSE OUTPUT")

        print(
            "\nThe following output was returned by the model. "
            "This may contain messages, reasoning items, or function calls."
        )

        for index, item in enumerate(response.output, start=1):
            print("\n" + "-" * 80)
            print(f"Response output item {index}")
            print("-" * 80)

            if hasattr(item, "model_dump"):
                print_json(item.model_dump())
            else:
                print(item)

        print_banner("UPDATING CONVERSATION HISTORY")

        # Everything returned by the model must be preserved.
        #
        # This can include:
        #   - Assistant messages
        #   - Function calls
        #   - Other response items
        #
        # On the next iteration, the model needs this history so it knows
        # what it previously requested.
        input_items.extend(response.output)

        print(
            "\nThe model's output has been added to the conversation history."
        )

        print_banner("SEARCHING FOR TOOL CALLS")

        # Search all output items for items whose type is function_call.
        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        print(f"\nNumber of function calls found: {len(function_calls)}")

        # If the model did not request a function, it has finished.
        if not function_calls:
            print("\nNo tool calls were requested.")
            print("The model believes it has enough information to answer.")
            print("The agent loop is finished.")

            final_answer = response.output_text

            if not final_answer:
                return "The model finished without returning visible text."

            return final_answer

        print(
            "\nThe model requested one or more tools. "
            "Python will execute each request."
        )

        for tool_number, function_call in enumerate(
            function_calls,
            start=1,
        ):
            print_banner(
                f"PROCESSING TOOL CALL {tool_number} "
                f"OF {len(function_calls)}"
            )

            print(f"\nTool name: {function_call.name}")
            print(f"Tool call ID: {function_call.call_id}")
            print(f"Raw JSON arguments: {function_call.arguments}")

            try:
                print("\nConverting the JSON arguments into a Python dictionary.")

                arguments = json.loads(function_call.arguments)

                print("Converted Python dictionary:")
                print_json(arguments)

                print("\nPassing the request to the tool router.")

                result = execute_tool(
                    tool_name=function_call.name,
                    arguments=arguments,
                )

            except json.JSONDecodeError as exc:
                print("\nPython could not decode the tool arguments as JSON.")
                print(f"JSON error: {exc}")

                result = json.dumps(
                    {
                        "error": f"Invalid JSON tool arguments: {exc}",
                    }
                )

            except KeyError as exc:
                print("\nA required tool argument was missing.")
                print(f"Missing argument: {exc}")

                result = json.dumps(
                    {
                        "error": f"Missing required tool argument: {exc}",
                    }
                )

            except TypeError as exc:
                print("\nThe tool arguments had an invalid Python type.")
                print(f"Type error: {exc}")

                result = json.dumps(
                    {
                        "error": f"Invalid tool argument type: {exc}",
                    }
                )

            except Exception as exc:
                print("\nAn unexpected error occurred while executing the tool.")
                print(f"Unexpected error: {exc}")

                result = json.dumps(
                    {
                        "error": f"Unexpected tool error: {exc}",
                    }
                )

            print_banner("TOOL EXECUTION COMPLETE")

            print("\nThe Python tool returned this JSON string:")
            print(result)

            print_banner("RETURNING TOOL OUTPUT TO THE MODEL")

            print(
                "\nThe tool result does not go directly to the user."
            )
            print(
                "It is added to the conversation and sent back to the model."
            )
            print(
                "The call_id connects this result to the model's original "
                "tool request."
            )

            tool_output_item = {
                "type": "function_call_output",
                "call_id": function_call.call_id,
                "output": result,
            }

            print("\nThe following conversation item will be added:")
            print_json(tool_output_item)

            input_items.append(tool_output_item)

        print_banner("ITERATION COMPLETE")

        print(
            "\nAll requested tools have been executed and their results "
            "have been added to the conversation."
        )
        print(
            "The loop will now make another API request so the model can "
            "inspect the results."
        )
        print(
            "The model may request another tool or return its final answer."
        )

    # The loop only reaches this line if it uses every permitted iteration.
    raise RuntimeError(
        f"Agent exceeded the maximum of {max_iterations} iterations."
    )


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

def main() -> None:
    """
    Run the terminal interface.

    This outer loop lets the user submit multiple independent questions.
    Each question starts a new run_agent() session.
    """

    print_banner("SIMPLE AI AGENT")

    print("\nThe agent is ready.")
    print("Type 'quit' or 'exit' to stop the program.")

    while True:
        user_message = input("\nYou: ").strip()

        # Ignore an empty input and ask again.
        if not user_message:
            print("No message was entered.")
            continue

        # End the program when the user types quit or exit.
        if user_message.lower() in {"quit", "exit"}:
            print("\nClosing the agent.")
            break

        try:
            answer = run_agent(user_message)

            print_banner("FINAL ANSWER")
            print(f"\nAgent: {answer}")

        except KeyboardInterrupt:
            print("\n\nThe current operation was interrupted by the user.")

        except Exception as exc:
            print_banner("ERROR")
            print(f"\nThe agent encountered an error: {exc}")


# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================

# Python sets __name__ to "__main__" when this file is run directly:
#
#     python agent.py
#
# This prevents main() from running automatically if this file is imported
# into another Python file.
if __name__ == "__main__":
    main()