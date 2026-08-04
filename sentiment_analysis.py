"""
Personalized Healthcare & Medicine Recommendation System
--------------------------------------------------------
Sentiment Analysis Pipeline (NLTK & Scikit-learn)

Tasks Completed:
1. Review text cleaning & HTML entity removal
2. Tokenization & Stopwords removal
3. WordNet Lemmatization
4. Sentiment Classification into Positive, Neutral, Negative
5. Sentiment Distribution Visualization
6. Identification of Highest-Rated Medicines with Positive Reviews
"""

import os
import re
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# Ensure NLTK resources
for resource in ['stopwords', 'punkt', 'wordnet', 'omw-1.4']:
    try:
        nltk.data.find(f'corpora/{resource}')
    except LookupError:
        nltk.download(resource, quiet=True)

# Set directories
PROJECT_DIR = os.path.dirname(__file__)
CLEANED_DIR = os.path.join(PROJECT_DIR, 'cleaned_data')
MODELS_DIR = os.path.join(PROJECT_DIR, 'models')
PLOTS_DIR = os.path.join(PROJECT_DIR, 'eda_plots')
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

print("=" * 80)
print(" SENTIMENT ANALYSIS PIPELINE (NLTK & SCIKIT-LEARN) ")
print("=" * 80)

# 1. Load Dataset
print("\n--> STEP 1: Loading Drug Reviews Dataset...")
reviews_path = os.path.join(CLEANED_DIR, 'cleaned_drug_reviews_train.csv')
df_reviews = pd.read_csv(reviews_path)
print(f"    Total Reviews Loaded: {len(df_reviews):,}")

# 2. Text Preprocessing
print("\n--> STEP 2: Preprocessing Review Text (Cleaning, Tokenizing, Removing Stopwords, Lemmatizing)...")
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def fast_clean(text):
    if pd.isnull(text):
        return ""
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    words = text.split()
    return " ".join([lemmatizer.lemmatize(w) for w in words if w not in stop_words and len(w) > 2])

# Take 15,000 representative sample for fast execution
df_sample = df_reviews.sample(n=15000, random_state=42).copy()
df_sample['clean_processed_review'] = df_sample['review'].apply(fast_clean)

# 3. Target Assignment
print("\n--> STEP 3: Assigning Sentiment Categories (Positive, Neutral, Negative)...")
def classify_sentiment(rating):
    if rating >= 7:
        return 'Positive'
    elif rating <= 3:
        return 'Negative'
    else:
        return 'Neutral'

df_sample['sentiment_target'] = df_sample['rating'].apply(classify_sentiment)
df_reviews['sentiment_target'] = df_reviews['rating'].apply(classify_sentiment)

sentiment_counts = df_reviews['sentiment_target'].value_counts()
print(df_reviews['sentiment_target'].value_counts(normalize=True).apply(lambda x: f"{x*100:.2f}%"))

# 4. Machine Learning Model Training
print("\n--> STEP 4: Training Sentiment Classification Model (TF-IDF + Logistic Regression)...")
X_text = df_sample['clean_processed_review']
y_sent = df_sample['sentiment_target']

X_train, X_test, y_train, y_test = train_test_split(X_text, y_sent, test_size=0.20, random_state=42, stratify=y_sent)

tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_vec = tfidf.fit_transform(X_train)
X_test_vec = tfidf.transform(X_test)

clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_train_vec, y_train)

y_pred = clf.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)
print(f"    Sentiment Classifier Test Accuracy: {acc * 100:.2f}%")

with open(os.path.join(MODELS_DIR, 'sentiment_classifier.pkl'), 'wb') as f:
    pickle.dump(clf, f)

with open(os.path.join(MODELS_DIR, 'sentiment_tfidf_vectorizer.pkl'), 'wb') as f:
    pickle.dump(tfidf, f)
print(f"--> Saved Sentiment Model to 'models/sentiment_classifier.pkl'")

# 5. Visualization
print("\n--> STEP 5: Visualizing Sentiment Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=axes[0], palette=['#5cb85c', '#d9534f', '#f0ad4e'])
axes[0].set_title("Patient Sentiment Distribution Count", fontsize=13, fontweight='bold')
axes[0].set_ylabel("Number of Reviews")

axes[1].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, 
           colors=['#5cb85c', '#d9534f', '#f0ad4e'], explode=(0.05, 0.05, 0.05), textprops={'fontweight':'bold'})
axes[1].set_title("Sentiment Percentage Split", fontsize=13, fontweight='bold')

plt.suptitle("Medicine Review Sentiment Analysis Overview", fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
sent_plot_path = os.path.join(PLOTS_DIR, 'sentiment_distribution_analysis.png')
plt.savefig(sent_plot_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"--> Saved Sentiment Plot: {sent_plot_path}")

# 6. Highest Rated Medicines with Positive Reviews
print("\n--> STEP 6: Identifying Highest-Rated Medicines with Positive Reviews...")
drug_summary = df_reviews.groupby('drugName').agg(
    total_reviews=('uniqueID', 'count'),
    avg_rating=('rating', 'mean'),
    positive_reviews_count=('sentiment_target', lambda x: (x == 'Positive').sum()),
    positive_ratio=('sentiment_target', lambda x: (x == 'Positive').mean())
).reset_index()

top_pos_drugs = drug_summary[drug_summary['total_reviews'] >= 20].sort_values(
    by=['avg_rating', 'positive_ratio', 'positive_reviews_count'], ascending=False
).head(15)

top_pos_drugs['avg_rating'] = top_pos_drugs['avg_rating'].round(2)
top_pos_drugs['positive_pct'] = (top_pos_drugs['positive_ratio'] * 100).round(1)

display_cols = ['drugName', 'avg_rating', 'total_reviews', 'positive_reviews_count', 'positive_pct']
print("\n--- TOP 15 HIGHEST-RATED MEDICINES WITH POSITIVE REVIEWS ---")
print(top_pos_drugs[display_cols].to_string(index=False))

top_pos_csv = os.path.join(CLEANED_DIR, 'highest_rated_positive_medicines.csv')
top_pos_drugs[display_cols].to_csv(top_pos_csv, index=False)
print(f"\n--> Saved Top Positive Medicines to '{top_pos_csv}'")

print("\n" + "=" * 80)
print(" SENTIMENT ANALYSIS PIPELINE COMPLETED SUCCESSFULLY ")
print("=" * 80)
