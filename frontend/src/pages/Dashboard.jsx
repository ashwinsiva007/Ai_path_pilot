import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { getDashboardSummary } from '../services/api';
import { Activity, Users, Star, Award, Target } from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // In a real app, you'd handle loading and errors
    getDashboardSummary().then(res => setData(res.data)).catch(err => console.error(err));
  }, []);

  const stats = [
    { label: 'Profile Strength', value: data?.profileStrength || '85%', icon: <Star className="text-yellow-400" /> },
    { label: 'Active Applications', value: data?.activeApplications || 3, icon: <Activity className="text-blue-400" /> },
    { label: 'Skills Matched', value: data?.skillsMatched || 12, icon: <Award className="text-green-400" /> },
    { label: 'Network Connections', value: data?.connections || 156, icon: <Users className="text-purple-400" /> },
    { label: 'Goals Completed', value: data?.goalsCompleted || 7, icon: <Target className="text-red-400" /> },
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-8"
    >
      <h1 className="text-3xl font-bold mb-8">Welcome back!</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8">
        {stats.map((stat, i) => (
          <div key={i} className="bg-surface p-6 rounded-xl border border-gray-800 flex items-center justify-between hover:border-primary transition-colors cursor-pointer">
            <div>
              <p className="text-textSecondary text-sm mb-1">{stat.label}</p>
              <h3 className="text-2xl font-bold">{stat.value}</h3>
            </div>
            <div className="p-3 bg-gray-800 rounded-full bg-opacity-50">
              {stat.icon}
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-surface rounded-xl border border-gray-800 p-6">
          <h2 className="text-xl font-semibold mb-4">Recent AI Insights</h2>
          <div className="space-y-4">
            {data?.insights?.map((insight, i) => (
              <div key={i} className="p-4 bg-gray-800 bg-opacity-30 rounded-lg">
                <p className="text-sm">{insight}</p>
              </div>
            )) || (
              <>
                <div className="p-4 bg-gray-800 bg-opacity-30 rounded-lg"><p className="text-sm">We noticed a strong match for a Machine Learning Engineer role at OpenAI.</p></div>
                <div className="p-4 bg-gray-800 bg-opacity-30 rounded-lg"><p className="text-sm">You are 1 skill away from qualifying for Senior Frontend Developer roles.</p></div>
              </>
            )}
          </div>
        </div>

        <div className="bg-surface rounded-xl border border-gray-800 p-6">
          <h2 className="text-xl font-semibold mb-4">Upcoming Tasks</h2>
          <div className="space-y-4">
            <div className="flex items-center space-x-3 text-sm">
              <input type="checkbox" className="rounded text-primary focus:ring-primary bg-gray-800 border-gray-700" />
              <span>Update Resume for Q3</span>
            </div>
            <div className="flex items-center space-x-3 text-sm">
              <input type="checkbox" className="rounded text-primary focus:ring-primary bg-gray-800 border-gray-700" />
              <span>Complete React Advanced Course</span>
            </div>
            <div className="flex items-center space-x-3 text-sm">
              <input type="checkbox" className="rounded text-primary focus:ring-primary bg-gray-800 border-gray-700" />
              <span>Review new internship matches</span>
            </div>
          </div>
        </div>
      </div>

      {/* Empty 5 Grid Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mt-8">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="bg-surface p-6 rounded-xl border border-gray-800 border-dashed min-h-[120px] flex flex-col items-center justify-center text-textSecondary opacity-60 hover:opacity-100 transition-opacity">
            <span className="text-2xl mb-2">+</span>
            <span className="text-sm">Empty Slot</span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
