import re
import urllib.request
import requests
from app.services.gemini_service import gemini_service

class JobScraper:
    def clean_html(self, html_content: str) -> str:
        # Remove script and style elements
        html_content = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html_content, flags=re.I|re.S)
        html_content = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', html_content, flags=re.I|re.S)
        # Remove common page navigation/header/footer structures to reduce token noise
        html_content = re.sub(r'<header\b[^<]*(?:(?!<\/header>)<[^<]*)*<\/header>', '', html_content, flags=re.I|re.S)
        html_content = re.sub(r'<footer\b[^<]*(?:(?!<\/footer>)<[^<]*)*<\/footer>', '', html_content, flags=re.I|re.S)
        html_content = re.sub(r'<nav\b[^<]*(?:(?!<\/nav>)<[^<]*)*<\/nav>', '', html_content, flags=re.I|re.S)
        
        # Remove remaining HTML tags
        text = re.sub(r'<[^>]+>', ' ', html_content)
        # Standardize spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def scrape_url(self, url: str) -> str:
        if not url:
            return ""
        
        try:
            # Use requests library with a common user agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            raw_text = self.clean_html(response.text)
            
            # Use Gemini to extract ONLY the job description text from the noisy scraped text
            prompt = f"""
            Extract ONLY the core Job Description and Job Requirements from the scraped webpage text below.
            Exclude company boilerplates, general navigation headers, footer links, privacy policies, advertisements, and other unrelated elements.
            
            Scraped Text:
            {raw_text[:8000]}
            
            Extracted Job Description:
            """
            
            cleaned_description = gemini_service.generate_content(prompt)
            return cleaned_description.strip()
            
        except Exception as e:
            print(f"Scraping failed for URL {url}: {e}")
            raise ValueError(f"Failed to fetch or extract job description from URL. Please check the URL or paste the job description manually.")

job_scraper = JobScraper()
