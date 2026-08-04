"""
Personalized Healthcare & Medicine Recommendation System
--------------------------------------------------------
Complete Data Preprocessing and Cleaning Pipeline (Tasks 1-10)

Uses Pandas and NumPy only.
"""

import os
import html
import re
import pandas as pd
import numpy as np

# Create output directory for cleaned datasets
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'cleaned_data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def print_header(title):
    print("\n" + "=" * 80)
    print(f" {title.upper()} ")
    print("=" * 80)

def display_dataset_info(df, name="Dataset"):
    """
    Task 2 & Task 3: Display dataset information (shape, columns, data types, missing values)
    """
    print(f"\n--- [METADATA] {name} ---")
    print(f"Shape (Rows, Columns): {df.shape}")
    print(f"Total Duplicate Rows: {df.duplicated().sum()}")
    print("\nColumn Data Types & Missing Values:")
    info_df = pd.DataFrame({
        'Data Type': df.dtypes,
        'Missing Values': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
    })
    print(info_df)
    return info_df


# ==============================================================================
# DATASET 1: DISEASE & SYMPTOMS DATASET (archive (9))
# ==============================================================================
print_header("1. Processing Disease & Symptoms Dataset")

# Task 1: Load Datasets
train_symptoms_path = 'archive (9)/Training.csv'
test_symptoms_path = 'archive (9)/Testing.csv'

df_sym_train = pd.read_csv(train_symptoms_path)
df_sym_test = pd.read_csv(test_symptoms_path)

# Task 2 & 3: Display Dataset Info & Check Missing Values
display_dataset_info(df_sym_train, "Disease Symptoms Training Set (Raw)")
display_dataset_info(df_sym_test, "Disease Symptoms Testing Set (Raw)")

# Task 5: Handle Missing Values
# The Training.csv has a trailing empty column 'Unnamed: 133' filled with NaNs
if 'Unnamed: 133' in df_sym_train.columns:
    print("\n--> [Task 5: Handle Missing Values] Dropping 100% NaN column 'Unnamed: 133' from Training set.")
    df_sym_train.drop(columns=['Unnamed: 133'], inplace=True)

# Task 4: Remove Duplicate Records
train_dups = df_sym_train.duplicated().sum()
print(f"\n--> [Task 4: Remove Duplicates] Found {train_dups} duplicate records in Training set.")
df_sym_train_clean = df_sym_train.drop_duplicates().copy()
print(f"    Training set shape after dropping duplicates: {df_sym_train_clean.shape}")

df_sym_test_clean = df_sym_test.drop_duplicates().copy()

# Task 6: Correct Inconsistent Text Values
print("\n--> [Task 6: Text Standardization] Cleaning symptom column names & prognosis labels...")

# Clean column headers (strip spaces, lowercase)
df_sym_train_clean.columns = [col.strip().lower() for col in df_sym_train_clean.columns]
df_sym_test_clean.columns = [col.strip().lower() for col in df_sym_test_clean.columns]

# Standardize prognosis typos & formatting
prognosis_corrections = {
    'peptic ulcer diseae': 'Peptic Ulcer Disease',
    'dimorphic hemmorhoids(piles)': 'Dimorphic Hemorrhoids (Piles)',
    'diabetes ': 'Diabetes',
    'hypertension ': 'Hypertension'
}

def clean_prognosis(text):
    if pd.isnull(text):
        return text
    text_clean = str(text).strip()
    key_lower = text_clean.lower()
    if key_lower in prognosis_corrections:
        return prognosis_corrections[key_lower]
    return text_clean.title()

df_sym_train_clean['prognosis'] = df_sym_train_clean['prognosis'].apply(clean_prognosis)
df_sym_test_clean['prognosis'] = df_sym_test_clean['prognosis'].apply(clean_prognosis)

# Task 7: Detect and Handle Outliers
# Symptom features are binary flags (0 or 1). Verify no values fall outside {0, 1}
symptom_cols = [c for c in df_sym_train_clean.columns if c != 'prognosis']
non_binary_check = ((df_sym_train_clean[symptom_cols] != 0) & (df_sym_train_clean[symptom_cols] != 1)).sum().sum()
print(f"\n--> [Task 7: Outliers Check] Non-binary values in symptom columns: {non_binary_check}")

# Task 8: Convert Categorical Features into Numerical Format
print("\n--> [Task 8: Categorical Encoding] Target encoding for 'prognosis'...")
unique_diseases = sorted(df_sym_train_clean['prognosis'].unique())
disease_to_code = {disease: idx for idx, disease in enumerate(unique_diseases)}

df_sym_train_clean['prognosis_encoded'] = df_sym_train_clean['prognosis'].map(disease_to_code)
df_sym_test_clean['prognosis_encoded'] = df_sym_test_clean['prognosis'].map(disease_to_code)

# Task 9: Perform Feature Engineering
print("\n--> [Task 9: Feature Engineering] Creating 'symptom_count' feature...")
df_sym_train_clean['symptom_count'] = df_sym_train_clean[symptom_cols].sum(axis=1)
df_sym_test_clean['symptom_count'] = df_sym_test_clean[symptom_cols].sum(axis=1)

# Task 10: Save Cleaned Datasets
train_sym_out = os.path.join(OUTPUT_DIR, 'cleaned_disease_symptoms_train.csv')
test_sym_out = os.path.join(OUTPUT_DIR, 'cleaned_disease_symptoms_test.csv')
df_sym_train_clean.to_csv(train_sym_out, index=False)
df_sym_test_clean.to_csv(test_sym_out, index=False)
print(f"\n--> [Task 10: Export] Saved cleaned disease symptoms datasets:")
print(f"    - {train_sym_out} ({df_sym_train_clean.shape})")
print(f"    - {test_sym_out} ({df_sym_test_clean.shape})")


# ==============================================================================
# DATASET 2: DRUG REVIEWS DATASET (archive (10))
# ==============================================================================
print_header("2. Processing Drug Reviews Dataset")

# Task 1: Load Datasets
train_reviews_path = 'archive (10)/drugsComTrain_raw.csv'
test_reviews_path = 'archive (10)/drugsComTest_raw.csv'

df_rev_train = pd.read_csv(train_reviews_path)
df_rev_test = pd.read_csv(test_reviews_path)

# Task 2 & 3: Display Info & Check Missing Values
display_dataset_info(df_rev_train, "Drug Reviews Training Set (Raw)")
display_dataset_info(df_rev_test, "Drug Reviews Testing Set (Raw)")

# Task 4: Remove Duplicate Records
print("\n--> [Task 4: Remove Duplicates] Checking duplicates...")
rev_train_dups = df_rev_train.duplicated(subset=['uniqueID']).sum()
print(f"    Duplicate uniqueIDs in Train: {rev_train_dups}")

df_rev_train_clean = df_rev_train.drop_duplicates(subset=['uniqueID']).copy()
df_rev_test_clean = df_rev_test.drop_duplicates(subset=['uniqueID']).copy()

# Task 5: Handle Missing Values
print("\n--> [Task 5: Handle Missing Values] Imputing missing 'condition' values...")
df_rev_train_clean['condition'] = df_rev_train_clean['condition'].fillna('Unknown')
df_rev_test_clean['condition'] = df_rev_test_clean['condition'].fillna('Unknown')

# Task 6: Correct Inconsistent Text Values & Clean HTML Artifacts
print("\n--> [Task 6: Text Standardization & HTML Cleaning] Unescaping HTML entities & cleaning text...")

def clean_text_field(text):
    if pd.isnull(text):
        return 'Unknown'
    text_str = str(text)
    # Decode HTML entities like &#039;, &amp;, &quot;
    text_clean = html.unescape(text_str)
    # Remove HTML scraper artifacts like '</span> users found this comment helpful.'
    if '</span>' in text_clean:
        return 'Unknown'
    # Trim leading/trailing whitespace and normalize spacing
    text_clean = re.sub(r'\s+', ' ', text_clean).strip()
    return text_clean

def clean_drug_name(text):
    if pd.isnull(text):
        return text
    clean = html.unescape(str(text)).strip()
    return clean.title()

for df in [df_rev_train_clean, df_rev_test_clean]:
    df['drugName'] = df['drugName'].apply(clean_drug_name)
    df['condition'] = df['condition'].apply(clean_text_field)
    df['review'] = df['review'].apply(clean_text_field)

# Task 7: Detect and Handle Outliers
print("\n--> [Task 7: Outlier Detection & Handling] Analyzing 'usefulCount' and 'rating'...")
print(f"    Rating Range (Train): Min = {df_rev_train_clean['rating'].min()}, Max = {df_rev_train_clean['rating'].max()}")

# Useful count is highly right-skewed. Compute IQR and apply Log Transformation (log1p)
for df in [df_rev_train_clean, df_rev_test_clean]:
    Q1 = df['usefulCount'].quantile(0.25)
    Q3 = df['usefulCount'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    outlier_count = (df['usefulCount'] > upper_bound).sum()
    print(f"    'usefulCount' IQR Upper Bound: {upper_bound:.1f} | Outliers Count: {outlier_count} ({outlier_count/len(df)*100:.2f}%)")
    
    # Cap usefulCount at 99th percentile and add log-transformed feature
    cap_val = df['usefulCount'].quantile(0.99)
    df['usefulCount_capped'] = np.where(df['usefulCount'] > cap_val, cap_val, df['usefulCount'])
    df['usefulCount_log'] = np.log1p(df['usefulCount'])

# Task 8: Convert Categorical Features into Numerical Format
print("\n--> [Task 8: Categorical Encoding] Converting 'rating' into sentiment classes...")
# Sentiment mapping: 1-3 -> Negative (0), 4-6 -> Neutral (1), 7-10 -> Positive (2)
def map_rating_sentiment(rating):
    if rating <= 3:
        return 0 # Negative
    elif rating <= 6:
        return 1 # Neutral
    else:
        return 2 # Positive

for df in [df_rev_train_clean, df_rev_test_clean]:
    df['sentiment_class'] = df['rating'].apply(map_rating_sentiment)
    df['sentiment_label'] = df['sentiment_class'].map({0: 'Negative', 1: 'Neutral', 2: 'Positive'})

# Task 9: Perform Feature Engineering
print("\n--> [Task 9: Feature Engineering] Extracting date features and text length metrics...")
for df in [df_rev_train_clean, df_rev_test_clean]:
    # Date parsing
    df['date_parsed'] = pd.to_datetime(df['date'], format='%d-%b-%y', errors='coerce')
    df['review_year'] = df['date_parsed'].dt.year
    df['review_month'] = df['date_parsed'].dt.month
    
    # Review length metrics
    df['review_char_count'] = df['review'].apply(len)
    df['review_word_count'] = df['review'].apply(lambda x: len(x.split()))

# Task 10: Save Cleaned Datasets
train_rev_out = os.path.join(OUTPUT_DIR, 'cleaned_drug_reviews_train.csv')
test_rev_out = os.path.join(OUTPUT_DIR, 'cleaned_drug_reviews_test.csv')
df_rev_train_clean.to_csv(train_rev_out, index=False)
df_rev_test_clean.to_csv(test_rev_out, index=False)
print(f"\n--> [Task 10: Export] Saved cleaned drug reviews datasets:")
print(f"    - {train_rev_out} ({df_rev_train_clean.shape})")
print(f"    - {test_rev_out} ({df_rev_test_clean.shape})")


# ==============================================================================
# DATASET 3: PATIENT PRESCRIPTIONS DATASET (archive (11))
# ==============================================================================
print_header("3. Processing Patient Prescriptions Dataset (drug200.csv)")

# Task 1: Load Dataset
patient_prescriptions_path = 'archive (11)/drug200.csv'
df_patient = pd.read_csv(patient_prescriptions_path)

# Task 2 & 3: Display Info & Check Missing Values
display_dataset_info(df_patient, "Patient Prescriptions Dataset (Raw)")

# Task 4: Remove Duplicate Records
patient_dups = df_patient.duplicated().sum()
print(f"\n--> [Task 4: Remove Duplicates] Duplicate records count: {patient_dups}")
df_patient_clean = df_patient.drop_duplicates().copy()

# Task 5: Handle Missing Values
print(f"--> [Task 5: Handle Missing Values] Total missing values: {df_patient_clean.isnull().sum().sum()}")

# Task 6: Correct Inconsistent Text Values
print("\n--> [Task 6: Text Standardization] Standardizing drug names, gender, BP, and Cholesterol...")

# Standardize Drug Names (e.g., 'drugC' -> 'Drug C', 'DrugY' -> 'Drug Y')
def standardize_drug_name(drug_str):
    if pd.isnull(drug_str):
        return drug_str
    d = str(drug_str).strip()
    if d.lower() == 'drugy':
        return 'Drug Y'
    elif d.lower() == 'druga':
        return 'Drug A'
    elif d.lower() == 'drugb':
        return 'Drug B'
    elif d.lower() == 'drugc':
        return 'Drug C'
    elif d.lower() == 'drugx':
        return 'Drug X'
    return d.title()

df_patient_clean['Drug'] = df_patient_clean['Drug'].apply(standardize_drug_name)
df_patient_clean['Sex'] = df_patient_clean['Sex'].str.strip().str.upper()
df_patient_clean['BP'] = df_patient_clean['BP'].str.strip().str.upper()
df_patient_clean['Cholesterol'] = df_patient_clean['Cholesterol'].str.strip().str.upper()

# Task 7: Detect and Handle Outliers
print("\n--> [Task 7: Outlier Detection & Handling] Inspecting continuous feature 'Na_to_K'...")
Q1 = df_patient_clean['Na_to_K'].quantile(0.25)
Q3 = df_patient_clean['Na_to_K'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df_patient_clean[(df_patient_clean['Na_to_K'] < lower_bound) | (df_patient_clean['Na_to_K'] > upper_bound)]
print(f"    'Na_to_K' Bounds: [{lower_bound:.2f}, {upper_bound:.2f}] | Outliers detected: {len(outliers)}")

# Cap outliers to upper IQR bound for a clean feature variant
df_patient_clean['Na_to_K_capped'] = np.where(
    df_patient_clean['Na_to_K'] > upper_bound,
    upper_bound,
    df_patient_clean['Na_to_K']
)

# Task 8: Convert Categorical Features into Numerical Format
print("\n--> [Task 8: Categorical Encoding] Encoding ordinal & nominal features...")

# Ordinal encodings
bp_map = {'LOW': 0, 'NORMAL': 1, 'HIGH': 2}
chol_map = {'NORMAL': 0, 'HIGH': 1}
sex_map = {'F': 0, 'M': 1}
drug_map = {'Drug A': 0, 'Drug B': 1, 'Drug C': 2, 'Drug X': 3, 'Drug Y': 4}

df_patient_clean['BP_encoded'] = df_patient_clean['BP'].map(bp_map)
df_patient_clean['Cholesterol_encoded'] = df_patient_clean['Cholesterol'].map(chol_map)
df_patient_clean['Sex_encoded'] = df_patient_clean['Sex'].map(sex_map)
df_patient_clean['Drug_encoded'] = df_patient_clean['Drug'].map(drug_map)

# Task 9: Perform Feature Engineering
print("\n--> [Task 9: Feature Engineering] Creating 'Age_Group' and 'Na_K_High' threshold flag...")

# Age Grouping: Youth (<30), Adult (30-55), Senior (>55)
def categorize_age(age):
    if age < 30:
        return 0 # Youth
    elif age <= 55:
        return 1 # Adult
    else:
        return 2 # Senior

df_patient_clean['Age_Group'] = df_patient_clean['Age'].apply(categorize_age)
df_patient_clean['Age_Group_Label'] = df_patient_clean['Age_Group'].map({0: 'Youth (<30)', 1: 'Adult (30-55)', 2: 'Senior (>55)'})

# Clinical ratio indicator (Na_to_K > 15 is a key medical threshold for Drug Y)
df_patient_clean['Na_K_High'] = (df_patient_clean['Na_to_K'] > 15.0).astype(int)

# Task 10: Save Cleaned Dataset
patient_out = os.path.join(OUTPUT_DIR, 'cleaned_patient_prescriptions.csv')
df_patient_clean.to_csv(patient_out, index=False)
print(f"\n--> [Task 10: Export] Saved cleaned patient prescriptions dataset:")
print(f"    - {patient_out} ({df_patient_clean.shape})")

print_header("ALL 10 PREPROCESSING TASKS COMPLETED SUCCESSFULLY")
