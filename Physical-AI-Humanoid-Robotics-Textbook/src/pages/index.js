import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import FeatureCards from '@site/src/components/FeatureCards';
import CTASection from '@site/src/components/CTASection';
import Footer from '@site/src/components/Footer';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <Layout
      title="RoboTextbook - Master Physical AI & Robotics"
      description="A comprehensive guide to Physical AI, ROS 2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action systems for students and developers">
      <main>
        {/* Hero Section */}
        <div className="hero">
          <div className="hero__content">
            <h1 className="hero__title">RoboTextbook</h1>
            <p className="hero__subtitle">
              Master Physical AI, ROS 2, Digital Twins, and Vision-Language-Action Robotics
            </p>
            <div className="hero__cta">
              <Link to="/intro" className="button button--primary button--lg">
                Start Reading
              </Link>
              <Link to="#modules" className="button button--secondary button--lg ">
                Explore Modules
              </Link>
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <FeatureCards />

        {/* CTA Section */}
        <CTASection />
      </main>

      {/* Footer */}
      <Footer />
    </Layout>
  );
}
