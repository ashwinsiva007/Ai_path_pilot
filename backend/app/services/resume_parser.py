import os
import json
import pdfplumber
import docx
from app.services.gemini_service import gemini_service

class ResumeParser:
    def extract_text_from_pdf(self, filepath):
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def extract_text_from_docx(self, filepath):
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])

    def parse_resume(self, filepath, filename):
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext == 'pdf':
            text = self.extract_text_from_pdf(filepath)
        elif ext == 'docx':
            text = self.extract_text_from_docx(filepath)
        else:
            raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

        if not text.strip():
            raise ValueError("Extracted text is empty. The file might be scanned or corrupt.")

        prompt = f"""
        Extract the following information from the resume text below.
        Evaluate the profile to compute a 'Resume Score' and 'Career Readiness Score' (integers out of 100).
        Return ONLY a raw JSON object (without markdown code blocks or trailing backticks) matching this schema exactly:
        
        {{
            "FullName": "string",
            "EmailAddress": "string",
            "PhoneNumber": "string",
            "Skills": ["string"],
            "TechnicalSkills": ["string"],
            "SoftSkills": ["string"],
            "Education": ["string"],
            "Experience": ["string"],
            "Projects": [ {{"Title": "string", "Description": "string", "TechnologiesUsed": ["string"]}} ],
            "Certifications": ["string"],
            "Achievements": ["string"],
            "Interests": ["string"],
            "CareerDomain": "string",
            "PreferredRole": "string",
            "ResumeScore": 85,
            "CareerReadinessScore": 80
        }}
        
        Resume Text:
        {text}
        """
        response_text = gemini_service.generate_content(prompt)
        try:
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:-3]
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:-3]
            
            structured_data = json.loads(cleaned_text.strip())
            structured_data["raw_text"] = text
            return structured_data
        except Exception as e:
            print("Failed to parse JSON from Gemini (ResumeParser):", str(e))
            # Fallback mock data structure
            return {
                "FullName": "Unknown Candidate",
                "EmailAddress": "",
                "PhoneNumber": "",
                "Skills": [],
                "TechnicalSkills": [],
                "SoftSkills": [],
                "Education": [],
                "Experience": [],
                "Projects": [],
                "Certifications": [],
                "Achievements": [],
                "Interests": [],
                "CareerDomain": "Software Engineering",
                "PreferredRole": "Software Engineer",
                "ResumeScore": 50,
                "CareerReadinessScore": 50,
                "raw_text": text
            }

resume_parser = ResumeParser()
