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

    def generate_recommendations(self, links: dict, profile_scores: dict) -> dict:
        prompt = f"""
        Act as an expert AI career advisor for software engineering.
        The user has provided the following profile links/identifiers:
        {json.dumps(links, indent=2)}
        
        We have simulated an analysis of their profiles with the following scores (out of 100):
        {json.dumps(profile_scores, indent=2)}
        
        Based on this combined profile strength and implied skills, generate 3-5 specific, personalized recommendations for each of these categories:
        1. Jobs: Specific job titles or roles they should search for on LinkedIn.
        2. Internships: Types of internships or entry-level programs they should search for on LinkedIn.
        3. Hackathons: Themes or specific well-known hackathons they should participate in, particularly those found on Unstop.
        4. Workshops: Specific technical skills to learn or workshops to attend, like those on Unstop.
        5. LeetCode Problems: Specific problem types, algorithms, or classic problem names they should practice on LeetCode.
        
        Return ONLY a JSON object exactly matching this schema without any markdown formatting:
        {{
            "jobs": ["Frontend Developer (LinkedIn)", "React Engineer (LinkedIn)"],
            "internships": ["SWE Intern (LinkedIn)", "Web Dev Intern (LinkedIn)"],
            "hackathons": ["Smart India Hackathon (Unstop)", "Global Hack Week (Unstop)"],
            "workshops": ["System Design Workshop (Unstop)", "React Bootcamp (Unstop)"],
            "leetcode_problems": ["Two Sum", "Merge Intervals"]
        }}
        """
        
        ai_resp = gemini_service.generate_content(prompt)
        parsed = self._parse_json(ai_resp, default={})
        
        return {
            "jobs": parsed.get("jobs", ["Software Engineer (LinkedIn)", "Full Stack Developer (LinkedIn)", "Backend Developer (LinkedIn)"]),
            "internships": parsed.get("internships", ["Software Engineering Intern (LinkedIn)", "Backend Intern (LinkedIn)"]),
            "hackathons": parsed.get("hackathons", ["Smart India Hackathon (Unstop)", "Global Hack Week (Unstop)"]),
            "workshops": parsed.get("workshops", ["System Design Basics (Unstop)", "Advanced React Patterns (Unstop)"]),
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
            
        try:
            req = urllib.request.Request(value, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=4) as response:
                return True
        except urllib.error.HTTPError as e:
            # 404 means not found. Other errors like 403, 401, 999 (LinkedIn) mean the URL exists but bots are blocked.
            if e.code == 404:
                return False
            return True
        except Exception:
            return False

        
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
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                name = data.get("name") or data.get("login") or "Unknown"
                bio = data.get("bio") or "No bio provided"
                public_repos = data.get("public_repos", 0)
                followers = data.get("followers", 0)
                
                prompt = f"""
                Analyze this GitHub profile and provide a score out of 100 based on its strength for a software engineering role.
                Bio: {bio}
                Public Repos: {public_repos}
                Followers: {followers}
                
                Return ONLY a JSON object matching this schema:
                {{"score": 85}}
                """
                
                ai_resp = gemini_service.generate_content(prompt)
                score_data = self._parse_json(ai_resp, default={"score": 75})
                
                return {
                    "username": name,
                    "score": score_data.get("score", 75)
                }
        except Exception as e:
            print(f"GitHub API Error: {e}")
            return self._simulate_scan("github", url_or_username)
            
    def _simulate_scan(self, platform: str, value: str) -> dict:
        prompt = f"""
        The user provided the following input for their {platform} profile: "{value}"
        
        If the input is just a casual greeting (like "hi", "hello") or nonsensical, the score should be very low (e.g. 5-15) and the username should be "Invalid Input".
        
        If it looks like a valid URL or username, simulate analyzing their bio, posts, and professional history on {platform}.
        Generate a realistic name of the person (or use the one in the URL) and a score out of 100 based on how strong their profile appears.
        
        Return ONLY a JSON object matching this schema exactly without any markdown code blocks:
        {{
            "username": "string",
            "score": 80
        }}
        """
        
        ai_resp = gemini_service.generate_content(prompt)
        parsed = self._parse_json(ai_resp, default={"username": "Unknown", "score": 50})
        
        return {
            "username": parsed.get("username", "Unknown"),
            "score": parsed.get("score", 50)
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
