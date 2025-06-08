import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
from streamlit_carousel import carousel


# Sidebar with conditional menu enabling
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
        size='lg',
        variant='filled', 
        color='indigo', 
        open_all=True,
        index=2  # This will select "Beranda" as default (index 2 after Menu and divider)
    )


# Handle menu selection
if main_menu == 'Beranda':
    # Your Beranda page logic here
    st.title("🏠 Beranda")
    def show_carousel_header():
        # Add this CSS for much better text visibility

        # Your existing carousel code
        carousel_items = [
            dict(
                title="🎯 Sistem Klasifikasi Data",
                text="Mengklasifikasikan data penelitian dan pengabdian masyarakat",
                img="https://img.freepik.com/free-photo/artistic-blurry-colorful-wallpaper-background_58702-8233.jpg?semt=ais_items_boosted&w=740",
            ),
            dict(
                title="📊 Dashboard Analisis Data",
                text="Dashboard Analisis Penelitian dan Pengabdian Masyarakat dengan Visualisasi Interaktif",
                img="https://static.vecteezy.com/system/resources/previews/011/871/707/large_2x/indigo-gradient-abstract-background-use-it-as-a-banner-design-template-for-ads-websites-platforms-free-photo.jpg",
            )
        ]
        carousel(items=carousel_items)
    show_carousel_header()   
    st.write("Selamat datang! Silakan upload data Anda untuk memulai.")

    # File upload section (example)
    uploaded_file = st.file_uploader("Upload Dataset", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        # Process the uploaded file
        st.session_state['data_uploaded'] = True
        st.session_state['uploaded_data'] = uploaded_file
        st.success("Data berhasil diupload! Menu lain sekarang dapat diakses.")
        st.rerun()  # Refresh to update menu states

elif main_menu == 'Dashboard':
    if data_uploaded:
        # Your Dashboard logic here
        st.title("📊 Dashboard")
        st.write("Dashboard dengan visualisasi data yang telah diupload.")
    else:
        st.warning("Silakan upload data di halaman Beranda terlebih dahulu.")

elif main_menu == 'Klasifikasi Penelitian':
    if data_uploaded:
        # Your Klasifikasi Penelitian logic here
        st.title("📄 Klasifikasi Penelitian")
        st.write("Halaman klasifikasi data penelitian.")
    else:
        st.warning("Silakan upload data di halaman Beranda terlebih dahulu.")

elif main_menu == 'Klasifikasi Pengabdian Masyarakat':
    if data_uploaded:
        # Your Klasifikasi Pengabdian Masyarakat logic here
        st.title("👥 Klasifikasi Pengabdian Masyarakat")
        st.write("Halaman klasifikasi data pengabdian masyarakat.")
    else:
        st.warning("Silakan upload data di halaman Beranda terlebih dahulu.")