import json
import os
from dotenv import load_dotenv

load_dotenv()

# Try importing fitz (PyMuPDF)
try:
    import fitz
    FITZ_AVAILABLE = True
except ImportError:
    FITZ_AVAILABLE = False

# Try importing pdfplumber
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False


class ResumeParser:
    def extract_text(self, pdf_path):
        if FITZ_AVAILABLE:
            try:
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                if text.strip():
                    return text
            except Exception as e:
                print(f"fitz extraction failed: {e}")

        if PDFPLUMBER_AVAILABLE:
            try:
                text = ""
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        t = page.extract_text()
                        if t:
                            text += t + "\n"
                return text
            except Exception as e:
                print(f"pdfplumber extraction failed: {e}")
        return ""

    def extract_candidate_profile(self, resume_text):
        prompt = f"""
You are an ATS Resume Parser.

Your job is ONLY to extract information that is explicitly present in the uploaded resume.

IMPORTANT RULES

1. NEVER invent information.

2. NEVER assume missing values.

3. NEVER generate placeholder data.

4. NEVER infer certifications, skills, experience, projects, achievements or contact information.

5. If any field is missing,
return null, [] or "".

6. Every value must be directly supported by the resume text.

7. Accuracy is more important than completeness.

8. Return ONLY valid JSON.

9. Do not explain anything.

JSON Schema:
{{
"personal_information": {{
"full_name":"",
"career_summary":"",
"current_status":""
}},

"contact_details": {{
"email":"",
"phone":"",
"location":"",
"linkedin":"",
"github":"",
"portfolio":""
}},

"education":[],

"experience":[],

"skills":[],

"technical_skills": {{
"programming_languages":[],
"frameworks":[],
"libraries":[],
"tools":[],
"databases":[],
"cloud_platforms":[]
}},

"soft_skills":[],

"projects":[],

"certifications":[],

"achievements":[],

"research":[],

"languages":[],

"interests":[],

"career_domain":[],

"preferred_roles":[],

"resume_score":0,

"career_readiness": {{
"overall_score":0,
"level":"",
"strengths":[],
"areas_to_improve":[]
}},

"additional_metadata": {{
"skills_count":0,
"projects_count":0,
"experience_count":0
}}
}}

Resume:
{resume_text}
"""
        # Prefer existing gemini_service if in Flask context
        try:
            from app.services.gemini_service import gemini_service
            response_text = gemini_service.generate_content(prompt)
        except Exception:
            # Standalone execution
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            response_text = response.text

        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        profile = json.loads(cleaned_text)

        # Inject compatibility keys so matching and dashboard routes continue to function
        profile["FullName"] = profile.get("personal_information", {}).get("full_name") or ""
        profile["ResumeScore"] = profile.get("resume_score", 0)
        profile["CareerReadinessScore"] = profile.get("career_readiness", {}).get("overall_score") or 0
        profile["Skills"] = profile.get("skills", [])
        
        tech_skills_dict = profile.get("technical_skills", {})
        all_tech_skills = []
        if isinstance(tech_skills_dict, dict):
            for k, v in tech_skills_dict.items():
                if isinstance(v, list):
                    all_tech_skills.extend(v)
        profile["TechnicalSkills"] = all_tech_skills
        profile["SoftSkills"] = profile.get("soft_skills", [])
        profile["Education"] = profile.get("education", [])
        profile["Experience"] = profile.get("experience", [])
        profile["Projects"] = profile.get("projects", [])
        profile["Certifications"] = profile.get("certifications", [])
        profile["Achievements"] = profile.get("achievements", [])
        profile["Research"] = profile.get("research", [])
        profile["Languages"] = profile.get("languages", [])
        profile["Interests"] = profile.get("interests", [])
        
        c_domain = profile.get("career_domain", "")
        profile["CareerDomain"] = ", ".join(c_domain) if isinstance(c_domain, list) else str(c_domain)
        
        pref_roles = profile.get("preferred_roles", "")
        profile["PreferredRole"] = ", ".join(pref_roles) if isinstance(pref_roles, list) else str(pref_roles)

        return profile

    def parse_resume(self, filepath, filename):
        text = self.extract_text(filepath)
        return self.extract_candidate_profile(text)


resume_parser = ResumeParser()

if __name__ == "__main__":
    parser = ResumeParser()
    resume_text = parser.extract_text("uploads/resume.pdf")
    profile = parser.extract_candidate_profile(resume_text)
    print(json.dumps(profile, indent=4))