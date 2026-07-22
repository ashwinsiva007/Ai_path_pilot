import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Briefcase, Target, BookOpen, Zap, ChevronDown, ChevronUp, Sparkles, CheckCircle2, HelpCircle } from 'lucide-react';

const STANDARD_QUESTIONS = [
  {
    id: 1,
    title: "How do I find high-paying tech internships?",
    icon: <Briefcase size={22} className="text-cyan-400" />,
    gradient: "from-blue-600/20 via-cyan-500/10 to-transparent",
    badgeColor: "bg-cyan-500/10 text-cyan-400 border-cyan-500/30",
    category: "Internships & Jobs",
    summary: "Proven strategies to land top-tier tech internships on LinkedIn, Unstop, and open-source programs.",
    answer: [
      "Target verified platforms: Filter LinkedIn Jobs by 'Date Posted (Past 24 hours)' and 'Entry Level / Internship'.",
      "Leverage competitive coding & hackathons: Participate in Unstop Hackathons, Google Summer of Code, and MLH Hackathons.",
      "Direct Outreach: Message engineering managers and technical recruiters directly on LinkedIn with a 3-bullet pitch highlighting live project demos.",
      "Build Proof-of-Work: Host full-stack web applications on Vercel/Render with clear GitHub README documentation."
    ]
  },
  {
    id: 2,
    title: "What are the top AI & Full Stack skills to learn in 2025?",
    icon: <Zap size={22} className="text-violet-400" />,
    gradient: "from-violet-600/20 via-purple-500/10 to-transparent",
    badgeColor: "bg-violet-500/10 text-violet-400 border-violet-500/30",
    category: "Skill Roadmap",
    summary: "The essential modern tech stack demanded by high-growth startups and top tech firms.",
    answer: [
      "AI & LLM Integration: Master Python, Google Gemini API, OpenAI API, LangChain, and RAG architectures.",
      "Frontend Mastery: React 18+, Next.js (App Router), TypeScript, and Tailwind CSS for rapid UI development.",
      "Backend & APIs: Python (Flask / FastAPI / Django) and Node.js for high-performance RESTful APIs.",
      "Databases & Cloud: PostgreSQL, SQLite, Redis caching, Docker containerization, and Vercel serverless deployments."
    ]
  },
  {
    id: 3,
    title: "How can I optimize my resume to pass ATS screeners?",
    icon: <Target size={22} className="text-emerald-400" />,
    gradient: "from-emerald-600/20 via-teal-500/10 to-transparent",
    badgeColor: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    category: "Resume Strategy",
    summary: "Actionable ATS optimization guidelines to get your resume noticed by hiring managers.",
    answer: [
      "Use Single-Column Formatting: Avoid multi-column templates, tables, or image graphics that break ATS parsers.",
      "Match Keyword Density: Directly mirror technical skills (e.g. 'Python', 'React', 'REST APIs') from the target job description.",
      "Quantify Achievements: Use the Google XYZ formula: 'Accomplished [X] as measured by [Y], by doing [Z]' (e.g., 'Reduced query latency by 40% using Redis').",
      "Include Live Links: Add clickable GitHub repository links and live project deployment URLs."
    ]
  },
  {
    id: 4,
    title: "How do I prepare for technical coding & design interviews?",
    icon: <BookOpen size={22} className="text-amber-400" />,
    gradient: "from-amber-600/20 via-orange-500/10 to-transparent",
    badgeColor: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    category: "Interview Preparation",
    summary: "A systematic 4-week preparation plan for coding tests and system design discussions.",
    answer: [
      "Master Core DSA Patterns: Focus on the 'Blind 75' LeetCode list covering Arrays, HashMaps, Two Pointers, Trees, and Dynamic Programming.",
      "Mock Interview Practice: Practice thinking out loud while solving problems under timed constraints.",
      "System Design Fundamentals: Understand REST API design, database normalization, indexing, caching strategies, and load balancing.",
      "Project Deep-Dive Prep: Be ready to explain your architecture decisions, challenges faced, and trade-offs made in your top 2 projects."
    ]
  }
];

export default function AgentChat() {
  const [openId, setOpenId] = useState(1); // Open first question by default

  const toggleQuestion = (id) => {
    setOpenId(openId === id ? null : id);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-8 pb-24 text-white max-w-5xl mx-auto"
    >
      {/* Page Header */}
      <div className="mb-10 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-3">
          <Sparkles size={14} /> AI Career Knowledge Base
        </div>
        <h1 className="text-4xl font-extrabold mb-3">
          Frequently Asked <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">Career Questions</span>
        </h1>
        <p className="text-gray-400 text-base max-w-2xl mx-auto">
          Explore curated, expert AI answers to the top career, resume, and interview questions.
        </p>
      </div>

      {/* Questions List */}
      <div className="space-y-5">
        {STANDARD_QUESTIONS.map((q) => {
          const isOpen = openId === q.id;
          return (
            <motion.div
              key={q.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`bg-[#1e2128] border rounded-2xl overflow-hidden transition-all duration-300 shadow-xl ${
                isOpen ? 'border-cyan-500/50 ring-1 ring-cyan-500/30' : 'border-gray-800 hover:border-gray-700'
              }`}
            >
              {/* Question Header Card */}
              <button
                onClick={() => toggleQuestion(q.id)}
                className={`w-full p-6 text-left flex items-start justify-between gap-4 transition-colors ${
                  isOpen ? 'bg-gray-900/60' : 'hover:bg-gray-900/40'
                }`}
              >
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-xl bg-gray-900 border border-gray-800 flex-shrink-0 mt-0.5`}>
                    {q.icon}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                      <span className={`px-2.5 py-0.5 text-[11px] font-bold rounded-md border ${q.badgeColor}`}>
                        {q.category}
                      </span>
                    </div>
                    <h2 className="text-xl font-bold text-white group-hover:text-cyan-300 transition-colors">
                      {q.title}
                    </h2>
                    <p className="text-xs text-gray-400 mt-1">
                      {q.summary}
                    </p>
                  </div>
                </div>

                <div className={`p-2 rounded-xl border flex-shrink-0 transition-colors ${
                  isOpen ? 'bg-cyan-500/20 border-cyan-500/40 text-cyan-400' : 'bg-gray-900 border-gray-800 text-gray-400'
                }`}>
                  {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </div>
              </button>

              {/* Answer Content */}
              <AnimatePresence>
                {isOpen && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                    className="border-t border-gray-800/80 bg-[#16181f] p-6"
                  >
                    <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                      <CheckCircle2 size={14} className="text-cyan-400" /> AI Career Guidance Breakdown
                    </h3>
                    <ul className="space-y-3">
                      {q.answer.map((item, idx) => (
                        <li key={idx} className="flex items-start gap-3 bg-gray-900/50 p-4 rounded-xl border border-gray-800/80 text-sm leading-relaxed text-gray-200">
                          <span className="w-6 h-6 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 flex items-center justify-center font-bold text-xs flex-shrink-0 mt-0.5">
                            {idx + 1}
                          </span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          );
        })}
      </div>

      {/* Footer Info Box */}
      <div className="mt-10 p-6 rounded-2xl bg-gray-900/60 border border-gray-800 flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <HelpCircle size={20} />
          </div>
          <div>
            <h4 className="text-sm font-bold text-white">Need Customized Guidance?</h4>
            <p className="text-xs text-gray-400">Upload your resume on the Compare page for tailored job match analytics.</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
