import React from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';

const features = [
  {
    title: 'Module 1: ROS 2',
    icon: 'img/modules/ros2.svg',
    description: 'Learn the nervous system of robots. Understand nodes, topics, services, and how subsystems communicate.',
    link: '/module-1-ros2/03-intro-ros2'
  },
  {
    title: 'Module 2: Digital Twins',
    icon: 'img/modules/digital-twin.svg',
    description: 'Simulate robots safely. Master Gazebo, Unity, and Sim-to-Real transfer techniques.',
    link: '/module-2-digital-twin/07-intro-digital-twins'
  },
  {
    title: 'Module 3: NVIDIA Isaac',
    icon: 'img/modules/isaac.svg',
    description: 'Accelerate AI robotics. Train perception and control models with GPU-powered simulation.',
    link: '/module-3-nvidia-isaac/11-intro-isaac'
  },
  {
    title: 'Module 4: VLA Systems',
    icon: 'img/modules/vla.svg',
    description: 'Connect language to action. Build robots that understand voice commands and execute tasks.',
    link: '/module-4-vla/15-intro-vla'
  }
];

export default function FeatureCards() {
  return (
    <section className="features" id='modules'>
      <div className="container">
        <div className="features__grid">
          {features.map((feature, idx) => (
            <Link
              key={idx}
              to={feature.link}
              className="feature-card"
              style={{ textDecoration: 'none' }}
            >
              <div className="feature-card__content">
                <img
                  src={useBaseUrl(feature.icon)}
                  alt={`${feature.title} icon`}
                  className="feature-card__icon"
                />
                <h3 className="feature-card__title">{feature.title}</h3>
                <p className="feature-card__description">{feature.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
