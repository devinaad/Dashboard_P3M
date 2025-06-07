import streamlit as st

def show_features():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Dashboard Interaktif</h3>
            <p>Visualisasi data yang menarik dan informatif</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Klasifikasi Otomatis</h3>
            <p>AI-powered classification untuk judul penelitian</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
