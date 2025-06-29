import streamlit as st
import pandas as pd
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
        
        # # Only show next steps if data is processed
        # if st.session_state.get('data_processed', False):
        #     show_next_steps()
         
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
        st.subheader("🔄 Pemrosesan Data Diperlukan")
        
        # Show processing status
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info("📊 Data Anda perlu diproses dan diklasifikasikan sebelum digunakan di halaman Dasbor dan Dataset.")
            st.write("**Langkah-langkah selama pemrosesan:**")
            st.write("• Pembersihan dan pra-pemrosesan teks")
            st.write("• Klasifikasi otomatis bidang penelitian")
            st.write("• Persiapan data untuk visualisasi")
        
        with col2:
            st.metric("Status", "⏳ Menunggu", delta="Belum Diproses")
        
        # Processing button with unique key
        if st.button(
            "🚀 Mulai Pemrosesan Data", 
            type="primary", 
            use_container_width=True,
            key="process_data_beranda"
        ):
            process_data_pipeline()
            st.rerun()
    
    else:
        st.subheader("✅ Pemrosesan Data Selesai")
        
        # Show processing results
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.success("🎉 Data Anda berhasil diproses dan siap digunakan!")
            
            # Show processing results summary
            if 'processed_penelitian' in st.session_state:
                df_penelitian = st.session_state['processed_penelitian']
                st.write(f"**📚 Data Penelitian:** {len(df_penelitian)} entri telah diproses")
                if 'Bidang Penelitian' in df_penelitian.columns:
                    unique_bidang = df_penelitian['Bidang Penelitian'].nunique()
                    st.write(f"   → {unique_bidang} bidang penelitian unik teridentifikasi")
            
            if 'processed_pengabdian' in st.session_state:
                df_pengabdian = st.session_state['processed_pengabdian']
                st.write(f"**🤝 Data Pengabdian:** {len(df_pengabdian)} entri telah diproses")
                if 'Bidang Pengabdian Masyarakat' in df_pengabdian.columns:
                    unique_bidang = df_pengabdian['Bidang Pengabdian Masyarakat'].nunique()
                    st.write(f"   → {unique_bidang} bidang pengabdian unik teridentifikasi")
        
        with col2:
            st.metric("Status", "✅ Siap", delta="Sudah Diproses")
        
        with st.expander("🔄 Proses Ulang Data"):
            st.write("Klik tombol di bawah jika Anda ingin memproses ulang data dengan pengaturan terbaru.")
            if st.button("🔄 Proses Ulang Data", key="reprocess_data_beranda"):
                st.session_state['data_processed'] = False
                st.rerun()

def process_data_pipeline():
    """
    Execute the complete data processing pipeline
    """
    try:
        # Import processing functions
        from dataset_menu.load_data import load_data
        from classify_data.preprocessing_data import process_uploaded_data
        
        # Read dosen data - Add error handling for file reading
        try:
            dosen_prodi = pd.read_excel('classify_data/dosen_prodi.xlsx')
        except FileNotFoundError:
            st.error("❌ Kesalahan: File dosen_prodi.xlsx tidak ditemukan")
            return
        except Exception as e:
            st.error(f"❌ Gagal membaca data dosen: {str(e)}")
            return
        
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
                status_text.text(f'🔄 Memproses data Penelitian... ({current_step}/{total_steps})')
                
                try:
                    # Load raw data
                    raw_penelitian = load_data(st.session_state.uploaded_penelitian)
                    progress_bar.progress(current_step / total_steps * 0.5)
                    
                    # Process through pipeline - Use the correct function signature
                    processed_penelitian = process_uploaded_data(
                        raw_penelitian,         # First positional argument: raw data
                        dosen_prodi,           # Second positional argument: dosen dataframe
                        data_type='penelitian', # Keyword argument
                        title_column='Judul'    # Keyword argument
                    )
                    
                    # Store processed data
                    st.session_state['processed_penelitian'] = processed_penelitian
                    progress_bar.progress(current_step / total_steps * 0.75)
                    
                    # Show success for this dataset
                    st.success(f"✅ Data Penelitian berhasil diproses: {len(processed_penelitian)} entri")
                    
                except Exception as e:
                    st.error(f"❌ Gagal memproses data Penelitian: {str(e)}")
                    return
            
            # Process Pengabdian data
            if 'uploaded_pengabdian' in st.session_state and st.session_state.uploaded_pengabdian is not None:
                current_step += 1
                status_text.text(f'🔄 Memproses data Pengabdian Masyarakat... ({current_step}/{total_steps})')
                
                try:
                    # Load raw data
                    raw_pengabdian = load_data(st.session_state.uploaded_pengabdian)
                    
                    # Process through pipeline - Use the correct function signature
                    processed_pengabdian = process_uploaded_data(
                        raw_pengabdian,         # First positional argument: raw data
                        dosen_prodi,           # Second positional argument: dosen dataframe
                        data_type='pengabdian', # Keyword argument
                        title_column='Judul'    # Keyword argument
                    )
                    
                    # Store processed data
                    st.session_state['processed_pengabdian'] = processed_pengabdian
                    
                    # Show success for this dataset
                    st.success(f"✅ Data Pengabdian berhasil diproses: {len(processed_pengabdian)} entri")
                    
                except Exception as e:
                    st.error(f"❌ Gagal memproses data Pengabdian: {str(e)}")
                    return
            
            # Complete processing
            progress_bar.progress(1.0)
            status_text.text('🎉 Pemrosesan selesai dengan sukses!')
            
            # Mark as processed
            st.session_state['data_processed'] = True
            
            # Show celebration
            st.balloons()
        
    except ImportError as e:
        st.error(f"❌ Modul yang dibutuhkan tidak ditemukan: {str(e)}")
        st.info("💡 Pastikan semua modul sudah terinstal dan dikonfigurasi dengan benar.")
        
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses data: {str(e)}")
        st.info("💡 Periksa format data Anda dan coba lagi. Jika masalah terus berlanjut, hubungi tim bantuan.")
        st.session_state['data_processed'] = False

def show_processing_status_sidebar():
    """
    Helper function to show processing status in sidebar (call this from app.py if needed)
    """
    data_uploaded = st.session_state.get('data_uploaded', False)
    data_processed = st.session_state.get('data_processed', False)
    
    if data_uploaded and not data_processed:
        st.sidebar.warning("⚠️ Data sudah diunggah namun belum diproses")
        st.sidebar.info("👆 Kembali ke halaman Beranda untuk memproses data")
    elif data_processed:
        st.sidebar.success("✅ Data siap untuk dianalisis")
    else:
        st.sidebar.info("📤 Unggah data terlebih dahulu di halaman Beranda")