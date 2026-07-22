import json
from app.services.embedding_service import embedding_service
from app.services.gemini_service import gemini_service

class MatchingService:
    def evaluate_match(self, resume_data: dict, job_requirements: dict) -> dict:
        resume_text = resume_data.get("raw_text", "")
        
        # Combine job details into a single text block
        job_text = f"""
        Role: {job_requirements.get('JobRole', '')}
        Company: {job_requirements.get('CompanyName', '')}
        Skills: {', '.join(job_requirements.get('RequiredSkills', []))}
        Preferred Skills: {', '.join(job_requirements.get('PreferredSkills', []))}
        Experience: {job_requirements.get('ExperienceRequired', '')}
        Education: {job_requirements.get('Education', '')}
        Responsibilities: {', '.join(job_requirements.get('Responsibilities', []))}
        """
        
        # Use embedding service for overall raw semantic similarity
        semantic_score = embedding_service.calculate_similarity(resume_text, job_text)

        # Call Gemini to get specific evaluations
        prompt = f"""
        Act as an expert Applicant Tracking System (ATS).
        Compare the candidate's resume against the job description.
        Evaluate and score each category from 0 to 100.
        
        Candidate Resume:
        {resume_text[:4000]}
        
        Job Requirements:
        {job_text[:4000]}
        
        Return ONLY a raw JSON object (without markdown code blocks or trailing backticks) matching this schema exactly:
        {{
            "overall_match": 85,
            "skill_match": 80,
            "experience_match": 75,
            "education_match": 90,
            "project_relevance": 85,
            "ats_compatibility": 88
        }}
        """
        
        response_text = gemini_service.generate_content(prompt)
        try:
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:-3]
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:-3]
                
            scores = json.loads(cleaned_text.strip())
            
            # Hybrid overall score: average of semantic similarity and Gemini's ATS evaluation
            ats_overall = scores.get("overall_match", 70)
            scores["overall_match"] = round((semantic_score + ats_overall) / 2)
            
            return scores
        except Exception as e:
            print("Failed to parse JSON from Gemini (MatchingService):", str(e))
            # Fallback based on semantic score
            val = round(semantic_score)
            return {
                "overall_match": val,
                "skill_match": val,
                "experience_match": val,
                "education_match": 80,
                "project_relevance": val,
                "ats_compatibility": 80
            }

matching_service = MatchingService()
