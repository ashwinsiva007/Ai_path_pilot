import json
from app.services.gemini_service import gemini_service

class SkillGapService:
    def detect_gaps(self, resume_skills: list, job_skills: list, preferred_skills: list) -> dict:
        prompt = f"""
        Act as an expert Technical Mentor. Identify the skill gaps between the candidate's skills and the job requirements.
        
        Candidate Skills:
        {json.dumps(resume_skills)}
        
        Job Required Skills:
        {json.dumps(job_skills)}
        
        Job Preferred/Optional Skills:
        {json.dumps(preferred_skills)}
        
        Analyze the match, missing skills, weak skills (skills candidate has but needs improvement for this role), and strong skills.
        Categorize the priority skills to learn into: Critical, Recommended, and Optional.
        
        Return ONLY a raw JSON object (without markdown code blocks or trailing backticks) matching this schema exactly:
        {{
            "matched_skills": ["string"],
            "missing_skills": ["string"],
            "weak_skills": ["string"],
            "strong_skills": ["string"],
            "priority_skills": {{
                "critical": ["string"],
                "recommended": ["string"],
                "optional": ["string"]
            }}
        }}
        """
        response_text = gemini_service.generate_content(prompt)
        try:
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:-3]
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:-3]
                
            return json.loads(cleaned_text.strip())
        except Exception as e:
            print("Failed to parse JSON from Gemini (SkillGapService):", str(e))
            # Basic fallback mapping
            matched = list(set(resume_skills).intersection(set(job_skills)))
            missing = list(set(job_skills) - set(resume_skills))
            return {
                "matched_skills": matched,
                "missing_skills": missing,
                "weak_skills": [],
                "strong_skills": matched,
                "priority_skills": {
                    "critical": missing[:3],
                    "recommended": missing[3:6],
                    "optional": preferred_skills
                }
            }

skill_gap_service = SkillGapService()
