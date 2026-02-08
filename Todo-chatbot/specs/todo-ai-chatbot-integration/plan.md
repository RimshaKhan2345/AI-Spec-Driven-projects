# Todo AI Chatbot Integration - Phase 1 Plan

## Overview
This plan outlines the implementation of Phase 1: MCP Tools and Database Models Setup adapted for Cohere API.

## Goals
- Create database models for storing conversation state
- Develop Cohere-compatible tools for todo operations
- Implement authentication wrapper for tools
- Set up Cohere SDK integration in the backend

## Implementation Steps

### Step 1: Add Cohere Dependency
- Update `requirements.txt` to include the Cohere SDK
- Install the new dependency

### Step 2: Create Database Models
- Create a `Conversation` model to store conversation state
- Create a `Message` model to store individual messages in a conversation
- Update the database initialization to include these new models

### Step 3: Implement Authentication Wrapper
- Create a utility function to validate JWT tokens and extract user information
- This will be used by the Cohere tools to ensure proper authorization

### Step 4: Develop Cohere-Compatible Tools
- Create a `create_todo_tool` function that wraps the existing todo creation logic
- Create a `get_todos_tool` function that wraps the existing todo listing logic
- Create a `update_todo_tool` function that wraps the existing todo update logic
- Create a `delete_todo_tool` function that wraps the existing todo deletion logic
- Create a `toggle_todo_completion_tool` function that wraps the existing toggle completion logic
- Create a `get_user_info_tool` function to retrieve user information

### Step 5: Testing
- Write unit tests for the new database models
- Write unit tests for the authentication wrapper
- Write unit tests for the Cohere-compatible tools

## Deliverables
- Updated `requirements.txt` with Cohere SDK
- New database models for conversation state
- Authentication wrapper utility
- Cohere-compatible tools for all required operations
- Unit tests for all new components

## Success Criteria
- All new database models are properly defined and can be created in the database
- Authentication wrapper correctly validates JWT tokens and extracts user information
- All Cohere-compatible tools properly interact with the database and respect user authorization
- All unit tests pass successfully