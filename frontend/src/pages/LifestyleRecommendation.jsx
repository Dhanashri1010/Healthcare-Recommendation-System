import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Apple, Dumbbell, Moon, CheckSquare, Sparkles, HeartPulse, Flame, Target } from 'lucide-react';
import { KPICard } from '../components/KPICard';

export const LifestyleRecommendation = () => {
  const [formData, setFormData] = useState({
    bmi: 26.5,
    risk_level: 'Moderate',
    disease: 'Hypertension',
    activity_level: 'Moderate',
    dietary_pref: 'Balanced',
    sleep_hours: 6.5,
    stress_level: 'Moderate'
  });

  const [activeTab, setActiveTab] = useState('nutrition');
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState({
    nutrition: {
      caloric_strategy: 'Controlled Energy Balance (250-300 kcal deficit)',
      macronutrient_split: '35% Protein, 40% Complex Carbs, 25% Healthy Fats',
      hydration_goal_liters: 3.0,
      dietary_preference: 'Balanced',
      recommended_foods: [
        'Leafy Greens & Cruciferous Veggies (Spinach, Kale, Broccoli)',
        'Lean Protein Sources (Chicken Breast, Salmon, Tofu, Legumes)',
        'Whole Grains (Quinoa, Brown Rice, Oats)',
        'Healthy Fats (Avocado, Extra Virgin Olive Oil, Almonds, Walnuts)',
        'Potassium-Rich Foods (Bananas, Sweet Potatoes, Beans)'
      ],
      foods_to_avoid: [
        'Refined Sugars & Sugary Beverages (Soda, Processed Juices)',
        'Ultra-Processed Foods & Trans-Fats (Fried Foods, Packaged Snacks)',
        'Excessive Dietary Sodium (> 2,300 mg/day)',
        'High-Sodium Canned Soups, Pickles, Cured Meats'
      ]
    },
    fitness: {
      weekly_frequency: '4 to 5 days per week',
      aerobic_routine: '30-45 minutes of moderate aerobic exercise (brisk walking, swimming, cycling)',
      strength_routine: '2 sessions/week focusing on major muscle groups (squats, push-ups, bodyweight exercises)',
      daily_step_goal: '8,500 to 10,000 steps daily'
    },
    recovery: {
      sleep_recommendation: 'You are currently sleeping 6.5 hours. Aim for 7 to 8.5 hours of quality restorative sleep by setting a consistent bedtime schedule.',
      stress_recommendation: 'Incorporate 10-15 minutes of daily relaxation routines (guided breathing, stretching) to keep cortisol levels balanced.'
    },
    habit_modifications: [
      'Hydration Target: Drink 2.5 - 3.5 Liters of water daily.',
      'Routine Medical Checkups: Schedule bi-annual comprehensive blood work and vital screening.',
      'Mindful Eating: Avoid eating in front of screens; chew slowly to aid digestion.'
    ]
  });

  const handleGeneratePlan = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/lifestyle-recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      setPlan(data);
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
            <HeartPulse className="w-7 h-7 text-emerald-500" />
            <span>Personalized Lifestyle & Wellness Engine</span>
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Tailored nutrition strategies, workout routines, sleep optimization, and core habit modifications.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Form Inputs (4 Cols) */}
        <div className="lg:col-span-4 space-y-6">
          <form onSubmit={handleGeneratePlan} className="glass-card p-6 space-y-5">
            <h3 className="text-base font-bold text-[var(--text-primary)] border-b border-[var(--border-color)] pb-3">
              Configure Health Profile
            </h3>

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

            <div>
              <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Dietary Preference</label>
              <select
                value={formData.dietary_pref}
                onChange={e => setFormData({ ...formData, dietary_pref: e.target.value })}
                className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
              >
                <option value="Balanced">Balanced</option>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Vegan">Vegan</option>
                <option value="Keto">Keto</option>
                <option value="Low Carb">Low Carb</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Current Activity Level</label>
              <select
                value={formData.activity_level}
                onChange={e => setFormData({ ...formData, activity_level: e.target.value })}
                className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
              >
                <option value="Low">Low</option>
                <option value="Moderate">Moderate</option>
                <option value="High">High</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Average Sleep (Hours)</label>
              <input
                type="number"
                step="0.5"
                value={formData.sleep_hours}
                onChange={e => setFormData({ ...formData, sleep_hours: parseFloat(e.target.value) || 0 })}
                className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-[var(--text-secondary)] mb-1 block">Existing Health Condition</label>
              <input
                type="text"
                value={formData.disease}
                onChange={e => setFormData({ ...formData, disease: e.target.value })}
                className="w-full px-3 py-2 text-sm rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-blue-500"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-bold text-sm shadow-lg transition-all flex items-center justify-center space-x-2"
            >
              {loading ? <span>Generating...</span> : <><span>Generate Plan</span><Sparkles className="w-4 h-4" /></>}
            </button>
          </form>
        </div>

        {/* Dynamic Lifestyle Plan Output (8 Cols) */}
        <div className="lg:col-span-8 space-y-6">
          {/* Top Tabs */}
          <div className="flex border-b border-[var(--border-color)] space-x-4">
            <button
              onClick={() => setActiveTab('nutrition')}
              className={`pb-3 text-sm font-bold flex items-center space-x-2 border-b-2 transition-all ${
                activeTab === 'nutrition'
                  ? 'border-emerald-500 text-emerald-500'
                  : 'border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
              }`}
            >
              <Apple className="w-4 h-4" />
              <span>Nutrition & Diet</span>
            </button>

            <button
              onClick={() => setActiveTab('fitness')}
              className={`pb-3 text-sm font-bold flex items-center space-x-2 border-b-2 transition-all ${
                activeTab === 'fitness'
                  ? 'border-emerald-500 text-emerald-500'
                  : 'border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
              }`}
            >
              <Dumbbell className="w-4 h-4" />
              <span>Fitness Routine</span>
            </button>

            <button
              onClick={() => setActiveTab('recovery')}
              className={`pb-3 text-sm font-bold flex items-center space-x-2 border-b-2 transition-all ${
                activeTab === 'recovery'
                  ? 'border-emerald-500 text-emerald-500'
                  : 'border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
              }`}
            >
              <Moon className="w-4 h-4" />
              <span>Sleep & Stress</span>
            </button>

            <button
              onClick={() => setActiveTab('habits')}
              className={`pb-3 text-sm font-bold flex items-center space-x-2 border-b-2 transition-all ${
                activeTab === 'habits'
                  ? 'border-emerald-500 text-emerald-500'
                  : 'border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
              }`}
            >
              <CheckSquare className="w-4 h-4" />
              <span>Daily Habits</span>
            </button>
          </div>

          {/* Tab 1: Nutrition */}
          {activeTab === 'nutrition' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <KPICard
                  title="Caloric Strategy"
                  value={plan.nutrition.caloric_strategy}
                  description="Energy Balance Plan"
                  icon={Flame}
                  gradient="gradient-kpi-1"
                />
                <KPICard
                  title="Macronutrient Split"
                  value={plan.nutrition.macronutrient_split}
                  description="Target Macro Ratio"
                  icon={Target}
                  gradient="gradient-kpi-2"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="glass-card p-6 border-l-4 border-emerald-500 space-y-3">
                  <h4 className="text-sm font-bold text-[var(--text-primary)]">✅ Recommended Foods</h4>
                  <ul className="space-y-2">
                    {plan.nutrition.recommended_foods.map((food, idx) => (
                      <li key={idx} className="text-xs text-[var(--text-secondary)] font-medium flex items-start space-x-2">
                        <span className="text-emerald-500 font-bold">•</span>
                        <span>{food}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="glass-card p-6 border-l-4 border-red-500 space-y-3">
                  <h4 className="text-sm font-bold text-[var(--text-primary)]">❌ Foods to Avoid / Limit</h4>
                  <ul className="space-y-2">
                    {plan.nutrition.foods_to_avoid.map((food, idx) => (
                      <li key={idx} className="text-xs text-[var(--text-secondary)] font-medium flex items-start space-x-2">
                        <span className="text-red-500 font-bold">•</span>
                        <span>{food}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Tab 2: Fitness */}
          {activeTab === 'fitness' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <KPICard
                  title="Weekly Frequency"
                  value={plan.fitness.weekly_frequency}
                  description="Recommended Sessions"
                  icon={Dumbbell}
                  gradient="gradient-kpi-3"
                />
                <KPICard
                  title="Daily Step Target"
                  value={plan.fitness.daily_step_goal}
                  description="Physical Movement Goal"
                  icon={Flame}
                  gradient="gradient-kpi-4"
                />
              </div>

              <div className="glass-card p-6 space-y-4">
                <h4 className="text-sm font-bold text-[var(--text-primary)]">🏃 Aerobic & Cardio Routine</h4>
                <p className="text-xs text-[var(--text-secondary)] leading-relaxed">{plan.fitness.aerobic_routine}</p>

                <h4 className="text-sm font-bold text-[var(--text-primary)] pt-2 border-t border-[var(--border-color)]">💪 Strength & Conditioning Routine</h4>
                <p className="text-xs text-[var(--text-secondary)] leading-relaxed">{plan.fitness.strength_routine}</p>
              </div>
            </div>
          )}

          {/* Tab 3: Recovery */}
          {activeTab === 'recovery' && (
            <div className="space-y-6">
              <div className="glass-card p-6 border-l-4 border-indigo-500 space-y-2">
                <h4 className="text-sm font-bold text-[var(--text-primary)] flex items-center space-x-2">
                  <Moon className="w-4 h-4 text-indigo-500" />
                  <span>Sleep Hygiene & Optimization</span>
                </h4>
                <p className="text-xs text-[var(--text-secondary)] leading-relaxed">{plan.recovery.sleep_recommendation}</p>
              </div>

              <div className="glass-card p-6 border-l-4 border-purple-500 space-y-2">
                <h4 className="text-sm font-bold text-[var(--text-primary)] flex items-center space-x-2">
                  <HeartPulse className="w-4 h-4 text-purple-500" />
                  <span>Stress Reduction & Mindfulness</span>
                </h4>
                <p className="text-xs text-[var(--text-secondary)] leading-relaxed">{plan.recovery.stress_recommendation}</p>
              </div>
            </div>
          )}

          {/* Tab 4: Habits */}
          {activeTab === 'habits' && (
            <div className="glass-card p-6 space-y-4">
              <h4 className="text-sm font-bold text-[var(--text-primary)] flex items-center space-x-2">
                <CheckSquare className="w-4 h-4 text-emerald-500" />
                <span>Daily Core Health Habits</span>
              </h4>
              <ul className="space-y-3">
                {plan.habit_modifications.map((habit, idx) => (
                  <li key={idx} className="p-3 rounded-xl bg-slate-100 dark:bg-slate-800/50 border border-[var(--border-color)] text-xs text-[var(--text-primary)] font-medium flex items-center space-x-3">
                    <span className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-500 font-bold flex items-center justify-center text-xs">{idx + 1}</span>
                    <span>{habit}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};
