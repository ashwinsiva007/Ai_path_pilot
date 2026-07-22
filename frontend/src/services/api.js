import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

// Resume API
export const uploadResume = (formData) => api.post('/resume/upload', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Opportunity API
export const getOpportunities = () => api.get('/opportunity/match');

// Dashboard API
export const getDashboardSummary = () => api.get('/dashboard/summary');

// Skill Gap API
export const getSkillGapAnalysis = () => api.get('/skill_gap/analyze');

// Roadmap API
export const getLearningRoadmap = () => api.get('/roadmap/generate');

// Chat API
export const sendChatMessage = (message) => api.post('/chat/send', { message });

export default api;
