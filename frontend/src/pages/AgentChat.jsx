import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { sendChatMessage } from '../services/api';
import { Send, User, Sparkles, AlertCircle, Zap, BookOpen, Briefcase, Target } from 'lucide-react';

const QUICK_PROMPTS = [
  { icon: <Briefcase size={14} />, text: "How do I find internships?" },
  { icon: <Target size={14} />, text: "Review my resume strategy" },
  { icon: <BookOpen size={14} />, text: "Top skills to learn in 2025" },
  { icon: <Zap size={14} />, text: "How to crack tech interviews?" },
];

function MessageBubble({ msg }) {
  const isUser = msg.sender === 'user';
  return (
    <motion.div
      initial={{ opacity: 0, y: 16, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`flex items-end gap-2.5 max-w-[80%] ${isUser ? 'flex-row-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center
          ${isUser
            ? 'bg-gradient-to-br from-violet-500 to-purple-600 shadow-lg shadow-violet-500/30'
            : 'bg-gradient-to-br from-cyan-500 to-teal-600 shadow-lg shadow-cyan-500/30'}`}
        >
          {isUser
            ? <User size={15} className="text-white" />
            : <Sparkles size={15} className="text-white" />
          }
        </div>

        {/* Bubble */}
        <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap
          ${isUser
            ? 'bg-gradient-to-br from-violet-600 to-purple-700 text-white rounded-br-md shadow-lg shadow-violet-500/20'
            : msg.isError
              ? 'bg-red-900/40 border border-red-500/30 text-red-200 rounded-bl-md'
              : 'bg-white/5 border border-white/10 text-gray-100 rounded-bl-md backdrop-blur-sm'
          }`}
        >
          {msg.isError && <AlertCircle size={14} className="inline mr-1 mb-0.5 text-red-400" />}
          {msg.text}
        </div>
      </div>
    </motion.div>
  );
}

function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 10 }}
      className="flex justify-start mb-4"
    >
      <div className="flex items-end gap-2.5">
        <div className="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center bg-gradient-to-br from-cyan-500 to-teal-600 shadow-lg shadow-cyan-500/30">
          <Sparkles size={15} className="text-white" />
        </div>
        <div className="px-4 py-3 rounded-2xl rounded-bl-md bg-white/5 border border-white/10 flex gap-1.5 items-center">
          {[0, 0.2, 0.4].map((delay, i) => (
            <motion.div
              key={i}
              animate={{ y: [0, -5, 0] }}
              transition={{ repeat: Infinity, duration: 0.8, delay, ease: 'easeInOut' }}
              className="w-2 h-2 bg-cyan-400 rounded-full"
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}

export default function AgentChat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "👋 Hi! I'm your AI Career Agent powered by Gemini.\n\nI can help you with job searching, resume tips, interview prep, skill planning, and career strategy.\n\nWhat would you like to work on today?",
      sender: 'bot'
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSend = async (text) => {
    const message = text || input;
    if (!message.trim() || isTyping) return;

    const userMsg = { id: Date.now(), text: message.trim(), sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await sendChatMessage(message.trim());
      // Handle both response shapes: res.data.data.response or res.data.response
      const reply = res?.data?.data?.response || res?.data?.response;
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: reply || 'Response received but was empty. Please try again.',
        sender: 'bot'
      }]);
    } catch (err) {
      const statusCode = err?.response?.status;
      const serverMsg = err?.response?.data?.message;
      let errorText = '';

      if (!err.response) {
        errorText = '⚠️ Cannot connect to the backend server.\n\nMake sure Flask is running:\n  cd backend\n  .\\venv\\Scripts\\python.exe run.py';
      } else if (statusCode === 500 && serverMsg?.includes('AI service error')) {
        errorText = '⚠️ Gemini API error — the API key may be invalid or expired.\n\nPlease update GEMINI_API_KEY in your backend .env file with a valid key from aistudio.google.com';
      } else {
        errorText = `⚠️ Server error (${statusCode || 'unknown'}): ${serverMsg || err.message}`;
      }

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: errorText,
        sender: 'bot',
        isError: true
      }]);
    } finally {
      setIsTyping(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-transparent">
      {/* Header */}
      <div className="px-8 pt-8 pb-4 flex-shrink-0">
        <div className="flex items-center gap-3 mb-1">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-violet-600 flex items-center justify-center shadow-lg shadow-violet-500/30">
            <Sparkles size={20} className="text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">AI Career Agent</h1>
            <p className="text-sm text-gray-400">Powered by Gemini · Your personal career strategist</p>
          </div>
          {/* Live status dot */}
          <div className="ml-auto flex items-center gap-2 bg-white/5 border border-white/10 px-3 py-1.5 rounded-full">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse shadow-sm shadow-emerald-400" />
            <span className="text-xs text-emerald-400 font-medium">Online</span>
          </div>
        </div>
      </div>

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto px-8 py-4 space-y-1"
        style={{ scrollbarWidth: 'thin', scrollbarColor: 'rgba(255,255,255,0.1) transparent' }}>
        <AnimatePresence>
          {messages.map(msg => <MessageBubble key={msg.id} msg={msg} />)}
        </AnimatePresence>
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts */}
      {messages.length <= 1 && (
        <div className="px-8 pb-3 flex gap-2 flex-wrap">
          {QUICK_PROMPTS.map((p, i) => (
            <motion.button
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              onClick={() => handleSend(p.text)}
              className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white/5 border border-white/10
                text-gray-300 text-xs hover:bg-white/10 hover:border-violet-500/50 hover:text-white
                transition-all duration-200 cursor-pointer"
            >
              <span className="text-violet-400">{p.icon}</span>
              {p.text}
            </motion.button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="px-8 pb-8 flex-shrink-0">
        <div className="flex gap-3 items-end bg-white/5 border border-white/10 rounded-2xl px-4 py-3
          focus-within:border-violet-500/60 focus-within:bg-white/8 transition-all duration-200">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about interviews, resume tips, skills, career paths..."
            rows={1}
            className="flex-1 bg-transparent text-sm text-gray-100 placeholder-gray-500 resize-none
              focus:outline-none leading-relaxed"
            style={{ maxHeight: '120px' }}
            onInput={(e) => {
              e.target.style.height = 'auto';
              e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
            }}
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isTyping}
            className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 transition-all duration-200
              bg-gradient-to-br from-violet-500 to-purple-600 hover:from-violet-400 hover:to-purple-500
              disabled:opacity-30 disabled:cursor-not-allowed shadow-lg shadow-violet-500/30
              hover:shadow-violet-500/50 hover:scale-105 active:scale-95"
          >
            <Send size={16} className="text-white" />
          </button>
        </div>
        <p className="text-center text-xs text-gray-600 mt-2">Press Enter to send · Shift+Enter for new line</p>
      </div>
    </div>
  );
}
