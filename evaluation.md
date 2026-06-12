# Evaluation

## Project: Resume and Cover Letter Tailor

---

## 1. What We Are Measuring

Every generated document is scored on five dimensions. Each dimension is scored 1–5,
where 5 is excellent and 1 is failing.

| Dimension | What It Measures |
|-----------|-----------------|
| Keyword Alignment | Resume/cover letter uses language from the job posting |
| Relevance | Most pertinent experience highlighted; irrelevant content removed |
| Tone and Professionalism | Writing is polished and appropriate for the industry |
| Visual Structure | Document is clean, scannable, and professionally formatted |
| Completeness | All required sections are present and well-developed |

---

## 2. Scoring Rubric

### Keyword Alignment (1–5)
- **5:** Key terms from the job posting appear naturally throughout; no obvious gaps
- **4:** Most key terms present; one or two minor omissions
- **3:** Some key terms present but important ones missing
- **2:** Few keywords from the posting appear in the document
- **1:** Document does not reflect the language of the job posting

### Relevance (1–5)
- **5:** Every section directly supports the application; nothing irrelevant included
- **4:** Mostly relevant; one minor section could be cut or trimmed
- **3:** Relevant content present but some irrelevant content included
- **2:** Significant irrelevant content included; relevant content buried
- **1:** Document does not appear tailored to the specific posting

### Tone and Professionalism (1–5)
- **5:** Writing is polished, confident, and perfectly matched to industry tone
- **4:** Professional with minor wording improvements possible
- **3:** Generally professional but some awkward phrasing or tone mismatches
- **2:** Unprofessional language or significant tone mismatch
- **1:** Writing is not suitable for professional submission

### Visual Structure (1–5)
- **5:** Clean, scannable, consistent formatting; appropriate use of white space
- **4:** Good structure with minor formatting inconsistencies
- **3:** Readable but some formatting issues (inconsistent bullets, spacing)
- **2:** Hard to scan; significant formatting problems
- **1:** Unformatted or visually unprofessional

### Completeness (1–5)
- **5:** All required sections present and fully developed
- **4:** All sections present; one could be more developed
- **3:** Most sections present; one missing or very thin
- **2:** Multiple sections missing or underdeveloped
- **1:** Major sections missing

---

## 3. Passing Thresholds

A generated document is **approved** when:
- Keyword Alignment ≥ 4
- Relevance ≥ 4
- Tone and Professionalism ≥ 4
- Visual Structure ≥ 3
- Completeness ≥ 4
- No dimension scores below 3

Documents below any threshold are flagged for revision with specific feedback.

---

## 4. Test Cases (Synthetic Data)

| File | Description | Expected Result |
|------|-------------|----------------|
| synthetic-data/cv-academic.md | Sample academic CV | Parses correctly into structured sections |
| synthetic-data/job-posting-university.md | University admin posting | Key requirements extracted correctly |
| synthetic-data/job-posting-industry.md | Industry role posting | Tone shift detected; keywords extracted |

---

## 5. Evaluation Results Log

| Date | Document Type | Keyword | Relevance | Tone | Visual | Complete | Pass/Fail |
|------|--------------|---------|-----------|------|--------|----------|-----------|
| — | — | — | — | — | — | — | — |