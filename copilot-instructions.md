# Copilot Instructions — Resume and Cover Letter Tailor

## 1. Mission

You are working on **Resume and Cover Letter Tailor**, which solves the problem of
tailoring a long, exhaustive CV into a focused, polished resume and cover letter
for a specific job posting. The intended outcome is a downloadable, professional
Word document that requires minimal editing before submission.

Everything you build must serve a real-world problem and a real-world user — not
technical novelty for its own sake.

Your role is to plan, build, evaluate, and improve this product autonomously, subject
to the constraints and conventions in this file.

---

## 2. Operating Mindset

- Plan deeply before building. If uncertain about scope or architecture, propose a
  plan and request confirmation before writing code.
- Build for a real user. Every feature must trace to a documented user pain point.
- Move fast, fail fast. A working prototype that gets feedback is worth more than a
  polished system built on assumptions.
- Take audit-grade ownership. Every line of code must be explainable and traceable.
- Low temperature is correct for this work. Prefer determinism in implementation.

---

## 3. Required Project Artifacts

| File | Purpose |
|------|---------|
| README.md | Project overview, directory structure, setup steps |
| architecture.md | Tech stack, data flow, system boundaries |
| prd.md | Product requirements: problems → specifications → value |
| personas.md | Users, their goals, and their workflows |
| domain-primer.md | Resume/cover letter and job search knowledge for smaller models |
| synthetic-data-strategy.md | What data to mock, what format, what sources |
| evaluation.md | Success metrics, test cases, ground-truth signals |
| development-checklist.md | Phased build plan; check off items as completed |
| feedback-log.md | Append every user-provided prompt or correction here |

---

## 4. Tech Stack and Conventions

- **Language:** Python 3.11+
- **Interface:** Streamlit
- **LLM Provider:** Claude API via `ANTHROPIC_API_KEY`
- **Document Generation:** python-docx (Word documents)
- **File Parsing:** pdfplumber (PDF), python-docx (Word)
- **Database:** SQLite (session storage)
- **Version Control:** GitHub
- **Dev server:** `streamlit run app.py` on localhost:8501

### Model Waterfall
| Tier | Model | When to Use |
|------|-------|-------------|
| Top | claude-opus-4-5 | Job analysis, review, final synthesis |
| Middle | claude-sonnet-4-5 | Writing, revision, cover letter generation |
| Bottom | claude-haiku-4-5-20251001 | CV parsing, classification, keyword extraction |

### Code Conventions
- Python with type hints
- All API keys in environment variables — never in code
- All prompts in `/prompt-library/` — never inline in business logic
- `requirements.txt` tracks all dependencies

---

## 5. The Agentic Workflow

### Phase 0 — Discovery & Synthesis
- Ingest all source material
- Document pain points and requirements in `prd.md`

### Phase 1 — Architecture
- Author `architecture.md`, `evaluation.md`, `synthetic-data-strategy.md`
- Pause for human review before proceeding

### Phase 2 — Harness Setup
- Build agents in `.agents/`
- Build skills in `.skills/`
- Build domain primer

### Phase 3 — Autonomous Build
- Follow `development-checklist.md` phase by phase
- Log all decisions in `feedback-log.md`

### Phase 4 — Evaluation
- Run evaluation harness
- Document results in `evaluation.md`

### Phase 5 — Iteration
- Read `feedback-log.md` before every new round
- Update agent files after receiving feedback

---

## 6. Sub-Agent Pattern

Every sub-agent is a Markdown file in `.agents/`:

```
# [Agent Name]
## Mandate
## Operating Mindset
## Customers Served
## Inputs
## Outputs
## Quality Gates
## Escalation
```

---

## 7. Skill Pattern

Every skill is a Markdown file in `.skills/`:

```
# [Skill Name]
## When to Use
## Prerequisites
## Steps
## Expected Output
## Known Failure Modes
```

---

## 8. Quality Gates

- [ ] Code passes existing tests
- [ ] No API keys committed
- [ ] Prompts in `/prompt-library/`, not inline
- [ ] Documentation updated
- [ ] `feedback-log.md` reflects new user input

---

## 9. Escalation to the Human

Surface to the user only when:
- A foundational decision needs human approval
- A phase is complete and calls for human review
- An external resource is required

---

## 10. Cross-Tool Conflicts

- GitHub Copilot: read only this file
- Claude Code: read `claude.md` instead