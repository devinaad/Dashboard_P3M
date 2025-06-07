from datetime import datetime
import streamlit as st
from streamlit_date_picker import date_range_picker, PickerType

def filter_dataset_by_year(penelitian_df, pengmas_df, selected_year=None):
    # Ambil daftar tahun unik dari kedua dataset
    tahun_penelitian = penelitian_df['Tahun'].unique()
    tahun_pengmas = pengmas_df['Tahun'].unique()
    tahun_tersedia = sorted(set(tahun_penelitian).union(set(tahun_pengmas)))

    min_year = min(tahun_tersedia)
    max_year = max(tahun_tersedia)

    # Buat daftar tanggal 1 Jan tiap tahun yang tersedia (pastikan tahun >= 1970 untuk Windows)
    start_year = max(min_year, 1970)
    available_dates = [datetime(year, 1, 1) for year in range(start_year, max_year + 1)]

    # Default start-end untuk picker
    default_start = datetime(start_year, 1, 1)
    default_end = datetime(max_year, 1, 1)

    date_range_string = date_range_picker(
        picker_type=PickerType.year,
        start=default_start,
        end=default_end,
        key='year_range_picker',
        available_dates=available_dates
    )

    # Parsing nilai dari date_range_string menjadi tahun
    if date_range_string:
        start_dt, end_dt = date_range_string

        # Jika input berupa string tahun, konversi ke datetime dengan tanggal 1 Jan
        if isinstance(start_dt, str) and len(start_dt) == 4 and start_dt.isdigit():
            start_dt = datetime(int(start_dt), 1, 1)
        if isinstance(end_dt, str) and len(end_dt) == 4 and end_dt.isdigit():
            end_dt = datetime(int(end_dt), 1, 1)

        selected_year = list(range(start_dt.year, end_dt.year + 1))

    # Filter dataset berdasarkan tahun yang dipilih
    if not selected_year or 'All' in selected_year:
        filtered_penelitian = penelitian_df
        filtered_pengmas = pengmas_df
        label_tahun = "Semua Tahun"
    else:
        filtered_penelitian = penelitian_df[penelitian_df['Tahun'].isin(selected_year)]
        filtered_pengmas = pengmas_df[pengmas_df['Tahun'].isin(selected_year)]
        label_tahun = ", ".join(map(str, selected_year))

    return filtered_penelitian, filtered_pengmas, label_tahun
