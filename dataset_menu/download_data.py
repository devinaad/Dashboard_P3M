from itables import to_html_datatable
from streamlit.components.v1 import html
import pandas as pd
import streamlit as st
from dataset_menu.table_setting import get_datatable_options
from dataset_menu.table_css import custom_style
from io import BytesIO


def create_download_excel(dataframe, filename):
    """
    Create Excel file for download
    
    Args:
        dataframe: pandas DataFrame to convert
        filename: name for the downloaded file
    
    Returns:
        BytesIO object containing Excel data
    """
    # Create a BytesIO buffer (like a temporary file in memory)
    buffer = BytesIO()
    
    # Write DataFrame to Excel format in the buffer
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        dataframe.to_excel(writer, sheet_name='Data', index=False)
    
    # Reset buffer position to beginning
    buffer.seek(0)
    return buffer


def create_download_csv(dataframe):
    """
    Create CSV string for download
    
    Args:
        dataframe: pandas DataFrame to convert
    
    Returns:
        CSV string
    """
    # Convert DataFrame to CSV string
    return dataframe.to_csv(index=False)



# Optional: Helper function to add download options to any existing table
def add_download_section(dataframe, filename_prefix="data"):
    """
    Standalone function to add download buttons to any page
    
    Args:
        dataframe: pandas DataFrame to make downloadable
        filename_prefix: prefix for downloaded files
    """    
    st.markdown("###### 📥 Download Data")

    col1, col2 = st.columns([1, 1], gap="small")

    with col1:
        excel_buffer = create_download_excel(dataframe, f"{filename_prefix}.xlsx")
        st.download_button(
            label="📊 Excel",
            data=excel_buffer,
            file_name=f"{filename_prefix}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        csv_data = create_download_csv(dataframe)
        st.download_button(
            label="📄 CSV",
            data=csv_data,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv",
            use_container_width=True
        )