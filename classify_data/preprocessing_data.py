# classify_data/preprocessing_data.py
import pandas as pd
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def clean_text(text):
    """
    Clean and preprocess text data for classification
    
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

def clean_nama(nama):
    """
    Clean names by removing academic titles and punctuation
    This helps in matching names with the lecturer database
    
    Args:
        nama (str): Raw name with possible titles
    
    Returns:
        str: Cleaned name without titles
    
    Example:
        Input: "Dr. Ir. John Doe, M.T."
        Output: "John Doe"
    """
    if not isinstance(nama, str):
        return ""
    
    # Remove punctuation (commas, periods, etc.)
    nama = re.sub(r'[^a-zA-Z\s]', '', nama)
    
    # List of common academic titles to remove
    # These are Indonesian academic titles commonly found in university data
    titles = {
        'skom', 'dr', 'dra', 'ir', 'st', 'mt', 'sst', 'mpd', 'phd', 'amd', 
        'medl', 'mkom', 'msi', 'msc', 'ms', 'meng', 'mengg', 
        'meng', 'msc', 'msceng', 'mcs', 'ssi', 'dring',
        'spd', 'sstmt', 'mc', 'drs', 'bsc', 'prof', 'profir', 'mengphd'
    }
    
    # Split name into words and remove titles
    words = nama.split()
    cleaned_words = [word for word in words if word.lower() not in titles]
    
    return ' '.join(cleaned_words).strip()

def create_prodi_lookup(dosen_df, nama_col='Nama Dosen', prodi_col='Nama Prodi'):
    """
    Create a lookup dictionary for mapping lecturer names to their programs
    Note: dosen_df is already processed and cleaned by the system
    
    Args:
        dosen_df (pd.DataFrame): Pre-processed DataFrame containing lecturer information
        nama_col (str): Column name for lecturer names
        prodi_col (str): Column name for program names
    
    Returns:
        tuple: (prodi_lookup dict, dosen_set) for name matching
    """
    # Since dosen_df is already processed, we can directly create the lookup
    # Create lookup dictionary: {lecturer_name: program_name}
    prodi_lookup = dict(zip(dosen_df[nama_col], dosen_df[prodi_col]))
    
    # Normalize names for better matching (lowercase, remove extra spaces)
    # Even though dosen_df is processed, we still need to normalize for matching
    normalized_lookup = {}
    dosen_set = set()
    
    for nama, prodi in prodi_lookup.items():
        # Clean and normalize the name for consistent matching
        cleaned_nama = clean_nama(str(nama)).strip().lower()
        if cleaned_nama:  # Only add if name is not empty after cleaning
            normalized_lookup[cleaned_nama] = prodi
            dosen_set.add(cleaned_nama)
    
    return normalized_lookup, dosen_set

def map_prodi_by_nama(df, nama_col, prodi_lookup, dosen_set, prodi_col="Prodi"):
    """
    Map program names to DataFrame based on lecturer names
    Uses both exact matching and fuzzy matching for better results
    
    Args:
        df (pd.DataFrame): Target DataFrame (research or community service data)
        nama_col (str): Column name containing lecturer names
        prodi_lookup (dict): Dictionary mapping names to programs
        dosen_set (set): Set of lecturer names for fuzzy matching
        prodi_col (str): Output column name for program mapping
    
    Returns:
        pd.DataFrame: DataFrame with program mapping added
    
    Matching Strategy:
        1. Exact match: Direct lookup in the dictionary
        2. Fuzzy match: Compare first 2 words + first letter of 3rd word
           This handles cases where names are written slightly differently
    """
    # Initialize all entries as "Lainnya" (Others)
    df[prodi_col] = "Lainnya"
    
    for index, row in df.iterrows():
        nama_ketua = str(row[nama_col]).strip()
        found = False
        
        # Step 1: Try exact match first
        if nama_ketua in prodi_lookup:
            df.at[index, prodi_col] = prodi_lookup[nama_ketua]
            continue
        
        # Step 2: Try fuzzy matching
        # This is useful when names are written slightly different
        # between the research data and lecturer database
        nama_split = nama_ketua.lower().split()
        
        for nama_dosen in dosen_set:
            nama_dosen_split = nama_dosen.lower().split()
            
            # Fuzzy matching logic:
            # - Both names must have at least 2-3 words
            # - First 2 words must match exactly
            # - First letter of 3rd word must match (handles abbreviations)
            if len(nama_split) >= 2 and len(nama_dosen_split) >= 3:
                # Check if first 2 words match
                if nama_split[:2] == nama_dosen_split[:2]:
                    # Check if first letter of 3rd word matches
                    if len(nama_split) >= 3 and nama_split[2] and nama_dosen_split[2]:
                        if nama_split[2][0] == nama_dosen_split[2][0]:
                            df.at[index, prodi_col] = prodi_lookup[nama_dosen]
                            found = True
                            break
    
    return df

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

def add_prodi_mapping(df, dosen_df, nama_ketua_col='Nama Ketua'):
    """
    Add program (Prodi) mapping to research/community service data
    Uses the pre-processed lecturer database that's already available in the system
    
    Args:
        df (pd.DataFrame): Research or community service dataframe
        dosen_df (pd.DataFrame): Pre-processed lecturer database with names and programs
        nama_ketua_col (str): Column name containing team leader names
    
    Returns:
        pd.DataFrame: DataFrame with Prodi column added
    
    Process:
        1. Save original names for later restoration
        2. Clean names from uploaded data for better matching
        3. Use pre-processed lecturer database to create lookup
        4. Perform name matching (exact + fuzzy)
        5. Restore original names from uploaded data
    """
    # Step 1: Save original names before cleaning
    # We'll restore these later to keep the data readable
    original_nama_col = f"{nama_ketua_col} Asli"
    df[original_nama_col] = df[nama_ketua_col].copy()
    
    # Step 2: Clean names from uploaded data for matching
    # Only the uploaded data needs cleaning - dosen_df is already processed
    df[nama_ketua_col] = df[nama_ketua_col].fillna('').apply(clean_nama).str.lower()
    
    # Step 3: Create lookup from pre-processed lecturer database
    # dosen_df is already cleaned and ready to use by the system
    prodi_lookup, dosen_set = create_prodi_lookup(dosen_df)
    
    # Step 4: Perform name mapping
    df = map_prodi_by_nama(df, nama_ketua_col, prodi_lookup, dosen_set)
    
    # Step 5: Restore original names from uploaded data
    df[nama_ketua_col] = df[original_nama_col]
    df.drop(columns=[original_nama_col], inplace=True)
    
    return df

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
        required_columns = ['Tahun', 'Judul', 'Bidang Penelitian', 'Dana Disetujui', 'Nama Ketua', 'Prodi']
    else:  # pengabdian
        model_path = 'rf_model_pengmas.joblib'
        vectorizer_path = 'tfidf_vectorizer_pengmas.joblib'
        classification_column = 'Bidang Pengabdian Masyarakat'
        required_columns = ['Tahun', 'Judul', 'Bidang Pengabdian Masyarakat', 'Dana Disetujui', 'Nama Ketua', 'Prodi']
    
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


def process_uploaded_data(df, dosen_df, data_type='penelitian', title_column='Judul'):
    """
    Complete pipeline: preprocess -> add prodi mapping -> classify -> prepare final data
    
    Args:
        df (pd.DataFrame): Raw uploaded dataframe (needs processing)
        dosen_df (pd.DataFrame): Pre-processed lecturer database (already available in system)
        data_type (str): Type of data ('penelitian' or 'pengabdian')
        title_column (str): Name of the column containing titles
    
    Returns:
        pd.DataFrame: Final processed and classified dataframe
    """
    # ADD DEBUG PRINT AT THE VERY BEGINNING
    print(f"🚀 process_uploaded_data called with:")
    print(f"   - df type: {type(df)}, shape: {df.shape if hasattr(df, 'shape') else 'no shape'}")
    print(f"   - dosen_df type: {type(dosen_df)}, shape: {dosen_df.shape if hasattr(dosen_df, 'shape') else 'no shape'}")
    print(f"   - data_type: {data_type}")
    print(f"   - title_column: {title_column}")
    
    try:
        print(f"Starting data processing for {data_type}...")
        
        # Step 1: Preprocess uploaded data
        print("Step 1: Preprocessing uploaded data...")
        preprocessed_df = preprocess_data(df, title_column)
        print(f"✅ Step 1 completed. Shape: {preprocessed_df.shape}")
        
        # Step 2: Add program mapping using system's lecturer database
        if 'Nama Ketua' in preprocessed_df.columns:
            print("Step 2: Adding program mapping using lecturer database...")
            preprocessed_df = add_prodi_mapping(preprocessed_df, dosen_df)
            print(f"✅ Step 2 completed. Shape: {preprocessed_df.shape}")
        else:
            print("Step 2: No 'Nama Ketua' column found, skipping program mapping")
            # Add default Prodi column
            preprocessed_df['Prodi'] = 'Lainnya'
        
        # Step 3: Classify and prepare final data
        print("Step 3: Classifying data using ML models...")
        final_df = classify_and_prepare_data(preprocessed_df, data_type, title_column)
        print(f"✅ Step 3 completed. Final shape: {final_df.shape}")
        
        print(f"🎉 Data processing completed successfully!")
        return final_df
        
    except Exception as e:
        print(f"❌ Error in process_uploaded_data: {type(e).__name__}: {e}")
        raise e  # Re-raise the error so we can see it in Streamlit