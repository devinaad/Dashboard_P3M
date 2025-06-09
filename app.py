import streamlit as st

from page_setting.config import setup_page
setup_page()

from streamlit_option_menu import option_menu
import streamlit_antd_components as sac
from itables import to_html_datatable
from page_setting.config import setup_page, colors, fields
from dashboard_menu.dashboard import show_dashboard_page
from dataset_menu.show_dataset import show_table
from dataset_menu.load_data import load_data
from beranda_menu.beranda import show_beranda_page
from classify_data.preprocessing_data import process_uploaded_data

def process_and_store_data():
    """
    Process uploaded data through preprocessing and classification pipeline
    """
    try:
        # Check if raw data exists in session state
        if 'uploaded_penelitian' in st.session_state and st.session_state.uploaded_penelitian is not None:
            with st.spinner('Processing Penelitian data...'):
                # Load raw data
                raw_penelitian = load_data(st.session_state.uploaded_penelitian)
                
                # Process through pipeline
                processed_penelitian = process_uploaded_data(
                    raw_penelitian, 
                    data_type='penelitian', 
                    title_column='Judul'
                )
                
                # Store processed data in session state
                st.session_state['processed_penelitian'] = processed_penelitian
                st.success("✅ Penelitian data processed successfully!")
        
        if 'uploaded_pengabdian' in st.session_state and st.session_state.uploaded_pengabdian is not None:
            with st.spinner('Processing Pengabdian Masyarakat data...'):
                # Load raw data
                raw_pengabdian = load_data(st.session_state.uploaded_pengabdian)
                
                # Process through pipeline
                processed_pengabdian = process_uploaded_data(
                    raw_pengabdian, 
                    data_type='pengabdian', 
                    title_column='Judul'
                )
                
                # Store processed data in session state
                st.session_state['processed_pengabdian'] = processed_pengabdian
                st.success("✅ Pengabdian Masyarakat data processed successfully!")
        
        # Mark data as processed
        st.session_state['data_processed'] = True
        
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        st.session_state['data_processed'] = False

# Sidebar
with st.sidebar:
    # Check if data has been uploaded and processed
    data_uploaded = st.session_state.get('data_uploaded', False)
    data_processed = st.session_state.get('data_processed', False)
    
    # Show processing status
    if data_uploaded and not data_processed:
        st.info("📊 Data uploaded but not processed yet")
        if st.button("🔄 Process Data", help="Click to preprocess and classify uploaded data"):
            process_and_store_data()
            st.rerun()
    elif data_processed:
        st.success("✅ Data processed and ready to use")
    
    main_menu = sac.menu(
        items=[
            sac.MenuItem('Menu', disabled=True),
            sac.MenuItem(type='divider'),
            sac.MenuItem('Beranda', icon='house-door'),
            sac.MenuItem('Dashboard', icon='speedometer2', disabled=not data_processed),
            sac.MenuItem('Dataset', icon='table', disabled=not data_processed, children=[
                sac.MenuItem('Klasifikasi Penelitian', icon='file-text', disabled=not data_processed),
                sac.MenuItem('Klasifikasi Pengabdian Masyarakat', icon='people', disabled=not data_processed)
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
    if st.session_state.get('data_processed', False):
        # Use processed data instead of raw data
        data_penelitian = st.session_state.get('processed_penelitian')
        data_pengmas = st.session_state.get('processed_pengabdian')
        
        if data_penelitian is not None or data_pengmas is not None:
            show_dashboard_page(fields, colors, data_penelitian, data_pengmas)
        else:
            st.warning("⚠️ No processed data available. Please upload and process data first.")
    else:
        st.warning("⚠️ Please upload and process data in the Beranda page first.")

elif main_menu == "Klasifikasi Penelitian":
    if st.session_state.get('data_processed', False):
        data_penelitian = st.session_state.get('processed_penelitian')
        
        if data_penelitian is not None:
            show_table(data_penelitian, "Penelitian")
        else:
            st.warning("⚠️ No Penelitian data available. Please upload and process data first.")
    else:
        st.warning("⚠️ Please upload and process data in the Beranda page first.")

elif main_menu == "Klasifikasi Pengabdian Masyarakat":
    if st.session_state.get('data_processed', False):
        data_pengmas = st.session_state.get('processed_pengabdian')
        
        if data_pengmas is not None:
            show_table(data_pengmas, "Pengabdian Masyarakat")
        else:
            st.warning("⚠️ No Pengabdian Masyarakat data available. Please upload and process data first.")
    else:
        st.warning("⚠️ Please upload and process data in the Beranda page first.")