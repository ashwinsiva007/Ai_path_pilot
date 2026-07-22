import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { sendChatMessage } from '../services/api';
import { Send, User, Bot } from 'lucide-react';

export default function AgentChat() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI Career Agent. I've analyzed your profile. How can I help you today?", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await sendChatMessage(input);
      setMessages(prev => [...prev, { id: Date.now(), text: res.data.response || 'I processed that.', sender: 'bot' }]);
    } catch (err) {
      // Mock response on error
      setTimeout(() => {
        setMessages(prev => [...prev, { id: Date.now(), text: "I'm currently running in offline mock mode, but I'll make sure to note that down for your career strategy!", sender: 'bot' }]);
      }, 1000);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-screen p-8 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">AI Career Agent</h1>
        <p className="text-textSecondary">Chat with your personalized career assistant.</p>
      </div>

      <div className="flex-1 bg-surface border border-gray-800 rounded-xl flex flex-col overflow-hidden shadow-2xl">
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg) => (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={msg.id} 
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex items-start max-w-[80%] space-x-3 ${msg.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${msg.sender === 'user' ? 'bg-primary' : 'bg-secondary'}`}>
                  {msg.sender === 'user' ? <User size={16} className="text-white" /> : <Bot size={16} className="text-white" />}
                </div>
                <div className={`p-4 rounded-2xl text-sm ${msg.sender === 'user' ? 'bg-primary text-white rounded-tr-none' : 'bg-gray-800 text-textPrimary rounded-tl-none'}`}>
                  {msg.text}
                </div>
              </div>
            </motion.div>
          ))}
          {isTyping && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
              <div className="flex items-start space-x-3 max-w-[80%]">
                <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 bg-secondary">
                  <Bot size={16} className="text-white" />
                </div>
                <div className="p-4 rounded-2xl bg-gray-800 rounded-tl-none flex space-x-2 items-center">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                </div>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 border-t border-gray-800 bg-surface">
          <form onSubmit={handleSend} className="flex space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about interview prep, resume tips..."
              className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all text-sm"
            />
            <button 
              type="submit"
              disabled={!input.trim() || isTyping}
              className="bg-primary hover:bg-blue-600 disabled:opacity-50 text-white p-3 rounded-xl transition-colors flex items-center justify-center"
            >
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
