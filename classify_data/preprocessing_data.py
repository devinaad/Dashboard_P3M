# classify_data/preprocessing_data.py
import pandas as pd
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def clean_text(text):
    """
    Clean and preprocess text data
    
    Args:
        text (str): Raw text to be cleaned
    
    Returns:
        str: Cleaned text
    """
    if pd.isna(text):
        return ""
    
    # Convert to string and lowercase
    text = str(text).lower()
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespaces
    text = ' '.join(text.split())
    
    return text

def preprocess_data(df, title_column='Judul'):
    """
    Preprocess the uploaded dataframe
    
    Args:
        df (pd.DataFrame): Raw dataframe
        title_column (str): Name of the column containing titles to be classified
    
    Returns:
        pd.DataFrame: Preprocessed dataframe
    """
    # Make a copy to avoid modifying original data
    processed_df = df.copy()
    
    # Clean the title column for classification
    if title_column in processed_df.columns:
        processed_df['cleaned_title'] = processed_df[title_column].apply(clean_text)
    else:
        raise ValueError(f"Column '{title_column}' not found in the dataframe")
    
    return processed_df

def classify_and_prepare_data(df, data_type='penelitian', title_column='Judul'):
    """
    Classify data and prepare final dataset for dashboard/dataset pages
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        data_type (str): Type of data ('penelitian' or 'pengabdian')
        title_column (str): Name of the column containing titles
    
    Returns:
        pd.DataFrame: Final processed dataframe with classifications
    """
    from classify_data.clasify_model import load_model_and_predict
    
    # Prepare model paths based on data type
    if data_type == 'penelitian':
        model_path = 'rf_model_penelitian.joblib'
        vectorizer_path = 'tfidf_vectorizer_penelitian.joblib'
        classification_column = 'Bidang Penelitian'
    else:  # pengabdian
        model_path = 'rf_model_pengmas.joblib'
        vectorizer_path = 'tfidf_vectorizer_pengmas.joblib'
        classification_column = 'Bidang Pengabdian Masyarakat'
    
    try:
        # Get predictions for cleaned titles
        titles_for_prediction = df['cleaned_title'].tolist()
        predictions = load_model_and_predict(
            titles_for_prediction, 
            model_path=model_path, 
            vectorizer_path=vectorizer_path
        )
        
        # Add predictions to dataframe
        df[classification_column] = predictions
        
    except FileNotFoundError as e:
        print(f"Model files not found: {e}")
        # Fallback: assign default classification
        df[classification_column] = 'Belum Terklasifikasi'
    except Exception as e:
        print(f"Error during classification: {e}")
        df[classification_column] = 'Error Klasifikasi'
    
    # Select only required columns for final output
    if data_type == 'penelitian':
        required_columns = ['Tahun', 'Judul', 'Bidang Penelitian', 'Dana Disetujui']
    else:  # pengabdian
        required_columns = ['Tahun', 'Judul', 'Bidang Pengabdian Masyarakat', 'Dana Disetujui']
    
    # Check which columns exist in the dataframe
    available_columns = [col for col in required_columns if col in df.columns]
    
    if len(available_columns) < len(required_columns):
        missing_columns = set(required_columns) - set(available_columns)
        print(f"Warning: Missing columns {missing_columns}. Using available columns: {available_columns}")
    
    # Return dataframe with available required columns
    final_df = df[available_columns].copy()
    
    # Drop the temporary cleaned_title column if it exists
    if 'cleaned_title' in final_df.columns:
        final_df = final_df.drop('cleaned_title', axis=1)
    
    return final_df

def process_uploaded_data(df, data_type='penelitian', title_column='Judul'):
    """
    Complete pipeline: preprocess -> classify -> prepare final data
    
    Args:
        df (pd.DataFrame): Raw uploaded dataframe
        data_type (str): Type of data ('penelitian' or 'pengabdian')
        title_column (str): Name of the column containing titles
    
    Returns:
        pd.DataFrame: Final processed and classified dataframe
    """
    print(f"Starting data processing for {data_type}...")
    
    # Step 1: Preprocess data
    print("Step 1: Preprocessing data...")
    preprocessed_df = preprocess_data(df, title_column)
    
    # Step 2: Classify and prepare final data
    print("Step 2: Classifying data...")
    final_df = classify_and_prepare_data(preprocessed_df, data_type, title_column)
    
    print(f"Data processing completed. Final shape: {final_df.shape}")
    return final_df