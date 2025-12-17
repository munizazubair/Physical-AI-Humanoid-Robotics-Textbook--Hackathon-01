<!--
Sync Impact Report:
Version: 0.0.0 → 1.0.0
Modified Principles: Initial creation
Added Sections: Core Principles (5), Phase-Specific Standards (2), Development Workflow, Governance
Removed Sections: None
Templates Status:
  ✅ plan-template.md - Constitution Check section aligns with all 5 principles
  ✅ spec-template.md - Requirements alignment verified with Accuracy & Spec-Driven principles
  ✅ tasks-template.md - Task categorization supports spec-driven and independent testing principles
Follow-up TODOs: RATIFICATION_DATE marked as 2025-12-16 (today)
-->

# AI-Driven Technical Book Creation with Integrated RAG Chatbot Constitution

## Core Principles

### I. Accuracy & Faithfulness

All content MUST be technically correct and aligned with verified sources or clearly stated assumptions.

**Rules:**
- No hallucinated or fabricated technical information
- All claims must be verifiable or explicitly marked as assumptions
- When sources are used, they must be properly attributed
- Technical accuracy takes precedence over brevity or simplicity
- Errors discovered post-publication must be corrected immediately

**Rationale:** The book serves as an educational resource and the single source of truth for the RAG chatbot. Inaccurate content undermines both learning outcomes and chatbot reliability.

### II. Clarity & Accessibility

Content MUST be written in simple, easy-to-understand language for learners and developers with basic programming knowledge.

**Rules:**
- Assume audience has basic programming knowledge but no domain expertise
- Avoid unnecessary jargon; define technical terms on first use
- Include practical examples for complex concepts
- Use consistent terminology throughout the book
- Structure content progressively (simple → complex)

**Rationale:** The book's primary purpose is education. Complex ideas presented clearly have greater impact than technically dense prose that alienates learners.

### III. Spec-Driven Development

All writing and implementation MUST strictly follow defined specifications and project phases.

**Rules:**
- No content or code written without a corresponding spec
- Each phase (spec → plan → tasks → implementation) must complete before the next begins
- Changes to scope require spec updates first, then propagation to plan/tasks
- All work must be traceable to a spec requirement
- Deviations from spec require documented justification and approval

**Rationale:** Spec-driven development ensures alignment, prevents scope creep, and maintains project coherence across book content and chatbot implementation.

### IV. Single Source of Truth

The book content is the only authoritative knowledge source for the chatbot.

**Rules:**
- RAG chatbot MUST answer questions solely from book content
- If information is not in the book, chatbot must respond "I don't know"
- No external knowledge sources may be used by the chatbot
- Book structure must support efficient retrieval and re-indexing
- Content updates require corresponding RAG database re-indexing

**Rationale:** This constraint ensures the chatbot's responses are predictable, auditable, and aligned with the book's learning objectives. It prevents hallucination and maintains coherence.

### V. Transparency

Any limitations, assumptions, or incomplete areas MUST be explicitly stated.

**Rules:**
- Mark incomplete sections clearly (e.g., "TODO", "NEEDS CLARIFICATION")
- Document assumptions that affect technical accuracy
- State chatbot limitations explicitly in documentation
- Known issues or gaps in coverage must be tracked and disclosed
- Uncertainty in technical explanations must be acknowledged

**Rationale:** Honesty about limitations builds user trust and sets realistic expectations. It also provides a clear roadmap for future improvements.

## Phase 1 Standards: AI/Spec-Driven Book Creation

**Technology Stack:**
- Writing Framework: Spec-Kit Plus + Claude Code
- Documentation Platform: Docusaurus
- Deployment: GitHub Pages

**Content Requirements:**
- All content must be original or properly attributed
- Technical explanations MUST include clear, working examples where appropriate
- Conceptual pseudo-code examples must be logically sound and syntactically representative of real implementations
- Functional code (if included) must be tested and runnable
- Structure must use Docusaurus best practices (MDX, sidebars, front matter)
- Content must be organized to support RAG indexing (clear headings, logical sections, consistent structure)

**Deployment Requirements:**
- Book MUST build successfully with Docusaurus
- All links (internal and external) must be validated before deployment
- GitHub Pages deployment must be automated via GitHub Actions
- Broken builds block deployment

## Phase 2 Standards: Integrated RAG Chatbot Development

**Technology Stack:**
- AI Framework: OpenAI Agents / ChatKit SDKs
- Backend: FastAPI
- Database: Neon Serverless Postgres
- Vector Store: Qdrant Cloud Free Tier

**Functional Requirements:**
- Chatbot MUST use Retrieval-Augmented Generation (RAG)
- Chatbot MUST answer questions strictly based on book content (no external knowledge)
- Chatbot MUST support answering questions using user-selected text from the book
- If relevant information is not found in retrieved context, chatbot MUST respond with "I don't know" (no hallucination)
- Retrieval quality must be monitored and optimized

**Integration Requirements:**
- Book content must be indexed into Qdrant vector database
- Embeddings must be regenerated when book content changes
- Chat interface must allow users to select text and ask contextual questions
- Response must cite specific sections/pages from the book when applicable

## Development Workflow

**Spec-Driven Cycle:**
1. Create feature spec (`/sp.specify`)
2. Generate implementation plan (`/sp.plan`)
3. Generate tasks (`/sp.tasks`)
4. Implement tasks (`/sp.implement`)
5. Validate against spec acceptance criteria
6. Create Prompt History Record (PHR) for each significant interaction

**Quality Gates:**
- **Pre-Development**: All specs must have clear acceptance criteria
- **Pre-Implementation**: Plan must pass Constitution Check
- **Pre-Deployment**: All tests must pass, all acceptance criteria met
- **Post-Deployment**: Book must render correctly on GitHub Pages; chatbot must return accurate, grounded responses

**Documentation:**
- Every user prompt must generate a PHR (Prompt History Record) in `history/prompts/`
- Architecturally significant decisions must be documented as ADRs (Architecture Decision Records) in `history/adr/` when suggested and approved by user
- All specs, plans, and tasks stored in `specs/<feature>/`

## Governance

**Amendment Procedure:**
1. Proposed changes must be documented with rationale
2. Impact analysis must identify affected templates, specs, and code
3. User approval required before amendments take effect
4. Constitution version must be incremented per semantic versioning rules

**Versioning Policy:**
- **MAJOR**: Backward-incompatible principle changes, removals, or redefinitions
- **MINOR**: New principles added or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, non-semantic fixes

**Compliance:**
- All PRs and reviews MUST verify compliance with this constitution
- Any complexity or deviation from principles MUST be justified in `plan.md` Complexity Tracking section
- Constitution supersedes all other practices and preferences
- Refer to `CLAUDE.md` for runtime development guidance

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
