/**
 * Chat API Client
 *
 * Handles communication with the FastAPI backend for the RAG chatbot.
 * Implements error handling, retries, and CORS support.
 */

// Backend API base URL - Update this based on deployment environment
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Send a message to the chatbot and get a response
 *
 * @param {string} question - The user's question
 * @param {string|null} sessionId - Optional session ID for conversation continuity
 * @param {string|null} conversationId - Optional conversation ID for threading
 * @returns {Promise<Object>} Response object with answer, citations, and IDs
 */
export const sendMessage = async (question, sessionId = null, conversationId = null) => {
  const requestBody = {
    question: question.trim(),
  };

  // Include session_id if provided
  if (sessionId) {
    requestBody.session_id = sessionId;
  }

  // Include conversation_id if provided
  if (conversationId) {
    requestBody.conversation_id = conversationId;
  }

  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      // Handle HTTP errors
      const errorData = await response.json().catch(() => ({}));
      throw new ChatApiError(
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData
      );
    }

    const data = await response.json();

    // Validate response structure
    if (!data.response) {
      throw new ChatApiError('Invalid response format from server', 500, data);
    }

    return {
      answer: data.response,
      citations: data.citations || [],
      messageId: data.message_id,
      conversationId: data.conversation_id,
      sessionId: data.session_id,
      isOffTopic: data.is_off_topic || false,
    };
  } catch (error) {
    if (error instanceof ChatApiError) {
      throw error;
    }

    // Handle network errors
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new ChatApiError(
        'Unable to connect to the chatbot service. Please check your internet connection.',
        0,
        { originalError: error.message }
      );
    }

    // Handle other unexpected errors
    throw new ChatApiError(
      `Unexpected error: ${error.message}`,
      500,
      { originalError: error.message }
    );
  }
};

/**
 * Fetch with automatic retry logic
 *
 * @param {string} url - The URL to fetch
 * @param {Object} options - Fetch options
 * @param {number} maxRetries - Maximum number of retry attempts (default: 3)
 * @param {number} retryDelay - Delay between retries in ms (default: 1000)
 * @returns {Promise<Response>} Fetch response
 */
const fetchWithRetry = async (url, options, maxRetries = 3, retryDelay = 1000) => {
  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(url, options);

      // Don't retry on 4xx client errors (except 429 Too Many Requests)
      if (response.status >= 400 && response.status < 500 && response.status !== 429) {
        return response;
      }

      // Retry on 5xx server errors or 429 Too Many Requests
      if (response.status >= 500 || response.status === 429) {
        if (attempt < maxRetries) {
          await sleep(retryDelay * Math.pow(2, attempt)); // Exponential backoff
          continue;
        }
      }

      return response;
    } catch (error) {
      lastError = error;

      // Don't retry on the last attempt
      if (attempt < maxRetries) {
        await sleep(retryDelay * Math.pow(2, attempt)); // Exponential backoff
        continue;
      }
    }
  }

  // All retries exhausted
  throw lastError;
};

/**
 * Sleep utility for retry delays
 *
 * @param {number} ms - Milliseconds to sleep
 * @returns {Promise<void>}
 */
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Check API health status
 *
 * @returns {Promise<Object>} Health status object
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new ChatApiError(
        `Health check failed: ${response.statusText}`,
        response.status
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ChatApiError) {
      throw error;
    }

    throw new ChatApiError(
      `Unable to check API health: ${error.message}`,
      0,
      { originalError: error.message }
    );
  }
};

/**
 * Custom error class for Chat API errors
 */
export class ChatApiError extends Error {
  constructor(message, statusCode, details = {}) {
    super(message);
    this.name = 'ChatApiError';
    this.statusCode = statusCode;
    this.details = details;
  }

  /**
   * Check if error is a network error
   */
  isNetworkError() {
    return this.statusCode === 0;
  }

  /**
   * Check if error is a server error (5xx)
   */
  isServerError() {
    return this.statusCode >= 500 && this.statusCode < 600;
  }

  /**
   * Check if error is a client error (4xx)
   */
  isClientError() {
    return this.statusCode >= 400 && this.statusCode < 500;
  }

  /**
   * Get user-friendly error message
   */
  getUserMessage() {
    if (this.isNetworkError()) {
      return 'Unable to connect to the chatbot. Please check your internet connection.';
    }

    if (this.isServerError()) {
      return 'The chatbot service is temporarily unavailable. Please try again in a moment.';
    }

    if (this.statusCode === 429) {
      return 'Too many requests. Please wait a moment before trying again.';
    }

    return this.message || 'An unexpected error occurred. Please try again.';
  }
}

export default {
  sendMessage,
  checkHealth,
  ChatApiError,
};
