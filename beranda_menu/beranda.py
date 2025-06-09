import streamlit as st
from beranda_menu.components.header import show_header
from beranda_menu.components.features import show_features
from beranda_menu.components.upload_section import show_upload_section
from beranda_menu.sections.preview_data import show_data_preview
from beranda_menu.sections.next_steps import show_next_steps
from beranda_menu.templates.template_download import show_template_download


def show_beranda_page(): 
    show_header() 
    show_features() 
     
    # Check if data is already uploaded 
    if st.session_state.get('data_uploaded', False): 
        # Show data processing section
        show_data_processing_section() 
        
        # Only show next steps if data is processed
        if st.session_state.get('data_processed', False):
            show_next_steps()
         
    else: 
        uploaded_penelitian, uploaded_pengabdian, submit_upload = show_upload_section() 
        if uploaded_penelitian and uploaded_pengabdian and submit_upload: 
            st.session_state['data_uploaded'] = True 
            st.session_state['uploaded_penelitian'] = uploaded_penelitian 
            st.session_state['uploaded_pengabdian'] = uploaded_pengabdian 
            # Reset processing status when new data is uploaded 
            st.session_state['data_processed'] = False 
            st.rerun() 
        else: 
            show_template_download()

def show_data_processing_section():
    """
    New section for data processing integration
    """    
    # Check processing status
    data_processed = st.session_state.get('data_processed', False)
    
    if not data_processed:
        st.subheader("🔄 Data Processing Required")
        
        # Show processing status
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info("📊 Your data needs to be preprocessed and classified before use in Dashboard and Dataset pages.")
            st.write("**What will happen during processing:**")
            st.write("• Text cleaning and preprocessing")
            st.write("• Automatic classification of research fields")
            st.write("• Data preparation for visualization")
        
        with col2:
            st.metric("Status", "⏳ Pending", delta="Not Processed")
        
        # Processing button
        if st.button("🚀 Start Data Processing", type="primary", use_container_width=True):
            process_data_pipeline()
    
    else:
        st.subheader("✅ Data Processing Complete")
        
        # Show processing results
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.success("🎉 Your data has been successfully processed and is ready to use!")
            
            # Show processing results summary
            if 'processed_penelitian' in st.session_state:
                df_penelitian = st.session_state['processed_penelitian']
                st.write(f"**📚 Penelitian Data:** {len(df_penelitian)} records processed")
                if 'Bidang Penelitian' in df_penelitian.columns:
                    unique_bidang = df_penelitian['Bidang Penelitian'].nunique()
                    st.write(f"   → {unique_bidang} unique research fields identified")
            
            if 'processed_pengabdian' in st.session_state:
                df_pengabdian = st.session_state['processed_pengabdian']
                st.write(f"**🤝 Pengabdian Data:** {len(df_pengabdian)} records processed")
                if 'Bidang Pengabdian Masyarakat' in df_pengabdian.columns:
                    unique_bidang = df_pengabdian['Bidang Pengabdian Masyarakat'].nunique()
                    st.write(f"   → {unique_bidang} unique service fields identified")
        
        with col2:
            st.metric("Status", "✅ Ready", delta="Processed")
        
        # Option to reprocess
        with st.expander("🔄 Reprocess Data"):
            st.write("Click below if you want to reprocess your data with updated settings.")
            if st.button("🔄 Reprocess Data", key="reprocess"):
                st.session_state['data_processed'] = False
                st.rerun()

def process_data_pipeline():
    """
    Execute the complete data processing pipeline
    """
    try:
        # Import processing functions
        from classify_data.preprocessing_data import process_uploaded_data
        from dataset_menu.load_data import load_data
        
        # Create progress tracking
        progress_container = st.container()
        
        with progress_container:
            # Create progress bar and status
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_steps = 0
            current_step = 0
            
            # Count steps
            if 'uploaded_penelitian' in st.session_state and st.session_state.uploaded_penelitian is not None:
                total_steps += 1
            if 'uploaded_pengabdian' in st.session_state and st.session_state.uploaded_pengabdian is not None:
                total_steps += 1
            
            # Process Penelitian data
            if 'uploaded_penelitian' in st.session_state and st.session_state.uploaded_penelitian is not None:
                current_step += 1
                status_text.text(f'🔄 Processing Penelitian data... ({current_step}/{total_steps})')
                
                # Load raw data
                raw_penelitian = load_data(st.session_state.uploaded_penelitian)
                progress_bar.progress(current_step / total_steps * 0.5)
                
                # Process through pipeline
                processed_penelitian = process_uploaded_data(
                    raw_penelitian, 
                    data_type='penelitian', 
                    title_column='Judul'
                )
                
                # Store processed data
                st.session_state['processed_penelitian'] = processed_penelitian
                progress_bar.progress(current_step / total_steps * 0.75)
                
                # Show success for this dataset
                st.success(f"✅ Penelitian data processed: {len(processed_penelitian)} records")
            
            # Process Pengabdian data
            if 'uploaded_pengabdian' in st.session_state and st.session_state.uploaded_pengabdian is not None:
                current_step += 1
                status_text.text(f'🔄 Processing Pengabdian Masyarakat data... ({current_step}/{total_steps})')
                
                # Load raw data
                raw_pengabdian = load_data(st.session_state.uploaded_pengabdian)
                
                # Process through pipeline
                processed_pengabdian = process_uploaded_data(
                    raw_pengabdian, 
                    data_type='pengabdian', 
                    title_column='Judul'
                )
                
                # Store processed data
                st.session_state['processed_pengabdian'] = processed_pengabdian
                
                # Show success for this dataset
                st.success(f"✅ Pengabdian Masyarakat data processed: {len(processed_pengabdian)} records")
            
            # Complete processing
            progress_bar.progress(1.0)
            status_text.text('🎉 Processing completed successfully!')
            
            # Mark as processed
            st.session_state['data_processed'] = True
            
            # Show celebration
            st.balloons()
            
            # Auto-refresh to update UI
            st.rerun()
        
    except ImportError as e:
        st.error(f"❌ Missing required modules: {str(e)}")
        st.info("💡 Make sure all processing modules are properly installed and configured.")
        
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        st.info("💡 Please check your data format and try again. If the problem persists, contact support.")
        
        # Reset processing status on error
        st.session_state['data_processed'] = False

def show_processing_status_sidebar():
    """
    Helper function to show processing status in sidebar (call this from app.py if needed)
    """
    data_uploaded = st.session_state.get('data_uploaded', False)
    data_processed = st.session_state.get('data_processed', False)
    
    if data_uploaded and not data_processed:
        st.sidebar.warning("⚠️ Data uploaded but not processed")
        st.sidebar.info("👆 Go to Beranda to process your data")
    elif data_processed:
        st.sidebar.success("✅ Data ready for analysis")
    else:
        st.sidebar.info("📤 Upload data in Beranda first")

show_beranda_page()