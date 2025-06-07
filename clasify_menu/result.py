import streamlit as st
from clasify_model import load_model_and_predict

jenis = "Penelitian"
judul = "Judul Penelitian"
tahun = 2016

# CSS untuk mempercantik tampilan
st.markdown("""
    <style>
        .success-box {
            background-color: #d4edda;
            border-left: 5px solid #28a745;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .section-header {
            font-size: 24px;
            font-weight: 600;
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 10px;
        }
        .result-box {
            background-color: #f0f8ff;
            border-left: 5px solid #1e90ff;
            padding: 1rem;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Show the entered data
st.markdown('<div class="success-box">✅ <strong>Data berhasil disubmit!</strong></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">📋 Data yang Dimasukkan</div>', unsafe_allow_html=True)
# st.dataframe(df)
st.markdown(f"""
    <div class="result-box">
        <strong>Judul:</strong> {judul}<br>
        <strong>Jenis Data:</strong> {jenis}<br>
        <strong>Tahun:</strong> {tahun}<br>
    </div>
""", unsafe_allow_html=True)

# Clasify the title
if jenis == "Penelitian":
    preds = load_model_and_predict("judul", model_path='rf_model_penelitian.joblib', vectorizer_path='tfidf_vectorizer.joblib')
    st.write(preds)
else:
    # Load the model for Pengabdian Masyarakat
    # model = load_model("path_to_pengmas_model")
    # result = model.predict(df)
    result = "Klasifikasi Pengabdian Masyarakat"

st.markdown('<div class="section-header">📚 Hasil Klasifikasi</div>', unsafe_allow_html=True)
st.markdown(f'<div class="result-box"><strong>{result}</strong></div>', unsafe_allow_html=True)
