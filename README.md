# CareerPilot-AI
CareerPilot AI – An AI-powered career and placement assistant that helps students and job seekers analyze resumes, match job descriptions, identify skill gaps, and prepare for interviews using Google Gemini.
✨ Core Capabilities
1. Evidence-Grounded Resume Analysis (5 Pillars)
Local Text Parsing: PyMuPDF extracts text, headings, and formatting locally without sending unverified binaries to third parties.
Strict PDF Gatekeeping: Rejects files > 5MB, verifies %PDF magic bytes, and flags unreadable scanned PDFs (requires at least 150 characters of selectable text).
5-Pillar Rubric Audit:
Skills Depth & Technical Rigor (0–20 pts)
Project Complexity & Scope (0–20 pts)
Impact, Results & Quantification (0–20 pts)
ATS Readability & Layout Formatting (0–20 pts)
Career Clarity & Role Targeting (0–20 pts)
Zero Hallucination Proof: Every score deduction and praise includes a verbatim quoted excerpt from the candidate's actual resume text.
2. Dual-Metric Job Description Matching & Gap Analysis
Dual Evaluation System: Separates Semantic Alignment (3072-dim vector cosine similarity) from Explicit Skill Coverage (keyword match percentage).
Gemini Granular Skill Extraction: Categorizes skills as Required Core, Preferred, or Soft Skills.
Gap Recommendations: Pinpoints missing skills and generates targeted 3-step project remedies.
3. Interactive Interview Studio & Turn-by-Turn Evaluation
Role-Targeted Question Sets: Generates customized technical, behavioral, or HR questions calibrated to the candidate's target job role and experience level.
Turn-by-Turn Rubric Feedback: Evaluates candidate answers across 4 distinct pillars:
Correctness: Technical and factual precision
Completeness: Addressing all parts of the question
Clarity: Structure, conciseness, and articulation
Reasoning: Architectural depth, trade-off analysis, and problem-solving methodology
Session Summaries: Computes candidate average score, highlighted strengths, and growth recommendations.
4. Real Metrics Dashboard & Activity History
Composite Career Readiness Score: Weighted formula: 40% Latest Resume Rubric + 30% Avg Job Coverage + 30% Interview Score.
Zero Mock Metrics: Real-time aggregation of stored database records across resumes, job matches, and interview sessions.
Transactional Email Reports: Server-side report summaries delivered directly to candidate emails via Resend.
Unified Activity History: Reverse-chronological timeline with search filtering, category tabs, and secure deletion.
🔒 Security, Isolation & Privacy Guarantees
Row-Level Security (RLS): Every Supabase table (profiles, resumes, resume_analyses, job_descriptions, job_matches, interview_sessions, interview_questions) enforces auth.uid() = user_id. Cross-user data access is physically rejected at the database level.
Private Storage Buckets: Uploaded resume PDFs reside in a private bucket accessible only via short-lived signed URLs.
No PII Tracking: Umami analytics collects aggregate traffic and interactions with zero personal information, IP hashing, and no cookies.
IDOR Defense: All API routes strictly verify JWT sub claims before reading, updating, or deleting any candidate asset.
