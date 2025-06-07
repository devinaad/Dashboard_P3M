from sklearn.model_selection import train_test_split
import joblib
    

def load_model_and_predict(texts, model_path='rf_model_penelitian.joblib', vectorizer_path='tfidf_vectorizer.joblib'):
    # Load model dan vectorizer
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    # Transform input text
    X_input = vectorizer.transform(texts)
    
    # Prediksi
    predictions = model.predict(X_input)
    
    return predictions
