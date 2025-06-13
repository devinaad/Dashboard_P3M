import streamlit as st

def show_features():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📈 Dashboard Interaktif</h4>
            <p>Visualisasi data yang menarik dan informatif</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 Klasifikasi Otomatis</h4>
            <p>AI-powered classification untuk judul P3M</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
