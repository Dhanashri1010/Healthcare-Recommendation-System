import React from 'react';
import { motion } from 'framer-motion';

export const KPICard = ({ title, value, description, icon: Icon, gradient, badge }) => {
  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.02 }}
      transition={{ duration: 0.2 }}
      className={`glass-card p-6 relative overflow-hidden ${gradient}`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">
            {title}
          </p>
          <h3 className="text-3xl font-extrabold mt-2 text-[var(--text-primary)] tracking-tight">
            {value}
          </h3>
        </div>

        {Icon && (
          <div className="w-12 h-12 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center text-blue-500 shadow-md">
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>

      <div className="mt-4 flex items-center justify-between">
        <p className="text-xs text-[var(--text-secondary)] font-medium">
          {description}
        </p>
        {badge && (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            {badge}
          </span>
        )}
      </div>
    </motion.div>
  );
};
