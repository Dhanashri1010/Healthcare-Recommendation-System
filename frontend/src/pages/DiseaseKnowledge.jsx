import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Dna, ShieldAlert, CheckCircle2 } from 'lucide-react';

export const DiseaseKnowledge = () => {
  const diseases = [
    { name: 'Hypertension', category: 'Cardiovascular', precautions: ['Reduce sodium intake (< 2,000 mg/day)', 'Exercise regularly (30 mins/day)', 'Monitor blood pressure daily', 'Avoid smoking and limit alcohol'] },
    { name: 'Diabetes', category: 'Metabolic / Endocrine', precautions: ['Monitor blood glucose levels regularly', 'Follow a low-glycemic diet', 'Engage in regular exercise', 'Take prescribed insulin/medication'] },
    { name: 'GERD', category: 'Gastrointestinal', precautions: ['Avoid spicy and acidic foods', 'Eat smaller meals', 'Do not lie down immediately after eating', 'Elevate head during sleep'] },
    { name: 'Bronchial Asthma', category: 'Respiratory', precautions: ['Keep rescue inhalers accessible', 'Avoid cold air and dust triggers', 'Take controller medications as directed', 'Monitor lung function'] },
    { name: 'Malaria', category: 'Infectious / Parasitic', precautions: ['Consult a doctor for antimalarials', 'Use mosquito nets and repellents', 'Stay well-hydrated', 'Avoid stagnant water'] }
  ];

  const [selected, setSelected] = useState(diseases[0]);

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
            <Dna className="w-7 h-7 text-purple-500" />
            <span>Disease Knowledgebase & Health Guidelines</span>
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Clinical reference library detailing medical categories and health precautions.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)] mb-3">Select Disease</h3>
          {diseases.map(d => (
            <button
              key={d.name}
              onClick={() => setSelected(d)}
              className={`w-full text-left p-4 rounded-xl border transition-all text-sm font-semibold ${
                selected.name === d.name
                  ? 'bg-purple-600/20 text-purple-400 border-purple-500/40 shadow-md'
                  : 'glass-card text-[var(--text-primary)] hover:border-purple-500/30'
              }`}
            >
              <div className="flex items-center justify-between">
                <span>{d.name}</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-300">{d.category}</span>
              </div>
            </button>
          ))}
        </div>

        <div className="md:col-span-2 glass-card p-8 space-y-6">
          <div className="border-b border-[var(--border-color)] pb-4">
            <span className="text-xs font-bold uppercase text-purple-400">{selected.category}</span>
            <h2 className="text-3xl font-extrabold text-[var(--text-primary)] mt-1">{selected.name}</h2>
          </div>

          <div>
            <h4 className="text-sm font-bold text-amber-400 uppercase tracking-wider mb-3 flex items-center space-x-2">
              <ShieldAlert className="w-5 h-5" />
              <span>Recommended Medical Precautions</span>
            </h4>
            <div className="space-y-3">
              {selected.precautions.map((p, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-slate-800/30 border border-[var(--border-color)] flex items-center space-x-3 text-sm text-[var(--text-primary)]">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
                  <span>{p}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
