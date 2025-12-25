import React from 'react';
import Link from '@docusaurus/Link';

export default function CTASection() {
  return (
    <section className="cta-section">
      <div className="container">
        <div className="cta-section__content">
          <h2 className="cta-section__title">Ready to Build the Future of Robotics?</h2>
          <p className="cta-section__subtitle">
            From fundamentals to cutting-edge AI systems, start your journey today.
          </p>
          <div className="cta-section__buttons">
            <Link
              to="/intro"
              className="button button--primary button--lg"
            >
              Start Reading
            </Link>
            
          </div>
        </div>
      </div>
    </section>
  );
}
