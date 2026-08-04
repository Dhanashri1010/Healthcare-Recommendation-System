import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, Sparkles, PieChart as PieIcon, Activity } from 'lucide-react';
import { 
  AreaChart, Area, LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, 
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Treemap, Tooltip, ResponsiveContainer, XAxis, YAxis 
} from 'recharts';

export const AnalyticsDashboard = () => {
  const lineData = [
    { month: 'Jan', diseaseCount: 38, avgRating: 6.8 },
    { month: 'Feb', diseaseCount: 39, avgRating: 6.9 },
    { month: 'Mar', diseaseCount: 40, avgRating: 7.0 },
    { month: 'Apr', accuracy: 41, avgRating: 7.1 },
    { month: 'May', accuracy: 41, avgRating: 7.2 },
    { month: 'Jun', accuracy: 41, avgRating: 7.4 }
  ];

  const symptomFreqData = [
    { name: 'Fatigue', count: 45 },
    { name: 'Vomiting', count: 41 },
    { name: 'High Fever', count: 32 },
    { name: 'Loss of Appetite', count: 30 },
    { name: 'Nausea', count: 29 },
    { name: 'Headache', count: 27 }
  ];

  const sentimentData = [
    { name: 'Positive (7-10)', value: 66.25, fill: '#10B981' },
    { name: 'Negative (1-3)', value: 21.74, fill: '#EF4444' },
    { name: 'Neutral (4-6)', value: 12.01, fill: '#F59E0B' }
  ];

  const radarData = [
    { metric: 'Accuracy', value: 100 },
    { metric: 'Precision', value: 100 },
    { metric: 'Recall', value: 100 },
    { metric: 'F1-Score', value: 100 },
    { metric: 'CV Score', value: 100 },
    { metric: 'NLP Accuracy', value: 77.3 }
  ];

  const treemapData = [
    { name: 'Infectious', size: 3500 },
    { name: 'Gastrointestinal', size: 2800 },
    { name: 'Cardiovascular', size: 2300 },
    { name: 'Neurological', size: 1900 },
    { name: 'Metabolic', size: 1700 },
    { name: 'Respiratory', size: 1400 }
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="p-8 space-y-8"
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-[var(--border-color)] pb-6">
        <div>
          <h2 className="text-2xl font-extrabold text-[var(--text-primary)] flex items-center space-x-3">
            <BarChart3 className="w-7 h-7 text-orange-500" />
            <span>Interactive Analytics & Data Visualization Dashboard</span>
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Enterprise analytics visualizing disease prevalence, symptom frequencies, review sentiments, and model benchmarks.
          </p>
        </div>
      </div>

      {/* Grid 1: Line Chart & Bar Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Line Chart */}
        <div className="glass-card p-6">
          <h3 className="text-base font-bold text-[var(--text-primary)] mb-2 flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-blue-500" />
            <span>Average Patient Satisfaction Rating Trend (Line Chart)</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={lineData}>
                <XAxis dataKey="month" stroke="#64748B" />
                <YAxis domain={[6, 8]} stroke="#64748B" />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }} />
                <Line type="monotone" dataKey="avgRating" stroke="#06B6D4" strokeWidth={3} dot={{ r: 6, fill: '#06B6D4' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar Chart */}
        <div className="glass-card p-6">
          <h3 className="text-base font-bold text-[var(--text-primary)] mb-2 flex items-center space-x-2">
            <Activity className="w-5 h-5 text-emerald-500" />
            <span>Top Symptom Frequencies Across Pathology Profiles (Bar Chart)</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={symptomFreqData}>
                <XAxis dataKey="name" stroke="#64748B" fontSize={11} />
                <YAxis stroke="#64748B" />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }} />
                <Bar dataKey="count" fill="#10B981" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Grid 2: Radar Chart & Donut Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Radar Chart */}
        <div className="glass-card p-6">
          <h3 className="text-base font-bold text-[var(--text-primary)] mb-2 flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-purple-500" />
            <span>Machine Learning Performance Radar Metrics (Radar Chart)</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart outerRadius={80} data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="metric" stroke="#94A3B8" fontSize={11} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#64748B" />
                <Radar name="Model Performance" dataKey="value" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Donut Chart */}
        <div className="glass-card p-6">
          <h3 className="text-base font-bold text-[var(--text-primary)] mb-2 flex items-center space-x-2">
            <PieIcon className="w-5 h-5 text-amber-500" />
            <span>Patient Sentiment Classification Split (Donut Chart)</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={sentimentData} cx="50%" cy="50%" innerRadius={60} outerRadius={85} paddingAngle={5} dataKey="value">
                  {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
