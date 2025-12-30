import React, { useState } from 'react';
import ChatWidget from '../ChatWidget';
import styles from './FloatingChatWidget.module.css';

/**
 * FloatingChatWidget Component
 *
 * A floating chat button positioned in the bottom-right corner of the page.
 * Clicking the button toggles the chat widget open/closed.
 * Appears on all pages throughout the Docusaurus site.
 */
const FloatingChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          className={styles.floatingButton}
          onClick={toggleChat}
          aria-label="Open AI Chatbot"
          title="Ask AI about the textbook"
        >
          <svg
            className={styles.chatIcon}
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
          <span className={styles.badge}>AI</span>
        </button>
      )}

      {/* Floating Chat Window */}
      {isOpen && (
        <div className={styles.floatingChatContainer}>
          <div className={styles.chatHeader}>
            <h3 className={styles.chatTitle}>AI Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={closeChat}
              aria-label="Close chat"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className={styles.closeIcon}
              >
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>
          <div className={styles.chatContent}>
            <ChatWidget />
          </div>
        </div>
      )}
    </>
  );
};

export default FloatingChatWidget;
