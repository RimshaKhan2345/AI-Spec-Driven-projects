import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ChatPanel from './ChatPanel';
import { useAuth } from '../contexts/AuthContext';

// Mock the useAuth hook
vi.mock('../contexts/AuthContext', () => ({
  useAuth: vi.fn(),
}));

// Mock the chatAPI
vi.mock('../../utils/api', () => ({
  chatAPI: {
    sendMessage: vi.fn(),
  },
}));

describe('ChatPanel', () => {
  const mockOnClose = vi.fn();
  const mockUser = { email: 'test@example.com' };

  beforeEach(() => {
    vi.clearAllMocks();
    useAuth.mockReturnValue({ user: mockUser });
  });

  it('renders correctly', () => {
    render(<ChatPanel onClose={mockOnClose} />);
    
    expect(screen.getByText('Todo AI Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Ask me to add, list, complete, or delete tasks...')).toBeInTheDocument();
  });

  it('allows user to type and submit a message', async () => {
    const { chatAPI } = require('../../utils/api');
    chatAPI.sendMessage.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ response: 'Test response', conversation_id: 'test-id' }),
    });

    render(<ChatPanel onClose={mockOnClose} />);
    
    const input = screen.getByPlaceholderText('Ask me to add, list, complete, or delete tasks...');
    const form = screen.getByRole('form');
    
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.submit(form);
    
    await waitFor(() => {
      expect(chatAPI.sendMessage).toHaveBeenCalledWith('Hello', undefined);
    });
  });

  it('shows loading state when submitting', async () => {
    const { chatAPI } = require('../../utils/api');
    chatAPI.sendMessage.mockImplementation(() => new Promise(() => {})); // Never resolves for this test

    render(<ChatPanel onClose={mockOnClose} />);
    
    const input = screen.getByPlaceholderText('Ask me to add, list, complete, or delete tasks...');
    const form = screen.getByRole('form');
    
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.submit(form);
    
    expect(screen.getByLabelText('Send message')).toBeDisabled();
  });
});