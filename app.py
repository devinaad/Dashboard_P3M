import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_antd_components as sac
from itables import to_html_datatable
from page_setting.config import setup_page, colors, fields
from dashboard_menu.dashboard import show_dashboard_page
from dataset_menu.show_dataset import show_table
from dataset_menu.load_data import load_data
from beranda_menu.beranda import show_beranda_page

setup_page()

# Sidebar
with st.sidebar:
    # Check if data has been uploaded (you'll need to adapt this condition based on your actual data storage)
    # Example conditions - replace with your actual data check logic:
    data_uploaded = st.session_state.get('data_uploaded', False)
    # Or check if specific data exists:
    # data_uploaded = 'uploaded_data' in st.session_state and st.session_state.uploaded_data is not None
    
    main_menu = sac.menu(
        items=[
            sac.MenuItem('Menu', disabled=True),
            sac.MenuItem(type='divider'),
            sac.MenuItem('Beranda', icon='house-door'),
            sac.MenuItem('Dashboard', icon='speedometer2', disabled=not data_uploaded),
            sac.MenuItem('Dataset', icon='table', disabled=not data_uploaded, children=[
                sac.MenuItem('Klasifikasi Penelitian', icon='file-text', disabled=not data_uploaded),
                sac.MenuItem('Klasifikasi Pengabdian Masyarakat', icon='people', disabled=not data_uploaded)
            ])
        ],
        size='md',
        variant='filled', 
        color='indigo', 
        open_all=True,
        index=2  # This will select "Beranda" as default (index 2 after Menu and divider)
    )

# Main content
if main_menu == 'Beranda':
    show_beranda_page()
    
elif main_menu == "Dashboard":
    if st.session_state.get('data_uploaded', False):
        uploaded_penelitian = st.session_state.get('uploaded_penelitian')
        data_penelitian = load_data(uploaded_penelitian) 
        uploaded_pengabdian = st.session_state.get('uploaded_pengabdian')
        data_pengmas = load_data(uploaded_pengabdian)
        show_dashboard_page(fields, colors, data_penelitian, data_pengmas)
    else:
        st.warning("Silakan upload data di halaman Beranda terlebih dahulu.")

elif main_menu == "Klasifikasi Penelitian":
    if st.session_state.get('data_uploaded', False):
        uploaded_penelitian = st.session_state.get('uploaded_penelitian')
        data_penelitian = load_data(uploaded_penelitian)  
        show_table(data_penelitian, "Penelitian")
    else:
        st.warning("Silakan upload data di halaman Beranda terlebih dahulu.")

elif main_menu == "Klasifikasi Pengabdian Masyarakat":
    if st.session_state.get('data_uploaded', False):
        uploaded_pengabdian = st.session_state.get('uploaded_pengabdian')
        data_pengmas = load_data(uploaded_pengabdian)
        show_table(data_pengmas, "Pengabdian Masyarakat")
    else:
        st.warning("Silakan upload data di halaman Beranda terlebih dahulu.")




