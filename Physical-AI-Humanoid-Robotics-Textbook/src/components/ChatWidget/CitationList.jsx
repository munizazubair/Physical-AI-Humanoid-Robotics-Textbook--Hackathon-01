import React from 'react';
import styles from './CitationList.module.css';

/**
 * CitationList Component
 *
 * Displays a list of citations for an assistant message.
 * Citations are clickable and link to the relevant sections in the textbook.
 */
const CitationList = ({ citations }) => {
  if (!citations || citations.length === 0) {
    return null;
  }

  /**
   * Get icon for content type
   */
  const getContentTypeIcon = (contentType) => {
    switch (contentType) {
      case 'code':
        return '💻';
      case 'diagram':
        return '📊';
      case 'text':
      default:
        return '📄';
    }
  };

  /**
   * Get tooltip text for content type
   */
  const getContentTypeTooltip = (contentType) => {
    switch (contentType) {
      case 'code':
        return 'Code Example';
      case 'diagram':
        return 'Diagram/Figure';
      case 'text':
      default:
        return 'Text Content';
    }
  };

  /**
   * Parse citation text to extract chapter and section
   * Expected format: "[Chapter X, Section Y]" or "[Chapter X]"
   */
  const parseCitation = (citationText) => {
    const chapterMatch = citationText.match(/Chapter\s+(\d+)/i);
    const sectionMatch = citationText.match(/Section\s+([\d.]+)/i);

    return {
      chapter: chapterMatch ? chapterMatch[1] : null,
      section: sectionMatch ? sectionMatch[1] : null,
      text: citationText,
    };
  };

  /**
   * Generate a link to the textbook section
   * TODO: Update the base URL to match your actual textbook structure
   */
  const generateLink = (citation) => {
    const parsed = parseCitation(citation.reference || citation);

    if (parsed.chapter) {
      // Assuming textbook chapters are at /chapter-{number}
      const baseUrl = `/chapter-${parsed.chapter}`;

      if (parsed.section) {
        // If section exists, link to specific section anchor
        return `${baseUrl}#section-${parsed.section.replace('.', '-')}`;
      }

      return baseUrl;
    }

    // Fallback to intro page if parsing fails
    return '/intro';
  };

  return (
    <div className={styles.citationList}>
      <div className={styles.citationHeader}>
        <span className={styles.citationIcon}>📚</span>
        <span className={styles.citationTitle}>References:</span>
      </div>
      <ul className={styles.citations}>
        {citations.map((citation, index) => {
          const citationText = typeof citation === 'string' ? citation : citation.text || citation.reference;
          const contentType = typeof citation === 'object' ? citation.content_type : 'text';
          const link = generateLink(citation);
          const icon = getContentTypeIcon(contentType);
          const tooltip = getContentTypeTooltip(contentType);

          return (
            <li key={index} className={styles.citationItem}>
              <span
                className={styles.contentTypeIcon}
                title={tooltip}
                role="img"
                aria-label={tooltip}
              >
                {icon}
              </span>
              <a
                href={link}
                className={styles.citationLink}
                target="_self"
                rel="noopener"
              >
                {citationText}
              </a>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default CitationList;
