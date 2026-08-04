#%%
import json
import os
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from openai import OpenAI


# =============================================================================
# DEBUG SETTING
# =============================================================================

# True:
#   Display detailed information about API calls, conversation history,
#   tool requests, tool execution, and agent iterations.
#
# False:
#   Display only the normal command-line interface and final answers.
DEBUG = True


# =============================================================================
# DEBUG DISPLAY HELPERS
# =============================================================================

def debug_print(*values: Any) -> None:
    """
    Print values only when DEBUG is enabled.

    This replaces ordinary print() calls used for diagnostic information.
    """
    if DEBUG:
        print(*values)


def debug_banner(title: str) -> None:
    """
    Print a large section heading only when DEBUG is enabled.
    """
    if not DEBUG:
        return

    print("\n")
    print("=" * 80)
    print(title.center(80))
    print("=" * 80)


def debug_json(data: Any) -> None:
    """
    Pretty-print data as JSON only when DEBUG is enabled.

    default=str prevents errors for values that JSON does not normally
    understand, such as datetime objects.
    """
    if DEBUG:
        print(json.dumps(data, indent=4, default=str))


def debug_conversation(input_items: list[Any]) -> None:
    """
    Display the complete agent conversation only when DEBUG is enabled.

    Some conversation items are ordinary dictionaries.
    Others are OpenAI SDK objects that provide model_dump().
    """
    if not DEBUG:
        return

    print(f"\nThe conversation contains {len(input_items)} item(s):")

    for index, item in enumerate(input_items, start=1):
        print("\n" + "-" * 80)
        print(f"Conversation item {index}")
        print("-" * 80)

        if hasattr(item, "model_dump"):
            debug_json(item.model_dump())
        else:
            debug_json(item)


# =============================================================================
# LOAD CONFIGURATION
# =============================================================================

debug_banner("STARTING THE PROGRAM")

debug_print("\nStep 1: Loading variables from the .env file.")

# Load variables from the local .env file into the environment.
load_dotenv()

debug_print("Step 2: Looking for OPENAI_API_KEY.")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. "
        "Add it to your .env file before running the program."
    )

# Never print the actual API key.
debug_print("OPENAI_API_KEY was found.")

debug_print("Step 3: Creating the OpenAI client.")

# OpenAI() automatically reads OPENAI_API_KEY from the environment.
client = OpenAI()

debug_print("OpenAI client created successfully.")


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

    This is an ordinary Python function.

    The model cannot execute it directly. The model can only ask our
    Python program to execute it.
    """

    debug_banner("PYTHON TOOL: GET CURRENT TIME")

    debug_print("\nThe get_current_time() Python function has started.")
    debug_print(f"Timezone received by the function: {timezone}")

    try:
        debug_print("\nPython is creating a ZoneInfo object.")

        timezone_object = ZoneInfo(timezone)

        debug_print("Python is reading the current time in that timezone.")

        current_time = datetime.now(timezone_object)

        debug_print(f"Current datetime object: {current_time}")

        result = {
            "timezone": timezone,
            "datetime": current_time.isoformat(),
        }

        debug_print("\nThe tool created this result:")
        debug_json(result)

        debug_print("\nThe result will be converted into a JSON string.")

        result_json = json.dumps(result)

        debug_print("The get_current_time() tool has finished.")

        return result_json

    except Exception as exc:
        debug_print("\nThe time tool encountered an error.")
        debug_print(f"Python error: {exc}")

        error_result = {
            "error": f"Unable to read timezone: {exc}",
        }

        debug_print("\nThe tool will return this error to the model:")
        debug_json(error_result)

        return json.dumps(error_result)


# =============================================================================
# TOOL DEFINITIONS SHOWN TO THE MODEL
# =============================================================================

# This does not execute the tool.
#
# It describes the tool to the model:
#
#   1. The tool's name
#   2. What the tool does
#   3. What arguments it accepts
#   4. Which arguments are required
#
# The model uses this description to decide whether it should request
# that Python execute the tool.

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

def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> str:
    """
    Route a model-requested tool call to the correct Python function.

    The model supplies a tool name. This router matches that name to an
    actual Python function.
    """

    debug_banner("TOOL ROUTER")

    debug_print("\nThe model requested a tool.")
    debug_print(f"Requested tool name: {tool_name}")
    debug_print("Arguments received by the router:")
    debug_json(arguments)

    if tool_name == "get_current_time":
        debug_print("\nA matching Python function was found.")
        debug_print("The router is calling get_current_time().")

        return get_current_time(
            timezone=arguments["timezone"],
        )

    debug_print("\nNo matching Python function was found.")

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

    The loop continues until:

        1. The model returns a final answer without requesting a tool, or
        2. The maximum number of iterations is reached.

    Each iteration can make one API request.
    """

    debug_banner("NEW AGENT RUN")

    debug_print("\nThe user asked:")
    debug_print(user_message)

    debug_print("\nCreating the initial conversation history.")

    input_items: list[Any] = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    # This prevents an accidental infinite agent loop.
    max_iterations = 10

    debug_print(f"Maximum permitted iterations: {max_iterations}")

    for iteration in range(max_iterations):
        debug_banner(f"AGENT ITERATION {iteration + 1}")

        debug_conversation(input_items)

        debug_banner("CALLING THE OPENAI API")

        debug_print(
            "\nPython is sending the following information to the model:"
        )
        debug_print("  1. The agent instructions")
        debug_print("  2. The available tool descriptions")
        debug_print("  3. The conversation so far")
        debug_print("\nSending the request now...")

        # This is where the program communicates with OpenAI.
        #
        # The model can:
        #
        #   1. Return a final answer
        #   2. Request one or more tools
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

        debug_print("\nA response was received from OpenAI.")

        debug_banner("RESPONSE SUMMARY")

        debug_print(f"\nResponse ID: {response.id}")
        debug_print(
            f"Final text currently available: {response.output_text!r}"
        )
        debug_print(f"Number of output items: {len(response.output)}")

        debug_print("\nOutput item types:")

        for index, item in enumerate(response.output, start=1):
            debug_print(f"  Item {index}: {item.type}")

        debug_banner("RAW RESPONSE OUTPUT")

        debug_print(
            "\nThe model returned the following output items."
        )

        for index, item in enumerate(response.output, start=1):
            if DEBUG:
                print("\n" + "-" * 80)
                print(f"Response output item {index}")
                print("-" * 80)

            if hasattr(item, "model_dump"):
                debug_json(item.model_dump())
            else:
                debug_print(item)

        debug_banner("UPDATING CONVERSATION HISTORY")

        # Preserve everything returned by the model.
        #
        # The next request needs this history so the model remembers what
        # it previously said or requested.
        input_items.extend(response.output)

        debug_print(
            "\nThe model's output has been added to the conversation history."
        )

        debug_banner("SEARCHING FOR TOOL CALLS")

        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        debug_print(
            f"\nNumber of function calls found: {len(function_calls)}"
        )

        # No tool call means the model has finished.
        if not function_calls:
            debug_print("\nNo tool calls were requested.")
            debug_print(
                "The model believes it has enough information to answer."
            )
            debug_print("The agent loop is finished.")

            final_answer = response.output_text

            if not final_answer:
                return "The model finished without returning visible text."

            return final_answer

        debug_print(
            "\nThe model requested one or more tools. "
            "Python will execute each request."
        )

        for tool_number, function_call in enumerate(
            function_calls,
            start=1,
        ):
            debug_banner(
                f"PROCESSING TOOL CALL {tool_number} "
                f"OF {len(function_calls)}"
            )

            debug_print(f"\nTool name: {function_call.name}")
            debug_print(f"Tool call ID: {function_call.call_id}")
            debug_print(
                f"Raw JSON arguments: {function_call.arguments}"
            )

            try:
                debug_print(
                    "\nConverting the JSON arguments into a Python dictionary."
                )

                arguments = json.loads(function_call.arguments)

                debug_print("Converted Python dictionary:")
                debug_json(arguments)

                debug_print("\nPassing the request to the tool router.")

                result = execute_tool(
                    tool_name=function_call.name,
                    arguments=arguments,
                )

            except json.JSONDecodeError as exc:
                debug_print(
                    "\nPython could not decode the tool arguments as JSON."
                )
                debug_print(f"JSON error: {exc}")

                result = json.dumps(
                    {
                        "error": f"Invalid JSON tool arguments: {exc}",
                    }
                )

            except KeyError as exc:
                debug_print("\nA required tool argument was missing.")
                debug_print(f"Missing argument: {exc}")

                result = json.dumps(
                    {
                        "error": f"Missing required tool argument: {exc}",
                    }
                )

            except TypeError as exc:
                debug_print(
                    "\nThe tool arguments had an invalid Python type."
                )
                debug_print(f"Type error: {exc}")

                result = json.dumps(
                    {
                        "error": f"Invalid tool argument type: {exc}",
                    }
                )

            except Exception as exc:
                debug_print(
                    "\nAn unexpected error occurred while executing the tool."
                )
                debug_print(f"Unexpected error: {exc}")

                result = json.dumps(
                    {
                        "error": f"Unexpected tool error: {exc}",
                    }
                )

            debug_banner("TOOL EXECUTION COMPLETE")

            debug_print("\nThe Python tool returned this JSON string:")
            debug_print(result)

            debug_banner("RETURNING TOOL OUTPUT TO THE MODEL")

            debug_print(
                "\nThe tool result does not go directly to the user."
            )
            debug_print(
                "It is added to the conversation and sent back to the model."
            )
            debug_print(
                "The call_id connects the result to the model's "
                "original tool request."
            )

            tool_output_item = {
                "type": "function_call_output",
                "call_id": function_call.call_id,
                "output": result,
            }

            debug_print(
                "\nThe following conversation item will be added:"
            )
            debug_json(tool_output_item)

            input_items.append(tool_output_item)

        debug_banner("ITERATION COMPLETE")

        debug_print(
            "\nAll requested tools were executed and their results "
            "were added to the conversation."
        )
        debug_print(
            "The loop will make another API request so the model "
            "can inspect the tool results."
        )
        debug_print(
            "The model may request another tool or return a final answer."
        )

    raise RuntimeError(
        f"Agent exceeded the maximum of {max_iterations} iterations."
    )


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

def main() -> None:
    """
    Run the terminal interface.

    Each user question starts a new run_agent() session.
    """

    print("=" * 80)
    print("SIMPLE AI AGENT".center(80))
    print("=" * 80)

    if DEBUG:
        print("\nDebug mode: ON")
        print("Detailed agent activity will be displayed.")
    else:
        print("\nDebug mode: OFF")

    print("\nThe agent is ready.")
    print("Type 'quit' or 'exit' to stop the program.")

    while True:
        user_message = input("\nYou: ").strip()

        if not user_message:
            print("No message was entered.")
            continue

        if user_message.lower() in {"quit", "exit"}:
            print("\nClosing the agent.")
            break

        try:
            answer = run_agent(user_message)

            if DEBUG:
                debug_banner("FINAL ANSWER")

            print(f"\nAgent: {answer}")

        except KeyboardInterrupt:
            print("\n\nThe current operation was interrupted.")

        except Exception as exc:
            print(f"\nError: {exc}")


# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()