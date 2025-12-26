---
id: 031
title: RoboTextbook Landing Page Redesign Tasks
stage: tasks
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-robotics-book
branch: 001-physical-ai-robotics-book
user: SIBGHAT
command: /sp.tasks
labels: ["tasks", "landing-page", "redesign", "robotextbook", "branding"]
links:
  spec: specs/001-physical-ai-robotics-book/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-robotics-book/tasks.md
tests: []
---

# Prompt History Record: RoboTextbook Landing Page Redesign Tasks

## Prompt Text

User executed `/sp.tasks` command with detailed requirements for a branded landing page redesign:

"make tasks for Design a professional, modern landing page for a robotics education book titled 'RoboTextbook'.

The hero section must feature a continuous rotating logo of a toy-style cartoon robot face, inspired by friendly educational robotics (not realistic, not humanoid), suitable for students and beginners.

**Logo Design Requirements:**
- Robot face only (no body)
- Friendly, intelligent, futuristic cartoon style
- Continuous smooth rotation animation (360° loop)
- Centered in the hero section
- Styled as a premium book logo

**Color Theme:**
- Primary colors: Black and Yellow
- Secondary accents: metallic gray, soft cyan, subtle white highlights
- High contrast, modern, tech-focused palette

**Typography:**
- Professional, bold, futuristic sans-serif fonts
- Strong hierarchy: Large bold title 'RoboTextbook', clean subtitle explaining robotics, AI, and learning
- Typography should feel academic + tech startup level

**Buttons & UI Elements:**
- CTA buttons: 'Start Reading' [...]"

(User message appears truncated but requirements are clear)

## Response Summary

### Analysis

**User Intent:** Complete redesign of the landing page with new "RoboTextbook" branding, featuring:
1. Rotating cartoon robot logo (toy-style, educational, friendly)
2. Black/yellow high-contrast color scheme
3. Futuristic typography (academic + tech startup aesthetic)
4. Modern educational design targeting students/beginners

**Current State:**
- Docusaurus site with content complete
- Missing: Custom landing page (`src/pages/index.js`)
- Existing theme: Default Docusaurus (blue/white)

### Task Generation Strategy

**Organized into 4 Phases:**
1. **Phase 1:** Logo & Assets Creation (4 tasks)
2. **Phase 2:** Landing Page Components (6 tasks)
3. **Phase 3:** Styling & Animation (5 tasks)
4. **Phase 4:** Deployment & Validation (2 tasks)

**Total:** 17 tasks, all pending

### Tasks Created

**Phase 1: Logo & Assets (Parallelizable)**
- T001: Design robot face logo SVG with black/yellow/cyan theme
- T002: Generate multi-resolution favicon from logo
- T003: Create 4 module icons (ROS 2, Digital Twin, Isaac, VLA)
- T004: Design social card for Open Graph sharing (1200x630px)

**Phase 2: Landing Page Components**
- T005: Create landing page structure (`src/pages/index.js`)
- T006: Implement hero section with rotating logo, title, subtitle, CTAs
- T007: Build feature cards component (4 modules in 2x2 grid)
- T008: Add secondary CTA section ("Ready to Build the Future of Robotics?")
- T009: Create footer component
- T010: Integrate all sections into landing page

**Phase 3: Styling & Animation**
- T011: Define CSS color variables (black/yellow theme)
- T012: Style hero section with gradient background
- T013: Implement 360° rotation animation (20s, linear, infinite)
- T014: Style feature cards with hover effects (lift + shadow)
- T015: Add responsive breakpoints (mobile/tablet/desktop)

**Phase 4: Deployment**
- T016: Update `docusaurus.config.js` (title, favicon, social card)
- T017: Validate build, test animations, verify responsiveness

### Key Implementation Details

**Logo Animation:**
```css
@keyframes rotate360 {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.hero__logo--rotating {
  animation: rotate360 20s linear infinite;
}
```

**Color Palette:**
- Black: `#000000` (backgrounds)
- Yellow: `#FFD700` (primary accent)
- Gray: `#C0C0C0` (secondary)
- Cyan: `#00CED1` (highlights)
- White: `#FFFFFF` (text)

**Typography:**
- Primary: Exo 2 (futuristic, bold)
- Body: Inter (clean, readable)

**Responsive Design:**
- Desktop: 2x2 grid, 4rem title, 200px logo
- Mobile: 1 column, 2.5rem title, 150px logo

### Format Validation

✅ **All tasks follow checklist format:**
- Checkbox: `- [ ]`
- Task ID: T001-T017 (sequential)
- [P] markers: T001, T002, T003 (parallel asset creation), T009 (footer)
- File paths: All tasks specify exact file locations
- Descriptions: Clear, actionable with acceptance criteria

### Documentation Enhancements

**Added to tasks.md:**
- SVG design template for robot logo
- Complete code templates for React components
- CSS variable definitions
- Animation keyframes
- Responsive media queries
- Validation commands
- Color palette reference table
- Font loading instructions
- Dependency graph visualization

## Evaluation

| Criteria | Status |
|----------|--------|
| Tasks organized by phase | ✅ Yes (4 phases) |
| All tasks follow checklist format | ✅ Yes (17/17) |
| File paths specified | ✅ Yes |
| Parallel opportunities identified | ✅ Yes (T001-T004, T009) |
| Implementation guidance provided | ✅ Yes (code templates, examples) |
| Acceptance criteria defined | ✅ Yes (detailed per task) |
| Dependency graph included | ✅ Yes |
| Responsive design addressed | ✅ Yes (T015) |
| Animation specifications | ✅ Yes (rotation details) |
| Branding requirements captured | ✅ Yes (black/yellow, robot logo) |

## Outcome

**Status:** ✅ Complete

**New tasks.md Structure:**
- 17 tasks across 4 phases
- 0% complete (all pending)
- Execution order: Assets → Components → Styling → Deployment
- Estimated effort: 6-8 hours

**Parallel Execution Opportunities:**
- Phase 1: All 4 asset tasks can run in parallel
- T009 (Footer) independent of T005-T008

**MVP Scope:**
- All 17 tasks required (no optional tasks)
- Critical path: T001 → T005 → T006 → T011 → T013 → T017

**Branding Changes:**
- Title: "Physical AI & Humanoid Robotics" → "RoboTextbook"
- Theme: Default Docusaurus blue/white → Black/yellow educational
- Logo: Generic → Custom rotating robot face
- Audience: General → Students/beginners

**Next Steps:** User can run `/sp.implement` to execute tasks, starting with Phase 1 (asset creation).

**File Updated:** `specs/001-physical-ai-robotics-book/tasks.md`

**PHR Created:** 031-robotextbook-landing-redesign.tasks.prompt.md
