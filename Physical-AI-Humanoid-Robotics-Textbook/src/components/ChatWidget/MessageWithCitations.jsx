import React from 'react';
import { Message } from '@chatscope/chat-ui-kit-react';
import CitationList from './CitationList';
import FeedbackButtons from './FeedbackButtons';
import styles from './MessageWithCitations.module.css';

/**
 * MessageWithCitations Component
 *
 * A wrapper around the chat-ui-kit Message component that adds citation support.
 * Displays assistant messages with citations and feedback buttons below the message text.
 */
const MessageWithCitations = ({ message, citations, isOffTopic, messageId, ...messageProps }) => {
  return (
    <div className={styles.messageContainer}>
      <Message {...messageProps} />

      {/* Show off-topic badge if applicable */}
      {isOffTopic && (
        <div className={styles.offTopicBadge}>
          <span className={styles.offTopicIcon}>ℹ️</span>
          <span className={styles.offTopicText}>
            This question appears to be outside the scope of the textbook.
          </span>
        </div>
      )}

      {/* Show citations if available */}
      {citations && citations.length > 0 && (
        <div className={styles.citationsWrapper}>
          <CitationList citations={citations} />
        </div>
      )}

      {/* Show feedback buttons for assistant messages */}
      {!isOffTopic && messageId && (
        <div className={styles.feedbackWrapper}>
          <FeedbackButtons messageId={messageId} />
        </div>
      )}
    </div>
  );
};

export default MessageWithCitations;
