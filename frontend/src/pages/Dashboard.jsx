import React, { useEffect, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getLinks, updateLinks, uploadResume, compareResumeToJob } from '../services/api';
import {
  FileText, Globe, Briefcase, Terminal, Cpu, Loader2, Sparkles,
  GraduationCap, Code2, BookOpen, User, Mail, Phone, MapPin,
  Star, Award, ExternalLink, MessageCircle, CheckCircle, XCircle,
  ChevronDown, ChevronUp
} from 'lucide-react';

// ─── Reusable Section Card ────────────────────────────────
function Section({ icon: Icon, title, color, children }) {
  const [open, setOpen] = useState(true);
  return (
    <div className="mb-4 rounded-2xl border border-gray-800 overflow-hidden">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between px-5 py-4 bg-gray-900/80 hover:bg-gray-800/80 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Icon size={18} className={color} />
          <span className={`font-bold text-sm uppercase tracking-widest ${color}`}>{title}</span>
        </div>
        {open ? <ChevronUp size={16} className="text-gray-500" /> : <ChevronDown size={16} className="text-gray-500" />}
      </button>
      {open && <div className="px-5 py-4 bg-[#0f1117]">{children}</div>}
    </div>
  );
}

function Chip({ text, color = 'bg-blue-900/50 text-blue-300 border-blue-800' }) {
  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border ${color} mr-2 mb-2`}>
      {text}
    </span>
  );
}

function InfoRow({ label, value }) {
  if (!value || (Array.isArray(value) && !value.length)) return null;
  return (
    <div className="flex items-start gap-3 mb-2 text-sm">
      <span className="text-gray-500 w-36 flex-shrink-0">{label}</span>
      <span className="text-gray-200 break-words">{value}</span>
    </div>
  );
}

// ─── Resume Profile Viewer ─────────────────────────────────
function ResumeProfileViewer({ data }) {
  if (!data) return null;

  // Support both snake_case and PascalCase responses
  const name = data.personal_information?.full_name || data.FullName || '';
  const email = data.contact_details?.email || data.EmailAddress || '';
  const phone = data.contact_details?.phone || data.PhoneNumber || '';
  const location = data.contact_details?.location || data.Location || '';
  const linkedin = data.contact_details?.linkedin || data.LinkedInURL || '';
  const github = data.contact_details?.github || data.GitHubURL || '';
  const portfolio = data.contact_details?.portfolio || data.PortfolioURL || '';
  const domain = data.career_domain || data.CareerDomain || '';
  const roles = data.preferred_roles || data.PreferredRoles || [];
  const resumeScore = data.resume_score ?? data.ResumeScore ?? 0;
  const careerReadiness = data.career_readiness ?? data.CareerReadinessScore ?? 0;

  // Skills
  const skills = data.skills || data.Skills || [];
  const softSkills = data.soft_skills || data.SoftSkills || [];
  const techSkills = data.technical_skills
    ? Object.values(data.technical_skills).flat()
    : (data.TechnicalSkills || []);
  const allTech = [...new Set([...techSkills, ...skills])];

  const education = (data.education || data.Education || []).map(e => ({
    Degree: e.degree || e.Degree || '',
    FieldOfStudy: e.field_of_study || e.FieldOfStudy || '',
    Institution: e.institution || e.Institution || '',
    Year: e.year || e.Year || '',
    CGPA: e.cgpa || e.CGPA || ''
  }));

  const experience = (data.experience || data.Experience || []).map(e => ({
    Title: e.role || e.Title || '',
    Company: e.company || e.Company || '',
    Duration: e.duration || e.Duration || '',
    Description: e.description || e.Description || ''
  }));

  const projects = (data.projects || data.Projects || []).map(p => ({
    Title: p.name || p.Title || '',
    Description: p.description || p.Description || '',
    Tech: p.tech_stack || p.TechnologiesUsed || [],
    Link: p.link || p.Link || ''
  }));

  const certifications = data.certifications || data.Certifications || [];
  const achievements = data.achievements || data.Achievements || [];
  const languages = data.languages || data.Languages || [];

  return (
    <div className="space-y-1">

      {/* Personal Information */}
      <Section icon={User} title="Personal Information" color="text-sky-400">
        <InfoRow label="Full Name" value={name} />
        <InfoRow label="Career Domain" value={domain} />
        <InfoRow label="Preferred Roles" value={Array.isArray(roles) ? roles.join(', ') : roles} />
        <InfoRow label="Location" value={location} />
      </Section>

      {/* Contact Details */}
      <Section icon={Mail} title="Contact Details" color="text-violet-400">
        <InfoRow label="Email" value={email} />
        <InfoRow label="Phone" value={phone} />
        {linkedin && (
          <div className="flex items-center gap-2 text-sm mb-2">
            <span className="text-gray-500 w-36">LinkedIn</span>
            <a href={linkedin.startsWith('http') ? linkedin : `https://${linkedin}`} target="_blank" rel="noreferrer" className="text-violet-400 hover:underline flex items-center gap-1">
              View Profile <ExternalLink size={12} />
            </a>
          </div>
        )}
        {github && (
          <div className="flex items-center gap-2 text-sm mb-2">
            <span className="text-gray-500 w-36">GitHub</span>
            <a href={github.startsWith('http') ? github : `https://${github}`} target="_blank" rel="noreferrer" className="text-violet-400 hover:underline flex items-center gap-1">
              View Profile <ExternalLink size={12} />
            </a>
          </div>
        )}
        {portfolio && (
          <div className="flex items-center gap-2 text-sm mb-2">
            <span className="text-gray-500 w-36">Portfolio</span>
            <a href={portfolio.startsWith('http') ? portfolio : `https://${portfolio}`} target="_blank" rel="noreferrer" className="text-violet-400 hover:underline flex items-center gap-1">
              View Portfolio <ExternalLink size={12} />
            </a>
          </div>
        )}
      </Section>

      {/* Technical Skills */}
      {allTech.length > 0 && (
        <Section icon={Code2} title="Technical Skills" color="text-emerald-400">
          <div className="flex flex-wrap">
            {allTech.map((s, i) => <Chip key={i} text={s} color="bg-emerald-900/40 text-emerald-300 border-emerald-800" />)}
          </div>
        </Section>
      )}

      {/* Soft Skills */}
      {softSkills.length > 0 && (
        <Section icon={Star} title="Soft Skills" color="text-pink-400">
          <div className="flex flex-wrap">
            {softSkills.map((s, i) => <Chip key={i} text={s} color="bg-pink-900/40 text-pink-300 border-pink-800" />)}
          </div>
        </Section>
      )}

      {/* Education */}
      {education.length > 0 && (
        <Section icon={GraduationCap} title="Education" color="text-amber-400">
          {education.map((edu, i) => (
            <div key={i} className="mb-4 pl-3 border-l-2 border-amber-700">
              <p className="font-semibold text-amber-300">{edu.Degree} {edu.FieldOfStudy ? `— ${edu.FieldOfStudy}` : ''}</p>
              <p className="text-gray-400 text-sm">{edu.Institution}</p>
              <p className="text-gray-500 text-xs">{edu.Year} {edu.CGPA ? `• CGPA: ${edu.CGPA}` : ''}</p>
            </div>
          ))}
        </Section>
      )}

      {/* Experience */}
      {experience.length > 0 && (
        <Section icon={Briefcase} title="Experience" color="text-blue-400">
          {experience.map((exp, i) => (
            <div key={i} className="mb-4 pl-3 border-l-2 border-blue-700">
              <p className="font-semibold text-blue-300">{exp.Title} {exp.Company ? `@ ${exp.Company}` : ''}</p>
              <p className="text-gray-500 text-xs mb-1">{exp.Duration}</p>
              <p className="text-gray-400 text-sm">{exp.Description}</p>
            </div>
          ))}
        </Section>
      )}

      {/* Projects */}
      {projects.length > 0 && (
        <Section icon={Terminal} title="Projects" color="text-orange-400">
          {projects.map((proj, i) => (
            <div key={i} className="mb-4 rounded-xl bg-gray-900/60 border border-gray-800 p-4">
              <div className="flex items-center justify-between mb-1">
                <p className="font-bold text-orange-300">{proj.Title}</p>
                {proj.Link && proj.Link !== 'null' && (
                  <a href={proj.Link} target="_blank" rel="noreferrer" className="text-orange-400 text-xs hover:underline flex items-center gap-1">
                    View <ExternalLink size={11} />
                  </a>
                )}
              </div>
              <p className="text-gray-400 text-sm mb-2">{proj.Description}</p>
              <div className="flex flex-wrap">
                {(proj.Tech || []).map((t, j) => <Chip key={j} text={t} color="bg-orange-900/30 text-orange-300 border-orange-800" />)}
              </div>
            </div>
          ))}
        </Section>
      )}

      {/* Certifications */}
      {certifications.length > 0 && (
        <Section icon={Award} title="Certifications" color="text-yellow-400">
          <ul className="list-disc pl-4 space-y-1">
            {certifications.map((c, i) => <li key={i} className="text-gray-300 text-sm">{c}</li>)}
          </ul>
        </Section>
      )}

      {/* Achievements */}
      {achievements.length > 0 && (
        <Section icon={Star} title="Achievements" color="text-rose-400">
          <ul className="list-disc pl-4 space-y-1">
            {achievements.map((a, i) => <li key={i} className="text-gray-300 text-sm">{a}</li>)}
          </ul>
        </Section>
      )}

      {/* Languages */}
      {languages.length > 0 && (
        <Section icon={Globe} title="Languages" color="text-cyan-400">
          <div className="flex flex-wrap">
            {languages.map((l, i) => <Chip key={i} text={l} color="bg-cyan-900/40 text-cyan-300 border-cyan-800" />)}
          </div>
        </Section>
      )}
    </div>
  );
}

// ─── Main Dashboard Component ──────────────────────────────
export default function Dashboard() {
  const [links, setLinks] = useState({ resume: null, portfolio: null, linkedin: null, github: null, leetcode: null });
  const [isScanning, setIsScanning] = useState(false);
  const [resumeProfile, setResumeProfile] = useState(null);
  const [editingSlot, setEditingSlot] = useState(null);
  const [editValue, setEditValue] = useState('');
  const [editError, setEditError] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [scanError, setScanError] = useState('');
  const resumeFileRef = useRef(null);

  const validateLink = (id, url) => {
    if (!url || url.trim() === '') return '';
    try {
      const parsed = new URL(url);
      if (parsed.protocol !== 'https:') return 'Must be a valid https:// URL';
      if (id === 'linkedin' && !parsed.hostname.includes('linkedin.com')) return 'Must be a valid linkedin.com URL';
      if (id === 'github' && !parsed.hostname.includes('github.com')) return 'Must be a valid github.com URL';
      if (id === 'leetcode' && !parsed.hostname.includes('leetcode.com')) return 'Must be a valid leetcode.com URL';
      return '';
    } catch (e) {
      return 'Please enter a valid URL (e.g., https://...)';
    }
  };

  useEffect(() => {
    setIsLoading(true);
    getLinks()
      .then(res => setLinks(res.data))
      .catch(err => console.error("Failed to fetch links", err))
      .finally(() => setIsLoading(false));
  }, []);

  const handleSave = async (key, val) => {
    const error = validateLink(key, val);
    if (error) { setEditError(error); return; }
    const newLinks = { ...links, [key]: val };
    setLinks(newLinks);
    setEditingSlot(null);
    setEditError('');
    try { await updateLinks({ [key]: val }); }
    catch (err) { console.error("Failed to save to backend", err); }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setIsUploading(true);
    resumeFileRef.current = file;
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await uploadResume(formData);
      setLinks(prev => ({ ...prev, resume: file.name }));
      // Store the parsed profile directly from the upload response
      if (res.data?.data) {
        setResumeProfile(res.data.data);
      }
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleScan = async () => {
    // If we already have profile from upload, just scroll/reveal it
    if (resumeProfile) {
      // Re-trigger animation by clearing and resetting
      const saved = resumeProfile;
      setResumeProfile(null);
      setTimeout(() => setResumeProfile(saved), 100);
      return;
    }
    if (!resumeFileRef.current) {
      setScanError('Please upload your resume PDF first.');
      return;
    }
    setIsScanning(true);
    setScanError('');
    try {
      const formData = new FormData();
      formData.append('file', resumeFileRef.current);
      const res = await uploadResume(formData);
      if (res.data?.data) {
        setResumeProfile(res.data.data);
      } else {
        setScanError('Could not extract profile. Please try again.');
      }
    } catch (err) {
      console.error("Scan failed", err);
      setScanError('Failed to connect to the AI backend. Please try again.');
    } finally {
      setIsScanning(false);
    }
  };

  const hasResume = !!links.resume;

  const slots = [
    { id: 'resume', label: 'Upload Resume', subtext: 'PDF or DOCX', icon: <FileText size={28} className="mb-3 text-gray-300" /> },
    { id: 'portfolio', label: 'Portfolio', subtext: 'Visit Profile', icon: <Globe size={28} className="mb-3 text-blue-400" /> },
    { id: 'linkedin', label: 'LinkedIn', subtext: 'Visit Profile', icon: <Briefcase size={28} className="mb-3 text-amber-600" /> },
    { id: 'github', label: 'GitHub', subtext: 'Visit Profile', icon: <Terminal size={28} className="mb-3 text-pink-400" /> },
    { id: 'leetcode', label: 'LeetCode', subtext: 'Visit Profile', icon: <Cpu size={28} className="mb-3 text-yellow-500" /> }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-8 pb-24 text-white"
    >
      <div className="mb-10">
        <h1 className="text-3xl font-bold">Welcome <span className="text-primary">Back</span> 👋</h1>
        <p className="text-gray-400 mt-2 text-sm">Your career health at a glance</p>
      </div>

      {/* Profile Links Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8">
        {slots.map((slot) => {
          const url = links[slot.id] ? (links[slot.id].startsWith('http') ? links[slot.id] : `https://${links[slot.id]}`) : '#';
          const isEditing = editingSlot === slot.id;
          const hasLink = !!links[slot.id];

          if (slot.id === 'resume') {
            return (
              <div key={slot.id} className="bg-[#1e2128] p-6 rounded-2xl border border-gray-800 min-h-[140px] flex flex-col items-center justify-center transition-all hover:border-gray-600 relative">
                <label className="flex flex-col items-center w-full cursor-pointer hover:opacity-80 transition-opacity">
                  {isUploading ? <Loader2 size={28} className="mb-3 text-gray-300 animate-spin" /> : slot.icon}
                  <h3 className="font-semibold mb-1 text-center text-sm">{slot.label}</h3>
                  <span className="text-xs text-gray-500 text-center block w-full truncate px-2">
                    {links.resume ? links.resume : 'Click to Upload'}
                  </span>
                  <input type="file" className="hidden" accept=".pdf,.doc,.docx" onChange={handleFileUpload} disabled={isUploading} />
                </label>
              </div>
            );
          }

          return (
            <div key={slot.id} className="bg-[#1e2128] p-6 rounded-2xl border border-gray-800 min-h-[140px] flex flex-col items-center justify-center transition-all hover:border-gray-600 relative">
              {isEditing ? (
                <div className="flex flex-col items-center w-full">
                  <input
                    type="text"
                    value={editValue}
                    onChange={(e) => { const val = e.target.value; setEditValue(val); setEditError(validateLink(slot.id, val)); }}
                    placeholder="Enter URL (https://...)"
                    className={`w-full bg-gray-900 border ${editError ? 'border-red-500' : 'border-gray-700'} rounded p-2 text-sm text-white mb-1 outline-none`}
                    onKeyDown={(e) => { if (e.key === 'Enter' && !editError) handleSave(slot.id, editValue); }}
                    autoFocus
                  />
                  {editError && <span className="text-red-400 text-[10px] mb-2 w-full text-left">{editError}</span>}
                  <div className="flex space-x-2 w-full mt-1">
                    <button onClick={() => handleSave(slot.id, editValue)} disabled={!!editError} className="flex-1 bg-primary text-white text-xs py-1 rounded hover:bg-blue-600 disabled:opacity-50">Save</button>
                    <button onClick={() => { setEditingSlot(null); setEditError(''); }} className="flex-1 bg-gray-700 text-white text-xs py-1 rounded hover:bg-gray-600">Cancel</button>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center w-full">
                  <a
                    href={hasLink ? url : '#'}
                    target={hasLink ? "_blank" : "_self"}
                    rel="noopener noreferrer"
                    className="flex flex-col items-center w-full cursor-pointer hover:opacity-80 transition-opacity"
                    onClick={(e) => { if (!hasLink) { e.preventDefault(); setEditingSlot(slot.id); setEditValue(''); setEditError(''); } }}
                  >
                    {slot.icon}
                    <h3 className="font-semibold mb-1 text-center text-sm">{slot.label}</h3>
                    <span className="text-xs text-gray-500 text-center block w-full">{hasLink ? 'Visit Profile' : '+ Add Link'}</span>
                  </a>
                  {hasLink && (
                    <button onClick={() => { setEditingSlot(slot.id); setEditValue(links[slot.id] || ''); setEditError(''); }} className="absolute top-2 right-2 text-gray-500 hover:text-white text-xs">
                      Edit
                    </button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* WhatsApp Community Banner */}
      <div className="mt-8 bg-[#00A884] rounded-2xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between relative overflow-hidden shadow-lg border border-[#00c59a]">
        <div className="absolute -right-20 -top-20 w-64 h-64 border-[30px] border-white/5 rounded-full pointer-events-none"></div>
        <div className="absolute -right-10 -bottom-10 w-48 h-48 border-[20px] border-white/5 rounded-full pointer-events-none"></div>
        <div className="flex items-center space-x-6 z-10 w-full md:w-auto">
          <div className="hidden sm:flex bg-white/20 p-4 rounded-2xl items-center justify-center backdrop-blur-sm border border-white/30 shrink-0">
            <MessageCircle size={36} className="text-white" />
          </div>
          <div>
            <h2 className="text-xl md:text-2xl font-bold text-white mb-2">Join the Official WhatsApp Community</h2>
            <p className="text-white/90 text-sm md:text-base max-w-2xl leading-relaxed">
              Connect with ambitious professionals. Share career milestones, discuss AI-powered roadmaps, and get tips to land your dream role.
            </p>
          </div>
        </div>
        <a
          href="https://chat.whatsapp.com/GDXtxLFZdvs228lJm6WBLd"
          target="_blank"
          rel="noopener noreferrer"
          className="mt-6 md:mt-0 flex items-center justify-center space-x-2 bg-white text-[#00A884] font-bold px-6 py-3 rounded-xl hover:bg-gray-50 transition-colors shrink-0 shadow-sm z-10 w-full md:w-auto"
        >
          <span>Join WhatsApp Group</span>
          <ExternalLink size={18} />
        </a>
      </div>

      {/* Scan Button */}
      <div className="mt-12 flex flex-col items-center">
        <button
          disabled={!hasResume || isScanning}
          onClick={handleScan}
          className="flex items-center justify-center space-x-2 px-10 py-4 bg-primary text-white font-bold text-lg rounded-xl shadow-[0_0_15px_rgba(59,130,246,0.4)] disabled:shadow-none disabled:bg-gray-800 disabled:text-gray-500 disabled:cursor-not-allowed hover:bg-blue-600 transition-all min-w-[250px]"
        >
          {isScanning ? (
            <><Loader2 className="animate-spin" size={24} /><span>SCANNING AI...</span></>
          ) : (
            <><Sparkles size={24} /><span>SCAN PROFILE</span></>
          )}
        </button>
        {!hasResume && (
          <p className="text-gray-500 text-xs mt-3">Upload your resume above to enable scanning</p>
        )}
        {scanError && (
          <p className="text-red-400 text-sm mt-3">{scanError}</p>
        )}
      </div>

      {/* Resume Profile Results */}
      <AnimatePresence>
        {resumeProfile && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mt-12"
          >
            <div className="flex items-center gap-3 mb-6">
              <FileText size={22} className="text-cyan-400" />
              <h2 className="text-xl font-bold text-white">Resume Details</h2>
            </div>
            <ResumeProfileViewer data={resumeProfile} />
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
