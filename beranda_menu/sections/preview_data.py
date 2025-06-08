import streamlit as st
from beranda_menu.utils.data_loader import data_loader

def show_data_preview(file_penelitian, file_pengabdian):
    st.markdown("---")
    st.markdown("## 📊 Preview Data")
    col1, col2 = st.columns(2)

    with col1:
        df_penelitian = data_loader(file_penelitian)
        if df_penelitian is not None:
            st.session_state['df_penelitian'] = df_penelitian
            st.markdown("### 🔬 Data Penelitian")
            st.dataframe(df_penelitian.head(), use_container_width=True)

    with col2:
        df_pengabdian = data_loader(file_pengabdian)
        if df_pengabdian is not None:
            st.session_state['df_pengabdian'] = df_pengabdian
            st.markdown("### 🤝 Data Pengabdian Masyarakat")
            st.dataframe(df_pengabdian.head(), use_container_width=True)
