# Specification: Backend API and Database Setup

## Overview
This specification defines the backend API and database setup for the full-stack todo application. It establishes the foundation for all subsequent development phases.

## Requirements

### Functional Requirements
1. **Database Schema**: Implement a PostgreSQL database schema with tables for users and todos
2. **RESTful API**: Create 6 minimum API endpoints for todo operations
3. **Data Models**: Define SQLModel models for users and todos with relationships
4. **Authentication Integration**: Prepare endpoints for JWT-based authentication
5. **CRUD Operations**: Support all basic CRUD operations for todos
6. **Multi-user Isolation**: Ensure data isolation between users

### Technical Requirements
1. **Framework**: Use FastAPI for the backend API
2. **Database**: Use SQLModel with Neon PostgreSQL
3. **Authentication**: Prepare for JWT-based authentication with Better Auth
4. **API Format**: All endpoints must return JSON responses
5. **Security**: Implement proper validation and sanitization

## Database Schema

### Users Table
- `id`: UUID primary key
- `email`: String unique identifier
- `password_hash`: String for password storage
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Todos Table
- `id`: UUID primary key
- `title`: String (required)
- `description`: Text (optional)
- `completed`: Boolean (default: false)
- `user_id`: UUID foreign key referencing users table
- `created_at`: Timestamp
- `updated_at`: Timestamp

## API Endpoints

### 1. Create Todo
- **Method**: POST
- **Path**: `/api/todos`
- **Request Body**: 
  ```json
  {
    "title": "string",
    "description": "string (optional)"
  }
  ```
- **Response**: Created todo object with 201 status
- **Auth Required**: Yes

### 2. Get All Todos
- **Method**: GET
- **Path**: `/api/todos`
- **Query Params**: None initially
- **Response**: Array of todos for authenticated user
- **Auth Required**: Yes

### 3. Get Single Todo
- **Method**: GET
- **Path**: `/api/todos/{id}`
- **Response**: Single todo object
- **Auth Required**: Yes

### 4. Update Todo
- **Method**: PUT
- **Path**: `/api/todos/{id}`
- **Request Body**: 
  ```json
  {
    "title": "string (optional)",
    "description": "string (optional)",
    "completed": "boolean (optional)"
  }
  ```
- **Response**: Updated todo object
- **Auth Required**: Yes

### 5. Delete Todo
- **Method**: DELETE
- **Path**: `/api/todos/{id}`
- **Response**: Empty with 204 status
- **Auth Required**: Yes

### 6. Toggle Complete Status
- **Method**: PATCH
- **Path**: `/api/todos/{id}/complete`
- **Response**: Updated todo object
- **Auth Required**: Yes

## Authentication Integration Points
- All endpoints require JWT token validation
- User ID extracted from JWT claims
- Data access limited to authenticated user's records

## Success Criteria
- [ ] Database schema created with proper relationships
- [ ] All 6 API endpoints implemented and tested
- [ ] Proper authentication validation implemented
- [ ] Data isolation between users confirmed
- [ ] All endpoints return JSON responses
- [ ] Error handling implemented appropriately
- [ ] Database connection established with Neon PostgreSQL