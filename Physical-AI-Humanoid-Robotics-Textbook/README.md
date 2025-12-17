# Physical AI & Humanoid Robotics Textbook

A comprehensive educational resource covering Physical AI, ROS 2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action systems for humanoid robotics.

## 📚 Content Modules

- **Foundation** (Chapters 1-2): Physical AI concepts and humanoid architecture
- **Module 1: ROS 2** (Chapters 3-6): Robotic middleware and system integration
- **Module 2: Digital Twin** (Chapters 7-10): Simulation with Gazebo and Unity
- **Module 3: NVIDIA Isaac** (Chapters 11-14): GPU-accelerated AI robotics
- **Module 4: VLA** (Chapters 15-18): Vision-Language-Action systems

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The site will open at `http://localhost:3000/Physical-AI-Humanoid-Robotics-Textbook/`

### Build for Production

```bash
# Build static site
npm run build

# Test production build locally
npm run serve
```

## 🌐 Deployment

This textbook is deployed to GitHub Pages using GitHub Actions.

### Setup GitHub Pages

1. Go to repository Settings → Pages
2. Set **Source** to "Deploy from a branch"
3. Set **Branch** to `gh-pages` and folder to `/ (root)`
4. Save settings

The workflow will automatically:
- Build the site on every push to `main`
- Deploy to `gh-pages` branch
- Make the site available at `https://SIBGHAT.github.io/Physical-AI-Humanoid-Robotics-Textbook/`

### Preview Builds

Pull requests generate preview builds but do not deploy to production. Only merges to `main` trigger deployment.

## 📖 Tech Stack

- **Framework**: Docusaurus 3.x
- **Content**: MDX (Markdown + JSX)
- **Diagrams**: SVG (exported from Lucidchart/Figma)
- **Deployment**: GitHub Pages via GitHub Actions
- **CI/CD**: Automated on merge to main

## 🎯 Target Audience

This textbook is designed for:
- Developers with basic programming knowledge
- Students learning robotics and AI
- Researchers seeking conceptual clarity
- Anyone curious about how humanoid robots work

**Prerequisites**: Basic programming (variables, functions, control flow). No robotics experience required.

## 📝 Content Standards

- **Conceptual Focus**: What and why, not implementation details
- **Standalone Chapters**: Read in any order
- **Learning Objectives**: Clear goals for each chapter
- **Diagrams**: Visual aids for complex systems
- **Pseudo-code**: Representative patterns, not full implementations

## 🔄 Continuous Deployment

This textbook follows a continuous deployment model:
- Content updates deploy automatically
- No formal versioning
- Always up-to-date with latest knowledge

## 🛠️ Built With

- Spec-Kit Plus
- Claude Code
- Context7 MCP (for up-to-date documentation access)
- Docusaurus

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is an educational project. For suggestions or corrections, please open an issue.

---

**Status**: Phase 1 Complete - Docusaurus infrastructure deployed ✅
