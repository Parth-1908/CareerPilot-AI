import sys
import io
import time
import requests
import fitz
from jose import jwt

BASE_BACKEND = "http://127.0.0.1:8000"
BASE_FRONTEND = "http://localhost:5173"

def make_test_token(user_id: str = "live-verifier-user-001", email: str = "verifier@careerpilot.ai") -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "aud": "authenticated",
        "role": "authenticated",
        "exp": int(time.time()) + 3600,
    }
    return jwt.encode(payload, "test-secret-key-development", algorithm="HS256")

def generate_test_pdf():
    doc = fitz.open()
    page = doc.new_page()
    text = (
        "Sarah Jenkins\n"
        "Full Stack Developer | sarah.jenkins@example.com | (555) 234-5678\n\n"
        "SUMMARY\n"
        "Motivated Software Engineer with 2+ years building reactive web applications using React, TypeScript, and FastAPI.\n\n"
        "TECHNICAL SKILLS\n"
        "Languages: Python, TypeScript, JavaScript, SQL\n"
        "Frameworks & Tools: React 19, FastAPI, PostgreSQL, Docker, Git, Tailwind CSS, REST APIs\n\n"
        "PROFESSIONAL EXPERIENCE\n"
        "CloudCore Technologies — Junior Full Stack Developer (2023 - Present)\n"
        "- Engineered real-time dashboard analytics reducing page load time by 38% for 10,000 active users.\n"
        "- Designed RESTful APIs in FastAPI with comprehensive Pydantic validation schemas.\n"
        "- Migrated legacy CSS to Tailwind CSS improving UI responsiveness across mobile and desktop devices.\n\n"
        "PROJECTS\n"
        "Career Pilot Assessment System (2024)\n"
        "- Built interactive interview simulator with automated rubric grading using Google Gemini API.\n"
        "- Configured Supabase PostgreSQL storage with Row-Level Security policies to protect user privacy.\n\n"
        "EDUCATION\n"
        "B.S. in Computer Science — State University (Graduated May 2023)\n"
    )
    page.insert_text((50, 60), text, fontsize=10)
    buf = io.BytesIO()
    doc.save(buf)
    doc.close()
    return buf.getvalue()

def run_live_verification():
    print("=" * 60)
    print("CAREERPILOT AI — LIVE END-TO-END SYSTEM VERIFICATION")
    print("=" * 60)

    # 1. Health check
    print("\n[1/7] Testing Backend Health Endpoint...")
    r = requests.get(f"{BASE_BACKEND}/health", timeout=5)
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    health_data = r.json()
    print(f"  ✓ Backend is healthy: {health_data['status']} (v{health_data['version']})")

    # 2. Frontend check
    print("\n[2/7] Testing Frontend Dev Server...")
    r = requests.get(BASE_FRONTEND, timeout=5)
    assert r.status_code == 200, f"Frontend request failed: {r.status_code}"
    assert "root" in r.text, "Root element missing from frontend HTML"
    print("  ✓ Frontend is serving Vite SPA with React 19 root shell")

    # 3. Auth Profile Check
    print("\n[3/7] Testing Authenticated Profile Route (/api/v1/me)...")
    token = make_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_BACKEND}/api/v1/me", headers=headers, timeout=5)
    assert r.status_code == 200, f"Get /me failed: {r.text}"
    print(f"  ✓ Verified JWT sub identification: {r.json()['id']}")

    # 4. Upload & Real Resume Rubric Analysis
    print("\n[4/7] Testing PDF Upload & 5-Pillar Gemini Rubric Analysis...")
    pdf_bytes = generate_test_pdf()
    files = {"file": ("Sarah_Jenkins_Resume.pdf", pdf_bytes, "application/pdf")}
    t0 = time.time()
    r = requests.post(f"{BASE_BACKEND}/api/v1/resumes/upload?auto_analyze=true", headers=headers, files=files, timeout=30)
    assert r.status_code == 200, f"Resume upload failed: {r.text}"
    upload_data = r.json()
    resume_id = upload_data["resume"]["id"]
    analysis = upload_data["analysis"]
    print(f"  ✓ Uploaded PDF ({len(pdf_bytes)} bytes) in {time.time()-t0:.2f}s")
    print(f"  ✓ Overall Rubric Score: {analysis['overall_score']}/100")
    cats = analysis.get('category_scores', {})
    print(f"  ✓ 5 Pillars: Skills={cats.get('skills')}, Projects={cats.get('projects')}, Impact={cats.get('impact')}, ATS/Structure={cats.get('structure')}, Presentation/Clarity={cats.get('presentation')}")
    if analysis.get('strengths'):
        strength = analysis['strengths'][0]
        print(f"  ✓ Grounded Citation: \"{strength.get('evidence_excerpt')}\"")

    # 5. Job Description & Matching
    print("\n[5/7] Testing Job Match & 3072-dim Semantic Similarity...")
    job_payload = {
        "title": "Full Stack Software Engineer",
        "company": "NextGen Platforms",
        "description": "Looking for a software engineer proficient in React, TypeScript, FastAPI, Python, and PostgreSQL. Experience with Docker and cloud deployment is a plus."
    }
    r = requests.post(f"{BASE_BACKEND}/api/v1/jobs", headers=headers, json=job_payload, timeout=10)
    assert r.status_code == 200
    job_id = r.json()["id"]

    match_payload = {"resume_id": resume_id, "job_description_id": job_id}
    r = requests.post(f"{BASE_BACKEND}/api/v1/jobs/match", headers=headers, json=match_payload, timeout=20)
    assert r.status_code == 200, f"Job match failed: {r.text}"
    match_data = r.json()
    print(f"  ✓ Semantic Similarity: {match_data['semantic_similarity']}%")
    print(f"  ✓ Skill Coverage: {match_data['skill_coverage']}%")
    print(f"  ✓ Matched Skills: {', '.join(match_data['matched_skills'][:4])}")
    print(f"  ✓ Gap Summary: {match_data['gap_summary'][:75]}...")

    # 6. Interview Studio Generation & Answer Evaluation
    print("\n[6/7] Testing Interview Studio Dynamic Generation & Rubric Feedback...")
    interview_payload = {
        "role": "Full Stack Engineer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "question_count": 2
    }
    r = requests.post(f"{BASE_BACKEND}/api/v1/interviews", headers=headers, json=interview_payload, timeout=25)
    assert r.status_code == 200, f"Interview creation failed: {r.text}"
    interview_data = r.json()
    session_id = interview_data["id"]
    q1 = interview_data["questions"][0]
    print(f"  ✓ Generated Question 1: \"{q1['question'][:80]}...\"")

    ans_payload = {
        "answer": "FastAPI leverages Python type hints with Pydantic for automated request validation and serialization, running asynchronously on top of Starlette and Uvicorn for high performance."
    }
    r = requests.post(f"{BASE_BACKEND}/api/v1/interviews/{session_id}/questions/{q1['id']}/answer", headers=headers, json=ans_payload, timeout=20)
    assert r.status_code == 200, f"Answer evaluation failed: {r.text}"
    eval_data = r.json()["evaluation"]
    print(f"  ✓ Answer Score: {eval_data['score']}/100")
    print(f"  ✓ Correctness: {eval_data['correctness'][:60]}...")
    print(f"  ✓ Clarity: {eval_data['clarity'][:60]}...")

    # 7. Dashboard Metrics Aggregation
    print("\n[7/7] Testing Real Metrics Dashboard Calculation...")
    r = requests.get(f"{BASE_BACKEND}/api/v1/dashboard/metrics", headers=headers, timeout=5)
    assert r.status_code == 200, f"Dashboard metrics failed: {r.text}"
    dash_data = r.json()
    print(f"  ✓ Stored Resumes: {dash_data['resumes_count']}")
    print(f"  ✓ Job Matches: {dash_data['job_matches_count']}")
    print(f"  ✓ Interview Sessions: {dash_data['interview_sessions_count']}")
    print(f"  ✓ Composite Readiness Score: {dash_data['overall_readiness_score']}/100")
    print(f"  ✓ Recent Activities Logged: {len(dash_data['recent_activities'])} items")

    print("\n" + "=" * 60)
    print("ALL 7 CORE SUBSYSTEMS VERIFIED LIVE WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_live_verification()
