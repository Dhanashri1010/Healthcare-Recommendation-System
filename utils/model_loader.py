"""
Model Loader Helper Module
--------------------------
Loads machine learning model binaries and serializers safely with caching.
"""

import os
import pickle
import streamlit as st

# Explicitly import MedicineRecommender to ensure pickle deserialization
from recommend_medicine import MedicineRecommender

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')

@st.cache_resource
def load_disease_model():
    """Loads disease prediction ML model and label encoder."""
    model_path = os.path.join(MODELS_DIR, 'disease_prediction_model.pkl')
    label_path = os.path.join(MODELS_DIR, 'disease_label_encoder.pkl')
    feature_path = os.path.join(MODELS_DIR, 'symptom_features.pkl')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    with open(label_path, 'rb') as f:
        encoder = pickle.load(f)

    with open(feature_path, 'rb') as f:
        features = pickle.load(f)

    return model, encoder, features

@st.cache_resource
def load_recommender():
    """Loads TF-IDF Content-Based Medicine Recommender."""
    recommender_path = os.path.join(MODELS_DIR, 'medicine_recommender.pkl')
    with open(recommender_path, 'rb') as f:
        recommender = pickle.load(f)
    return recommender

@st.cache_resource
def load_sentiment_classifier():
    """Loads NLTK & Scikit-learn Sentiment Classifier."""
    clf_path = os.path.join(MODELS_DIR, 'sentiment_classifier.pkl')
    tfidf_path = os.path.join(MODELS_DIR, 'sentiment_tfidf_vectorizer.pkl')

    with open(clf_path, 'rb') as f:
        clf = pickle.load(f)

    with open(tfidf_path, 'rb') as f:
        tfidf = pickle.load(f)

    return clf, tfidf
