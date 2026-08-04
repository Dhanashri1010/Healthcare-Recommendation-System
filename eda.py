"""
Personalized Healthcare & Medicine Recommendation System
--------------------------------------------------------
Exploratory Data Analysis (EDA) Pipeline

Generates statistical analysis, summaries, and visualizations:
1. Dataset summary & statistical describe
2. Missing values visualization
3. Disease distribution (Disease-Symptom dataset)
4. Symptom frequency (Top 20 symptoms)
5. Top medical conditions (Drug Reviews dataset)
6. Top prescribed medicines & drug target distribution
7. Drug rating & sentiment distribution
8. Outlier visualization (usefulCount & Na_to_K)
9. Correlation heatmaps (patient biomarkers & symptom co-occurrence)
10. Pair plot of continuous patient features

Plots are exported to 'eda_plots/' directory.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style='whitegrid', palette='deep')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.autolayout'] = True

PLOTS_DIR = os.path.join(os.path.dirname(__file__), 'eda_plots')
os.makedirs(PLOTS_DIR, exist_ok=True)

print("=" * 80)
print(" EXPLORATORY DATA ANALYSIS (EDA) - HEALTHCARE DATASETS ")
print("=" * 80)

# Load Cleaned Datasets
df_sym = pd.read_csv('cleaned_data/cleaned_disease_symptoms_train.csv')
df_rev = pd.read_csv('cleaned_data/cleaned_drug_reviews_train.csv')
df_patient = pd.read_csv('cleaned_data/cleaned_patient_prescriptions.csv')

# Load Raw Datasets for missing values comparison
df_sym_raw = pd.read_csv('archive (9)/Training.csv')
df_rev_raw = pd.read_csv('archive (10)/drugsComTrain_raw.csv')
df_patient_raw = pd.read_csv('archive (11)/drug200.csv')


# ==============================================================================
# SECTION 1: DATASET SUMMARIES & STATISTICAL ANALYSIS
# ==============================================================================
print("\n--- 1. DATASET SUMMARIES & STATISTICAL DESCRIBE ---")

print("\n[A] Disease Symptoms Dataset Summary:")
print("Shape:", df_sym.shape)
print("Symptom Columns Count:", len(df_sym.columns) - 3) # Exclude prognosis, prognosis_encoded, symptom_count
print(df_sym[['symptom_count']].describe())

print("\n[B] Drug Reviews Dataset Summary:")
print("Shape:", df_rev.shape)
print(df_rev[['rating', 'usefulCount', 'usefulCount_capped', 'usefulCount_log', 'review_word_count']].describe())

print("\n[C] Patient Prescriptions Dataset Summary:")
print("Shape:", df_patient.shape)
print(df_patient[['Age', 'Na_to_K', 'Na_to_K_capped', 'BP_encoded', 'Cholesterol_encoded', 'Drug_encoded']].describe())


# ==============================================================================
# VISUALIZATION 1: MISSING VALUE VISUALIZATION
# ==============================================================================
print("\n--> Generating Plot 1: Missing Values Comparison...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Raw Datasets Missing Values
raw_nulls = {
    'Disease Train (Raw)': df_sym_raw.isnull().sum().sum(),
    'Drug Reviews (Raw)': df_rev_raw.isnull().sum().sum(),
    'Patient Prescriptions (Raw)': df_patient_raw.isnull().sum().sum()
}
sns.barplot(x=list(raw_nulls.keys()), y=list(raw_nulls.values()), ax=axes[0], palette='Reds_d')
axes[0].set_title("Missing Values Count (Raw Datasets)", fontsize=13, fontweight='bold')
axes[0].set_ylabel("Total Missing Values")

# Cleaned Datasets Missing Values
clean_nulls = {
    'Disease Train (Clean)': df_sym.isnull().sum().sum(),
    'Drug Reviews (Clean)': df_rev.isnull().sum().sum(),
    'Patient Prescriptions (Clean)': df_patient.isnull().sum().sum()
}
sns.barplot(x=list(clean_nulls.keys()), y=list(clean_nulls.values()), ax=axes[1], palette='Greens_d')
axes[1].set_title("Missing Values Count (Cleaned Datasets)", fontsize=13, fontweight='bold')
axes[1].set_ylabel("Total Missing Values")
axes[1].set_ylim(0, max(raw_nulls.values()) + 100)

plt.suptitle("Task 3 & 5: Missing Value Audit (Before vs. After Cleaning)", fontsize=15, fontweight='bold', y=1.02)
plt.savefig(os.path.join(PLOTS_DIR, '01_missing_values_before_after.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 2: DISEASE DISTRIBUTION
# ==============================================================================
print("--> Generating Plot 2: Disease Distribution...")
fig, ax = plt.subplots(figsize=(12, 10))
disease_counts = df_sym['prognosis'].value_counts()
sns.barplot(x=disease_counts.values, y=disease_counts.index, ax=ax, palette='viridis')
ax.set_title("Distribution of Diagnosed Diseases (Prognosis Count)", fontsize=14, fontweight='bold')
ax.set_xlabel("Number of Unique Patient Profiles")
ax.set_ylabel("Disease Prognosis")

for i, v in enumerate(disease_counts.values):
    ax.text(v + 0.1, i, str(v), color='black', va='center', fontweight='bold')

plt.savefig(os.path.join(PLOTS_DIR, '02_disease_distribution.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 3: SYMPTOM FREQUENCY (TOP 20 SYMPTOMS)
# ==============================================================================
print("--> Generating Plot 3: Symptom Frequency...")
symptom_cols = [c for c in df_sym.columns if c not in ['prognosis', 'prognosis_encoded', 'symptom_count']]
symptom_freq = df_sym[symptom_cols].sum().sort_values(ascending=False).head(20)

fig, ax = plt.subplots(figsize=(12, 7))
sns.barplot(x=symptom_freq.values, y=symptom_freq.index, ax=ax, palette='mako')
ax.set_title("Top 20 Most Frequent Symptoms Across Patient Profiles", fontsize=14, fontweight='bold')
ax.set_xlabel("Frequency Count Across Diagnoses")
ax.set_ylabel("Symptom Name")

for i, v in enumerate(symptom_freq.values):
    ax.text(v + 0.2, i, str(v), color='black', va='center', fontweight='bold')

plt.savefig(os.path.join(PLOTS_DIR, '03_top_symptoms.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 4: TOP DISEASES / CONDITIONS IN DRUG REVIEWS
# ==============================================================================
print("--> Generating Plot 4: Top Medical Conditions...")
top_conditions = df_rev['condition'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(12, 7))
sns.barplot(x=top_conditions.values, y=top_conditions.index, ax=ax, palette='crest')
ax.set_title("Top 15 Most Common Medical Conditions in Drug Reviews", fontsize=14, fontweight='bold')
ax.set_xlabel("Total Patient Reviews Count")
ax.set_ylabel("Medical Condition")

for i, v in enumerate(top_conditions.values):
    ax.text(v + 100, i, f"{v:,}", color='black', va='center', fontweight='bold')

plt.savefig(os.path.join(PLOTS_DIR, '04_top_diseases_conditions.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 5: TOP PRESCRIBED MEDICINES
# ==============================================================================
print("--> Generating Plot 5: Top Prescribed Medicines...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Top Medicines in Drug Reviews
top_drugs_rev = df_rev['drugName'].value_counts().head(10)
sns.barplot(x=top_drugs_rev.values, y=top_drugs_rev.index, ax=axes[0], palette='Spectral')
axes[0].set_title("Top 10 Most Reviewed Drugs (Drug Reviews Dataset)", fontsize=13, fontweight='bold')
axes[0].set_xlabel("Review Count")

# Drug Distribution in Patient Prescriptions
drug_patient_counts = df_patient['Drug'].value_counts()
sns.barplot(x=drug_patient_counts.index, y=drug_patient_counts.values, ax=axes[1], palette='flare')
axes[1].set_title("Prescribed Drug Distribution (Patient Prescription Dataset)", fontsize=13, fontweight='bold')
axes[1].set_ylabel("Patient Count")
axes[1].set_xlabel("Prescribed Medication")

for i, v in enumerate(drug_patient_counts.values):
    axes[1].text(i, v + 1, str(v), ha='center', fontweight='bold')

plt.suptitle("Top Prescribed & Reviewed Medicines Analysis", fontsize=15, fontweight='bold', y=1.03)
plt.savefig(os.path.join(PLOTS_DIR, '05_top_prescribed_drugs.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 6: DRUG RATING & SENTIMENT DISTRIBUTION
# ==============================================================================
print("--> Generating Plot 6: Drug Rating & Sentiment Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Rating Histogram & KDE
sns.histplot(df_rev['rating'], bins=10, kde=True, ax=axes[0], color='purple', discrete=True)
axes[0].set_title("Drug Rating Distribution (Scale 1-10)", fontsize=13, fontweight='bold')
axes[0].set_xlabel("Rating Score")
axes[0].set_ylabel("Frequency Count")

# Sentiment Label Distribution
sentiment_counts = df_rev['sentiment_label'].value_counts(normalize=True) * 100
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=axes[1], palette=['#d9534f', '#f0ad4e', '#5cb85c'])
axes[1].set_title("Patient Sentiment Categorization (%)", fontsize=13, fontweight='bold')
axes[1].set_ylabel("Percentage of Total Reviews (%)")
axes[1].set_xlabel("Sentiment Category")

for i, v in enumerate(sentiment_counts.values):
    axes[1].text(i, v + 1, f"{v:.1f}%", ha='center', fontweight='bold')

plt.suptitle("Drug Review Rating & Sentiment Analysis", fontsize=15, fontweight='bold', y=1.03)
plt.savefig(os.path.join(PLOTS_DIR, '06_rating_sentiment_distribution.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 7: OUTLIER VISUALIZATION (BOXPLOTS)
# ==============================================================================
print("--> Generating Plot 7: Outlier Box Plots...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Na_to_K Raw vs Capped
sns.boxplot(y=df_patient_raw['Na_to_K'], ax=axes[0, 0], color='salmon')
axes[0, 0].set_title("Na_to_K Ratio (Raw Data - Outliers Present)", fontsize=12, fontweight='bold')

sns.boxplot(y=df_patient['Na_to_K_capped'], ax=axes[0, 1], color='lightgreen')
axes[0, 1].set_title("Na_to_K Ratio (Capped Data - IQR Handled)", fontsize=12, fontweight='bold')

# usefulCount Raw vs Log Transformed
sns.boxplot(y=df_rev['usefulCount'], ax=axes[1, 0], color='violet')
axes[1, 0].set_title("usefulCount (Raw - Highly Skewed)", fontsize=12, fontweight='bold')

sns.boxplot(y=df_rev['usefulCount_log'], ax=axes[1, 1], color='cyan')
axes[1, 1].set_title("usefulCount (Log Transformed log1p)", fontsize=12, fontweight='bold')

plt.suptitle("Task 7: Outlier Detection and Mitigation Visualizations", fontsize=15, fontweight='bold', y=1.02)
plt.savefig(os.path.join(PLOTS_DIR, '07_outliers_boxplots.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 8: CORRELATION HEATMAP (PATIENT BIOMARKERS)
# ==============================================================================
print("--> Generating Plot 8: Patient Biomarker Correlation Heatmap...")
plt.figure(figsize=(10, 8))
patient_corr_cols = ['Age', 'BP_encoded', 'Cholesterol_encoded', 'Na_to_K', 'Na_K_High', 'Drug_encoded']
patient_corr = df_patient[patient_corr_cols].corr()

mask = np.triu(np.ones_like(patient_corr, dtype=bool))
sns.heatmap(patient_corr, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, mask=mask, linewidths=1)
plt.title("Correlation Heatmap: Patient Clinical Biomarkers & Drug Target", fontsize=14, fontweight='bold')
plt.savefig(os.path.join(PLOTS_DIR, '08_patient_correlation_heatmap.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 9: SYMPTOM CO-OCCURRENCE HEATMAP
# ==============================================================================
print("--> Generating Plot 9: Symptom Co-occurrence Heatmap...")
top_15_symptoms = df_sym[symptom_cols].sum().sort_values(ascending=False).head(15).index
symptom_corr = df_sym[top_15_symptoms].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(symptom_corr, annot=True, fmt=".2f", cmap='PuBu', vmin=-0.5, vmax=1, linewidths=0.5)
plt.title("Symptom Co-occurrence Correlation Matrix (Top 15 Symptoms)", fontsize=14, fontweight='bold')
plt.savefig(os.path.join(PLOTS_DIR, '09_symptom_cooccurrence_heatmap.png'), dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# VISUALIZATION 10: PAIR PLOT OF PATIENT BIOMARKERS
# ==============================================================================
print("--> Generating Plot 10: Patient Biomarkers Pair Plot...")
pair_df = df_patient[['Age', 'Na_to_K', 'BP_encoded', 'Cholesterol_encoded', 'Drug']].copy()

pair_plot = sns.pairplot(pair_df, hue='Drug', palette='bright', corner=True, diag_kind='kde')
pair_plot.fig.suptitle("Pair Plot of Patient Clinical Features Color-Coded by Prescribed Drug", fontsize=15, fontweight='bold', y=1.02)
pair_plot.savefig(os.path.join(PLOTS_DIR, '10_patient_biomarkers_pairplot.png'), dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "=" * 80)
print(" EDA COMPLETED SUCCESSFULLY! All 10 plots saved in 'eda_plots/' ")
print("=" * 80)
