import React, { useState, useEffect } from 'react';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import styles from './ChatWidget.module.css';
import { sendMessage, loadConversationHistory, createNewConversation, ChatApiError } from '../../services/chatApi';
import MessageWithCitations from './MessageWithCitations';

/**
 * ChatWidget Component
 *
 * A chat interface for the RAG chatbot integrated with the Physical AI textbook.
 * Handles user questions, displays AI responses with citations, and manages conversation history.
 */
const ChatWidget = () => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [conversationId, setConversationId] = useState(null);

  // Initialize session on component mount
  useEffect(() => {
    initializeSession();
  }, []);

  /**
   * Initialize or restore session from localStorage and load history
   */
  const initializeSession = async () => {
    const storedSessionId = localStorage.getItem('rag_chatbot_session_id');
    const storedConversationId = localStorage.getItem('rag_chatbot_conversation_id');

    if (storedSessionId) {
      setSessionId(storedSessionId);

      // Load conversation history if session exists
      try {
        const history = await loadConversationHistory(storedSessionId, storedConversationId);

        if (history.messages && history.messages.length > 0) {
          // Convert API messages to chat UI format
          const historyMessages = history.messages.map((msg) => ({
            message: msg.content,
            sentTime: msg.created_at,
            sender: msg.role === 'user' ? 'user' : 'assistant',
            direction: msg.role === 'user' ? 'outgoing' : 'incoming',
            position: 'single',
            citations: msg.citations || [],
            isOffTopic: false,
            messageId: msg.id,
          }));

          setMessages(historyMessages);
          return; // Don't show welcome message if history exists
        }
      } catch (error) {
        console.error('Failed to load conversation history:', error);
        // Continue to show welcome message on error
      }
    }

    if (storedConversationId) {
      setConversationId(storedConversationId);
    }

    // Add welcome message (only if no history loaded)
    setMessages([
      {
        message: "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics Textbook. Ask me anything about ROS 2, Digital Twins, NVIDIA Isaac, Vision-Language-Action systems, or humanoid robotics!",
        sentTime: new Date().toISOString(),
        sender: 'assistant',
        direction: 'incoming',
        position: 'single',
      },
    ]);
  };

  /**
   * Handle starting a new conversation
   */
  const handleNewConversation = async () => {
    if (!sessionId) {
      console.warn('No session ID available to create new conversation');
      return;
    }

    try {
      const newConv = await createNewConversation(sessionId);
      setConversationId(newConv.conversationId);
      localStorage.setItem('rag_chatbot_conversation_id', newConv.conversationId);

      // Clear messages and show welcome message
      setMessages([
        {
          message: "New conversation started! Ask me anything about the Physical AI & Humanoid Robotics Textbook.",
          sentTime: new Date().toISOString(),
          sender: 'assistant',
          direction: 'incoming',
          position: 'single',
        },
      ]);
    } catch (error) {
      console.error('Failed to create new conversation:', error);

      // Show error message
      const errorMessage = {
        message: 'Failed to start new conversation. Please try again.',
        sentTime: new Date().toISOString(),
        sender: 'assistant',
        direction: 'incoming',
        position: 'single',
        type: 'error',
      };

      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  /**
   * Handle sending a new message
   */
  const handleSend = async (message) => {
    if (!message.trim()) return;

    // Add user message to UI
    const newUserMessage = {
      message: message,
      sentTime: new Date().toISOString(),
      sender: 'user',
      direction: 'outgoing',
      position: 'single',
    };

    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      // Call the backend API
      const response = await sendMessage(message, sessionId, conversationId);

      // Update session and conversation IDs from response
      if (response.sessionId && response.sessionId !== sessionId) {
        setSessionId(response.sessionId);
        localStorage.setItem('rag_chatbot_session_id', response.sessionId);
      }

      if (response.conversationId && response.conversationId !== conversationId) {
        setConversationId(response.conversationId);
        localStorage.setItem('rag_chatbot_conversation_id', response.conversationId);
      }

      // Add assistant response to UI
      const assistantMessage = {
        message: response.answer,
        sentTime: new Date().toISOString(),
        sender: 'assistant',
        direction: 'incoming',
        position: 'single',
        citations: response.citations || [],
        isOffTopic: response.isOffTopic,
        messageId: response.messageId,
      };

      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Get user-friendly error message
      let errorText = 'Sorry, I encountered an error processing your request. Please try again.';
      if (error instanceof ChatApiError) {
        errorText = error.getUserMessage();
      }

      // Add error message
      const errorMessage = {
        message: errorText,
        sentTime: new Date().toISOString(),
        sender: 'assistant',
        direction: 'incoming',
        position: 'single',
        type: 'error',
      };

      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className={styles.chatWidgetContainer}>
      <MainContainer>
        <ChatContainer>
          <MessageList
            scrollBehavior="smooth"
            typingIndicator={isTyping ? <TypingIndicator content="AI is thinking..." /> : null}
          >
            {messages.map((msg, index) => {
              // For assistant messages with citations, use MessageWithCitations
              if (msg.sender === 'assistant' && (msg.citations || msg.isOffTopic)) {
                return (
                  <MessageWithCitations
                    key={index}
                    message={msg.message}
                    citations={msg.citations}
                    isOffTopic={msg.isOffTopic}
                    model={{
                      message: msg.message,
                      sentTime: msg.sentTime,
                      sender: msg.sender,
                      direction: msg.direction,
                      position: msg.position,
                    }}
                  />
                );
              }

              // For regular messages, use standard Message component
              return (
                <Message
                  key={index}
                  model={{
                    message: msg.message,
                    sentTime: msg.sentTime,
                    sender: msg.sender,
                    direction: msg.direction,
                    position: msg.position,
                  }}
                />
              );
            })}
          </MessageList>
          {messages.length > 1 && (
            <div className={styles.newConversationButtonContainer}>
              <button
                className={styles.newConversationButton}
                onClick={handleNewConversation}
                title="Start a new conversation"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className={styles.newConversationIcon}
                >
                  <path d="M12 5v14M5 12h14" />
                </svg>
                New Conversation
              </button>
            </div>
          )}
          <MessageInput
            placeholder="Ask a question about the textbook..."
            value={inputValue}
            onChange={(val) => setInputValue(val)}
            onSend={handleSend}
            attachButton={false}
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export default ChatWidget;
