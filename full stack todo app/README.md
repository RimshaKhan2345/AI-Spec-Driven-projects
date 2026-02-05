# Todo App Frontend

This is the frontend component of the full-stack todo application built with Next.js.

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **HTTP Client**: Native fetch API with utility functions
- **Icons**: Lucide React

## Features

- User registration and authentication
- Full CRUD operations for todos
- Responsive design for all device sizes
- Protected routes
- Real-time updates

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Environment Variables

- `NEXT_PUBLIC_BACKEND_API_URL`: URL of the backend API (default: http://localhost:8000)

## Project Structure

- `app/`: Contains all Next.js pages using App Router
- `contexts/`: React context providers (e.g., AuthContext)
- `utils/`: Utility functions (e.g., API helpers)
- `components/`: Reusable UI components (to be added as needed)

## Available Scripts

- `npm run dev`: Starts the development server
- `npm run build`: Builds the production-ready application
- `npm run start`: Starts the production server
- `npm run lint`: Runs ESLint for code quality checks

## API Integration

The frontend communicates with the backend API through utility functions in `utils/api.js`. These functions handle authentication headers and common error handling.

## Authentication Flow

1. Users register or login via the forms
2. JWT tokens are stored in localStorage
3. Tokens are included in requests to protected endpoints
4. Protected routes check for valid tokens before rendering