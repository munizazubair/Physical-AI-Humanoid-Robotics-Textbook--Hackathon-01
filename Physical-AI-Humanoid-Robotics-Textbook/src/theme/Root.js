import React from 'react';
import FloatingChatWidget from '../components/FloatingChatWidget';

/**
 * Error Boundary for FloatingChatWidget
 * Prevents the chat widget from crashing the entire app
 */
class ChatWidgetErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ChatWidget Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return null; // Fail gracefully - don't show chat widget if it errors
    }
    return this.props.children;
  }
}

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
      <ChatWidgetErrorBoundary>
        <FloatingChatWidget />
      </ChatWidgetErrorBoundary>
    </>
  );
}
