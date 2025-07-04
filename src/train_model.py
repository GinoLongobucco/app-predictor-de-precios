# src/train_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

def train_model():
    """
    Loads the data, performs feature engineering, trains the
    Random Forest model, and saves the necessary artifacts.
    """
    print("Starting model training...")
    
    data_path = os.path.join('data', 'biblioteca_completa.csv')
    
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: '{data_path}' not found.")
        print("Please run 'src/scraper.py' first.")
        return

    print("Performing feature engineering...")
    price_condition = df['precio'] > 40
    df['etiqueta_precio'] = np.where(price_condition, 'Caro', 'Normal')
    rating_condition = df['calificacion'] > 3
    df['descripcion_rating'] = np.where(rating_condition, 'Bueno', 'Regular')

    tfidf = TfidfVectorizer(max_features=50, stop_words='english')
    text_features = pd.DataFrame(
        tfidf.fit_transform(df['titulo']).toarray(), 
        columns=tfidf.get_feature_names_out()
    )

    df_dummies = pd.get_dummies(df[['etiqueta_precio', 'descripcion_rating']], drop_first=True, dtype=int)

    X = pd.concat([df[['calificacion']], df_dummies, text_features], axis=1)
    y = df['precio']

    print("Training the RandomForest model...")
    final_model = RandomForestRegressor(n_estimators=100, random_state=42)
    final_model.fit(X, y)
    
    models_dir = 'models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    joblib.dump(final_model, os.path.join(models_dir, 'predictor_precios_rf.joblib'))
    joblib.dump(tfidf, os.path.join(models_dir, 'tfidf_vectorizer.joblib'))
    joblib.dump(list(X.columns), os.path.join(models_dir, 'model_columns.joblib'))

    print(f"✅ Model and {len(X.columns)} features saved to the /models folder.")

if __name__ == '__main__':
    train_model()