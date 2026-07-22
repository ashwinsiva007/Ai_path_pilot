import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getSkillGapAnalysis } from '../services/api';
import { Target, AlertTriangle, BookOpen } from 'lucide-react';

export default function SkillGap() {
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    // Mock data
    const mockData = {
      targetRole: 'Senior Frontend Developer',
      currentScore: 72,
      skills: [
        { name: 'React', current: 90, required: 90, status: 'met' },
        { name: 'TypeScript', current: 60, required: 85, status: 'gap' },
        { name: 'System Design', current: 40, required: 75, status: 'gap' },
        { name: 'GraphQL', current: 80, required: 70, status: 'met' },
      ],
      recommendations: [
        'Complete Advanced TypeScript Patterns course.',
        'Read "Designing Data-Intensive Applications".'
      ]
    };
    
    getSkillGapAnalysis().then(res => {
      setAnalysis(res.data || mockData);
    }).catch(err => {
      console.error(err);
      setAnalysis(mockData);
    });
  }, []);

  if (!analysis) return <div className="p-8">Loading...</div>;

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Skill Gap Analysis</h1>
        <p className="text-textSecondary flex items-center">
          <Target size={18} className="mr-2 text-primary" />
          Target Role: <strong className="ml-1 text-textPrimary">{analysis.targetRole}</strong>
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-surface rounded-xl border border-gray-800 p-6">
            <h2 className="text-xl font-semibold mb-6">Skills Assessment</h2>
            
            <div className="space-y-6">
              {analysis.skills.map((skill, i) => (
                <div key={i}>
                  <div className="flex justify-between items-end mb-2">
                    <span className="font-medium text-sm flex items-center">
                      {skill.name}
                      {skill.status === 'gap' && <AlertTriangle size={14} className="ml-2 text-yellow-500" />}
                    </span>
                    <span className="text-xs text-textSecondary">Target: {skill.required}%</span>
                  </div>
                  <div className="h-3 w-full bg-gray-800 rounded-full overflow-hidden relative">
                    <div 
                      className={`absolute top-0 left-0 h-full rounded-full transition-all duration-1000 ${
                        skill.status === 'gap' ? 'bg-yellow-500' : 'bg-primary'
                      }`}
                      style={{ width: `${skill.current}%` }}
                    />
                    <div 
                      className="absolute top-0 h-full w-1 bg-white opacity-50 z-10"
                      style={{ left: `${skill.required}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-surface rounded-xl border border-gray-800 p-6 h-fit">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <BookOpen size={20} className="mr-2 text-primary" />
            AI Recommendations
          </h2>
          <ul className="space-y-4">
            {analysis.recommendations.map((rec, i) => (
              <li key={i} className="flex items-start bg-gray-800 bg-opacity-40 p-3 rounded-lg">
                <div className="h-2 w-2 rounded-full bg-secondary mt-2 mr-3 flex-shrink-0" />
                <span className="text-sm text-textSecondary">{rec}</span>
              </li>
            ))}
          </ul>
          <button className="w-full mt-6 py-2 bg-primary hover:bg-blue-600 transition-colors rounded-lg font-medium">
            Generate Learning Roadmap
          </button>
        </div>
      </div>
    </motion.div>
  );
}
