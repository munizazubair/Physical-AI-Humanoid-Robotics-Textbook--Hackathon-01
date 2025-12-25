import React from 'react';
import Link from '@docusaurus/Link';

export default function Footer() {
  return (
    <footer className="footer-custom">
      <div className="container">
        <div className="footer-custom__content">
          <p className="footer-custom__copyright">
            © 2025 RoboTextbook. Built with Docusaurus.
          </p>
          <div className="footer-custom__links">
            <Link to="https://github.com/munizazubair/Physical-AI-Humanoid-Robotics-Textbook--Hackathon-01">
              GitHub
            </Link>
            <span className="footer-custom__separator">•</span>
            <Link to="/intro">
              Documentation
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
