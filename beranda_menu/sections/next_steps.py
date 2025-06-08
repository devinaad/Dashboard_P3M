import streamlit as st

def show_next_steps():
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Lihat Dashboard", use_container_width=True):
            st.info("🔄 Navigasi ke halaman Dashboard")

    with col2:
        if st.button("🤖 Mulai Klasifikasi", use_container_width=True):
            st.info("🔄 Navigasi ke halaman Klasifikasi")
