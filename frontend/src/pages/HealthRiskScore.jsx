import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ShieldAlert, Heart, Activity, AlertTriangle, CheckCircle, Stethoscope, Sparkles } from 'lucide-react';
import { KPICard } from '../components/KPICard';

export const HealthRiskScore = () => {
  const [formData, setFormData] = useState({
    age: 45,
    sex: 'Male',
    bp: 'HIGH',
    cholesterol: 'NORMAL',
    na_to_k: 14.5,
    bmi: 26.5,
    smoking: false,
    alcohol: false,
    physical_activity: 'Moderate',
    family_history: false
  });

  const [loading, setLoading] = useState(false);
  const [riskResult, setRiskResult] = useState({
    overall_risk_score: 48,
    risk_level: 'Moderate',
    risk_color: '#F59E0B',
    summary: 'Moderate risk detected. Preventive modifications in diet, exercise, and routine monitoring are advised.',
    cardiovascular_risk_percent: 62.8,
    metabolic_risk_percent: 34.3,
    lifestyle_risk_percent: 26.7,
    identified_risk_factors: [
      'Hypertension (High BP)',
      'Overweight Status (BMI 25-29.9)',
      'Sedentary Physical Activity'
    ],
    preventive_interventions: [
      'Restrict dietary sodium to < 2,000 mg/day and monitor blood pressure weekly.',
      'Target 5-10% body weight reduction through caloric deficit and daily aerobic exercise.',
      'Incorporate 150 minutes of moderate aerobic exercise per week.'
    ]
  });

  const handleComputeRisk = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/calculate-health-risk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      setRiskResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

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
            <ShieldAlert className="w-7 h-7 text-amber-500" />
            <span>Comprehensive Clinical Health Risk Score Model</span>
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Evaluates multi-factorial health risk indices across cardiovascular, metabolic, and lifestyle risk dimensions.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Input Form (5 Cols) */}
        <div className="lg:col-span-5">
          <form onSubmit={handleComputeRisk} className="glass-card p-6 space-y-5">
            <h3 className="text-base font-bold text-[var(--text-primary)] border-b border-[var(--border-color)] pb-3 flex items-center space-x-2">
              <Stethoscope className="w-5 h-5 text-blue-500" />
              <span>Biomarker & Risk Factor Inputs</span>
            </h3>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Age (Years)</label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={e => setFormData({ ...formData, age: parseInt(e.target.value) || 0 })}
                  className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Gender</label>
                <select
                  value={formData.sex}
                  onChange={e => setFormData({ ...formData, sex: e.target.value })}
                  className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Blood Pressure</label>
                <select
                  value={formData.bp}
                  onChange={e => setFormData({ ...formData, bp: e.target.value })}
                  className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
                >
                  <option value="HIGH">HIGH</option>
                  <option value="NORMAL">NORMAL</option>
                  <option value="LOW">LOW</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Cholesterol</label>
                <select
                  value={formData.cholesterol}
                  onChange={e => setFormData({ ...formData, cholesterol: e.target.value })}
                  className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
                >
                  <option value="HIGH">HIGH</option>
                  <option value="NORMAL">NORMAL</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Na to K Ratio</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.na_to_k}
                  onChange={e => setFormData({ ...formData, na_to_k: parseFloat(e.target.value) || 0 })}
                  className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Body Mass Index (BMI)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.bmi}
                  onChange={e => setFormData({ ...formData, bmi: parseFloat(e.target.value) || 0 })}
                  className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="space-y-2 pt-2 border-t border-[var(--border-color)]">
              <label className="flex items-center space-x-2 text-xs font-semibold text-[var(--text-primary)] cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.smoking}
                  onChange={e => setFormData({ ...formData, smoking: e.target.checked })}
                  className="w-4 h-4 rounded text-blue-600 accent-blue-500"
                />
                <span>Active Tobacco Smoking</span>
              </label>

              <label className="flex items-center space-x-2 text-xs font-semibold text-[var(--text-primary)] cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.alcohol}
                  onChange={e => setFormData({ ...formData, alcohol: e.target.checked })}
                  className="w-4 h-4 rounded text-blue-600 accent-blue-500"
                />
                <span>Frequent Alcohol Intake</span>
              </label>

              <label className="flex items-center space-x-2 text-xs font-semibold text-[var(--text-primary)] cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.family_history}
                  onChange={e => setFormData({ ...formData, family_history: e.target.checked })}
                  className="w-4 h-4 rounded text-blue-600 accent-blue-500"
                />
                <span>Family History of Chronic Illness</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-sm shadow-lg transition-all flex items-center justify-center space-x-2"
            >
              {loading ? <span>Calculating...</span> : <><span>Compute Risk Score</span><Sparkles className="w-4 h-4" /></>}
            </button>
          </form>
        </div>

        {/* Right Output Dashboard (7 Cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Main Risk Gauge Card */}
          {riskResult && (
            <div className="glass-card p-6 border-l-8 space-y-4" style={{ borderColor: riskResult.risk_color }}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-wider text-[var(--text-secondary)] font-bold">Aggregated Risk Score Index</p>
                  <h3 className="text-4xl font-extrabold text-[var(--text-primary)] mt-1">{riskResult.overall_risk_score} <span className="text-sm font-normal text-[var(--text-secondary)]">/ 100</span></h3>
                </div>
                <span
                  className="px-4 py-1.5 rounded-full font-bold text-sm border"
                  style={{
                    backgroundColor: `${riskResult.risk_color}20`,
                    color: riskResult.risk_color,
                    borderColor: `${riskResult.risk_color}40`
                  }}
                >
                  {riskResult.risk_level} Risk Level
                </span>
              </div>

              {/* Progress bar */}
              <div className="w-full h-3 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full transition-all duration-500"
                  style={{ width: `${riskResult.overall_risk_score}%`, backgroundColor: riskResult.risk_color }}
                />
              </div>

              <p className="text-xs text-[var(--text-secondary)] leading-relaxed font-medium">
                {riskResult.summary}
              </p>
            </div>
          )}

          {/* Risk Sub-Scores */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <KPICard
              title="Cardiovascular Risk"
              value={`${riskResult.cardiovascular_risk_percent}%`}
              description="BP & Cholesterol Markers"
              icon={Heart}
              gradient="gradient-kpi-1"
            />
            <KPICard
              title="Metabolic Risk"
              value={`${riskResult.metabolic_risk_percent}%`}
              description="Obesity & Electrolyte Balance"
              icon={Activity}
              gradient="gradient-kpi-2"
            />
            <KPICard
              title="Lifestyle Risk"
              value={`${riskResult.lifestyle_risk_percent}%`}
              description="Smoking & Physical Inactivity"
              icon={AlertTriangle}
              gradient="gradient-kpi-3"
            />
          </div>

          {/* Identified Risk Factors */}
          <div className="glass-card p-6 space-y-3">
            <h4 className="text-sm font-bold text-[var(--text-primary)] flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              <span>Identified Key Risk Drivers</span>
            </h4>
            <div className="flex flex-wrap gap-2">
              {riskResult.identified_risk_factors.map((rf, idx) => (
                <span key={idx} className="text-xs font-semibold px-3 py-1 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">
                  ⚠️ {rf}
                </span>
              ))}
            </div>
          </div>

          {/* Interventions */}
          <div className="glass-card p-6 space-y-3">
            <h4 className="text-sm font-bold text-[var(--text-primary)] flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-emerald-500" />
              <span>Targeted Preventive Interventions</span>
            </h4>
            <ul className="space-y-2">
              {riskResult.preventive_interventions.map((iv, idx) => (
                <li key={idx} className="text-xs text-[var(--text-secondary)] font-medium flex items-start space-x-2">
                  <span className="text-emerald-500 font-bold">•</span>
                  <span>{iv}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
