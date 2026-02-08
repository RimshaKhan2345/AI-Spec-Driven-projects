'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import ProtectedRoute from './ProtectedRoute';
import { todosAPI } from '../../utils/api';
import ChatIcon from '../../components/ChatIcon';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [editingTodo, setEditingTodo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await todosAPI.getAll();

      if (response.ok) {
        const data = await response.json();
        setTodos(data);
      } else {
        setError('Failed to fetch todos');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();
    try {
      const response = await todosAPI.create(newTodo);

      if (response.ok) {
        const addedTodo = await response.json();
        setTodos([...todos, addedTodo]);
        setNewTodo({ title: '', description: '' });
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add todo');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  const handleUpdateTodo = async (e) => {
    e.preventDefault();
    try {
      const response = await todosAPI.update(editingTodo.id, editingTodo);

      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(todo =>
          todo.id === updatedTodo.id ? updatedTodo : todo
        ));
        setEditingTodo(null);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update todo');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  const toggleTodoComplete = async (id) => {
    try {
      const response = await todosAPI.toggleComplete(id);

      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(todo =>
          todo.id === id ? updatedTodo : todo
        ));
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update todo');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  const deleteTodo = async (id) => {
    try {
      const response = await todosAPI.delete(id);

      if (response.ok) {
        setTodos(todos.filter(todo => todo.id !== id));
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to delete todo');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  const startEditing = (todo) => {
    setEditingTodo({ ...todo });
  };

  const cancelEditing = () => {
    setEditingTodo(null);
  };

  const handleEditChange = (field, value) => {
    setEditingTodo(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow-lg shadow-indigo-100">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-indigo-700">Todo Dashboard</h1>
              <p className="text-gray-600 mt-1">Manage your tasks efficiently</p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700 font-medium">Welcome, {user?.email}</span>
              <button
                onClick={handleLogout}
                className="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <main className="py-8">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
              {/* Add/Edit Todo Form */}
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6 pb-2 border-b border-gray-200">
                  {editingTodo ? 'Edit Todo' : 'Add New Todo'}
                </h2>

                {(error || editingTodo?.error) && (
                  <div className="mb-4 rounded-lg bg-red-50 p-4 border border-red-200">
                    <div className="text-sm text-red-700">{error || editingTodo?.error}</div>
                  </div>
                )}

                <form onSubmit={editingTodo ? handleUpdateTodo : handleAddTodo} className="space-y-4">
                  <div>
                    <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                      Title *
                    </label>
                    <input
                      type="text"
                      id="title"
                      value={editingTodo ? editingTodo.title : newTodo.title}
                      onChange={(e) =>
                        editingTodo
                          ? handleEditChange('title', e.target.value)
                          : setNewTodo({...newTodo, title: e.target.value})
                      }
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200"
                      placeholder="What needs to be done?"
                    />
                  </div>

                  <div>
                    <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                      Description
                    </label>
                    <textarea
                      id="description"
                      rows="3"
                      value={editingTodo ? editingTodo.description : newTodo.description}
                      onChange={(e) =>
                        editingTodo
                          ? handleEditChange('description', e.target.value)
                          : setNewTodo({...newTodo, description: e.target.value})
                      }
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200"
                      placeholder="Add details..."
                    ></textarea>
                  </div>

                  <div className="flex space-x-3 pt-2">
                    {editingTodo ? (
                      <>
                        <button
                          type="submit"
                          className="flex-1 inline-flex items-center justify-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200"
                        >
                          Update Todo
                        </button>
                        <button
                          type="button"
                          onClick={cancelEditing}
                          className="flex-1 inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-base font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200"
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <button
                        type="submit"
                        className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200"
                      >
                        Add Todo
                      </button>
                    )}
                  </div>
                </form>
              </div>

              {/* Todo List */}
              <div>
                <div className="flex justify-between items-center mb-6 pb-2 border-b border-gray-200">
                  <h2 className="text-2xl font-bold text-gray-800">Your Tasks</h2>
                  <span className="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
                    {todos.length} {todos.length === 1 ? 'task' : 'tasks'}
                  </span>
                </div>

                {todos.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="text-gray-400 mb-4">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
                    <p className="text-gray-500">Get started by adding a new task above</p>
                  </div>
                ) : (
                  <ul className="space-y-4">
                    {todos.map((todo) => (
                      <li
                        key={todo.id}
                        className={`bg-white overflow-hidden shadow rounded-xl p-5 transition-all duration-200 hover:shadow-md ${
                          todo.completed ? 'bg-green-50 border-l-4 border-green-500' : 'border-l-4 border-indigo-500'
                        }`}
                      >
                        <div className="flex items-start">
                          <input
                            type="checkbox"
                            checked={todo.completed}
                            onChange={() => toggleTodoComplete(todo.id)}
                            className="mt-1 h-5 w-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 cursor-pointer"
                          />
                          <div className="ml-4 flex-1 min-w-0">
                            <h3 className={`text-lg font-semibold ${
                              todo.completed ? 'line-through text-gray-500' : 'text-gray-900'
                            }`}>
                              {todo.title}
                            </h3>
                            {todo.description && (
                              <p className={`mt-2 text-gray-600 ${
                                todo.completed ? 'line-through' : ''
                              }`}>
                                {todo.description}
                              </p>
                            )}
                            <div className="mt-3 flex items-center text-xs text-gray-500">
                              <span>Created: {new Date(todo.created_at).toLocaleDateString()}</span>
                              {todo.updated_at !== todo.created_at && (
                                <span className="ml-3">Updated: {new Date(todo.updated_at).toLocaleDateString()}</span>
                              )}
                            </div>
                          </div>
                          <div className="flex space-x-2 ml-4">
                            <button
                              onClick={() => startEditing(todo)}
                              className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => deleteTodo(todo.id)}
                              className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>

            <div className="text-center text-gray-500 text-sm">
              Made with ❤️ using Next.js and Tailwind CSS
            </div>
          </div>
        </main>
        
        {/* Chat Icon - only visible when user is logged in */}
        {user && <ChatIcon />}
      </div>
    </ProtectedRoute>
  );
}