import json
from app.services.gemini_service import gemini_service

class RecommendationService:
    def generate_recommendation(self, resume_data: dict, job_requirements: dict, matching_results: dict, skill_gaps: dict) -> dict:
        prompt = f"""
        Act as an expert Recruiter and Career Advisor. Based on the candidate's profile, job requirements, match scores, and skill gaps, provide strategic career recommendations.
        
        Candidate: {resume_data.get('FullName', 'Candidate')}
        Target Role: {job_requirements.get('JobRole', 'Software Engineer')}
        Company: {job_requirements.get('CompanyName', 'Target Company')}
        
        Match Scores:
        {json.dumps(matching_results, indent=2)}
        
        Skill Gaps:
        {json.dumps(skill_gaps, indent=2)}
        
        Provide the following details in a JSON format:
        1. should_apply: "YES", "MAYBE", or "NO"
        2. reason: A brief paragraph explaining why.
        3. resume_improvements: 3-5 specific, actionable points to improve their resume formatting or content for this role.
        4. missing_keywords: Important technical or industry-specific keywords that are in the job description but missing from the resume.
        5. interview_tips: 3-4 specific concepts or topics the candidate must prepare for during the interview.
        6. recommended_changes: Suggested updates to specific sections of their resume.
        7. career_advice: General guidance for their long-term growth in this career domain.
        
        Return ONLY a raw JSON object (without markdown code blocks or trailing backticks) matching this schema exactly:
        {{
            "should_apply": "YES/MAYBE/NO",
            "reason": "string",
            "resume_improvements": ["string"],
            "missing_keywords": ["string"],
            "interview_tips": ["string"],
            "recommended_changes": ["string"],
            "career_advice": "string"
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
            print("Failed to parse JSON from Gemini (RecommendationService):", str(e))
            # Fallback mock recommendations
            return {
                "should_apply": "MAYBE",
                "reason": "You have a solid base technical background but need to bridge some critical gaps before applying.",
                "resume_improvements": ["Quantify impact on your projects.", "Highlight relevant skills in your experience section."],
                "missing_keywords": [],
                "interview_tips": ["Prepare on core technologies mentioned in the job role.", "Revise system design basics."],
                "recommended_changes": [],
                "career_advice": "Focus on building complete side projects with the required stack."
            }

recommendation_service = RecommendationService()
