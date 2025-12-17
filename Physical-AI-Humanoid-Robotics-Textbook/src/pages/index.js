import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Reading
          </Link>
        </div>
      </div>
    </header>
  );
}

const FeatureList = [
  {
    title: 'Module 1: ROS 2 Foundations',
    description: (
      <>
        Learn the communication backbone of robotics. Understand nodes, topics,
        services, and actions - the primitives that enable humanoid robot systems
        to operate as coordinated systems.
      </>
    ),
    link: '/docs/module-1-ros2/03-intro-ros2',
  },
  {
    title: 'Module 2: Digital Twins',
    description: (
      <>
        Explore simulation environments with Gazebo and Unity. Master the
        Sim-to-Real transfer process and understand how digital twins accelerate
        robotics development safely and efficiently.
      </>
    ),
    link: '/docs/module-2-digital-twin/07-intro-digital-twins',
  },
  {
    title: 'Module 3: NVIDIA Isaac',
    description: (
      <>
        Discover GPU-accelerated robotics with NVIDIA Isaac Sim, Isaac ROS,
        and Isaac Gym. Learn how AI models integrate with robotic perception,
        planning, and control pipelines.
      </>
    ),
    link: '/docs/module-3-nvidia-isaac/11-intro-isaac',
  },
  {
    title: 'Module 4: Vision-Language-Action',
    description: (
      <>
        Master the cutting-edge VLA pipeline connecting vision, language models,
        and robotic action. Build understanding of voice-commanded humanoid robots
        that understand and execute natural language instructions.
      </>
    ),
    link: '/docs/module-4-vla/15-intro-vla',
  },
];

function Feature({title, description, link}) {
  return (
    <div className={clsx('col col--6', styles.feature)}>
      <div className={styles.featureCard}>
        <h3>{title}</h3>
        <p>{description}</p>
        <Link className="button button--primary button--sm" to={link}>
          Explore Module
        </Link>
      </div>
    </div>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

function HomepageAbout() {
  return (
    <section className={styles.about}>
      <div className="container">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <h2>About This Textbook</h2>
            <p>
              Physical AI represents the next frontier in artificial intelligence -
              AI systems that understand and interact with the physical world through
              embodied robotic systems. This comprehensive textbook guides you from
              foundational concepts to cutting-edge Vision-Language-Action systems.
            </p>
            <p>
              Whether you're a student, developer, or researcher, this book provides
              the conceptual understanding needed to work with humanoid robotics,
              simulation environments, and AI-driven control systems.
            </p>
            <div className={styles.buttons}>
              <Link
                className="button button--primary button--lg"
                to="/docs/foundation/01-intro-physical-ai">
                Begin with Chapter 1
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive guide to Physical AI, ROS 2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action systems for humanoid robotics">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <HomepageAbout />
      </main>
    </Layout>
  );
}
