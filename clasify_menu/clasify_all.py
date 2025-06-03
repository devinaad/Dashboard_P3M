import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.model_selection import train_test_split 

# Create the base stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Unduh stopwords jika belum dilakukan
# nltk.download('stopwords')
stop_words = set(stopwords.words('indonesian'))

def clean_text(text):
    """Menghapus tanda baca, angka, dan spasi di awal/akhir."""
    text = text.translate(str.maketrans('', '', string.punctuation + string.digits))
    return text.strip()

def tokenize_text(text):
    """Memisahkan teks menjadi token."""
    return text.split()

def remove_stopwords(tokens):
    """Menghapus stop words dari token."""
    return [word for word in tokens if word.lower() not in stop_words]

def clean_word_by_word(tokens):
    cleaned_words = []
    for word in tokens:
        # Skip if word is just a single letter
        if len(word) <= 1:
            continue
            
        # Add to cleaned words
        cleaned_words.append(word)
    return cleaned_words

def custom_stem(tokens):
    # Words we want to protect from stemming
    protected = ['berbasis']
    
    # Process each word
    stemmed_words = []
    for word in tokens:
        if word in protected:
            stemmed_words.append(word)  # Keep protected words as is
        else:
            stemmed_words.append(stemmer.stem(word))  # Stem other words
            
    # Join back into text
    return ' '.join(stemmed_words)


def preprocess_text(df, text_column):
    """
    Melakukan preprocessing teks.
    
    Args:
        df (pd.DataFrame): DataFrame yang berisi teks.
        text_column (str): Nama kolom teks yang akan diproses.
        
    Returns:
        pd.DataFrame: DataFrame dengan kolom tambahan hasil preprocessing.
    """
    df['cleaned_text'] = df[text_column].apply(clean_text)
    df['lower_text'] = df['cleaned_text'].str.lower()
    df['tokenized_text'] = df['lower_text'].apply(tokenize_text)
    df['no_stopwords'] = df['tokenized_text'].apply(remove_stopwords)
    df['clean_word_by_word'] = df['no_stopwords'].apply(clean_word_by_word)
    df['stemmed_text'] = df['clean_word_by_word'].apply(custom_stem)
    return df

def prepare_data(data, text_column, target_column, test_size=0.2, random_state=42):
    """Prepare the data by splitting into train and test sets and vectorizing the text."""
    X = data[text_column]
    y = data[target_column]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Vectorize the text data
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    return X_train_vec, X_test_vec, y_train, y_test, vectorizer
    
def clasify_pengmas():
    data_pengmas = pd.read_excel("fix_data/pengmas_categorized.xlsx")
    X, y = prepare_data(data_pengmas,'Bidang Pengabdian Masyarakat')  

    # 1. Using SMOTE
    X_train_smote, X_test_smote, y_train_smote, y_test_smote = handle_imbalance(X, y, method='smote')
    
    # 2. Using random oversampling
    X_train_o, X_test_o, y_train_o, y_test_o= handle_imbalance(X, y, method='random_over')
    
    # Initialize classifier
    classifier = TextClassifier()
    
    # Train and evaluate models for SMOTE resampling
    all_results_smote = classifier.train_and_evaluate_all(
        X_train_smote, X_test_smote, y_train_smote, y_test_smote
    )
    
    # Train and evaluate models for random oversampling
    all_results_over = classifier.train_and_evaluate_all(
        X_train_o, X_test_o, y_train_o, y_test_o
    )
    
    # Print comparison of results
    print("\nResults with SMOTE:")
    classifier.print_results_comparison()
    
    print("\nResults with Random Oversampling:")
    classifier.print_results_comparison()

def clasify_penelitian():
