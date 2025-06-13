from itables import to_html_datatable
from streamlit.components.v1 import html
import pandas as pd
import streamlit as st
from dataset_menu.table_setting import get_datatable_options
from dataset_menu.table_css import custom_style
from dataset_menu.download_data import add_download_section

def format_currency(value):
    """
    Format angka menjadi format mata uang Indonesia
    Contoh: 1000000 -> "Rp 1.000.000"
    """
    try:
        # Coba konversi ke float jika value adalah string
        if isinstance(value, str):
            # Hapus karakter non-digit kecuali titik dan koma
            cleaned_value = ''.join(c for c in value if c.isdigit() or c in '.,')
            if not cleaned_value:
                return value  # Return original jika tidak ada angka
            # Ganti koma dengan titik untuk konversi float
            cleaned_value = cleaned_value.replace(',', '.')
            num = float(cleaned_value)
        else:
            num = float(value)
        
        # Format dengan pemisah ribuan menggunakan titik
        formatted = f"{num:,.0f}".replace(',', '.')
        return f"Rp {formatted}"
    
    except (ValueError, TypeError):
        # Jika tidak bisa dikonversi, return value asli
        return value

def format_dataframe_currency(df, currency_columns=None):
    """
    Format kolom-kolom currency dalam DataFrame
    
    Parameters:
    df: DataFrame yang akan diformat
    currency_columns: list nama kolom yang ingin diformat sebagai currency
                     Jika None, akan otomatis detect kolom "dana disetujui"
    
    Returns:
    DataFrame dengan kolom currency yang sudah diformat
    """
    # Buat copy DataFrame agar tidak mengubah original
    df_formatted = df.copy()
    
    # Jika currency_columns tidak dispesifikasi, cari otomatis
    if currency_columns is None:
        currency_columns = []
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['dana disetujui', 'dana', 'budget', 'anggaran', 'biaya']):
                currency_columns.append(col)
    
    # Format setiap kolom currency
    for col in currency_columns:
        if col in df_formatted.columns:
            df_formatted[col] = df_formatted[col].apply(format_currency)
    
    return df_formatted

def show_table(dataframe, dataframe_name):
    st.markdown(f"<h2 class='title-gradient'>Klasifikasi {dataframe_name}</h1>", unsafe_allow_html=True)

    # Format currency columns SEBELUM ditampilkan
    dataframe_formatted = format_dataframe_currency(dataframe)
    
    add_download_section(dataframe, filename_prefix="data"+dataframe_name)
    
    # Get dynamic datatable options based on the dataframe
    datatable_options = get_datatable_options(dataframe_formatted)

    # Combine custom style with datatable
    table_html = custom_style + to_html_datatable(
        dataframe_formatted,  # Gunakan dataframe yang sudah diformat
        classes="display",
        options=datatable_options
    )
    return html(table_html, height=1000, scrolling=True)