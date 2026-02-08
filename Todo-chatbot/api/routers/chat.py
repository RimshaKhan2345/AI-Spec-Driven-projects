from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session
from typing import List, Dict, Any, Optional
from models import Conversation, Message, User
from database_session import get_session
from auth.jwt_handler import get_current_user
from utils.auth_wrapper import validate_and_get_user_from_token
from tools.todo_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
    get_current_user_info
)
from tools.cohere_tool_schemas import ALL_TOOLS_SCHEMAS
import uuid
import os
import cohere
from datetime import datetime


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "YuF799jPp8kelc6x4lxPiXfjzwswdZ3iRC8ndzPO")
co = cohere.Client(api_key=COHERE_API_KEY)


@router.post("/chat")
@limiter.limit("10/minute")
def chat_with_bot(
    request: Request,
    message_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint that connects to Cohere API with tool calling capabilities.

    Args:
        message_data: Contains "message" (str) and optional "conversation_id" (int)
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        Dictionary containing "response" (str) and "conversation_id" (int)
    """
    try:
        user_message = message_data.get("message", "")
        conversation_id = message_data.get("conversation_id")

        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Get or create conversation
        conversation_uuid = None
        if conversation_id:
            conversation_uuid = uuid.UUID(conversation_id)
            # Verify conversation belongs to user
            conversation = session.get(Conversation, conversation_uuid)
            if not conversation or conversation.user_id != current_user.id:
                raise HTTPException(status_code=404, detail="Conversation not found or access denied")
        else:
            # Create new conversation
            new_conversation = Conversation(user_id=current_user.id)
            session.add(new_conversation)
            session.flush()  # Use flush to get the ID without committing the whole transaction
            conversation_uuid = new_conversation.id
            conversation_id = str(conversation_uuid)

        # Save user message to database
        user_message_db = Message(
            conversation_id=conversation_uuid,
            role="user",
            content=user_message,
            timestamp=datetime.utcnow()
        )
        session.add(user_message_db)
        session.flush()

        # Fetch full conversation history
        conversation_history = session.query(Message).filter(
            Message.conversation_id == conversation_uuid
        ).order_by(Message.timestamp).all()

        # Prepare messages for Cohere - only include content, not the DB objects
        cohere_chat_history = []
        for msg in conversation_history[:-1]:  # Exclude the current message we just added
            role = "USER" if msg.role == "user" else "CHATBOT"
            cohere_chat_history.append({
                "role": role,
                "message": msg.content
            })

        # Define the system message
        preamble = (
            "You are a helpful Todo AI assistant. "
            "Always respond in friendly, natural language (match user language: Urdu/English mix ok). "
            "Confirm every action clearly. "
            "Use tools only when needed — never guess task ids. "
            "For unclear requests → ask clarifying questions."
        )

        # Call Cohere with tool use enabled
        response = co.chat(
            message=user_message,
            chat_history=cohere_chat_history,
            tools=ALL_TOOLS_SCHEMAS,
            preamble=preamble
        )

        # Process tool calls if any
        final_response_text = ""
        if response.tool_calls:
            # Execute each tool call
            for i, tool_call in enumerate(response.tool_calls):
                tool_name = tool_call.name
                tool_parameters = tool_call.parameters

                # Ensure user_id is always from the authenticated user, never from tool parameters
                tool_parameters["user_id"] = str(current_user.id)

                # Execute the appropriate tool
                if tool_name == "add_task":
                    result = add_task(**tool_parameters)
                elif tool_name == "list_tasks":
                    result = list_tasks(**tool_parameters)
                elif tool_name == "complete_task":
                    result = complete_task(**tool_parameters)
                elif tool_name == "delete_task":
                    result = delete_task(**tool_parameters)
                elif tool_name == "update_task":
                    result = update_task(**tool_parameters)
                elif tool_name == "get_current_user_info":
                    result = get_current_user_info(**tool_parameters)
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}

                # Process the result
                if result.get("success"):
                    # Format the result appropriately
                    if tool_name == "list_tasks" and isinstance(result, list):
                        if result:
                            task_list = "\n".join([f"- {task.get('title', 'Untitled')} ({'✓' if task.get('completed') else '○'})" for task in result])
                            tool_result_text = f"Here are your tasks:\n{task_list}"
                        else:
                            tool_result_text = "You don't have any tasks right now."
                    elif "message" in result:
                        tool_result_text = result["message"]
                    elif "data" in result and "message" in result["data"]:
                        tool_result_text = result["data"]["message"]
                    else:
                        tool_result_text = "Operation completed successfully."

                    # Add the result to final response
                    final_response_text += tool_result_text + "\n"
                else:
                    error_msg = result.get('error', 'Unknown error occurred')
                    final_response_text += f"Error: {error_msg}\n"

            # If there's a follow-up response from Cohere after tool execution
            if hasattr(response, 'text') and response.text:
                final_response_text += response.text
            elif not final_response_text:
                final_response_text = "Operation completed successfully."
        else:
            # No tool calls, just return Cohere's response
            final_response_text = response.text or "I'm here to help you manage your tasks. You can ask me to add, list, complete, or delete tasks."

        # Save assistant message to database
        assistant_message_db = Message(
            conversation_id=conversation_uuid,
            role="assistant",
            content=final_response_text.strip(),
            timestamp=datetime.utcnow()
        )
        session.add(assistant_message_db)
        session.commit()

        return {
            "response": final_response_text.strip(),
            "conversation_id": conversation_id
        }

    except cohere.CohereAPIError as e:
        raise HTTPException(status_code=500, detail=f"Cohere API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")