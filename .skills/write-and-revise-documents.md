# Skill: Write and Revise Documents

## When to Use
When generating a new resume or cover letter, or when applying user feedback
to an existing draft.

## Prerequisites
- Parsed CV content available in session state
- Job analysis results available in session state
- User answers to clarifying questions available
- `prompt-library/write-resume.txt` or `write-cover-letter.txt` loaded
- For revision: `prompt-library/revise-document.txt` loaded

## Steps — New Document
1. Load domain primer
2. Load appropriate prompt template
3. Insert CV content, job analysis, and user answers into template
4. Send to Resume Writer or Cover Letter Writer agent (Sonnet)
5. Pass draft to Reviewer agent (Opus)
6. If reviewer approves, display to user
7. If reviewer requires revision, send back to writer with feedback (max 2 retries)

## Steps — Revision
1. Load current document content from session state
2. Load revise-document prompt template
3. Insert current document, user feedback, and job analysis
4. Send to Revision Agent (Sonnet)
5. Replace current document in session state with revised version
6. Display revised document to user

## Expected Output
Complete document content ready for Word document conversion.

## Known Failure Modes
- **Missing context:** If CV or job analysis is missing, display error asking
  user to complete previous steps first
- **Vague feedback:** If user feedback is too vague to act on, display a message
  asking for more specific instructions
- **Token limit:** Very long CVs may hit token limits; truncate least relevant
  sections and notify user