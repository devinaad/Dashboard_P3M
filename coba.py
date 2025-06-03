import streamlit as st
import pandas as pd

# Load dataset
data_penelitian = pd.read_csv("E:/kuliah/Tugas Akhir/code/fix code/data/processed_penelitian.csv")
data_pengmas = pd.read_csv("E:/kuliah/Tugas Akhir/code/fix code/data/processed_pengmas.csv")

# Ambil daftar tahun unik dari kedua dataset
tahun_penelitian = data_penelitian['Tahun'].unique()
tahun_pengmas = data_pengmas['Tahun'].unique()
tahun_tersedia = sorted(set(tahun_penelitian).union(set(tahun_pengmas)))

# Tambahkan opsi "All"
opsi_tahun = ['All'] + tahun_tersedia

# Pilihan tahun dari sidebar atau main area
selected_year = st.multiselect(
    "🗓️ Pilih Tahun (bisa lebih dari satu):",
    opsi_tahun,
    default=['All']
)

# Tentukan apakah semua tahun dipilih
if 'All' in selected_year:
    filtered_penelitian = data_penelitian
    filtered_pengmas = data_pengmas
    label_tahun = "Semua Tahun"
else:
    filtered_penelitian = data_penelitian[data_penelitian['Tahun'].isin(selected_year)]
    filtered_pengmas = data_pengmas[data_pengmas['Tahun'].isin(selected_year)]
    label_tahun = ", ".join(map(str, selected_year))

# Tampilkan hasil filter
st.subheader(f"📊 Data Penelitian Tahun {label_tahun}")
st.dataframe(filtered_penelitian)

st.subheader(f"📊 Data Pengmas Tahun {label_tahun}")
st.dataframe(filtered_pengmas)


import hydralit_components as hc
import time

# a dedicated single loader 
# with hc.HyLoader('Now doing loading',hc.Loaders.pulse_bars):
#     time.sleep(5)

# for 3 loaders from the standard loader group
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[3,0,5]):
#     time.sleep(5)

# for 1 (index=5) from the standard loader group
with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=5):
    time.sleep(5)

# # for 4 replications of the same loader (index=2) from the standard loader group
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[2,2,2,2]):
#     time.sleep(5)