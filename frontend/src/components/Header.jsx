import React from 'react';
import { useTheme } from '../context/ThemeContext';
import { Sun, Moon, Search, Bell, ShieldCheck, User } from 'lucide-react';
import { motion } from 'framer-motion';

export const Header = ({ title, subtitle }) => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 bg-[var(--bg-card)]/80 backdrop-blur-md border-b border-[var(--border-color)] px-8 py-4 flex items-center justify-between shadow-sm">
      {/* Title & Subtitle */}
      <div>
        <h2 className="text-xl font-bold text-[var(--text-primary)] tracking-tight">
          {title}
        </h2>
        {subtitle && (
          <p className="text-xs text-[var(--text-secondary)] font-medium mt-0.5">
            {subtitle}
          </p>
        )}
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-4">
        {/* Global Search */}
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text-secondary)]" />
          <input
            type="text"
            placeholder="Search symptoms, drugs, diseases..."
            className="pl-9 pr-4 py-1.5 text-xs rounded-xl bg-slate-700/10 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500 w-64 transition-all"
          />
        </div>

        {/* Dark / Light Animated Toggle Button */}
        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={toggleTheme}
          className="relative p-2 rounded-xl bg-slate-700/10 border border-[var(--border-color)] hover:bg-slate-700/20 text-[var(--text-primary)] transition-colors flex items-center justify-center"
          title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
        >
          <motion.div
            initial={false}
            animate={{ rotate: isDark ? 0 : 180 }}
            transition={{ duration: 0.3 }}
          >
            {isDark ? (
              <Sun className="w-5 h-5 text-amber-400" />
            ) : (
              <Moon className="w-5 h-5 text-indigo-600" />
            )}
          </motion.div>
        </motion.button>

        {/* Notifications */}
        <button className="relative p-2 rounded-xl bg-slate-700/10 border border-[var(--border-color)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-blue-500" />
        </button>

        {/* User Badge */}
        <div className="flex items-center space-x-3 pl-3 border-l border-[var(--border-color)]">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow-md">
            <User className="w-5 h-5" />
          </div>
          <div className="hidden lg:block text-left">
            <div className="text-xs font-semibold text-[var(--text-primary)] flex items-center space-x-1">
              <span>Dr. Alex Reed</span>
              <ShieldCheck className="w-3.5 h-3.5 text-blue-500 inline" />
            </div>
            <p className="text-[10px] text-[var(--text-secondary)]">Lead Clinician</p>
          </div>
        </div>
      </div>
    </header>
  );
};
