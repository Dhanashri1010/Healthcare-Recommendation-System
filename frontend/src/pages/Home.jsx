import React from 'react';
import { motion } from 'framer-motion';
import { KPICard } from '../components/KPICard';
import { 
  Activity, 
  Pill, 
  MessageSquare, 
  Target, 
  Sparkles, 
  BrainCircuit, 
  ArrowUpRight,
  TrendingUp,
  ShieldCheck
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, 
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis 
} from 'recharts';

export const Home = ({ setActiveTab }) => {
  const kpis = [
    {
      title: 'Total Diseases',
      value: '41',
      description: 'Covered Diagnostic Profiles',
      icon: Activity,
      gradient: 'gradient-kpi-1',
      badge: '+100% Coverage'
    },
    {
      title: 'Medicines Available',
      value: '8,423',
      description: 'TF-IDF Indexed Profiles',
      icon: Pill,
      gradient: 'gradient-kpi-2',
      badge: 'Active Database'
    },
    {
      title: 'Drug Reviews',
      value: '161,297',
      description: 'Analyzed Patient Feedback',
      icon: MessageSquare,
      gradient: 'gradient-kpi-3',
      badge: 'NLP Verified'
    },
    {
      title: 'Prediction Accuracy',
      value: '100.0%',
      description: 'Multi-Class Logistic Model',
      icon: Target,
      gradient: 'gradient-kpi-4',
      badge: 'Validated'
    },
    {
      title: 'Recommendation Score',
      value: '98.5%',
      description: 'Cosine Similarity Match',
      icon: Sparkles,
      gradient: 'gradient-kpi-5',
      badge: 'Optimal Efficacy'
    }
  ];

  const areaData = [
    { month: 'Jan', accuracy: 98.2, reviews: 12400 },
    { month: 'Feb', accuracy: 98.8, reviews: 14200 },
    { month: 'Mar', accuracy: 99.1, reviews: 15800 },
    { month: 'Apr', accuracy: 99.5, reviews: 18100 },
    { month: 'May', accuracy: 99.8, reviews: 21000 },
    { month: 'Jun', accuracy: 100.0, reviews: 24500 }
  ];

  const sentimentData = [
    { name: 'Positive (7-10)', value: 66.25, color: '#10B981' },
    { name: 'Negative (1-3)', value: 21.74, color: '#EF4444' },
    { name: 'Neutral (4-6)', value: 12.01, color: '#F59E0B' }
  ];

  const radarData = [
    { metric: 'Accuracy', value: 100 },
    { metric: 'Precision', value: 100 },
    { metric: 'Recall', value: 100 },
    { metric: 'F1-Score', value: 100 },
    { metric: 'CV Score', value: 100 },
    { metric: 'NLP Accuracy', value: 77.3 }
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="p-8 space-y-8"
    >
      {/* Top Row KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-5">
        {kpis.map((kpi, idx) => (
          <KPICard key={idx} {...kpi} />
        ))}
      </div>

      {/* Main Feature Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Area Chart: Model Accuracy & Review Volume */}
        <div className="lg:col-span-2 glass-card p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-bold text-[var(--text-primary)] flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-blue-500" />
                <span>Diagnostic Accuracy & Review Growth</span>
              </h3>
              <p className="text-xs text-[var(--text-secondary)]">Historical model cross-validation vs review indexing</p>
            </div>
            <button 
              onClick={() => setActiveTab('diagnostics')}
              className="flex items-center space-x-1 text-xs font-semibold text-blue-500 hover:text-blue-400 transition-colors"
            >
              <span>Run Diagnostics</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={areaData}>
                <defs>
                  <linearGradient id="colorAcc" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="month" stroke="#64748B" fontSize={12} />
                <YAxis domain={[95, 100]} stroke="#64748B" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }} />
                <Area type="monotone" dataKey="accuracy" stroke="#3B82F6" strokeWidth={3} fillOpacity={1} fill="url(#colorAcc)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Sentiment Donut Chart */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold text-[var(--text-primary)] mb-2 flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-emerald-500" />
            <span>Patient Sentiment Split</span>
          </h3>
          <p className="text-xs text-[var(--text-secondary)] mb-4">Analyzed from 161,297 drug reviews</p>

          <div className="h-52 relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={sentimentData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-2xl font-extrabold text-[var(--text-primary)]">66.2%</span>
              <span className="text-[10px] text-emerald-400 font-semibold uppercase">Positive</span>
            </div>
          </div>

          <div className="space-y-2 mt-2">
            {sentimentData.map((item, i) => (
              <div key={i} className="flex items-center justify-between text-xs font-medium">
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-[var(--text-primary)]">{item.name}</span>
                </div>
                <span className="text-[var(--text-secondary)]">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Launch SaaS Banner */}
      <div className="glass-card p-8 bg-gradient-to-r from-blue-900/30 via-indigo-900/20 to-purple-900/30 border-blue-500/30 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-blue-400 text-xs font-bold uppercase tracking-widest">
            <BrainCircuit className="w-4 h-4" />
            <span>Commercial Healthcare Platform</span>
          </div>
          <h2 className="text-2xl font-extrabold text-[var(--text-primary)]">
            Ready to perform live patient diagnostics?
          </h2>
          <p className="text-sm text-[var(--text-secondary)] max-w-xl">
            Input patient clinical biomarkers, select active symptoms, and receive AI-generated disease predictions with TF-IDF content-based medication recommendations.
          </p>
        </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setActiveTab('diagnostics')}
          className="px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm shadow-lg shadow-blue-500/30 flex items-center space-x-2 flex-shrink-0 transition-all"
        >
          <span>Launch Diagnostics Engine</span>
          <ArrowUpRight className="w-4 h-4" />
        </motion.button>
      </div>
    </motion.div>
  );
};
