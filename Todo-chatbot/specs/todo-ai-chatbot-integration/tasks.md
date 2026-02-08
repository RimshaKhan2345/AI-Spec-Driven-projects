# Todo AI Chatbot Integration - Phase 1 Tasks

## Overview
This document outlines the specific tasks for implementing Phase 1: MCP Tools and Database Models Setup adapted for Cohere API.

## Tasks

### Task 1: Add Cohere Dependency
- [ ] Update `backend/requirements.txt` to include `cohere==x.x.x` (latest stable version)
- [ ] Install the new dependency using pip
- [ ] Verify the installation works correctly

### Task 2: Create Database Models
- [ ] Create a new file `backend/models/chat_models.py`
- [ ] Define a `Conversation` model with fields: id, user_id, created_at, updated_at
- [ ] Define a `Message` model with fields: id, conversation_id, role, content, timestamp
- [ ] Import the new models in `backend/models/__init__.py` or `backend/models.py`
- [ ] Update `backend/init_db.py` to include the new models in table creation

### Task 3: Implement Authentication Wrapper
- [ ] Create a utility function in `backend/utils/auth_wrapper.py`
- [ ] Function should accept a JWT token and return user information
- [ ] Function should raise appropriate exceptions for invalid tokens
- [ ] Write unit tests for the authentication wrapper

### Task 4: Develop Cohere-Compatible Tools
- [ ] Create a new file `backend/tools/todo_tools.py`
- [ ] Implement `create_todo_tool` function that accepts parameters from Cohere and creates a todo
- [ ] Implement `get_todos_tool` function that accepts parameters from Cohere and returns todos
- [ ] Implement `update_todo_tool` function that accepts parameters from Cohere and updates a todo
- [ ] Implement `delete_todo_tool` function that accepts parameters from Cohere and deletes a todo
- [ ] Implement `toggle_todo_completion_tool` function that accepts parameters from Cohere and toggles completion
- [ ] Implement `get_user_info_tool` function that accepts parameters from Cohere and returns user info
- [ ] Each tool should validate the user's authorization using the auth wrapper
- [ ] Write unit tests for each tool function

### Task 5: Testing and Verification
- [ ] Create test files for the new models and tools
- [ ] Run all tests to ensure they pass
- [ ] Verify that the new models can be created in the database
- [ ] Verify that the tools work correctly with mock data

## Acceptance Criteria
- [ ] Cohere SDK is successfully added to the project
- [ ] New database models are properly defined and can be created in the database
- [ ] Authentication wrapper correctly validates JWT tokens and extracts user information
- [ ] All Cohere-compatible tools properly interact with the database and respect user authorization
- [ ] All unit tests pass successfully
- [ ] The implementation follows the existing code style and patterns in the project