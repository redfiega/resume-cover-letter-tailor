# Synthetic Data Strategy

## Project: Resume and Cover Letter Tailor

---

## 1. Purpose

Synthetic data is used to test whether the agents parse, analyze, and generate
documents correctly without requiring real personal data during development.

---

## 2. What Data We Need

| File | Description |
|------|-------------|
| `synthetic-data/cv-academic.md` | A realistic academic CV with teaching, research, publications, and service |
| `synthetic-data/job-posting-university.md` | A university administrator or director role posting |
| `synthetic-data/job-posting-industry.md` | An industry role (e.g., instructional designer, curriculum developer) |

---

## 3. Format

All synthetic data files are in Markdown format.

---

## 4. Planted Signals

### cv-academic.md
- Contains teaching, research, publications, awards, and service sections
- Includes both relevant and irrelevant content for different job types
- **Expected result:** CV Parser correctly identifies all sections

### job-posting-university.md
- Clear requirements for leadership, curriculum, and student success
- **Expected result:** Job Analyzer extracts 5+ keywords and 3+ requirements

### job-posting-industry.md
- Uses industry language (ROI, stakeholder, deliverable, agile)
- Requires tone shift from academic to corporate
- **Expected result:** Job Analyzer detects tone shift and flags academic jargon to avoid

---

## 5. Privacy Note

No real personal data is used in synthetic data files. All names, institutions,
and details are fictional.