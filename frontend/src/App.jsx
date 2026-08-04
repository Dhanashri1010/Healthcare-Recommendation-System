import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { Home } from './pages/Home';
import { PatientDiagnostics } from './pages/PatientDiagnostics';
import { BMICalculator } from './pages/BMICalculator';
import { HealthRiskScore } from './pages/HealthRiskScore';
import { LifestyleRecommendation } from './pages/LifestyleRecommendation';
import { MedicineRecommendation } from './pages/MedicineRecommendation';
import { DiseaseKnowledge } from './pages/DiseaseKnowledge';
import { AnalyticsDashboard } from './pages/AnalyticsDashboard';
import { Reports } from './pages/Reports';
import { AIModels } from './pages/AIModels';

function DashboardContent() {
  const [activeTab, setActiveTab] = useState('home');
  const [collapsed, setCollapsed] = useState(false);

  const getPageInfo = () => {
    switch (activeTab) {
      case 'home':
        return { title: 'Executive Healthcare Dashboard', subtitle: 'Overview of diagnostic model accuracy, patient feedback, and indexed prescription profiles.' };
      case 'diagnostics':
        return { title: 'Patient Information & AI Diagnostics Engine', subtitle: 'Input clinical parameters and active symptoms to execute multi-class disease diagnosis.' };
      case 'bmi':
        return { title: 'BMI & Metabolic Assessment Calculator', subtitle: 'Calculate Body Mass Index (BMI), ideal target weight bounds, and estimated basal metabolic rate.' };
      case 'health_risk':
        return { title: 'Comprehensive Clinical Health Risk Assessment', subtitle: 'Evaluates multi-factorial health risk indices across cardiovascular, metabolic, and lifestyle risk dimensions.' };
      case 'lifestyle':
        return { title: 'Personalized Lifestyle & Wellness Engine', subtitle: 'Tailored nutrition strategies, workout routines, sleep optimization, and core habit modifications.' };
      case 'medicines':
        return { title: 'Content-Based Medicine Recommendation Engine', subtitle: 'Search medications using TF-IDF text vectorization and hybrid rating scores.' };
      case 'knowledge':
        return { title: 'Disease Knowledge Base', subtitle: 'Explore disease symptoms, precautions, and recommended medication guidelines.' };
      case 'analytics':
        return { title: 'Advanced Healthcare Analytics & Insights', subtitle: 'Power BI-style charts, sentiment distributions, and diagnostic metric benchmarks.' };
      case 'reports':
        return { title: 'Clinical Diagnostics & Patient Reports', subtitle: 'Export patient records, diagnostic history, and recommendation summaries.' };
      case 'models':
        return { title: 'AI & Machine Learning Model Performance Benchmarks', subtitle: 'Performance metrics across trained disease prediction classifiers and NLP sentiment models.' };
      default:
        return { title: 'MediCare AI Platform', subtitle: 'Enterprise Healthcare Intelligence' };
    }
  };

  const pageInfo = getPageInfo();

  return (
    <div className="flex min-h-screen bg-[var(--bg-main)] text-[var(--text-primary)] transition-colors duration-300">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />
      <div className="flex-1 flex flex-col min-w-0">
        <Header title={pageInfo.title} subtitle={pageInfo.subtitle} />
        <main className="flex-1 overflow-y-auto">
          {activeTab === 'home' && <Home setActiveTab={setActiveTab} />}
          {activeTab === 'diagnostics' && <PatientDiagnostics />}
          {activeTab === 'bmi' && <BMICalculator setActiveTab={setActiveTab} />}
          {activeTab === 'health_risk' && <HealthRiskScore />}
          {activeTab === 'lifestyle' && <LifestyleRecommendation />}
          {activeTab === 'medicines' && <MedicineRecommendation />}
          {activeTab === 'knowledge' && <DiseaseKnowledge />}
          {activeTab === 'analytics' && <AnalyticsDashboard />}
          {activeTab === 'reports' && <Reports />}
          {activeTab === 'models' && <AIModels />}
          {activeTab === 'settings' && (
            <div className="p-8 text-[var(--text-secondary)]">
              <h3 className="text-xl font-bold text-[var(--text-primary)] mb-2">Platform Settings</h3>
              <p>Configure API integrations, model thresholds, and user management preferences.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <DashboardContent />
    </ThemeProvider>
  );
}
