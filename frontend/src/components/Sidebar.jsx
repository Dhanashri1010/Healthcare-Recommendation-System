import React from 'react';
import { motion } from 'framer-motion';
import { 
  Home, 
  Stethoscope, 
  Pill, 
  Dna, 
  BarChart3, 
  FileText, 
  Cpu, 
  Settings, 
  Scale,
  ShieldAlert,
  HeartPulse,
  ChevronLeft, 
  ChevronRight,
  Activity
} from 'lucide-react';

export const Sidebar = ({ activeTab, setActiveTab, collapsed, setCollapsed }) => {
  const menuItems = [
    { id: 'home', label: 'Home', icon: Home, color: 'text-blue-500' },
    { id: 'diagnostics', label: 'Patient Diagnostics', icon: Stethoscope, color: 'text-cyan-500' },
    { id: 'bmi', label: 'BMI Calculator', icon: Scale, color: 'text-indigo-500' },
    { id: 'health_risk', label: 'Health Risk Score', icon: ShieldAlert, color: 'text-amber-500' },
    { id: 'lifestyle', label: 'Lifestyle Plan', icon: HeartPulse, color: 'text-emerald-500' },
    { id: 'medicines', label: 'Medicine Recommendation', icon: Pill, color: 'text-teal-500' },
    { id: 'knowledge', label: 'Disease Knowledge', icon: Dna, color: 'text-purple-500' },
    { id: 'analytics', label: 'Analytics Dashboard', icon: BarChart3, color: 'text-orange-500' },
    { id: 'reports', label: 'Reports', icon: FileText, color: 'text-pink-500' },
    { id: 'models', label: 'AI Models', icon: Cpu, color: 'text-blue-600' },
    { id: 'settings', label: 'Settings', icon: Settings, color: 'text-slate-400' }
  ];

  return (
    <motion.aside
      animate={{ width: collapsed ? 80 : 280 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="relative min-h-screen bg-[var(--bg-card)] border-r border-[var(--border-color)] flex flex-col z-30 shadow-lg"
    >
      {/* Brand Header */}
      <div className="p-6 flex items-center justify-between border-b border-[var(--border-color)]">
        <div className="flex items-center space-x-3 overflow-hidden">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center text-white shadow-md flex-shrink-0">
            <Activity className="w-6 h-6 animate-pulse" />
          </div>
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
            >
              <h1 className="font-bold text-lg leading-tight tracking-wide bg-gradient-to-r from-blue-500 to-cyan-400 bg-clip-text text-transparent">
                MediCare AI
              </h1>
              <p className="text-xs text-[var(--text-secondary)] font-medium">Enterprise SaaS</p>
            </motion.div>
          )}
        </div>
        
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg hover:bg-slate-700/20 text-[var(--text-secondary)] transition-colors"
        >
          {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
        </button>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 py-6 px-3 space-y-1.5 overflow-y-auto">
        {menuItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;

          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`relative w-full flex items-center space-x-3 px-3.5 py-3 rounded-xl transition-all duration-200 font-medium text-sm ${
                isActive
                  ? 'bg-blue-600/10 text-blue-500 font-semibold'
                  : 'text-[var(--text-secondary)] hover:bg-slate-700/10 hover:text-[var(--text-primary)]'
              }`}
            >
              {isActive && (
                <motion.div
                  layoutId="activeIndicator"
                  className="active-nav-indicator"
                  transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                />
              )}

              <Icon className={`w-5 h-5 flex-shrink-0 ${item.color}`} />
              
              {!collapsed && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="truncate"
                >
                  {item.label}
                </motion.span>
              )}
            </button>
          );
        })}
      </nav>

      {/* System Status Footer */}
      {!collapsed && (
        <div className="p-4 m-3 rounded-xl bg-blue-600/5 border border-blue-500/20 text-xs">
          <div className="flex items-center space-x-2 text-emerald-500 font-semibold mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            <span>AI Models Live (100%)</span>
          </div>
          <p className="text-[var(--text-secondary)]">FastAPI Backend Connected</p>
        </div>
      )}
    </motion.aside>
  );
};
