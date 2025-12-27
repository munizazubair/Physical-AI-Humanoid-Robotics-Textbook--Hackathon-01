import React from 'react';
import FloatingChatWidget from '../components/FloatingChatWidget';

/**
 * Root Component
 *
 * Wraps the entire Docusaurus application.
 * This is the ideal place to add global components like the floating chat widget.
 */
export default function Root({ children }) {
  return (
    <>
      {children}
      <FloatingChatWidget />
    </>
  );
}
