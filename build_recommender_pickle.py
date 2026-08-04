import os
import pandas as pd
import pickle
from recommend_medicine import MedicineRecommender

print("--> Building and serializing MedicineRecommender with correct module path...")
cleaned_reviews_path = os.path.join(os.path.dirname(__file__), 'cleaned_data', 'cleaned_drug_reviews_train.csv')
df_reviews = pd.read_csv(cleaned_reviews_path)

recommender = MedicineRecommender(max_features=5000)
recommender.fit(df_reviews)

model_path = os.path.join(os.path.dirname(__file__), 'models', 'medicine_recommender.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(recommender, f)

print("--> Successfully saved models/medicine_recommender.pkl with recommend_medicine.MedicineRecommender class reference!")
