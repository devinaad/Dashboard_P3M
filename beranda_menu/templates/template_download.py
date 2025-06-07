import streamlit as st
import pandas as pd
import io

def show_template_download():
    st.markdown("---")
    st.markdown("#### 📥 Template Dataset")
    
    template_df = pd.DataFrame({
        "Judul": ["Contoh Judul Penelitian"],
        "Tahun": [2024],
        "Penulis": ["Nama Penulis"],
        "Dana": ["Dana"],
    })

    csv = template_df.to_csv(index=False)
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        template_df.to_excel(writer, sheet_name='Data Penelitian', index=False)
    excel_data = excel_buffer.getvalue()

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Download Template CSV", data=csv, file_name="template_data_penelitian.csv", mime="text/csv", use_container_width=True)
    with col2:
        st.download_button("📥 Download Template Excel", data=excel_data, file_name="template_data_penelitian.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
