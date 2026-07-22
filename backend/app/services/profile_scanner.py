import json
import urllib.request
from app.services.gemini_service import gemini_service

class ProfileScanner:
    def scan_profiles(self, links: dict) -> dict:
        results = {}
        for key, value in links.items():
            if not value or not str(value).strip():
                continue
            
            val_str = str(value).strip()
            
            if not self._is_valid_link(key, val_str):
                results[key] = {"username": "Invalid Link", "score": 0}
                continue
            
            if key == "github":
                results[key] = self._scan_github(val_str)
            else:
                results[key] = self._simulate_scan(key, val_str)
                
        return results

    def generate_recommendations(self, bio: str, skills: list) -> dict:
        bio = (bio or "").lower()
        skills = [s.lower() for s in (skills or [])]

        prompt = f"""
        Act as an expert AI career advisor. 
        The user has the following background based on their resume:
        Bio: {bio}
        Technical Skills: {', '.join(skills)}
        
        Based on these skills and background, generate exactly 3-5 personalized recommendations for each category:
        1. Jobs: Specific job titles they should search for.
        2. Internships: Types of internships.
        3. Hackathons: Specific hackathon themes or names.
        4. Workshops: Specific technical skills to learn or workshops.
        5. LeetCode Problems: Specific algorithmic problem types or classic problems to practice.
        
        Also identify 2-4 critical 'missing_skills' they should learn next, and estimate a 'career_score' (0-100) based on their current skill depth.
        
        Return ONLY a JSON object matching this schema exactly:
        {{
            "career_score": 75,
            "detected_skills": {json.dumps(skills)},
            "missing_skills": ["Docker", "AWS"],
            "jobs": ["Frontend Developer", "React Engineer"],
            "internships": ["SWE Intern", "Web Dev Intern"],
            "workshops": ["System Design Basics", "Advanced React"],
            "hackathons": ["Smart India Hackathon", "Global Hack Week"],
            "leetcode_problems": ["Two Sum", "Merge Intervals"]
        }}
        """
        
        ai_resp = gemini_service.generate_content(prompt)
        parsed = self._parse_json(ai_resp, default={})
        
        return {
            "career_score": parsed.get("career_score", 70),
            "detected_skills": parsed.get("detected_skills", skills),
            "missing_skills": parsed.get("missing_skills", ["Docker", "AWS", "System Design"]),
            "jobs": parsed.get("jobs", ["Software Engineer", "Full Stack Developer", "Backend Developer"]),
            "internships": parsed.get("internships", ["Software Engineering Intern", "Backend Intern"]),
            "workshops": parsed.get("workshops", ["System Design Basics", "Advanced React Patterns"]),
            "hackathons": parsed.get("hackathons", ["Smart India Hackathon", "Global Hack Week"]),
            "leetcode_problems": parsed.get("leetcode_problems", ["Two Sum", "Merge Intervals", "LRU Cache"])
        }

    def _is_valid_link(self, platform: str, value: str) -> bool:
        if platform == "resume":
            return value.lower().endswith(".pdf")
            
        # Allow just usernames for github/leetcode
        if platform in ["github", "leetcode"] and " " not in value and not value.startswith("http"):
            return True
            
        if not value.startswith("http://") and not value.startswith("https://"):
            return False
            
        # Trust frontend validation to avoid Vercel 10-second serverless timeout
        # Avoid making slow synchronous HTTP requests for every link
        return True

        
    def _scan_github(self, url_or_username: str) -> dict:
        # Extract username
        username = url_or_username
        if "github.com/" in url_or_username:
            username = url_or_username.split("github.com/")[-1].strip("/")
            
        try:
            req = urllib.request.Request(
                f"https://api.github.com/users/{username}", 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                
                name = data.get("name") or data.get("login") or "Unknown"
                public_repos = data.get("public_repos", 0)
                followers = data.get("followers", 0)
                
                # Fast Python-based heuristic score
                score = min(100, 50 + (public_repos * 2) + (followers * 5))
                
                return {
                    "username": name,
                    "score": score
                }
        except Exception as e:
            print(f"GitHub API Error: {e}")
            return self._simulate_scan("github", url_or_username)
            
    def _simulate_scan(self, platform: str, value: str) -> dict:
        # Avoid Vercel 10s timeout by not using Gemini for fake scores
        # We simulate a solid profile score for demo purposes
        username = "Profile Found"
        if "linkedin.com/in/" in value:
            username = value.split("linkedin.com/in/")[-1].strip("/").replace("-", " ").title()
        elif "github.com/" in value:
            username = value.split("github.com/")[-1].strip("/")
            
        return {
            "username": username,
            "score": 85
        }
        
    def _parse_json(self, text: str, default: dict) -> dict:
        try:
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
            
            # sometimes the response has leading/trailing whitespaces or newlines
            text = text.strip()
            return json.loads(text)
        except Exception:
            return default

profile_scanner = ProfileScanner()
