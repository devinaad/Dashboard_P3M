import streamlit as st
import pandas as pd

def filter_dataset_by_year(penelitian_df, pengmas_df):
    # Ambil daftar tahun unik dari kedua dataset
    tahun_penelitian = penelitian_df['Tahun'].unique()
    tahun_pengmas = pengmas_df['Tahun'].unique()
    tahun_tersedia = sorted(set(tahun_penelitian).union(set(tahun_pengmas)))

    # Tambahkan opsi "All"
    opsi_tahun = ['All'] + tahun_tersedia

    # Pilihan tahun
    selected_year = st.multiselect(
        "🗓️ Pilih Tahun (bisa lebih dari satu):",
        opsi_tahun,
        default=['All']
    )

    # Filter berdasarkan pilihan
    if 'All' in selected_year or not selected_year:
        filtered_penelitian = penelitian_df
        filtered_pengmas = pengmas_df
        label_tahun = "Semua Tahun"
    else:
        filtered_penelitian = penelitian_df[penelitian_df['Tahun'].isin(selected_year)]
        filtered_pengmas = pengmas_df[pengmas_df['Tahun'].isin(selected_year)]
        label_tahun = ", ".join(map(str, selected_year))

    return filtered_penelitian, filtered_pengmas, label_tahun
