import pandas as pd
import numpy as np
import os
import requests
from flask import current_app

class SemanticMatcher:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    def load_opportunities(self):
        # Load CSV files
        base_dir = os.path.join(current_app.root_path, '..', 'datasets')
        jobs_df = pd.DataFrame()
        try:
            jobs_df = pd.read_csv(os.path.join(base_dir, 'jobs.csv'))
        except FileNotFoundError:
            pass
            
        internships_df = pd.DataFrame()
        try:
            internships_df = pd.read_csv(os.path.join(base_dir, 'internships.csv'))
        except FileNotFoundError:
            pass
            
        if jobs_df.empty and internships_df.empty:
            return pd.DataFrame()
            
        return pd.concat([jobs_df, internships_df], ignore_index=True)

    def get_embedding(self, text):
        if not self.api_key:
            self.api_key = os.getenv("GEMINI_API_KEY")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent?key={self.api_key}"
        payload = {
            "content": {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data["embedding"]["values"]
        except Exception as e:
            print(f"Error fetching embedding: {e}")
            return []

    def cosine_similarity(self, vec1, vec2):
        if not vec1 or not vec2:
            return 0.0
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

    def match_opportunities(self, user_profile_json, top_n=10):
        df = self.load_opportunities()
        if df.empty:
            return []

        # Construct a string representation of the user's skills
        user_skills_text = " ".join(user_profile_json.get("Skills", []))
        if not user_skills_text:
            return []

        user_emb = self.get_embedding(user_skills_text)

        matches = []
        for index, row in df.iterrows():
            req_text = str(row.get('requirements', ''))
            desc_text = str(row.get('description', ''))
            opp_text = req_text + " " + desc_text
            
            opp_emb = self.get_embedding(opp_text)
            score = self.cosine_similarity(user_emb, opp_emb)
            
            matches.append({
                "title": row.get('title', ''),
                "company": row.get('company', ''),
                "match_score": round(float(score) * 100, 2),
                "requirements": req_text,
                "location": row.get('location', '')
            })

        # Sort by match score descending
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches[:top_n]

semantic_matcher = SemanticMatcher()
