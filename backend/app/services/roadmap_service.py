import json
from app.services.gemini_service import gemini_service

class RoadmapService:
    def generate_roadmap_plan(self, missing_skills: list, role: str) -> dict:
        prompt = f"""
        Act as an expert Technical Mentor. The candidate needs to learn the following skills to match the '{role}' job requirements:
        {json.dumps(missing_skills)}
        
        Create a detailed, step-by-step learning roadmap and resource guide.
        Include:
        1. A 7-Day crash course roadmap.
        2. A 30-Day depth-learning roadmap.
        3. 3-4 recommended courses.
        4. Key certifications to acquire.
        5. 2-3 specific project ideas to build to show proficiency.
        6. Essential learning resources (articles, docs, tutorials).
        7. An interview prep plan for these skills.
        
        Return ONLY a raw JSON object (without markdown code blocks or trailing backticks) matching this schema exactly:
        {{
            "plan_7_day": ["string"],
            "plan_30_day": ["string"],
            "recommended_courses": ["string"],
            "certifications": ["string"],
            "project_ideas": ["string"],
            "learning_resources": ["string"],
            "interview_prep_plan": ["string"]
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
            print("Failed to parse JSON from Gemini (RoadmapService):", str(e))
            # Fallback roadmap structure
            return {
                "plan_7_day": ["Day 1-3: Learn core syntax and concepts.", "Day 4-7: Build simple exercises."],
                "plan_30_day": ["Week 1-2: Master intermediate design patterns.", "Week 3-4: Build a full-stack demo application."],
                "recommended_courses": ["Coursera Web Development Specialties", "Udemy Modern Developer Masterclass"],
                "certifications": ["AWS Certified Cloud Practitioner", "Google Professional Cloud Architect"],
                "project_ideas": ["Task Manager Web App", "Personal Portfolio Page"],
                "learning_resources": ["Official Documentation", "MDN Web Docs"],
                "interview_prep_plan": ["Revise common algorithmic problems.", "Participate in mock interviews."]
            }

roadmap_service = RoadmapService()
