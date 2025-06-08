import streamlit as st

def show_upload_section():
    st.markdown("## 📤 Upload Dataset")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""<div class="upload-container"><h4>🔬 Data Penelitian</h3></div>""", unsafe_allow_html=True)
        uploaded_penelitian = st.file_uploader("Pilih file data penelitian", type=['csv', 'xlsx'], key="penelitian")

    with col2:
        st.markdown("""<div class="upload-container"><h4>🤝 Data Pengabdian Masyarakat</h3></div>""", unsafe_allow_html=True)
        uploaded_pengabdian = st.file_uploader("Pilih file data pengabdian masyarakat", type=['csv', 'xlsx'], key="pengabdian")

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    submit_upload = False

    with col2:
        if uploaded_penelitian and uploaded_pengabdian:
            st.success("✅ Kedua dataset sudah dipilih!")
            submit_upload = st.button("🚀 Submit & Proses Data", type="primary", use_container_width=True)
        else:
            st.warning("⚠️ Silakan upload kedua dataset terlebih dahulu!")
    
    return uploaded_penelitian, uploaded_pengabdian, submit_upload
