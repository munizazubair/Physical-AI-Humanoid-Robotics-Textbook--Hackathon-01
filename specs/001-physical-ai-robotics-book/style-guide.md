# Style Guide: Physical AI & Humanoid Robotics Book

**Feature**: Physical AI & Humanoid Robotics Book
**Created**: 2025-12-16
**Purpose**: Define consistent writing style and formatting standards
**Compliance**: FR-020 (Consistent terminology, tone, and formatting)

---

## Table of Contents

1. [Writing Principles](#1-writing-principles)
2. [Voice and Tone](#2-voice-and-tone)
3. [Structure and Organization](#3-structure-and-organization)
4. [Terminology Standards](#4-terminology-standards)
5. [Code Examples](#5-code-examples)
6. [Formatting Conventions](#6-formatting-conventions)
7. [Accessibility Requirements](#7-accessibility-requirements)
8. [Review Checklist](#8-review-checklist)

---

## 1. Writing Principles

### Educational First

**Primary Principle**: Every chapter must teach, not just inform.

**Guidelines**:
- Start with "why" before "how"
- Use concrete examples before abstractions
- Build concepts progressively (known → unknown)
- Include real-world applications
- Answer common questions preemptively

**Example Structure**:
```markdown
❌ Bad: "ROS 2 uses DDS middleware."
✅ Good: "ROS 2 uses DDS middleware to ensure real-time communication.
This matters because humanoid robots need sub-millisecond response times
to maintain balance and avoid falls."
```

### Clarity Over Cleverness

**Principle**: Technical accuracy with accessible language.

**Guidelines**:
- Prefer simple words over jargon (unless teaching the term)
- Define technical terms on first use
- Use analogies for complex concepts
- Avoid unnecessary acronyms
- Break down complex sentences

**Readability Targets**:
- **Grade Level**: 10-12 (high school/college freshman)
- **Sentence Length**: 15-25 words average
- **Paragraph Length**: 3-5 sentences
- **Section Length**: 200-400 words per subsection

### Consistency

**Principle**: Same concepts, same terms, same style throughout.

**Guidelines**:
- Use approved terminology list (Section 4)
- Maintain parallel structure in lists
- Follow consistent heading hierarchy
- Use same code comment style
- Apply formatting rules uniformly

---

## 2. Voice and Tone

### Voice Characteristics

**Professional but Approachable**

- **Use**: "we", "you" (second person, active voice)
- **Avoid**: "one should", passive constructions
- **Example**:
  - ❌ "The node can be started by executing..."
  - ✅ "You can start the node by running..."

**Encouraging and Practical**

- Acknowledge challenges ("This concept is tricky...")
- Celebrate progress ("You've now mastered...")
- Provide practical next steps
- Focus on capabilities gained

**Technically Accurate**

- Cite sources for claims (APA format in footnotes)
- Distinguish facts from opinions ("typically", "usually" for generalizations)
- Admit unknowns ("This is an active research area...")
- Update with current information (as of 2025)

### Tone Guidelines

**Chapter Introductions**: Motivating, sets context
- "Imagine a humanoid robot navigating a crowded room..."

**Explanations**: Clear, patient, builds understanding
- "Let's break this down step by step..."

**Examples**: Concrete, relatable, tied to humanoid robotics
- "For instance, when a humanoid reaches for a cup..."

**Summaries**: Reinforcing, forward-looking
- "Now that you understand X, you're ready to explore Y..."

---

## 3. Structure and Organization

### Chapter Template

**Standard Structure** (800-1200 words):

1. **Introduction** (100-150 words)
   - Hook (analogy, question, scenario)
   - Learning objectives (3-4 bullet points)
   - Chapter roadmap

2. **Main Content** (600-900 words)
   - 3-5 major sections
   - Each section: concept → explanation → example
   - Diagrams integrated inline
   - Code examples with explanations

3. **Summary** (100-150 words)
   - Key takeaways (3-5 bullet points)
   - Preview next chapter
   - Suggested exercises (optional)

### Heading Hierarchy

**Levels and Usage**:

```markdown
# Chapter Title (H1) - Only one per file
## Major Section (H2) - Main divisions
### Subsection (H3) - Detailed topics
#### Minor Heading (H4) - Rarely needed

Avoid H5 and H6 (indicates over-organization)
```

**Heading Style**:
- Use sentence case ("Introduction to ROS 2", not "Introduction To ROS 2")
- Make headings descriptive ("Why Physical AI Matters" not "Introduction")
- Avoid questions in headings (use in body text instead)

### Lists and Enumerations

**Bulleted Lists** (unordered, parallel items):
```markdown
- First item starts with capital letter
- Second item also starts with capital
- No period at the end for fragments
- Use period for complete sentences.
```

**Numbered Lists** (sequential steps, ranked items):
```markdown
1. **Step One**: Description of what to do
2. **Step Two**: Next action to take
3. **Step Three**: Final step
```

**Definition Lists** (term + explanation):
```markdown
**Physical AI**: AI systems that interact with the physical world through sensors and actuators.

**Embodied Intelligence**: The idea that intelligence emerges from physical interaction with the environment.
```

---

## 4. Terminology Standards

### Core Terms (Alphabetical)

**Approved Terminology** (use consistently):

| Term | Usage | Avoid |
|------|-------|-------|
| **Physical AI** | Physical AI system, embodied AI | "Robotics AI", "embodied robot" |
| **Digital AI** | Digital-only AI, traditional AI | "Software AI", "virtual AI" |
| **Humanoid Robot** | Humanoid, humanoid robot | "Human-like robot", "android" (unless specifically Android OS) |
| **ROS 2** | ROS 2 (not ROS2), Robot Operating System 2 | "ROS version 2", "ROS-2" |
| **Digital Twin** | Digital twin, simulation twin | "Virtual twin", "sim model" (use "simulation" separately) |
| **Sensor-Actuator Loop** | Sensor-actuator feedback loop, perception-action cycle | "Sense-act loop", "feedback system" |
| **NVIDIA Isaac** | NVIDIA Isaac Sim, Isaac ROS | "Isaac Simulator", "NVidia Isaac" |
| **VLA** | Vision-Language-Action model, VLA model | "VLA system", "vision-language model" (different concept) |
| **Sim-to-Real** | Sim-to-real transfer, reality gap | "Sim2Real", "simulation transfer" |

### Capitalization Rules

**Proper Nouns**:
- ROS 2 (always capitalized)
- Gazebo (simulator name)
- Unity (game engine)
- NVIDIA Isaac (company + product)
- MoveIt 2 (motion planning library)

**Common Nouns**:
- sensor, actuator, node, topic, message
- digital twin (lowercase unless starting sentence)
- humanoid robot (lowercase)

**Acronyms**:
- Define on first use: "Vision-Language-Action (VLA)"
- Use acronym thereafter: "VLA models enable..."
- Common acronyms (assume known): AI, ROS, GPU, CPU, API

### Technical Term Definitions

**On First Use**:
```markdown
**Robot Operating System 2 (ROS 2)** is a middleware framework that...
[Continue explanation]

Later in text: "ROS 2 provides..."
```

**Glossary Terms** (link to glossary if created):
- Define inline on first use
- Mark with **bold** for emphasis
- Add to chapter glossary if needed

---

## 5. Code Examples

### Pseudo-Code Standards

**Purpose**: Illustrate concepts without language-specific syntax.

**Style**:
```pseudo
// Use clear, descriptive names
FUNCTION move_robot_arm(target_position):
    current_position = GET current joint angles
    trajectory = PLAN path from current_position to target_position

    FOR each point in trajectory:
        SEND joint commands to motors
        WAIT for motion completion
    END FOR

    RETURN success
END FUNCTION
```

**Rules**:
- Use ALL CAPS for keywords (FUNCTION, IF, FOR, RETURN)
- Use snake_case for variables and function names
- Include comments for clarity
- Keep examples under 20 lines
- Focus on logic, not syntax

### Language-Specific Code

**Python** (primary language for examples):
```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    """Example ROS 2 publisher node."""

    def __init__(self):
        super().__init__('minimal_publisher')
        # Create publisher for string messages
        self.publisher_ = self.create_publisher(String, 'topic', 10)

    def publish_message(self, text):
        """Publish a string message."""
        msg = String()
        msg.data = text
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')
```

**Code Style**:
- Follow PEP 8 for Python
- Include docstrings for functions/classes
- Add inline comments for non-obvious logic
- Use type hints where helpful
- Keep examples focused (one concept per snippet)

### Code Block Formatting

**Markdown Syntax**:
```markdown
```python
# Python code here
```
```

**Language Tags**:
- `python` - Python code
- `bash` - Terminal commands
- `yaml` - Configuration files
- `xml` - URDF, launch files
- `pseudo` - Pseudo-code

**Terminal Commands**:
```bash
# Install ROS 2 packages
sudo apt install ros-humble-demo-nodes-py

# Run a node
ros2 run demo_nodes_py talker
```

---

## 6. Formatting Conventions

### Text Formatting

**Bold** (`**bold**`):
- New terms on first use
- Important concepts
- UI elements ("Click the **Start** button")

**Italic** (`*italic*`):
- Emphasis ("This is *critical* for safety")
- Book/paper titles (*Digital Twin Applications*)
- Variable names in prose ("Set *x* to 10")

**Code** (`` `code` ``):
- Function names (`move_robot()`)
- Variable names (`joint_positions`)
- File names (`config.yaml`)
- Package names (`rclpy`)
- Commands (`ros2 run`)

**Links** (`[text](url)`):
- External references
- Cross-references within book
- Documentation links

### Special Elements

**Callout Boxes** (Docusaurus admonitions):

```markdown
:::note
Use notes for additional context or helpful tips.
:::

:::tip
Use tips for best practices and recommendations.
:::

:::warning
Use warnings for common mistakes or gotchas.
:::

:::danger
Use danger for critical safety or security issues.
:::
```

**Figures and Captions**:
```markdown
![Robot arm trajectory](../../../static/img/diagrams/foundation/foundation-02-02-data-flow.svg)

**Figure 2.2**: Data flow from visual perception to motor commands in a humanoid robot.
```

**Tables**:
```markdown
| Component | Purpose | Example |
|-----------|---------|---------|
| Sensor | Perceive environment | Camera, LiDAR |
| Actuator | Physical action | Motor, gripper |
| Controller | Decision making | PID, MPC |
```

### Mathematics

**Inline Math** (simple expressions):
- Use plain text with Unicode: "velocity = distance / time"
- Or LaTeX if Docusaurus supports: $v = \frac{d}{t}$

**Block Math** (equations):
```markdown
$$
\tau = J^T F
$$

Where:
- τ = joint torques
- J^T = Jacobian transpose
- F = endpoint force
```

---

## 7. Accessibility Requirements

### Writing for Accessibility

**Plain Language**:
- Use common words ("use" not "utilize")
- Explain technical terms
- Avoid idioms and cultural references
- Write in active voice

**Structure**:
- Use descriptive headings
- Break content into short sections
- Use lists for sequential information
- Provide clear transitions

### Visual Accessibility

**Images**:
- Every image must have alt text
- Alt text describes content, not "image of..."
- Complex diagrams need extended descriptions

```markdown
![Digital AI vs Physical AI comparison diagram showing digital AI processing abstract data on the left and Physical AI interacting with physical world through sensors and actuators on the right](../../../static/img/diagrams/foundation/foundation-01-01-digital-vs-physical-ai.svg)

**Figure 1.1**: Digital AI (left) processes abstract data, while Physical AI (right) interacts with the physical world through sensors and actuators.
```

**Code**:
- Use semantic HTML in MDX
- Maintain proper heading hierarchy
- Use ARIA labels where needed (Docusaurus handles most)

**Color**:
- Don't rely on color alone to convey information
- Ensure sufficient contrast (handled by diagram-specs.md)
- Use patterns or labels in addition to color

---

## 8. Review Checklist

### Content Review

Before submitting any chapter:

**Structure**:
- [ ] Follows chapter template (intro, content, summary)
- [ ] Has 800-1200 words (target range)
- [ ] Includes 3-4 learning objectives
- [ ] Has appropriate heading hierarchy (H1 → H2 → H3)

**Content Quality**:
- [ ] Explains "why" before "how"
- [ ] Uses concrete examples
- [ ] Defines technical terms on first use
- [ ] Includes real-world applications
- [ ] Builds on previous chapters

**Technical Accuracy**:
- [ ] All code examples tested (if executable)
- [ ] Terminology matches approved list
- [ ] Citations included where needed
- [ ] Current information (as of 2025)

### Style Review

**Writing**:
- [ ] Uses active voice ("you can" not "one can")
- [ ] Avoids jargon or defines it
- [ ] Maintains consistent tone
- [ ] Sentence length average 15-25 words

**Formatting**:
- [ ] Bold for new terms
- [ ] Code formatting for technical elements
- [ ] Proper list formatting (bullets/numbers)
- [ ] Callout boxes used appropriately

**Visual Elements**:
- [ ] All images have alt text
- [ ] All diagrams have captions (Figure X.Y format)
- [ ] Tables formatted correctly
- [ ] Code blocks have language tags

### Accessibility Review

**Readability**:
- [ ] Plain language used
- [ ] Short paragraphs (3-5 sentences)
- [ ] Clear transitions between sections
- [ ] Descriptive headings

**Visual**:
- [ ] Alt text for all images (descriptive, not "image of...")
- [ ] Color not sole means of conveying info
- [ ] Sufficient contrast in diagrams
- [ ] Proper semantic structure

### Cross-References

**Internal Links**:
- [ ] Previous chapter referenced if building on concepts
- [ ] Next chapter previewed in summary
- [ ] Diagrams referenced in text ("as shown in Figure 2.1")
- [ ] Code examples explained in prose

**External Links**:
- [ ] Documentation links current and accurate
- [ ] Research citations in APA format
- [ ] No broken links (check before commit)

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-16 | Initial style guide |

---

**File**: `specs/001-physical-ai-robotics-book/style-guide.md`
**Status**: Complete
**Compliance**: FR-020 ✅ (Consistent terminology, tone, and formatting standards defined)
**Ready for**: Chapter writing (Phase 3+)
