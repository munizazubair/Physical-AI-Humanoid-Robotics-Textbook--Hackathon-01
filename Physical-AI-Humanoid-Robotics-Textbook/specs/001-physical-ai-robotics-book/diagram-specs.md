# Diagram Specifications: Physical AI & Humanoid Robotics Book

**Feature**: Physical AI & Humanoid Robotics Book
**Created**: 2025-12-16
**Purpose**: Define standards for all visual diagrams
**Compliance**: FR-019 (Professional diagramming tools, SVG export, consistent styling)

---

## Table of Contents

1. [Tooling Requirements](#1-tooling-requirements)
2. [File Format Standards](#2-file-format-standards)
3. [Style Guidelines](#3-style-guidelines)
4. [Diagram Types](#4-diagram-types)
5. [Naming Conventions](#5-naming-conventions)
6. [Accessibility Requirements](#6-accessibility-requirements)
7. [Quality Checklist](#7-quality-checklist)

---

## 1. Tooling Requirements

### Approved Professional Tools

**Primary Options** (must use one of the following):
1. **Lucidchart** (https://www.lucidchart.com)
   - Pros: Professional templates, SVG export, collaboration
   - Use for: System diagrams, flowcharts, architecture diagrams

2. **Figma** (https://www.figma.com)
   - Pros: Vector-based, precise control, design system support
   - Use for: UI mockups, detailed technical illustrations

3. **Draw.io / diagrams.net** (https://app.diagrams.net)
   - Pros: Free, open-source, SVG native, extensive libraries
   - Use for: All diagram types, good for robotics symbols

**Prohibited Tools**:
- ❌ PowerPoint / Keynote (raster-based, inconsistent quality)
- ❌ Hand-drawn diagrams (not professional quality)
- ❌ Screenshot-based diagrams (low resolution)
- ❌ MS Paint or similar raster tools

### Tool-Specific Export Settings

**Lucidchart**:
- Export format: SVG
- Options: "Use CSS" enabled, "Responsive" enabled
- Resolution: Vector (no rasterization)

**Figma**:
- Export format: SVG
- Settings: "Outline stroke" disabled, "Include 'id' attribute" enabled
- Compression: None (keep human-readable)

**Draw.io**:
- Export format: SVG
- Options: "Embed Images" disabled, "Include a copy of my diagram" enabled
- Border: 0px (managed by Docusaurus)

---

## 2. File Format Standards

### Required Format

**Format**: SVG (Scalable Vector Graphics)
**Version**: SVG 1.1 or SVG 2.0
**Encoding**: UTF-8
**Compression**: None (plain SVG, not SVGZ)

### File Size Limits

**Maximum file size**: 500 KB per diagram
**Optimization**: Use SVGO or similar tools if exceeding limit
**Fallback**: PNG at 2x resolution (1600px width) if SVG optimization fails

### Metadata Requirements

All SVG files must include:
```xml
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 800 600"
     aria-labelledby="diagram-title"
     role="img">
  <title id="diagram-title">Descriptive Title</title>
  <desc>Detailed description for accessibility</desc>
  <!-- Diagram content -->
</svg>
```

---

## 3. Style Guidelines

### Color Palette

**Primary Colors** (use for main elements):
- **Blue**: `#2563EB` (primary elements, nodes)
- **Green**: `#10B981` (success states, data flow)
- **Orange**: `#F59E0B` (warnings, highlights)
- **Red**: `#EF4444` (errors, critical paths)
- **Gray**: `#6B7280` (secondary text, borders)

**Background Colors**:
- **White**: `#FFFFFF` (default background)
- **Light Gray**: `#F9FAFB` (secondary backgrounds)

**Accent Colors** (use sparingly):
- **Purple**: `#8B5CF6` (special elements)
- **Teal**: `#14B8A6` (alternative highlights)

### Typography

**Fonts**:
- **Primary**: Arial, Helvetica, sans-serif
- **Monospace** (for code/technical): "Courier New", monospace
- **Fallback**: System fonts (ensure broad compatibility)

**Font Sizes**:
- **Title**: 18-20px (diagram title, if included in SVG)
- **Labels**: 14-16px (main labels for nodes, boxes)
- **Annotations**: 12-14px (descriptions, notes)
- **Code/Technical**: 11-13px (code snippets, terminal text)

**Font Weights**:
- **Bold** (600-700): Titles, important labels
- **Regular** (400): Standard text
- **Light** (300): Avoid (poor readability)

### Line Styles

**Stroke Widths**:
- **Primary lines**: 2px (boxes, main shapes)
- **Connections/Arrows**: 1.5-2px (data flow, relationships)
- **Secondary lines**: 1px (grid lines, minor elements)

**Line Types**:
- **Solid**: Primary relationships, definite connections
- **Dashed** (4px dash, 4px gap): Optional paths, weak relationships
- **Dotted** (2px dash, 3px gap): Background elements, auxiliary info

**Arrow Styles**:
- **Filled triangle**: Data flow, strong direction
- **Open triangle**: Weak direction, optional flow
- **No arrow**: Bidirectional or undirected connections

### Spacing and Layout

**Margins**:
- **Outer margin**: 20px from SVG viewBox edge
- **Element spacing**: 30-40px between major components
- **Label spacing**: 8-12px from shapes

**Alignment**:
- **Grid system**: Use 10px grid for alignment
- **Centering**: Center diagrams within viewBox
- **Consistency**: Maintain consistent spacing across similar diagrams

---

## 4. Diagram Types

### System Architecture Diagrams

**Purpose**: Show high-level system components and their relationships

**Required Elements**:
- Rectangular boxes for components
- Labeled arrows for data/control flow
- Grouping boxes for subsystems (dashed borders)
- Legend if using special symbols

**Example Diagrams**:
- Digital AI vs. Physical AI (Chapter 1)
- Humanoid layered architecture (Chapter 2)
- Complete ROS 2 system (Chapter 6)

**Style Notes**:
- Use blue for software components
- Use green for data flows
- Use orange for hardware components

---

### Data Flow Diagrams

**Purpose**: Illustrate how data moves through the system

**Required Elements**:
- Circular/rounded nodes for processes
- Arrows showing data direction
- Labels on all arrows indicating data type
- Start/end points clearly marked

**Example Diagrams**:
- Sensor-actuator feedback loop (Chapter 1)
- ROS 2 topic communication (Chapter 4)
- Isaac ROS perception pipeline (Chapter 12)

**Style Notes**:
- Use green for data flows
- Use blue for processing nodes
- Use solid arrows for primary flow
- Use dashed arrows for feedback loops

---

### Comparison Tables

**Purpose**: Side-by-side comparison of technologies or concepts

**Required Elements**:
- Clear column headers
- Row labels for features
- Checkmarks (✓) or cross marks (✗) for boolean values
- Brief text for descriptive values

**Example Diagrams**:
- ROS 1 vs. ROS 2 comparison (Chapter 3)
- Gazebo vs. Unity comparison (Chapter 9)

**Style Notes**:
- Use alternating row colors (white, light gray)
- Bold headers
- Center-align symbols, left-align text

---

### State Diagrams

**Purpose**: Show system states and transitions

**Required Elements**:
- Rounded rectangles for states
- Arrows for transitions
- Labels on transitions (trigger events)
- Start (filled circle) and end (double circle) states

**Example Diagrams**:
- Robot lifecycle states
- Action execution flow (Chapter 5)

**Style Notes**:
- Use blue for normal states
- Use green for success states
- Use red for error states
- Use gray for inactive states

---

### Sequence Diagrams

**Purpose**: Show interactions over time between components

**Required Elements**:
- Vertical lifelines for each component
- Horizontal arrows for messages
- Numbered steps (optional)
- Time flows top to bottom

**Example Diagrams**:
- Service call sequence (Chapter 5)
- VLA execution pipeline (Chapter 18)

**Style Notes**:
- Use dashed lines for lifelines
- Use solid arrows for synchronous calls
- Use open arrows for asynchronous messages

---

## 5. Naming Conventions

### File Naming Pattern

**Format**: `{module}-{chapter}-{diagram-number}-{short-description}.svg`

**Examples**:
- `foundation-01-01-digital-vs-physical-ai.svg`
- `foundation-01-02-sensor-actuator-loop.svg`
- `ros2-03-01-ros2-ecosystem.svg`
- `ros2-04-01-node-topic-message-flow.svg`

**Rules**:
- All lowercase
- Hyphens for word separation (no underscores or spaces)
- Module prefix: `foundation`, `ros2`, `digital-twin`, `isaac`, `vla`
- Chapter number: Two digits (01-18)
- Diagram number: Two digits (01-99)
- Short description: 2-5 words

### Storage Location

**Path**: `Physical-AI-Humanoid-Robotics-Textbook/static/img/diagrams/`

**Subdirectories** (by module):
```
static/img/diagrams/
├── foundation/
│   ├── foundation-01-01-digital-vs-physical-ai.svg
│   └── foundation-01-02-sensor-actuator-loop.svg
├── ros2/
│   ├── ros2-03-01-ros2-ecosystem.svg
│   └── ros2-04-01-node-topic-message-flow.svg
├── digital-twin/
├── isaac/
└── vla/
```

---

## 6. Accessibility Requirements

### Alt Text and Descriptions

**Requirements**:
1. Every SVG must have `<title>` element (diagram name)
2. Every SVG must have `<desc>` element (detailed description)
3. Complex diagrams must have `aria-describedby` pointing to external description

**Example**:
```xml
<svg aria-labelledby="ros2-title" aria-describedby="ros2-desc">
  <title id="ros2-title">ROS 2 Node Communication</title>
  <desc id="ros2-desc">
    Diagram showing three ROS 2 nodes: Camera Node publishes to /image topic,
    Navigation Node subscribes to /image and publishes to /cmd_vel,
    Motor Node subscribes to /cmd_vel.
  </desc>
  <!-- Diagram content -->
</svg>
```

### Color Contrast

**Requirements**:
- Text must have 4.5:1 contrast ratio against background (WCAG AA)
- Important elements must have 3:1 contrast ratio
- Do not rely on color alone to convey information (use labels, patterns)

**Testing**: Use WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/)

### Keyboard Navigation

**Not applicable**: Static diagrams do not require keyboard navigation
**Exception**: Interactive diagrams (if added later) must support keyboard controls

---

## 7. Quality Checklist

### Pre-Export Checklist

Before exporting any diagram, verify:

- [ ] Created with approved professional tool (Lucidchart, Figma, or Draw.io)
- [ ] Uses approved color palette
- [ ] Font sizes within specified ranges (12-18px)
- [ ] Consistent line widths (1-2px)
- [ ] Proper spacing and alignment
- [ ] All text is legible at 100% zoom
- [ ] No spelling or grammar errors in labels
- [ ] Legend included (if needed)

### Post-Export Checklist

After exporting to SVG, verify:

- [ ] File is valid SVG (opens in browser without errors)
- [ ] File size under 500 KB
- [ ] `<title>` and `<desc>` elements present
- [ ] ViewBox attribute set correctly
- [ ] No embedded raster images (unless necessary)
- [ ] Colors match specification (check hex codes)
- [ ] File named according to convention
- [ ] Stored in correct directory

### Integration Checklist

When adding diagram to MDX file:

- [ ] Image imported or referenced correctly
- [ ] Alt text provided (even if SVG has title/desc)
- [ ] Caption added below diagram
- [ ] Diagram referenced in text ("as shown in Figure 1.1")
- [ ] Responsive sizing (`width: 100%`, `max-width: 800px`)
- [ ] Tested in both light and dark mode (Docusaurus themes)

**Example MDX Integration**:
```mdx
![Digital AI vs Physical AI](../../../static/img/diagrams/foundation/foundation-01-01-digital-vs-physical-ai.svg)

**Figure 1.1**: Comparison of Digital AI (left) processing abstract data versus Physical AI (right) interacting with the physical world through sensors and actuators.
```

---

## Diagram Inventory

### Foundation Module (4 diagrams)

| Diagram ID | File Name | Chapter | Description |
|------------|-----------|---------|-------------|
| 1.1 | foundation-01-01-digital-vs-physical-ai.svg | 1 | Digital AI vs. Physical AI comparison |
| 1.2 | foundation-01-02-sensor-actuator-loop.svg | 1 | Sensor-actuator feedback loop |
| 2.1 | foundation-02-01-layered-architecture.svg | 2 | Layered system architecture |
| 2.2 | foundation-02-02-data-flow.svg | 2 | Data flow from visual data to motor commands |

### ROS 2 Module (8 diagrams)

| Diagram ID | File Name | Chapter | Description |
|------------|-----------|---------|-------------|
| 3.1 | ros2-03-01-ros2-ecosystem.svg | 3 | High-level ROS 2 ecosystem |
| 3.2 | ros2-03-02-ros1-vs-ros2.svg | 3 | ROS 1 vs ROS 2 comparison table |
| 4.1 | ros2-04-01-node-topic-message-flow.svg | 4 | Node-topic-message communication flow |
| 4.2 | ros2-04-02-multi-node-system.svg | 4 | Multi-node humanoid system |
| 5.1 | ros2-05-01-service-call-flow.svg | 5 | Service request-response flow |
| 5.2 | ros2-05-02-action-feedback-flow.svg | 5 | Action goal-feedback-result flow |
| 6.1 | ros2-06-01-complete-system.svg | 6 | Complete ROS 2 humanoid system |
| 6.2 | ros2-06-02-tf-tree.svg | 6 | TF coordinate frame tree |

*[Full inventory continues for all 36-42 diagrams across all modules]*

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-16 | Initial diagram specifications |

---

**File**: `specs/001-physical-ai-robotics-book/diagram-specs.md`
**Status**: Complete
**Compliance**: FR-019 ✅ (Professional tools, SVG export, consistent styling defined)
**Ready for**: Diagram creation (Phase 3+)
