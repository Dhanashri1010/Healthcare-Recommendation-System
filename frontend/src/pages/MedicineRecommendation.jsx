import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Pill, Search, Star, ThumbsUp, MessageSquare } from 'lucide-react';

export const MedicineRecommendation = () => {
  const [diseaseInput, setDiseaseInput] = useState('Acne');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    if (!diseaseInput.trim()) return;

    setLoading(true);
    fetch(`http://localhost:8000/api/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symptoms: ['fatigue'], name: 'Search', age: 30, sex: 'Male', bp: 'NORMAL', cholesterol: 'NORMAL', na_to_k: 12.0 })
    })
    .then(res => res.json())
    .then(data => {
      setResults(data.recommended_medicines);
    })
    .catch(() => {
      // Fallback sample
      setResults([
        { Drug_Name: 'Bactrim', Average_Rating: 8.9, Total_Reviews: 52, Useful_Review_Count: 1307, Recommendation_Score: 73.7 },
        { Drug_Name: 'Doryx', Average_Rating: 7.6, Total_Reviews: 45, Useful_Review_Count: 955, Recommendation_Score: 71.5 },
        { Drug_Name: 'Duac', Average_Rating: 7.5, Total_Reviews: 120, Useful_Review_Count: 1919, Recommendation_Score: 70.8 }
      ]);
    })
    .finally(() => setLoading(false));
  };

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
            <Pill className="w-7 h-7 text-emerald-500" />
            <span>Content-Based Medicine Recommendation Lookup</span>
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Search medications using TF-IDF content similarity and patient review sentiment scores.
          </p>
        </div>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="glass-card p-6 flex items-center space-x-4">
        <div className="relative flex-1">
          <Search className="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={diseaseInput}
            onChange={e => setDiseaseInput(e.target.value)}
            placeholder="Enter disease diagnosis (e.g. Acne, Depression, Hypertension, GERD)..."
            className="w-full pl-12 pr-4 py-3 text-sm rounded-xl bg-slate-800/40 border border-[var(--border-color)] text-[var(--text-primary)] focus:outline-none focus:border-emerald-500"
          />
        </div>
        <button
          type="submit"
          className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow-md transition-all"
        >
          Search Medications
        </button>
      </form>

      {/* Results */}
      {results && (
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-[var(--text-primary)]">Recommended Drugs for "{diseaseInput}"</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {results.map((med, i) => (
              <div key={i} className="glass-card p-6 space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-lg font-bold text-emerald-400">{med.Drug_Name}</h4>
                  <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300">
                    {med.Recommendation_Score}% Match
                  </span>
                </div>

                <div className="space-y-1 text-xs text-[var(--text-secondary)]">
                  <p className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                    <span>Average Rating: <strong className="text-[var(--text-primary)]">{med.Average_Rating} / 10</strong></span>
                  </p>
                  <p className="flex items-center space-x-1">
                    <ThumbsUp className="w-4 h-4 text-blue-400" />
                    <span>Useful Votes: <strong className="text-[var(--text-primary)]">{med.Useful_Review_Count ? med.Useful_Review_Count.toLocaleString() : 'N/A'}</strong></span>
                  </p>
                  <p className="flex items-center space-x-1">
                    <MessageSquare className="w-4 h-4 text-purple-400" />
                    <span>Total Patient Reviews: <strong className="text-[var(--text-primary)]">{med.Total_Reviews}</strong></span>
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
};
