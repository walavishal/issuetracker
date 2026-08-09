import json
from groq import Groq, GroqError
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.ai_response import AIssueSummaryResponse
from app.utils.prompts import llm_prompts
from app.services.ai_tools import TOOL_FUNCTIONS
from app.utils.tools_definitions import TOOLS
from sqlalchemy.orm import Session
from app.db.models.user import User

# Using the official Groq client
client = Groq(api_key=settings.GROQ_API_KEY)

def generate_issue_summary(user_description: str) -> AIssueSummaryResponse:
    prompt = llm_prompts["issue_title_and_description_summarize"]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"{prompt}\nReturn the output in JSON format."},
                {"role": "user", "content": user_description}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content

        data = json.loads(content)

        if "error" in data:
            raise ValueError(data["error"])
        
        # model_validate_json handles the json.loads step automatically
        return AIssueSummaryResponse.model_validate_json(content)

    except GroqError as e:
        # Handle API specific errors (Rate limits, authentication, etc.)
        raise ValueError(f"Groq API error: {e}")
    except (json.JSONDecodeError, ValidationError) as e:
        # Handle cases where AI didn't follow schema or returned bad JSON
        raise ValueError(f"Failed to parse AI response: {e}")
    

# def ai_agent(
#     db: Session,
#     user_prompt: str
# ):

# #     messages = [
# #         {
# #             "role": "system",
# #             "content": """
# # You are an AI issue management assistant.

# # Your job:
# # - Understand user requests
# # - Use tools whenever required
# # - Help manage issues/projects/users

# # Always use tools for actions.
# # """
# #         },
# #         {
# #             "role": "user",
# #             "content": user_prompt
# #         }
# #     ]

#     messages = [
#     {
#         "role": "system",
#         "content": "You are an automated issue management assistant. Help the user manage projects using your provided tools."
#     },
#     {
#         "role": "user",
#         "content": user_prompt
#     }
# ]

#     try:

#         # -----------------------------------
#         # FIRST LLM CALL
#         # -----------------------------------

#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=messages,
#             tools=TOOLS,
#             tool_choice="auto",
#             temperature=0
#         )
#         print('*'*100)
#         print(response)
#         print('*'*100)

#         response_message = response.choices[0].message

#         tool_calls = response_message.tool_calls

#         # No tool call
#         if not tool_calls:
#             return {
#                 "message": response_message.content
#             }

#         # Add assistant response
#         messages.append(response_message)
#         call_tool = True
        
#         while call_tool:
#             # -----------------------------------
#             # EXECUTE TOOLS DYNAMICALLY
#             # -----------------------------------

#             messages = tool_calling(db, messages, tool_calls)

#             # -----------------------------------
#             # FINAL RESPONSE
#             # -----------------------------------

#             final_response = client.chat.completions.create(
#                 model="llama-3.3-70b-versatile",
#                 messages=messages,
#                 temperature=0
#             )

#         return {
#             "message": final_response
#             .choices[0]
#             .message
#             .content
#         }

#     except GroqError as e:

#         raise ValueError(
#             f"Groq API Error: {e}"
#         )

#     except Exception as e:

#         raise ValueError(
#             f"AI Agent Error: {e}"
#         )
    
# def tool_calling(db,messages,tool_calls):
#     for tool_call in tool_calls:
#         function_name = (
#             tool_call.function.name
#         )

#         arguments = json.loads(
#             tool_call.function.arguments
#         )

#         # Get actual python function
#         tool_function = TOOL_FUNCTIONS.get(
#             function_name
#         )

#         if not tool_function:

#             tool_result = {
#                 "success": False,
#                 "message": f"Unknown tool: {function_name}"
#             }

#         else:

#             # Dynamically execute
#             tool_result = tool_function(
#                 db=db,
#                 **arguments
#             )

#         # Append tool result
#         messages.append({
#             "role": "tool",
#             "tool_call_id": tool_call.id,
#             "content": json.dumps(tool_result)
#         })
#     return messages
# -----------------------------------
# TOOL EXECUTION ENGINE
# -----------------------------------
def tool_calling(db: Session, messages, tool_calls):

    print(f"\n[TOOL ENGINE] Executing {len(tool_calls)} tool(s)")

    for tool_call in tool_calls:

        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"\n[TOOL CALL] {function_name}")
        print(f"[ARGUMENTS] {arguments}")

        tool_function = TOOL_FUNCTIONS.get(function_name)

        if not tool_function:
            tool_result = {
                "success": False,
                "message": f"Unknown tool: {function_name}"
            }

            print(f"[ERROR] Unknown tool: {function_name}")

        else:
            tool_result = tool_function(
                db=db,
                **arguments
            )

            print(f"[RESULT] {tool_result}")

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

    return messages


# -----------------------------------
# AI AGENT
# -----------------------------------
def ai_agent(db: Session, user_prompt: str, current_user:User):

    print("\n" + "=" * 100)
    print("[AI AGENT START]")
    print(f"[USER PROMPT] {user_prompt}")
    print("=" * 100)

    messages = [
    {
        "role": "system",
        "content": f"""
        You are an automated issue management assistant. Help the user manage projects using your provided tools.

        Current user:
        - id: {current_user.id}
        - email: {current_user.email}

        Use tools for all data access and modifications.
        Never bypass access restrictions.

        General Rules:
        - The current user is the authenticated user. Never assume another user.
        - Only perform actions on projects, issues, and comments that belong to or are accessible by the current user.
        - Use tools for all data access and modifications.
        - Never bypass access restrictions.
        - Use the minimum number of tools required.
        - Be concise and professional.
        - If a request cannot be completed, explain why and suggest the next step.
        """
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

    try:

        iteration = 1

        while True:

            print("\n" + "-" * 100)
            print(f"[ITERATION #{iteration}]")
            print(f"[MESSAGE COUNT] {len(messages)}")
            print("-" * 100)

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0
            )

            message = response.choices[0].message

            print("\n[LLM RESPONSE]")
            print(message)

            messages.append(message)

            tool_calls = message.tool_calls

            # Final response
            if not tool_calls:

                print("\n[FINAL RESPONSE]")
                print(message.content)

                print("\n[AI AGENT END]")
                print("=" * 100)
                print(type(message.content))
                return {
                    "message": message.content
                }

            print(f"\n[TOOL CALLS DETECTED] {len(tool_calls)}")

            for tool_call in tool_calls:
                print(
                    f" -> {tool_call.function.name}"
                )

            messages = tool_calling(
                db=db,
                messages=messages,
                tool_calls=tool_calls
            )

            iteration += 1

    except GroqError as e:

        print("\n[GROQ ERROR]")
        print(str(e))

        raise ValueError(
            f"Groq API Error: {e}"
        )

    except Exception as e:

        print("\n[AI AGENT ERROR]")
        print(str(e))

        raise ValueError(
            f"AI Agent Error: {e}"
        )