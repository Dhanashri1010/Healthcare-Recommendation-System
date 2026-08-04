"""
Personalized Healthcare & Medicine Recommendation System
--------------------------------------------------------
Disease Prediction Machine Learning Pipeline

Models trained & evaluated:
1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier
4. XGBoost Classifier

Evaluated using: Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
Saves the best model to 'models/disease_prediction_model.pkl'.
"""

import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Set directories
PROJECT_DIR = os.path.dirname(__file__)
CLEANED_DIR = os.path.join(PROJECT_DIR, 'cleaned_data')
MODELS_DIR = os.path.join(PROJECT_DIR, 'models')
PLOTS_DIR = os.path.join(PROJECT_DIR, 'eda_plots')
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

print("=" * 80)
print(" DISEASE PREDICTION MACHINE LEARNING PIPELINE ")
print("=" * 80)

# ------------------------------------------------------------------------------
# STEP 1: LOAD AND COMBINE CLEANED SYMPTOM DATASETS
# ------------------------------------------------------------------------------
print("\n--> STEP 1: Loading Cleaned Symptom Datasets...")

df_train = pd.read_csv(os.path.join(CLEANED_DIR, 'cleaned_disease_symptoms_train.csv'))
df_test = pd.read_csv(os.path.join(CLEANED_DIR, 'cleaned_disease_symptoms_test.csv'))

# Combine datasets for complete unique profile coverage
df_all = pd.concat([df_train, df_test], ignore_index=True).drop_duplicates()
print(f"    Combined Dataset Shape: {df_all.shape}")

# Define feature columns (132 binary symptom flags) and target variable
ignore_cols = ['prognosis', 'prognosis_encoded', 'symptom_count']
feature_cols = [col for col in df_all.columns if col not in ignore_cols]

X = df_all[feature_cols].copy()
y = df_all['prognosis_encoded'].copy()

# Disease label mapping
disease_mapping = df_all[['prognosis_encoded', 'prognosis']].drop_duplicates().sort_values('prognosis_encoded')
label_to_disease = dict(zip(disease_mapping['prognosis_encoded'], disease_mapping['prognosis']))
disease_to_label = dict(zip(disease_mapping['prognosis'], disease_mapping['prognosis_encoded']))

print(f"    Total Feature Count (Symptoms): {len(feature_cols)}")
print(f"    Total Target Disease Classes: {len(label_to_disease)}")


# ------------------------------------------------------------------------------
# STEP 2: TRAIN-TEST SPLIT
# ------------------------------------------------------------------------------
print("\n--> STEP 2: Splitting Dataset (80% Train, 20% Test with Stratification)...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"    Training Set Shape: {X_train.shape}")
print(f"    Testing Set Shape:  {X_test.shape}")


# ------------------------------------------------------------------------------
# STEP 3: TRAIN MULTIPLE MACHINE LEARNING MODELS
# ------------------------------------------------------------------------------
print("\n--> STEP 3: Training Machine Learning Models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'XGBoost': XGBClassifier(eval_metric='mlogloss', random_state=42)
}

results = []
trained_model_objects = {}
confusion_matrices = {}

for model_name, model in models.items():
    print(f"\n    Training {model_name}...")
    model.fit(X_train, y_train)
    trained_model_objects[model_name] = model
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate Evaluation Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Cross-validation score (5-Fold)
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    cv_mean = cv_scores.mean()
    
    cm = confusion_matrix(y_test, y_pred)
    confusion_matrices[model_name] = cm
    
    results.append({
        'Model': model_name,
        'Accuracy': round(acc, 4),
        'Precision': round(prec, 4),
        'Recall': round(rec, 4),
        'F1 Score': round(f1, 4),
        '5-Fold CV Accuracy': round(cv_mean, 4)
    })
    
    print(f"    --> {model_name} Results | Accuracy: {acc:.4f} | F1-Score: {f1:.4f} | 5-Fold CV: {cv_mean:.4f}")


# ------------------------------------------------------------------------------
# STEP 4: MODEL PERFORMANCE COMPARISON
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print(" STEP 4: MODEL PERFORMANCE COMPARISON TABLE ")
print("=" * 80)

df_results = pd.DataFrame(results).sort_values(by='F1 Score', ascending=False)
print(df_results.to_string(index=False))

# Plot Comparison Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
df_melted = df_results.melt(id_vars=['Model'], value_vars=['Accuracy', 'Precision', 'Recall', 'F1 Score'], var_name='Metric', value_name='Score')
sns.barplot(data=df_melted, x='Model', y='Score', hue='Metric', ax=ax, palette='Set2')
ax.set_title("Disease Prediction Models Comparison", fontsize=14, fontweight='bold')
ax.set_ylim(0.8, 1.05)
for p in ax.patches:
    h = p.get_height()
    if h > 0:
        ax.annotate(f"{h:.2f}", (p.get_x() + p.get_width() / 2., h), ha='center', va='bottom', fontsize=8, xytext=(0, 3), textcoords='offset points')

plt.tight_layout()
comp_plot_path = os.path.join(PLOTS_DIR, 'disease_model_comparison.png')
plt.savefig(comp_plot_path, dpi=300)
plt.close()
print(f"\n--> Saved comparison plot: {comp_plot_path}")


# ------------------------------------------------------------------------------
# STEP 5: CONFUSION MATRIX VISUALIZATION
# ------------------------------------------------------------------------------
print("\n--> STEP 5: Generating Confusion Matrix Visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(16, 14))
axes_flat = axes.flatten()

for idx, (model_name, cm) in enumerate(confusion_matrices.items()):
    ax = axes_flat[idx]
    sns.heatmap(cm, annot=False, cmap='Blues', ax=ax, cbar=True)
    ax.set_title(f"Confusion Matrix: {model_name}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Predicted Disease Class")
    ax.set_ylabel("True Disease Class")

plt.suptitle("Disease Prediction Model Confusion Matrices", fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
cm_plot_path = os.path.join(PLOTS_DIR, 'disease_confusion_matrices.png')
plt.savefig(cm_plot_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"--> Saved confusion matrices plot: {cm_plot_path}")


# ------------------------------------------------------------------------------
# STEP 6: SAVE THE BEST MODEL (.PKL) AND ARTIFACTS
# ------------------------------------------------------------------------------
best_model_name = df_results.iloc[0]['Model']
best_model_obj = trained_model_objects[best_model_name]
best_f1 = df_results.iloc[0]['F1 Score']

print(f"\n--> STEP 6: Saving Best Model ('{best_model_name}' with F1-Score = {best_f1:.4f})...")

best_model_path = os.path.join(MODELS_DIR, 'disease_prediction_model.pkl')
label_enc_path = os.path.join(MODELS_DIR, 'disease_label_encoder.pkl')
feature_cols_path = os.path.join(MODELS_DIR, 'symptom_features.pkl')

with open(best_model_path, 'wb') as f:
    pickle.dump(best_model_obj, f)

with open(label_enc_path, 'wb') as f:
    pickle.dump({'label_to_disease': label_to_disease, 'disease_to_label': disease_to_label}, f)

with open(feature_cols_path, 'wb') as f:
    pickle.dump(feature_cols, f)

print(f"    Best Model Saved:          {best_model_path}")
print(f"    Label Mapping Saved:       {label_enc_path}")
print(f"    Symptom Feature List Saved:{feature_cols_path}")

print("\n" + "=" * 80)
print(" DISEASE PREDICTION MODEL TRAINING COMPLETE ")
print("=" * 80)
