import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Scale, Activity, Flame, Target, ArrowRight, Info, CheckCircle2 } from 'lucide-react';
import { KPICard } from '../components/KPICard';

export const BMICalculator = ({ setActiveTab }) => {
  const [weight, setWeight] = useState(75);
  const [height, setHeight] = useState(175);
  const [unit, setUnit] = useState('metric'); // 'metric' (kg, cm) or 'imperial' (lbs, inches)

  // Calculations
  const weightKg = unit === 'metric' ? weight : weight * 0.453592;
  const heightCm = unit === 'metric' ? height : height * 2.54;
  const heightM = heightCm / 100;

  const bmi = heightM > 0 ? (weightKg / (heightM * heightM)).toFixed(1) : 0;
  const numericBmi = parseFloat(bmi);

  const getBmiCategory = (val) => {
    if (val < 18.5) return { name: 'Underweight', color: 'text-blue-500', bg: 'bg-blue-500/20', border: 'border-blue-500/30', note: 'Higher risk of nutrient deficiency and low immunity.' };
    if (val <= 24.9) return { name: 'Normal Weight', color: 'text-emerald-500', bg: 'bg-emerald-500/20', border: 'border-emerald-500/30', note: 'Optimal metabolic health and lower cardiovascular risk.' };
    if (val <= 29.9) return { name: 'Overweight', color: 'text-amber-500', bg: 'bg-amber-500/20', border: 'border-amber-500/30', note: 'Moderate risk of hypertension, hyperlipidemia, and diabetes.' };
    if (val <= 34.9) return { name: 'Obese (Class I)', color: 'text-orange-500', bg: 'bg-orange-500/20', border: 'border-orange-500/30', note: 'High risk of insulin resistance and vascular strain.' };
    return { name: 'Obese (Class II+)', color: 'text-red-500', bg: 'bg-red-500/20', border: 'border-red-500/30', note: 'Significantly elevated risk of cardiovascular events.' };
  };

  const category = getBmiCategory(numericBmi);
  const minHealthyWeight = (18.5 * (heightM * heightM)).toFixed(1);
  const maxHealthyWeight = (24.9 * (heightM * heightM)).toFixed(1);
  const idealWeight = (22.0 * (heightM * heightM)).toFixed(1);
  const weightDiff = (weightKg - idealWeight).toFixed(1);
  const estimatedBmr = Math.round(10 * weightKg + 6.25 * heightCm - 5 * 30 + 5);

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
            <Scale className="w-7 h-7 text-blue-500" />
            <span>BMI & Metabolic Assessment Calculator</span>
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Calculate your Body Mass Index (BMI), ideal target weight bounds, and estimated basal metabolic rate (BMR).
          </p>
        </div>

        {/* Unit Switcher */}
        <div className="flex items-center space-x-2 bg-slate-200 dark:bg-slate-800 p-1.5 rounded-xl border border-[var(--border-color)]">
          <button
            onClick={() => setUnit('metric')}
            className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all ${
              unit === 'metric'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            Metric (kg, cm)
          </button>
          <button
            onClick={() => setUnit('imperial')}
            className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all ${
              unit === 'imperial'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            Imperial (lbs, in)
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Inputs Card */}
        <div className="lg:col-span-5 glass-card p-6 space-y-6">
          <h3 className="text-base font-bold text-[var(--text-primary)] flex items-center space-x-2 border-b border-[var(--border-color)] pb-3">
            <Activity className="w-5 h-5 text-blue-500" />
            <span>1. Body Measurements</span>
          </h3>

          {/* Weight Input */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm font-semibold text-[var(--text-primary)]">
              <span>Body Weight ({unit === 'metric' ? 'kg' : 'lbs'})</span>
              <span className="text-blue-500 font-extrabold text-lg">{weight} {unit === 'metric' ? 'kg' : 'lbs'}</span>
            </div>
            <input
              type="range"
              min={unit === 'metric' ? 30 : 66}
              max={unit === 'metric' ? 180 : 400}
              value={weight}
              onChange={(e) => setWeight(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-300 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <input
              type="number"
              value={weight}
              onChange={(e) => setWeight(parseFloat(e.target.value) || 0)}
              className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500 mt-2"
            />
          </div>

          {/* Height Input */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm font-semibold text-[var(--text-primary)]">
              <span>Height ({unit === 'metric' ? 'cm' : 'inches'})</span>
              <span className="text-blue-500 font-extrabold text-lg">{height} {unit === 'metric' ? 'cm' : 'in'}</span>
            </div>
            <input
              type="range"
              min={unit === 'metric' ? 100 : 40}
              max={unit === 'metric' ? 220 : 88}
              value={height}
              onChange={(e) => setHeight(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-300 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <input
              type="number"
              value={height}
              onChange={(e) => setHeight(parseFloat(e.target.value) || 0)}
              className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500 mt-2"
            />
          </div>

          <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 text-xs text-[var(--text-secondary)] space-y-1">
            <p className="font-semibold text-blue-500 flex items-center gap-1">
              <Info className="w-4 h-4" /> Standard WHO BMI Formula
            </p>
            <p>BMI = Weight (kg) / [Height (m)]²</p>
          </div>
        </div>

        {/* Right Results & Visual Gauge */}
        <div className="lg:col-span-7 space-y-6">
          {/* Main Category Box */}
          <div className={`glass-card p-6 border-l-8 ${category.border} space-y-4`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-wider text-[var(--text-secondary)] font-bold">Your Calculated BMI</p>
                <h3 className="text-4xl font-extrabold text-[var(--text-primary)] mt-1">{bmi} <span className="text-sm font-normal text-[var(--text-secondary)]">kg/m²</span></h3>
              </div>
              <span className={`px-4 py-1.5 rounded-full font-bold text-sm border ${category.bg} ${category.color} ${category.border}`}>
                {category.name}
              </span>
            </div>

            {/* Visual Gauge Bar */}
            <div className="space-y-1.5 pt-2">
              <div className="h-3 w-full bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden flex">
                <div style={{ width: '18.5%' }} className="bg-blue-500 h-full" title="Underweight (<18.5)" />
                <div style={{ width: '25%' }} className="bg-emerald-500 h-full" title="Normal (18.5-24.9)" />
                <div style={{ width: '20%' }} className="bg-amber-500 h-full" title="Overweight (25-29.9)" />
                <div style={{ width: '36.5%' }} className="bg-red-500 h-full" title="Obese (≥30)" />
              </div>
              <div className="flex justify-between text-[10px] text-[var(--text-secondary)] font-medium">
                <span>15.0</span>
                <span>18.5</span>
                <span>25.0</span>
                <span>30.0</span>
                <span>40.0+</span>
              </div>
            </div>

            <p className="text-xs text-[var(--text-secondary)] leading-relaxed font-medium">
              {category.note}
            </p>
          </div>

          {/* Metric KPIs */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <KPICard
              title="Healthy Weight Range"
              value={`${minHealthyWeight} - ${maxHealthyWeight} kg`}
              description="BMI 18.5 - 24.9 Target"
              icon={Target}
              gradient="gradient-kpi-1"
            />
            <KPICard
              title="Ideal Weight Target"
              value={`${idealWeight} kg`}
              description={`${weightDiff > 0 ? `+${weightDiff}` : weightDiff} kg difference`}
              icon={Scale}
              gradient="gradient-kpi-2"
            />
            <KPICard
              title="Estimated BMR"
              value={`${estimatedBmr} kcal`}
              description="Basal Metabolic Rate"
              icon={Flame}
              gradient="gradient-kpi-3"
            />
          </div>

          {/* Next Steps CTA */}
          <div className="glass-card p-6 flex items-center justify-between bg-gradient-to-r from-blue-600/10 to-indigo-600/10 border-blue-500/30">
            <div>
              <h4 className="text-sm font-bold text-[var(--text-primary)]">Ready for customized diet & workout plans?</h4>
              <p className="text-xs text-[var(--text-secondary)] mt-0.5">Generate a personalized lifestyle plan tailored to your BMI category.</p>
            </div>
            {setActiveTab && (
              <button
                onClick={() => setActiveTab('lifestyle')}
                className="px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-700 text-white flex items-center space-x-1.5 transition-all shadow-md"
              >
                <span>Lifestyle Plan</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
