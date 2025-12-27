/**
 * Integration Tests for Chat API Client
 *
 * Tests the API client's ability to communicate with the backend.
 */

import { sendMessage, checkHealth, ChatApiError } from './chatApi';

// Mock fetch for testing
global.fetch = jest.fn();

describe('Chat API Client', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  describe('sendMessage', () => {
    it('should send a message and return response data', async () => {
      const mockResponse = {
        response: 'This is a test response about ROS 2.',
        citations: [
          { reference: '[Chapter 1, Section 1.2]' },
          { reference: '[Chapter 2, Section 2.1]' },
        ],
        message_id: '123e4567-e89b-12d3-a456-426614174000',
        conversation_id: '987fcdeb-51a2-43e7-89ab-123456789abc',
        session_id: '456e7890-a12b-34c5-d678-901234567def',
        is_off_topic: false,
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await sendMessage('What is ROS 2?');

      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/chat',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: JSON.stringify({ question: 'What is ROS 2?' }),
        })
      );

      expect(result).toEqual({
        answer: 'This is a test response about ROS 2.',
        citations: mockResponse.citations,
        messageId: mockResponse.message_id,
        conversationId: mockResponse.conversation_id,
        sessionId: mockResponse.session_id,
        isOffTopic: false,
      });
    });

    it('should include session_id and conversation_id when provided', async () => {
      const mockResponse = {
        response: 'Follow-up response',
        citations: [],
        message_id: '123e4567-e89b-12d3-a456-426614174000',
        conversation_id: '987fcdeb-51a2-43e7-89ab-123456789abc',
        session_id: '456e7890-a12b-34c5-d678-901234567def',
        is_off_topic: false,
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const sessionId = '456e7890-a12b-34c5-d678-901234567def';
      const conversationId = '987fcdeb-51a2-43e7-89ab-123456789abc';

      await sendMessage('Follow-up question', sessionId, conversationId);

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/chat',
        expect.objectContaining({
          body: JSON.stringify({
            question: 'Follow-up question',
            session_id: sessionId,
            conversation_id: conversationId,
          }),
        })
      );
    });

    it('should handle off-topic responses', async () => {
      const mockResponse = {
        response: 'This question is not related to the textbook content.',
        citations: [],
        message_id: '123e4567-e89b-12d3-a456-426614174000',
        conversation_id: '987fcdeb-51a2-43e7-89ab-123456789abc',
        session_id: '456e7890-a12b-34c5-d678-901234567def',
        is_off_topic: true,
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await sendMessage('What is the weather today?');

      expect(result.isOffTopic).toBe(true);
      expect(result.citations).toEqual([]);
    });

    it('should handle HTTP errors', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({ detail: 'Server error occurred' }),
      });

      await expect(sendMessage('Test question')).rejects.toThrow(ChatApiError);
      await expect(sendMessage('Test question')).rejects.toThrow('Server error occurred');
    });

    it('should handle network errors', async () => {
      fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));

      await expect(sendMessage('Test question')).rejects.toThrow(ChatApiError);
      await expect(sendMessage('Test question')).rejects.toThrow(
        'Unable to connect to the chatbot service'
      );
    });

    it('should retry on server errors', async () => {
      // First attempt: 500 error
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({}),
      });

      // Second attempt: success
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          response: 'Success after retry',
          citations: [],
          message_id: '123',
          conversation_id: '456',
          session_id: '789',
          is_off_topic: false,
        }),
      });

      const result = await sendMessage('Test question');

      expect(fetch).toHaveBeenCalledTimes(2);
      expect(result.answer).toBe('Success after retry');
    });

    it('should validate response format', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({}), // Missing 'response' field
      });

      await expect(sendMessage('Test question')).rejects.toThrow(ChatApiError);
      await expect(sendMessage('Test question')).rejects.toThrow('Invalid response format');
    });
  });

  describe('checkHealth', () => {
    it('should check API health successfully', async () => {
      const mockHealthResponse = {
        status: 'healthy',
        database: 'connected',
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockHealthResponse,
      });

      const result = await checkHealth();

      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/health', {
        method: 'GET',
        headers: { Accept: 'application/json' },
      });

      expect(result).toEqual(mockHealthResponse);
    });

    it('should handle health check failure', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 503,
        statusText: 'Service Unavailable',
      });

      await expect(checkHealth()).rejects.toThrow(ChatApiError);
      await expect(checkHealth()).rejects.toThrow('Health check failed');
    });
  });

  describe('ChatApiError', () => {
    it('should identify network errors', () => {
      const error = new ChatApiError('Network error', 0);
      expect(error.isNetworkError()).toBe(true);
      expect(error.isServerError()).toBe(false);
      expect(error.isClientError()).toBe(false);
    });

    it('should identify server errors', () => {
      const error = new ChatApiError('Server error', 500);
      expect(error.isNetworkError()).toBe(false);
      expect(error.isServerError()).toBe(true);
      expect(error.isClientError()).toBe(false);
    });

    it('should identify client errors', () => {
      const error = new ChatApiError('Client error', 400);
      expect(error.isNetworkError()).toBe(false);
      expect(error.isServerError()).toBe(false);
      expect(error.isClientError()).toBe(true);
    });

    it('should provide user-friendly error messages', () => {
      const networkError = new ChatApiError('Network error', 0);
      expect(networkError.getUserMessage()).toContain('Unable to connect');

      const serverError = new ChatApiError('Server error', 500);
      expect(serverError.getUserMessage()).toContain('temporarily unavailable');

      const rateLimitError = new ChatApiError('Too many requests', 429);
      expect(rateLimitError.getUserMessage()).toContain('Too many requests');
    });
  });
});
