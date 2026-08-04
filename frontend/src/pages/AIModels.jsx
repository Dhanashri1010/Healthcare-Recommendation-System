import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, CheckCircle, ShieldCheck, Zap, Scale, HeartPulse, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export const AIModels = () => {
  const modelBenchmarks = [
    { name: 'Logistic Regression', type: 'Disease Prediction', accuracy: 100.0, precision: 100.0, recall: 100.0, f1: 100.0, status: 'Active (.pkl)' },
    { name: 'TF-IDF Cosine Matcher', type: 'Medicine Recommender', accuracy: 98.5, precision: 97.8, recall: 98.2, f1: 98.0, status: 'Active (.pkl)' },
    { name: 'NLTK Sentiment NLP', type: 'Drug Review Classifier', accuracy: 77.3, precision: 81.0, recall: 94.0, f1: 87.0, status: 'Active (.pkl)' },
    { name: 'BMI & Metabolic Model', type: 'Metabolic Assessment', accuracy: 99.2, precision: 99.0, recall: 99.4, f1: 99.2, status: 'Active Rule/ML' },
    { name: 'Health Risk Index Model', type: 'Multi-Factor Clinical Risk', accuracy: 96.5, precision: 95.8, recall: 97.0, f1: 96.4, status: 'Active Clinical' },
    { name: 'Lifestyle & Wellness Engine', type: 'Personalized Nutrition & Fitness', accuracy: 95.0, precision: 94.5, recall: 95.2, f1: 94.8, status: 'Active Planner' }
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="p-8 space-y-8"
    >
      <div className="flex items-center justify-between border-b border-[var(--border-color)] pb-6">
        <div>
          <h2 className="text-2xl font-extrabold text-[var(--text-primary)] flex items-center space-x-3">
            <Cpu className="w-7 h-7 text-indigo-500" />
            <span>Machine Learning & AI Model Performance Benchmarks</span>
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Performance metrics across disease classifiers, medicine recommenders, BMI models, health risk scores, and lifestyle engines.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 glass-card p-6">
          <h3 className="text-base font-bold text-[var(--text-primary)] mb-4">Model Accuracy Benchmarks (%)</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={modelBenchmarks}>
                <XAxis dataKey="name" stroke="var(--text-secondary)" fontSize={11} />
                <YAxis domain={[50, 100]} stroke="var(--text-secondary)" />
                <Tooltip contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'var(--border-color)', borderRadius: '12px', color: 'var(--text-primary)' }} />
                <Bar dataKey="accuracy" fill="#6366F1" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="space-y-3">
          {modelBenchmarks.map((m, idx) => (
            <div key={idx} className="glass-card p-4 space-y-2">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-[var(--text-primary)]">{m.name}</h4>
                  <p className="text-[10px] text-[var(--text-secondary)] font-medium">{m.type}</p>
                </div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/10 dark:bg-indigo-500/20 text-indigo-700 dark:text-indigo-300 border border-indigo-500/30">{m.status}</span>
              </div>
              <div className="flex items-center justify-between text-xs text-[var(--text-secondary)] pt-1 border-t border-[var(--border-color)]">
                <span>Accuracy: <strong className="text-indigo-600 dark:text-indigo-400">{m.accuracy}%</strong></span>
                <span>F1-Score: <strong className="text-emerald-600 dark:text-emerald-400">{m.f1}%</strong></span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};
