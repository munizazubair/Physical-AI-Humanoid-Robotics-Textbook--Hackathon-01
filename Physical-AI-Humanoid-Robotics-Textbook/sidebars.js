/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Main tutorial sidebar
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Foundation',
      items: [
        'foundation/01-intro-physical-ai',
        'foundation/02-humanoid-architecture',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2',
      items: [
        'module-1-ros2/03-intro-ros2',
        'module-1-ros2/04-nodes-topics',
        'module-1-ros2/05-services-actions',
        'module-1-ros2/06-system-integration',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin',
      items: [
        'module-2-digital-twin/07-intro-digital-twins',
        'module-2-digital-twin/08-gazebo',
        'module-2-digital-twin/09-unity',
        'module-2-digital-twin/10-sim-to-real',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac',
      items: [
        'module-3-nvidia-isaac/11-intro-isaac',
        'module-3-nvidia-isaac/12-isaac-sim',
        'module-3-nvidia-isaac/13-isaac-ros',
        'module-3-nvidia-isaac/14-isaac-gym',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: VLA Capstone',
      items: [
        'module-4-vla/15-intro-vla',
        'module-4-vla/16-vision-systems',
        'module-4-vla/17-llm-action-planning',
        'module-4-vla/18-capstone',
      ],
    },
  ],
};

module.exports = sidebars;
