# app.py

from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)

# --- Load model artifacts ---
MODEL_DIR = 'models'
try:
    model = joblib.load(os.path.join(MODEL_DIR, 'predictor_precios_rf.joblib'))
    tfidf = joblib.load(os.path.join(MODEL_DIR, 'tfidf_vectorizer.joblib'))
    model_columns = joblib.load(os.path.join(MODEL_DIR, 'model_columns.joblib'))
    print("✅ Model and artifacts loaded.")
except FileNotFoundError:
    print(f"❌ Model files not found in the '{MODEL_DIR}' folder.")
    print("Be sure to run 'src/train_model.py' first.")
    model = None

@app.route('/')
def home():
    """Displays the homepage with the form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Receives form data, processes it, and returns a prediction."""
    if model is None:
        return "Model not loaded. Please train the model by running 'src/train_model.py'."

    # Get data from form
    title = request.form.get('titulo', '')
    rating_str = request.form.get('calificacion', '3')
    
    try:
        rating = float(rating_str)
    except ValueError:
        rating = 3.0 # Default value if input is not a number

    # --- Recreate the input DataFrame with the same features ---
    
    # Create an initial DataFrame for the new input
    df_input = pd.DataFrame({'titulo': [title], 'calificacion': [rating]})

    # Apply the same feature engineering as in training
    df_input['etiqueta_precio'] = np.where(df_input['calificacion'] * 10 > 40, 'Caro', 'Normal')
    df_input['descripcion_rating'] = np.where(df_input['calificacion'] > 3, 'Bueno', 'Regular')

    # Apply TF-IDF to the title
    text_features_input = pd.DataFrame(
        tfidf.transform(df_input['titulo']).toarray(), 
        columns=tfidf.get_feature_names_out()
    )

    # Apply One-Hot Encoding to categories
    df_dummies_input = pd.get_dummies(df_input[['etiqueta_precio', 'descripcion_rating']], drop_first=True, dtype=int)
    
    # Combine all features
    processed_df = pd.concat([df_input[['calificacion']], df_dummies_input, text_features_input], axis=1)

    # Ensure the final DataFrame has exactly the same columns as the model expects
    final_df = processed_df.reindex(columns=model_columns, fill_value=0)

    # Make the prediction
    prediction = model.predict(final_df)[0]

    return render_template('resultado.html', prediccion=f'{prediction:.2f}', titulo=title)

if __name__ == '__main__':
    # debug=False is safer for production, True is for development
    app.run(debug=True)