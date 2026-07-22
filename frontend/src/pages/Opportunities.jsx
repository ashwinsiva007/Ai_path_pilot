import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getOpportunities } from '../services/api';
import { ExternalLink, Building, MapPin, DollarSign } from 'lucide-react';

export default function Opportunities() {
  const [opportunities, setOpportunities] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    // Mocking data if API is down
    const mockData = [
      { id: 1, title: 'Machine Learning Engineer', company: 'OpenAI', type: 'job', location: 'San Francisco, CA', salary: '$150k - $250k', match: 92 },
      { id: 2, title: 'AI Research Intern', company: 'DeepMind', type: 'internship', location: 'London, UK', salary: 'Paid', match: 88 },
      { id: 3, title: 'Global Hackathon 2026', company: 'Devpost', type: 'hackathon', location: 'Online', salary: '$50k Prize Pool', match: 95 },
      { id: 4, title: 'Data Scientist', company: 'Google', type: 'job', location: 'Remote', salary: '$130k - $190k', match: 85 },
    ];
    
    getOpportunities().then(res => {
      setOpportunities(res.data.opportunities || mockData);
    }).catch(err => {
      console.error(err);
      setOpportunities(mockData);
    });
  }, []);

  const filtered = filter === 'all' ? opportunities : opportunities.filter(o => o.type === filter);

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-8"
    >
      <div className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">Curated Opportunities</h1>
          <p className="text-textSecondary">AI-matched opportunities based on your profile.</p>
        </div>
        <div className="flex space-x-2 bg-surface p-1 rounded-lg border border-gray-800">
          {['all', 'job', 'internship', 'hackathon'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-md capitalize text-sm font-medium transition-colors ${
                filter === f ? 'bg-primary text-white' : 'text-textSecondary hover:text-textPrimary'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {filtered.map((job, index) => (
          <motion.div 
            key={job.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-surface border border-gray-800 rounded-xl p-6 hover:border-primary transition-all group"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-bold mb-1 group-hover:text-primary transition-colors">{job.title}</h2>
                <div className="flex items-center text-textSecondary text-sm space-x-4">
                  <span className="flex items-center"><Building size={14} className="mr-1" /> {job.company}</span>
                  <span className="flex items-center"><MapPin size={14} className="mr-1" /> {job.location}</span>
                </div>
              </div>
              <div className="flex flex-col items-end">
                <span className="bg-green-500 bg-opacity-20 text-green-400 text-xs font-bold px-3 py-1 rounded-full mb-2">
                  {job.match}% Match
                </span>
                <span className="capitalize text-xs text-textSecondary border border-gray-700 px-2 py-1 rounded">
                  {job.type}
                </span>
              </div>
            </div>
            
            <div className="flex justify-between items-center mt-6 pt-4 border-t border-gray-800">
              <span className="flex items-center text-textPrimary font-medium text-sm">
                <DollarSign size={16} className="text-primary mr-1" />
                {job.salary}
              </span>
              <button className="flex items-center text-primary text-sm font-medium hover:text-blue-400 transition-colors">
                Apply Now <ExternalLink size={16} className="ml-1" />
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
