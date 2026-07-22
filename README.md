# 🚀 AI Path Pilot — Resume-to-Opportunity Matching & Career Intelligence Platform

<p align="center">
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Vite-8.1-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Gemini_AI-1.5_Flash-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Vercel-Deploys-000000?style=for-the-badge&logo=vercel&logoColor=white" />
</p>

---

## 📌 Overview

**AI Path Pilot** is an intelligent, full-stack career platform that bridges the gap between candidate resumes and real-world job opportunities. Powered by **Google Gemini 1.5 Flash**, **Flask**, and **React**, AI Path Pilot parses PDF/DOCX resumes, scrapes job postings (including LinkedIn job URLs), evaluates candidate-role compatibility, detects critical skill gaps, builds step-by-step learning roadmaps, and provides real-time career coaching.

The platform features a **state-of-the-art UI** with glassmorphism styling, dynamic micro-animations, structured resume inspectors, raw JSON downloaders, and robust offline fallback engines for stateless serverless environments (Vercel).

---

## ✨ Key Features

### 📄 1. Resume Upload & AI Profile Extraction
- Supports **PDF** and **DOCX** resume formats.
- Extracts **20+ structured candidate attributes**:
  - Personal Information (Full Name, Career Summary, Current Status)
  - Contact Details (Email, Phone, Location, LinkedIn, GitHub, Portfolio URLs)
  - Technical Skills (Languages, Frameworks, Libraries, Tools, Databases, Cloud Platforms)
  - Soft Skills, Spoken Languages, Certifications, Achievements & Research
  - Education History (Degree, Institution, Year, CGPA)
  - Work Experience & Key Projects with Tech Stacks
  - Career Domain & Preferred Job Roles
  - **Resume Score** (1-100) and **Career Readiness Score** (1-100)
- **4-Layer Extraction Waterfall**: `pdfplumber` ➔ `pypdf` ➔ Gemini Multimodal OCR ➔ Heuristic Text Regex Parser (ensures zero crashes and zero hallucinated data when running offline).

### 🔍 2. Job Link Compatibility Matcher ("Compare Fit")
- Paste any job URL (LinkedIn, Unstop, company career pages) alongside your resume.
- Automated Job Scraper reads job descriptions with AI-powered scraping fallbacks for anti-bot blocked URLs.
- Calculates an instant **Match Score (%)** and returns:
  - ✅ **Matched Skills**
  - ⚠️ **Missing Skills**
  - 💡 **Resume Improvement Suggestions**
  - 📚 **Recommended Courses**
  - 🎯 **"Should You Apply?" Recommendation** (`YES` / `MAYBE` / `NO` with detailed rationale).

### 🛠️ 3. Detailed Resume Inspector & JSON Exporter
- Temporary developer panel available directly on the Compare page.
- Renders extracted profile data in **interactive collapsible cards** or **syntax-highlighted raw JSON**.
- Includes **Copy to Clipboard** and **Download Raw JSON** (`/api/resume/extract-json`) for easy debugging and data export.

### 🗺️ 4. Personalized Skill Gap & Roadmap Generator
- Automatically compiles missing skills into **7-day** and **30-day structured learning roadmaps**.
- Direct search links to LinkedIn Jobs, Unstop Hackathons, and LeetCode problem sets.

### 💬 5. AI Career Agent Chat
- Real-time conversational AI coach to answer career queries, review resume bullet points, and offer interview preparation strategies.

---

## 🛠️ Technology Stack

### **Frontend**
- **Framework**: [React 18](https://reactjs.org/) + [Vite 8](https://vitejs.dev/)
- **Styling**: Vanilla CSS + [Tailwind CSS 3.4](https://tailwindcss.com/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **HTTP Client**: [Axios](https://axios-http.com/)

### **Backend**
- **Framework**: [Flask 3.0](https://flask.palletsprojects.com/)
- **ORM & DB**: [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) + SQLite
- **Document Extractors**: `pdfplumber`, `pypdf`, `python-docx`
- **Networking**: `requests`, `urllib`

### **AI & NLP Engine**
- **LLM**: Google Gemini API (`gemini-1.5-flash`) via raw HTTP requests (bypasses Protobuf version issues)
- **Heuristic Engine**: Custom Regex Text Extractor fallback for offline operation without API keys.

### **Deployment & Infrastructure**
- **Hosting**: [Vercel](https://vercel.com/) (Vite Static Frontend + Flask Serverless WSGI Handler)
- **Vercel Adapter**: `api/index.py` entry point with `/tmp/app.db` ephemeral SQLite storage and `localStorage` frontend caching.

---

## 📂 Project Architecture

```
ai-path-pilot/
├── api/                        # Vercel Serverless Entry Point
│   └── index.py                # WSGI Flask bridge for Vercel
├── backend/                    # Flask Application Root
│   ├── app/
│   │   ├── models/             # SQLAlchemy Models (User, Resume, MatchReport)
│   │   ├── routes/             # REST API Blueprints
│   │   │   ├── auth.py         # Authentication routes
│   │   │   ├── compare.py      # Match agent endpoint (/api/compare/match)
│   │   │   ├── dashboard.py    # Dashboard stats & link management
│   │   │   ├── job.py          # Job match routes
│   │   │   ├── resume.py       # Resume upload, details & JSON download
│   │   │   ├── roadmap.py      # Learning roadmap generator
│   │   │   ├── skill_gap.py    # Skill gap analysis
│   │   │   └── chat.py         # AI Agent Chat endpoint
│   │   ├── services/           # Core AI & Business Services
│   │   │   ├── gemini_service.py     # Gemini API HTTP client & mock fallback
│   │   │   ├── resume_parser.py      # ATS Resume Parser (rules & fallback)
│   │   │   ├── job_scraper.py        # Web scraper with AI fallback
│   │   │   ├── job_parser.py         # Structured job parser
│   │   │   ├── matching_service.py   # Candidate-job compatibility engine
│   │   │   ├── skill_gap_service.py  # Gap detection engine
│   │   │   ├── recommendation_service.py # Recommendation generator
│   │   │   └── roadmap_service.py    # Step-by-step roadmap builder
│   │   ├── extensions.py       # SQLAlchemy db instance
│   │   ├── config.py           # Configuration (SQLite path handling for Vercel)
│   │   └── __init__.py         # Flask App Factory (create_app)
│   ├── requirements.txt        # Backend dependencies
│   └── run.py                  # Local development server entrypoint
├── frontend/                   # React Single Page Application
│   ├── src/
│   │   ├── assets/             # Static assets & styling
│   │   ├── pages/              # Main view pages
│   │   │   ├── Dashboard.jsx   # Overview & social profile link hub
│   │   │   ├── Compare.jsx     # Resume-to-Job Matcher & Detailed Inspector
│   │   │   ├── LearningRoadmap.jsx # Dynamic roadmap viewer
│   │   │   └── AgentChat.jsx   # AI Chat interface
│   │   ├── services/           # Axios API service calls (api.js)
│   │   ├── App.jsx             # Main router & Sidebar Navigation
│   │   └── main.jsx            # React root mount
│   ├── package.json            # Node.js dependencies & scripts
│   └── vite.config.js          # Vite build & proxy settings
├── vercel.json                 # Vercel deployment & rewrite rules
└── README.md                   # Project documentation
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/resume/upload` | Upload PDF/DOCX resume & receive extracted JSON profile |
| `GET` | `/api/resume/details` | Fetch current candidate profile from DB |
| `GET` | `/api/resume/extract-json` | Download extracted candidate profile as raw `.json` file attachment |
| `POST` | `/api/compare/match` | Match resume against job link URL & generate match report |
| `GET` | `/api/dashboard/summary` | Retrieve career health metrics & scores |
| `GET` | `/api/dashboard/links` | Retrieve social profile URLs (Portfolio, LinkedIn, GitHub, LeetCode) |
| `POST` | `/api/dashboard/links` | Update social profile URLs |
| `POST` | `/api/roadmap/generate` | Generate step-by-step learning roadmap for missing skills |
| `POST` | `/api/chat/message` | Send message to AI Career Agent |
| `GET` | `/health` | Healthcheck endpoint (`{"status": "ok"}`) |

---

## 🚀 Local Development Setup

### **Prerequisites**
- [Python 3.10+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/) & `npm`
- [Git](https://git-scm.com/)

### **1. Clone the Repository**
```bash
git clone https://github.com/kumaran-dee/ai-path-pilot.git
cd ai-path-pilot
```

### **2. Setup & Run Backend**
```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
# Activate on Windows: venv\Scripts\activate
# Activate on macOS/Linux: source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Set Gemini API Key (Optional for real AI extraction)
# Windows PowerShell: $env:GEMINI_API_KEY="your_api_key_here"
# macOS/Linux: export GEMINI_API_KEY="your_api_key_here"

# Start Flask backend server (runs on http://127.0.0.1:5000)
python run.py
```

### **3. Setup & Run Frontend**
In a new terminal window:
```bash
cd frontend

# Install frontend dependencies
npm install

# Start Vite dev server (runs on http://localhost:5173)
npm run dev
```

---

## 🌐 Deploying to Vercel

The project is pre-configured for single-click deployment on **Vercel** using `vercel.json` and `api/index.py`.

1. Push your repository to GitHub.
2. Import the repository into your [Vercel Dashboard](https://vercel.com/dashboard).
3. Set the Framework Preset to **Vite**.
4. Set the Root Directory to `./`.
5. Add Environment Variable:
   - Key: `GEMINI_API_KEY`
   - Value: *Your Google Gemini API Key*
6. Deploy! Vercel automatically compiles Vite static assets and serves Flask API routes under `/api/*` via Serverless Functions.

---

