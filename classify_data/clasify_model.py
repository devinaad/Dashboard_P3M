# classify_data/clasify_model.py
from sklearn.model_selection import train_test_split
import joblib
import os

def load_model_and_predict(texts, model_path='rf_model_penelitian.joblib', vectorizer_path='tfidf_vectorizer_penelitian.joblib'):
    """
    Load trained model and vectorizer, then predict classifications for input texts
    
    Args:
        texts (list): List of texts to classify
        model_path (str): Path to the trained model file
        vectorizer_path (str): Path to the fitted vectorizer file
    
    Returns:
        list: List of predictions
    """
    try:
        # Check if model files exist
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
        
        # Load model and vectorizer
        print(f"Loading model from: {model_path}")
        model = joblib.load(model_path)
        
        print(f"Loading vectorizer from: {vectorizer_path}")
        vectorizer = joblib.load(vectorizer_path)
        
        # Transform input text using the loaded vectorizer
        print(f"Transforming {len(texts)} texts...")
        X_input = vectorizer.transform(texts)
        
        # Make predictions
        print("Making predictions...")
        predictions = model.predict(X_input)
        
        print(f"Predictions completed. {len(predictions)} results generated.")
        return predictions.tolist()
        
    except Exception as e:
        print(f"Error in load_model_and_predict: {e}")
        # Return default predictions in case of error
        return ['Belum Terklasifikasi'] * len(texts)

def get_model_paths(data_type='penelitian'):
    """
    Get appropriate model and vectorizer paths based on data type
    
    Args:
        data_type (str): Type of data ('penelitian' or 'pengabdian')
    
    Returns:
        tuple: (model_path, vectorizer_path)
    """
    if data_type == 'penelitian':
        model_path = 'models/rf_model_penelitian.joblib'
        vectorizer_path = 'models/tfidf_vectorizer_penelitian.joblib'
    elif data_type == 'pengabdian':
        model_path = 'models/rf_model_pengabdian.joblib'
        vectorizer_path = 'models/tfidf_vectorizer_pengabdian.joblib'
    else:
        raise ValueError(f"Unknown data_type: {data_type}. Use 'penelitian' or 'pengabdian'")
    
    return model_path, vectorizer_path

def classify_texts(texts, data_type='penelitian'):
    """
    Convenience function to classify texts based on data type
    
    Args:
        texts (list): List of texts to classify
        data_type (str): Type of data ('penelitian' or 'pengabdian')
    
    Returns:
        list: List of predictions
    """
    model_path, vectorizer_path = get_model_paths(data_type)
    return load_model_and_predict(texts, model_path, vectorizer_path)