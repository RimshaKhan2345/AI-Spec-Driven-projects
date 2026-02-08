# Tasks: Backend API and Database Setup

## Task List

### Phase 1: Project Setup
- [ ] Initialize FastAPI project structure with required dependencies
- [ ] Create environment configuration with python-dotenv
- [ ] Set up SQLModel with Neon PostgreSQL connection
- [ ] Create base models for database entities
- [ ] Implement database session management utilities

### Phase 2: Database Models
- [ ] Implement User model with authentication fields (id, email, password_hash, timestamps)
- [ ] Implement Todo model with user relationship (id, title, description, completed, user_id, timestamps)
- [ ] Define proper foreign key relationships between users and todos
- [ ] Add UUID primary key generation for both models
- [ ] Create database initialization and migration utilities

### Phase 3: API Endpoints
- [ ] Create API router for todo endpoints
- [ ] Implement authentication dependency with JWT validation
- [ ] Build POST endpoint for creating todos with validation
- [ ] Build GET endpoint for retrieving all todos for authenticated user
- [ ] Build GET endpoint for retrieving a single todo by ID
- [ ] Build PUT endpoint for updating a todo with validation
- [ ] Build DELETE endpoint for deleting a todo
- [ ] Build PATCH endpoint for toggling todo completion status
- [ ] Add proper HTTP status codes to all endpoints

### Phase 4: Testing and Integration
- [ ] Write unit tests for User model
- [ ] Write unit tests for Todo model
- [ ] Write unit tests for all 6 API endpoints
- [ ] Test database relationships and constraints
- [ ] Validate JWT authentication flow
- [ ] Confirm multi-user data isolation
- [ ] Test error handling and edge cases

### Phase 5: Documentation and Final Checks
- [ ] Add API documentation with OpenAPI/Swagger
- [ ] Verify all endpoints return proper JSON responses
- [ ] Confirm all success criteria from spec are met
- [ ] Perform end-to-end integration test