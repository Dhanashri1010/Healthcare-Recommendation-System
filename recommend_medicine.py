"""
Personalized Healthcare & Medicine Recommendation System
--------------------------------------------------------
Content-Based Medicine Recommendation Engine (TF-IDF + Cosine Similarity)
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MedicineRecommender:
    """
    Content-Based Filtering Medicine Recommender System.
    Uses TF-IDF text vectorization on drug review content & medical conditions,
    combined with Cosine Similarity and rating/usefulness weighting.
    """
    def __init__(self, max_features=5000):
        self.vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english', ngram_range=(1, 2))
        self.drug_profiles = None
        self.tfidf_matrix = None
        self.df_reviews = None
        self.disease_list = []

    def fit(self, df_reviews):
        """
        Fits the TF-IDF vectorizer and builds aggregated drug profile knowledgebase.
        """
        self.df_reviews = df_reviews.copy()
        
        # Ensure text fields are strings
        self.df_reviews['condition'] = self.df_reviews['condition'].astype(str)
        self.df_reviews['drugName'] = self.df_reviews['drugName'].astype(str)
        self.df_reviews['review'] = self.df_reviews['review'].astype(str)

        # Aggregate drug metrics per condition & drugName
        aggregated = self.df_reviews.groupby(['condition', 'drugName']).agg(
            total_reviews=('uniqueID', 'count'),
            avg_rating=('rating', 'mean'),
            median_rating=('rating', 'median'),
            total_useful=('usefulCount', 'sum'),
            avg_useful=('usefulCount', 'mean'),
            combined_reviews=('review', lambda x: ' '.join(x[:20]))
        ).reset_index()

        # Formulate rich text representation for TF-IDF encoding
        aggregated['profile_text'] = (
            aggregated['condition'] + " " + 
            aggregated['drugName'] + " " + 
            aggregated['combined_reviews']
        )

        self.drug_profiles = aggregated
        self.disease_list = sorted(self.df_reviews['condition'].unique())
        
        # Store minimal review samples (1 positive & 1 negative review per pair) for recommendation lookup
        pos_revs = self.df_reviews[self.df_reviews['rating'] >= 7][['condition', 'drugName', 'rating', 'review']].groupby(['condition', 'drugName']).first().reset_index()
        neg_revs = self.df_reviews[self.df_reviews['rating'] <= 3][['condition', 'drugName', 'rating', 'review']].groupby(['condition', 'drugName']).first().reset_index()
        self.df_reviews = pd.concat([pos_revs, neg_revs], ignore_index=True)

        # Compute TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.drug_profiles['profile_text'])
        return self

    def recommend(self, disease_query, top_n=5):
        """
        Recommends top medicines for a query disease using TF-IDF Cosine Similarity & Hybrid Rating Scoring.
        """
        disease_query_clean = str(disease_query).strip()

        # 1. Exact or partial match in condition names
        exact_matches = self.drug_profiles[
            self.drug_profiles['condition'].str.lower() == disease_query_clean.lower()
        ]

        if len(exact_matches) >= top_n:
            candidates = exact_matches.copy()
        else:
            query_vec = self.vectorizer.transform([disease_query_clean])
            sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            candidates = self.drug_profiles.copy()
            candidates['similarity_score'] = sim_scores
            candidates = candidates.sort_values(by='similarity_score', ascending=False).head(50)

        if 'similarity_score' not in candidates.columns:
            query_vec = self.vectorizer.transform([disease_query_clean])
            cand_tfidf = self.vectorizer.transform(candidates['profile_text'])
            candidates['similarity_score'] = cosine_similarity(query_vec, cand_tfidf).flatten()

        max_useful = candidates['total_useful'].max() if candidates['total_useful'].max() > 0 else 1
        candidates['useful_norm'] = np.log1p(candidates['total_useful']) / np.log1p(max_useful)
        candidates['rating_norm'] = candidates['avg_rating'] / 10.0

        candidates['recommendation_score'] = (
            (0.40 * candidates['similarity_score']) +
            (0.40 * candidates['rating_norm']) +
            (0.20 * candidates['useful_norm'])
        )

        ranked_drugs = candidates.sort_values(by='recommendation_score', ascending=False).reset_index(drop=True)

        top_recommendations = ranked_drugs.head(top_n)
        alternatives = ranked_drugs.iloc[top_n:top_n+3]

        output_records = []
        for _, row in top_recommendations.iterrows():
            drug_name = row['drugName']
            cond_name = row['condition']

            subset_revs = self.df_reviews[
                (self.df_reviews['drugName'] == drug_name) & 
                (self.df_reviews['condition'] == cond_name)
            ]

            pos_revs = subset_revs[subset_revs['rating'] >= 7]['review'].tolist()
            neg_revs = subset_revs[subset_revs['rating'] <= 3]['review'].tolist()

            sample_pos = pos_revs[0][:150] + "..." if len(pos_revs) > 0 else "No positive reviews recorded."
            sample_neg = neg_revs[0][:150] + "..." if len(neg_revs) > 0 else "No negative reviews recorded."

            output_records.append({
                'Drug_Name': drug_name,
                'Condition': cond_name,
                'Average_Rating': round(row['avg_rating'], 2),
                'Total_Reviews': row['total_reviews'],
                'Useful_Review_Count': row['total_useful'],
                'Cosine_Similarity': round(row['similarity_score'], 4),
                'Recommendation_Score': round(row['recommendation_score'] * 100, 1),
                'Sample_Positive_Review': sample_pos,
                'Sample_Negative_Review': sample_neg
            })

        alt_records = []
        for _, row in alternatives.iterrows():
            alt_records.append({
                'Drug_Name': row['drugName'],
                'Average_Rating': round(row['avg_rating'], 2),
                'Useful_Review_Count': row['total_useful'],
                'Recommendation_Score': round(row['recommendation_score'] * 100, 1)
            })

        return {
            'Query_Disease': disease_query,
            'Top_5_Recommendations': pd.DataFrame(output_records),
            'Alternative_Medicines': pd.DataFrame(alt_records)
        }

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
