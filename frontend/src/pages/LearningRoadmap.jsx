import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getLearningRoadmap } from '../services/api';
import { CheckCircle, Circle, PlayCircle } from 'lucide-react';

export default function LearningRoadmap() {
  const [roadmap, setRoadmap] = useState([]);

  useEffect(() => {
    const mockData = [
      { id: 1, title: 'TypeScript Fundamentals', duration: '2 weeks', status: 'completed' },
      { id: 2, title: 'Advanced TypeScript Patterns', duration: '3 weeks', status: 'in-progress' },
      { id: 3, title: 'System Design Interview Prep', duration: '4 weeks', status: 'pending' },
      { id: 4, title: 'Mock Interviews', duration: '1 week', status: 'pending' },
    ];
    
    getLearningRoadmap().then(res => {
      setRoadmap(res.data.roadmap || mockData);
    }).catch(() => {
      setRoadmap(mockData);
    });
  }, []);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-8 max-w-4xl mx-auto">
      <div className="mb-10 text-center">
        <h1 className="text-3xl font-bold mb-3 bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">Your AI Learning Roadmap</h1>
        <p className="text-textSecondary">A personalized path to bridge your skill gaps and land your target role.</p>
      </div>

      <div className="relative border-l-2 border-gray-800 ml-6 space-y-10">
        {roadmap.map((step, i) => (
          <motion.div 
            key={step.id}
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: i * 0.15 }}
            className="relative pl-8"
          >
            <div className="absolute -left-[17px] top-1 bg-background p-1">
              {step.status === 'completed' && <CheckCircle className="text-secondary" size={24} />}
              {step.status === 'in-progress' && <PlayCircle className="text-primary" size={24} />}
              {step.status === 'pending' && <Circle className="text-gray-600" size={24} />}
            </div>
            
            <div className={`bg-surface p-6 rounded-xl border ${step.status === 'in-progress' ? 'border-primary shadow-[0_0_15px_rgba(59,130,246,0.1)]' : 'border-gray-800'} transition-all`}>
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-xl font-bold">{step.title}</h3>
                <span className="text-xs font-medium px-2 py-1 bg-gray-800 rounded text-textSecondary">{step.duration}</span>
              </div>
              <p className="text-sm text-textSecondary mt-2">
                {step.status === 'completed' ? 'You have successfully mastered this topic.' :
                 step.status === 'in-progress' ? 'Continue your learning journey with our curated resources.' :
                 'Complete previous steps to unlock this module.'}
              </p>
              
              {step.status === 'in-progress' && (
                <button className="mt-4 text-sm bg-primary bg-opacity-10 text-primary hover:bg-opacity-20 px-4 py-2 rounded-lg font-medium transition-colors">
                  Resume Learning
                </button>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
