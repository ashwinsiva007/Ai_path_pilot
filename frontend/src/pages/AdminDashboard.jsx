import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Users, Shield, TrendingUp, Activity } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    // In a real application, you'd fetch this from /api/admin/users
    // For now, we'll mock some data since we don't have that endpoint yet.
    // Or we could build it! Let's assume we have it or mock it.
    setTimeout(() => {
      setUsers([
        { id: 1, username: 'admin', email: 'admin@pathpilot.com', role: 'admin' },
        { id: 2, username: 'testuser', email: 'test@example.com', role: 'user' },
        { id: 3, username: 'kumaran', email: 'kumaran@example.com', role: 'user' },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const stats = [
    { title: 'Total Users', value: users.length, icon: Users, color: 'text-blue-400', bg: 'bg-blue-400/10' },
    { title: 'Active Sessions', value: '24', icon: Activity, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
    { title: 'Admin Accounts', value: users.filter(u => u.role === 'admin').length, icon: Shield, color: 'text-violet-400', bg: 'bg-violet-400/10' },
    { title: 'Weekly Growth', value: '+12%', icon: TrendingUp, color: 'text-cyan-400', bg: 'bg-cyan-400/10' },
  ];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Admin Dashboard</h1>
        <p className="text-gray-400 mt-2">Welcome back, {user?.username}. Here's what's happening on PathPilot.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-surface border border-gray-800 rounded-2xl p-6 flex items-center justify-between"
          >
            <div>
              <p className="text-sm font-medium text-gray-400">{stat.title}</p>
              <p className="text-3xl font-bold text-white mt-1">{stat.value}</p>
            </div>
            <div className={`p-4 rounded-xl ${stat.bg}`}>
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Users Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-surface border border-gray-800 rounded-2xl overflow-hidden"
      >
        <div className="px-6 py-5 border-b border-gray-800 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Registered Users</h2>
          <button className="text-sm font-medium text-cyan-400 hover:text-cyan-300">View All</button>
        </div>
        
        {loading ? (
          <div className="p-8 text-center text-gray-400">Loading users...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-900/50 text-gray-400">
                <tr>
                  <th className="px-6 py-4 font-medium">ID</th>
                  <th className="px-6 py-4 font-medium">Username</th>
                  <th className="px-6 py-4 font-medium">Email</th>
                  <th className="px-6 py-4 font-medium">Role</th>
                  <th className="px-6 py-4 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-gray-800/30 transition-colors">
                    <td className="px-6 py-4 text-gray-500">#{u.id}</td>
                    <td className="px-6 py-4 text-gray-200 font-medium">{u.username}</td>
                    <td className="px-6 py-4 text-gray-400">{u.email}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${
                        u.role === 'admin' 
                          ? 'bg-violet-400/10 text-violet-400 border border-violet-400/20'
                          : 'bg-blue-400/10 text-blue-400 border border-blue-400/20'
                      }`}>
                        {u.role.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button className="text-gray-400 hover:text-white transition-colors">Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </motion.div>
    </div>
  );
}
