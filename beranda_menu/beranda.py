import streamlit as st
from .components.header import show_header
from .components.features import show_features
from .components.upload_section import show_upload_section
from .sections.preview_data import show_data_preview
from .sections.next_steps import show_next_steps
from .templates.template_download import show_template_download

def show_beranda_page():
    show_header()
    show_features()

    uploaded_penelitian, uploaded_pengabdian, submit_upload = show_upload_section()

    if uploaded_penelitian and uploaded_pengabdian and submit_upload:
        show_data_preview(uploaded_penelitian, uploaded_pengabdian)
        st.session_state['data_uploaded'] = True
        st.session_state['uploaded_penelitian'] = uploaded_penelitian
        st.session_state['uploaded_pengabdian'] = uploaded_pengabdian
        show_next_steps()
    else:
        show_template_download()

