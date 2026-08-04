import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Download, CheckCircle2 } from 'lucide-react';

export const Reports = () => {
  const sampleReport = `================================================================================
 PERSONALIZED HEALTHCARE & MEDICINE RECOMMENDATION SYSTEM - DIAGNOSTIC REPORT
================================================================================
Date: 2026-07-31

1. PATIENT DEMOGRAPHICS & CLINICAL BIOMARKERS
--------------------------------------------------------------------------------
Patient Name:        John Doe
Age:                 45 years
Gender:              Male
Blood Pressure:      HIGH
Cholesterol Level:   NORMAL
Na/K Ratio:          14.5

2. ACTIVE PATIENT SYMPTOMS
--------------------------------------------------------------------------------
Fatigue, High Fever, Vomiting

3. AI DIAGNOSTIC MODEL PREDICTION
--------------------------------------------------------------------------------
Predicted Disease:   Hypertension
Model Confidence:    100.0%

4. RECOMMENDED MEDICATIONS
--------------------------------------------------------------------------------
1. Valsartan | Rating: 9.1/10 | Useful Votes: 1,420 | Match Score: 94.2%
2. Lisinopril | Rating: 8.8/10 | Useful Votes: 1,980 | Match Score: 91.5%

5. MEDICAL PRECAUTIONS & HEALTHCARE ADVICE
--------------------------------------------------------------------------------
1. Reduce sodium intake (< 2,000 mg/day)
2. Exercise regularly (30 mins/day)
3. Monitor blood pressure daily
`;

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
            <FileText className="w-7 h-7 text-teal-500" />
            <span>Patient Diagnostic Reports & Documentation</span>
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            View and download clinical summary diagnostic reports.
          </p>
        </div>
      </div>

      <div className="glass-card p-8 space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-[var(--text-primary)]">Latest Clinical Report</h3>
          <a
            href={`data:text/plain;charset=utf-8,${encodeURIComponent(sampleReport)}`}
            download="patient_diagnostic_report.txt"
            className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs flex items-center space-x-2 transition-all"
          >
            <Download className="w-4 h-4" />
            <span>Export Report (.txt)</span>
          </a>
        </div>

        <pre className="p-6 rounded-xl bg-slate-900/60 border border-[var(--border-color)] text-xs text-teal-300 font-mono overflow-x-auto whitespace-pre-wrap leading-relaxed">
          {sampleReport}
        </pre>
      </div>
    </motion.div>
  );
};
