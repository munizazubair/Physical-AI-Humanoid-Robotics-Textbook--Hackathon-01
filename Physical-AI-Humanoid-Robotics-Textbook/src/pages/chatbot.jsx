import React from 'react';
import Layout from '@theme/Layout';
import ChatWidget from '../components/ChatWidget';
import styles from './chatbot.module.css';

/**
 * Chatbot Demo Page
 *
 * A standalone page showcasing the RAG chatbot for the Physical AI textbook.
 * Users can interact with the AI assistant to ask questions about the textbook content.
 */
export default function ChatbotPage() {
  return (
    <Layout
      title="AI Chatbot Assistant"
      description="Ask questions about the Physical AI & Humanoid Robotics Textbook and get instant answers powered by AI"
    >
      <div className={styles.chatbotPage}>
        <div className={styles.header}>
          <h1>AI Chatbot Assistant</h1>
          <p>
            Ask me anything about Physical AI, ROS 2, Digital Twins, NVIDIA Isaac,
            Vision-Language-Action systems, or humanoid robotics!
          </p>
        </div>

        <div className={styles.chatContainer}>
          <ChatWidget />
        </div>

        <div className={styles.footer}>
          <p className={styles.disclaimer}>
            <strong>Note:</strong> This AI assistant is powered by retrieval-augmented generation (RAG)
            using content from the Physical AI & Humanoid Robotics Textbook. Responses include citations
            to relevant sections for further reading.
          </p>
        </div>
      </div>
    </Layout>
  );
}
