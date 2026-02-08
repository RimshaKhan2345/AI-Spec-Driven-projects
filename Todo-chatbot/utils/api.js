// API utility functions
const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000';

// Function to refresh the access token
const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');

  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await fetch(`${API_BASE_URL}/api/refresh`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      refresh_token: refreshToken,
    }),
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data.access_token;
  } else {
    // If refresh fails, clear tokens and redirect to login
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userEmail');
    window.location.href = '/login';
    throw new Error('Token refresh failed');
  }
};

// Generic function to make authenticated API requests with automatic token refresh
export const apiRequest = async (endpoint, options = {}) => {
  let token = localStorage.getItem('token');

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // If the response is unauthorized, try to refresh the token and retry the request
  if (response.status === 401) {
    try {
      token = await refreshToken();
      headers['Authorization'] = `Bearer ${token}`;

      response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });
    } catch (error) {
      // If refresh fails, the refreshToken function handles cleanup
      throw error;
    }
  }

  return response;
};

// Specific API functions
export const authAPI = {
  login: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: email,
        password: password,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      // Store both access and refresh tokens
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('refreshToken', data.refresh_token);
    }

    return response;
  },

  register: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/api/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      // Store both access and refresh tokens
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('refreshToken', data.refresh_token);
    }

    return response;
  },

  logout: async () => {
    // Clear tokens from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userEmail');
  },
};

export const todosAPI = {
  getAll: async () => {
    return await apiRequest('/api/todos');
  },

  create: async (todoData) => {
    return await apiRequest('/api/todos', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  },

  update: async (id, todoData) => {
    return await apiRequest(`/api/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
  },

  delete: async (id) => {
    return await apiRequest(`/api/todos/${id}`, {
      method: 'DELETE',
    });
  },

  toggleComplete: async (id) => {
    return await apiRequest(`/api/todos/${id}/complete`, {
      method: 'PATCH',
    });
  },
};

export const chatAPI = {
  sendMessage: async (message, conversationId) => {
    return await apiRequest('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      }),
    });
  },
};