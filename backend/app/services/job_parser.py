import json
from app.services.gemini_service import gemini_service

class JobParser:
    def parse_job_description(self, raw_text: str) -> dict:
        if not raw_text or not raw_text.strip():
            raise ValueError("Job description text is empty.")

        prompt = f"""
        Act as an expert Recruiter. Parse the following raw job description text.
        Extract the requested fields. If a field is not mentioned, use null or an empty array/string.
        Return ONLY a raw JSON object (without markdown code blocks or trailing backticks) matching this schema exactly:
        
        {{
            "CompanyName": "string",
            "JobRole": "string",
            "RequiredSkills": ["string"],
            "PreferredSkills": ["string"],
            "ExperienceRequired": "string",
            "Education": "string",
            "Responsibilities": ["string"],
            "Salary": "string",
            "Location": "string",
            "EmploymentType": "string",
            "ApplicationDeadline": "string"
        }}
        
        Job Description Text:
        {raw_text[:6000]}
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
            print("Failed to parse JSON from Gemini (JobParser):", str(e))
            # Fallback mock data structure
            return {
                "CompanyName": "Unknown Company",
                "JobRole": "Software Engineer",
                "RequiredSkills": [],
                "PreferredSkills": [],
                "ExperienceRequired": "Not specified",
                "Education": "Bachelor's degree",
                "Responsibilities": [],
                "Salary": "Not specified",
                "Location": "Remote / On-site",
                "EmploymentType": "Full-time",
                "ApplicationDeadline": "Not specified"
            }

job_parser = JobParser()
