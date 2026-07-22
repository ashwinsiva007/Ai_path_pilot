import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useLocation } from 'react-router-dom';
import { getLearningRoadmap } from '../services/api';
import { CheckCircle, Circle, PlayCircle, Loader2 } from 'lucide-react';

export default function LearningRoadmap() {
  const [roadmap, setRoadmap] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    const missingSkills = location.state?.missingSkills || ["General Software Engineering"];
    
    getLearningRoadmap({ skills: missingSkills }).then(res => {
      setRoadmap(res.data.data.roadmap || []);
      setIsLoading(false);
    }).catch(err => {
      console.error(err);
      setIsLoading(false);
    });
  }, [location]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-[70vh]">
        <Loader2 className="animate-spin text-primary mb-4" size={48} />
        <h2 className="text-xl text-gray-400">AI is designing your personalized curriculum...</h2>
      </div>
    );
  }

  if (!roadmap || roadmap.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-[70vh]">
        <h2 className="text-xl text-gray-400">No roadmap generated. Try running the Compare Fit tool first!</h2>
      </div>
    );
  }

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
              <p className="text-sm text-gray-300 mt-2 leading-relaxed">
                {step.description || "Master this module to progress in your learning path."}
              </p>
              
              <button className="mt-4 text-sm bg-primary bg-opacity-10 text-primary hover:bg-opacity-20 px-4 py-2 rounded-lg font-medium transition-colors">
                Explore Resources
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
