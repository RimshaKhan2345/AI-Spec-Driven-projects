"""
Cohere Tool Schemas for Todo AI Chatbot
"""

# Tool schema for adding a task
ADD_TASK_TOOL_SCHEMA = {
    "name": "add_task",
    "description": "Add a new task to the user's todo list",
    "parameter_definitions": {
        "user_id": {
            "description": "The ID of the user adding the task",
            "type": "string",
            "required": True
        },
        "title": {
            "description": "The title of the task to add",
            "type": "string",
            "required": True
        },
        "description": {
            "description": "Optional description of the task",
            "type": "string",
            "required": False
        }
    }
}

# Tool schema for listing tasks
LIST_TASKS_TOOL_SCHEMA = {
    "name": "list_tasks",
    "description": "List tasks for a user with optional status filter",
    "parameter_definitions": {
        "user_id": {
            "description": "The ID of the user whose tasks to list",
            "type": "string",
            "required": True
        },
        "status": {
            "description": "Filter tasks by status: 'all', 'pending', or 'completed'",
            "type": "string",
            "required": False,
            "default": "all"
        }
    }
}

# Tool schema for completing a task
COMPLETE_TASK_TOOL_SCHEMA = {
    "name": "complete_task",
    "description": "Mark a task as completed",
    "parameter_definitions": {
        "user_id": {
            "description": "The ID of the user who owns the task",
            "type": "string",
            "required": True
        },
        "task_id": {
            "description": "The ID of the task to mark as completed",
            "type": "string",
            "required": True
        }
    }
}

# Tool schema for deleting a task
DELETE_TASK_TOOL_SCHEMA = {
    "name": "delete_task",
    "description": "Delete a task from the user's todo list",
    "parameter_definitions": {
        "user_id": {
            "description": "The ID of the user who owns the task",
            "type": "string",
            "required": True
        },
        "task_id": {
            "description": "The ID of the task to delete",
            "type": "string",
            "required": True
        }
    }
}

# Tool schema for updating a task
UPDATE_TASK_TOOL_SCHEMA = {
    "name": "update_task",
    "description": "Update an existing task in the user's todo list",
    "parameter_definitions": {
        "user_id": {
            "description": "The ID of the user who owns the task",
            "type": "string",
            "required": True
        },
        "task_id": {
            "description": "The ID of the task to update",
            "type": "string",
            "required": True
        },
        "title": {
            "description": "New title for the task (optional)",
            "type": "string",
            "required": False
        },
        "description": {
            "description": "New description for the task (optional)",
            "type": "string",
            "required": False
        }
    }
}

# Tool schema for getting user info
GET_CURRENT_USER_INFO_TOOL_SCHEMA = {
    "name": "get_current_user_info",
    "description": "Get information about the current user",
    "parameter_definitions": {
        "user_id": {
            "description": "The ID of the user to get information for",
            "type": "string",
            "required": True
        }
    }
}

# List of all tool schemas
ALL_TOOLS_SCHEMAS = [
    ADD_TASK_TOOL_SCHEMA,
    LIST_TASKS_TOOL_SCHEMA,
    COMPLETE_TASK_TOOL_SCHEMA,
    DELETE_TASK_TOOL_SCHEMA,
    UPDATE_TASK_TOOL_SCHEMA,
    GET_CURRENT_USER_INFO_TOOL_SCHEMA
]