# Full-Stack Todo Application

A complete full-stack todo application with secure authentication, user data isolation, and responsive UI.

## Project Structure

```
fullstack-todo/
├── backend/                 # FastAPI backend with PostgreSQL
│   ├── api/                # API routes
│   │   ├── routers/        # Route handlers
│   │   └── auth/           # Authentication routes
│   ├── auth/               # Authentication utilities
│   ├── middleware/         # Security middleware
│   ├── models/             # Database models
│   ├── utils/              # Utility functions
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database setup
│   ├── init_db.py          # Database initialization
│   └── main.py             # Main application entry point
└── frontend/               # Next.js frontend
    ├── app/                # Application pages
    │   ├── login/          # Login page
    │   ├── register/       # Registration page
    │   └── dashboard/      # Dashboard page
    ├── contexts/           # React contexts
    ├── utils/              # Utility functions
    ├── components/         # Reusable components
    ├── styles/             # Styling
    └── pages/              # Next.js pages (if using pages router)
```

## Features

### Backend
- RESTful API with 6 endpoints for todo operations
- JWT-based authentication with refresh tokens
- User data isolation (each user sees only their todos)
- Rate limiting to prevent abuse
- Input validation and security headers
- PostgreSQL database with proper relationships

### Frontend
- Responsive UI built with Next.js and Tailwind CSS
- Secure authentication flow (login/register)
- Protected routes and user session management
- Full CRUD operations for todos
- Real-time updates and optimistic UI

## Tech Stack

### Backend
- FastAPI: Modern, fast web framework for building APIs
- SQLModel: SQL databases with Python types
- PostgreSQL: Robust relational database
- JWT: Secure token-based authentication
- SlowAPI: Rate limiting for API endpoints

### Frontend
- Next.js 14: React framework with App Router
- Tailwind CSS: Utility-first CSS framework
- React Context: State management
- Native fetch: HTTP client

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python run_server.py
```

The backend will be available at http://localhost:8000

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## API Endpoints

### Authentication
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get access/refresh tokens
- `POST /api/refresh` - Refresh access token

### Todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos` - Get all todos for authenticated user
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo
- `PATCH /api/todos/{id}/complete` - Toggle completion status

## Security Features

- JWT-based authentication with access and refresh tokens
- User data isolation (users can only access their own data)
- Rate limiting on all endpoints
- Input validation and sanitization
- Security headers (HSTS, CSP, etc.)
- HTTPS enforcement in production

## Deployment

### Backend
Deploy to any platform that supports Python applications (Heroku, AWS, Google Cloud, etc.)

### Frontend
Deploy to Vercel, Netlify, or any static hosting service that supports Next.js applications.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.