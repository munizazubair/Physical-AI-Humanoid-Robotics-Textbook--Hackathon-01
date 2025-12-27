import React, { useState } from 'react';
import styles from './FeedbackButtons.module.css';

/**
 * FeedbackButtons Component
 *
 * Displays thumbs up/down buttons for user feedback on assistant messages.
 */
const FeedbackButtons = ({ messageId, onFeedbackSubmit }) => {
  const [feedback, setFeedback] = useState(null); // 'up' or 'down' or null
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showThankYou, setShowThankYou] = useState(false);

  const handleFeedback = async (rating) => {
    if (feedback || isSubmitting) return; // Already submitted or submitting

    setIsSubmitting(true);

    try {
      const response = await fetch('http://localhost:8000/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message_id: messageId,
          rating: rating === 'up' ? 1 : -1,
        }),
      });

      if (response.ok) {
        setFeedback(rating);
        setShowThankYou(true);
        if (onFeedbackSubmit) {
          onFeedbackSubmit(rating);
        }
        // Hide thank you message after 3 seconds
        setTimeout(() => setShowThankYou(false), 3000);
      } else {
        console.error('Failed to submit feedback');
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.feedbackContainer}>
      {showThankYou && (
        <div className={styles.thankYouMessage}>Thank you for your feedback!</div>
      )}
      <div className={styles.feedbackButtons}>
        <button
          className={`${styles.feedbackButton} ${feedback === 'up' ? styles.active : ''}`}
          onClick={() => handleFeedback('up')}
          disabled={feedback !== null || isSubmitting}
          title="Helpful response"
          aria-label="Thumbs up"
        >
          👍
        </button>
        <button
          className={`${styles.feedbackButton} ${feedback === 'down' ? styles.active : ''}`}
          onClick={() => handleFeedback('down')}
          disabled={feedback !== null || isSubmitting}
          title="Not helpful"
          aria-label="Thumbs down"
        >
          👎
        </button>
      </div>
    </div>
  );
};

export default FeedbackButtons;
