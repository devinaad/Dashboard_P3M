import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from datetime import datetime
from itertools import islice
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
from streamlit_card import card
import streamlit.components.v1 as components
import plotly.express as px
import streamlit_antd_components as sac
from itables import to_html_datatable
from joblib import load  # Import load function for loading models
from streamlit.components.v1 import html
import datetime
import numpy as np
from dataset_menu.show_dataset import show_table
from dashboard_menu.classification_viz import create_donut_chart
from dashboard_menu.yearly_P3M import yearly_P3M_viz
from dashboard_menu.card import tampilkan_kartu_summary
from dashboard_menu.filter_dataset import filter_dataset_by_year
from clasify_menu.clasify_model import load_model_and_predict

# Membaca data dari file CSV
data_penelitian = pd.read_excel("E:/kuliah/Tugas Akhir/code/fix code/data_revisi/penelitian_categorized.xlsx")
data_pengmas = pd.read_excel("E:/kuliah/Tugas Akhir/code/fix code/fix_data/pengmas_categorized.xlsx",'Sheet1')

# Set page config
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Warna untuk kategori
colors = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
    "#FFA15A", "#19D3F3", "#FF6692"
]


# Custom CSS 
st.markdown("""
<style>
    /* Latar belakang utama */
    .main {
        background-color: #f8fafc;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: white;
        min-width: 250px !important;
        max-width: 0px !important;
    }

    /* Container untuk seluruh halaman */
    .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
    }

    /* Card untuk metrik */
    .metric-card {
        border-radius: 0.5rem;
        padding: 0.5rem; /* Diperbaiki agar lebih terlihat */
        margin: 0.5rem 0; /* Tambahkan margin agar tidak terlalu rapat */
        background-color: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    /* Warna khusus untuk metrik */
    .metric-card.blue {
        background-color: #dbeafe;
    }
    .metric-card.green {
        background-color: #dcfce7;
    }
    .metric-card.yellow {
        background-color: #fef9c3;
    }
        .metric-card.purple {
        background-color: #f3e8ff;
    }

    /* Nilai pada card metrik */
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        color: #1e293b;
    }

    /* Label pada card metrik */
    .metric-label {
        text-align: center;
        color: #475569;
        font-size: 1rem;
        margin-top: 0.25rem; /* Margin lebih proporsional */
    }

    /* Grid untuk card */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr); /* 4 kolom */
        gap: 0.7rem; /* Jarak antar card */
        padding: 1rem 0;
    }

    /* Plotly chart styling */
    .stPlotlyChart {
        outline: 10px solid #b8f9fc; /* Warna latar belakang plot */
        border-radius: 5px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.3);
    }

    /* Judul plot */
    .plot-title {
        color: black;
        text-align: center;
        padding: 5px;
        margin-bottom: 25px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>

    """, unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    main_menu = sac.menu(
        items=[
            sac.MenuItem('Menu', disabled=True),
            sac.MenuItem(type='divider'),
            sac.MenuItem('Dashboard', icon='house'),
            sac.MenuItem('Dataset', icon='table', children=[
                sac.MenuItem('Klasifikasi Penelitian', icon='file-text'),
                sac.MenuItem('Klasifikasi Pengabdian Masyarakat', icon='people')
            ]),
            sac.MenuItem('Klasifikasi Judul', icon='tag')
        ],
        size='lg',
        variant='filled', 
        color='indigo', 
        open_all=True
    )
# Main content
if main_menu == "Dashboard":
    st.markdown("<h1 style='text-align: center; color: #323b4f;'>Analytics Dashboard</h1>", unsafe_allow_html=True)

    filtered_penelitian, filtered_pengmas, label_tahun = filter_dataset_by_year(data_penelitian, data_pengmas)

    # Metrics Cards 
    # Data dummy untuk contoh
    total_penelitian = 664
    total_pengmas = 565
    top_penelitian = "Power & Energy System"
    top_pengmas = "Software Development"

    # Menampilkan Card summary data
    tampilkan_kartu_summary(total_penelitian, total_pengmas, top_penelitian, top_pengmas)

    #Visualisasi perbandingan jumlah penelitian dan pengabdian masyarakat per tahun
    yearly_P3M_viz(filtered_penelitian, filtered_pengmas)

    # Data untuk donut chart
    fields = [
        "Robotics and Mechatronics",
        "Telecommunications and Networking",
        "Power and Energy Systems",
        "Artificial Intelligence and Data Science",
        "Sensors and Embedded Systems",
        "Digital Media and Entertainment",
        "Software Development",
    ]
    values1 =  [103, 50, 115, 108, 113, 74, 98]
    values2 = [32, 42, 70, 38, 69, 82, 115]

    # Layout Streamlit
    col1, col2 = st.columns(2, gap="large")

    with col1:
        choose_ptm1 = st.selectbox(
            "Pilih Data",
            ["Penelitian", "Pengabdian Masyarakat"],
            key="ptm1"
        )

        if choose_ptm1 == "Penelitian":
            fig1 = create_donut_chart(fields, values1, "Kategori Data Penelitian P3M")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            fig2 = create_donut_chart(fields, values2, "Kategori Data Pengabdian Masyarakat P3M")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        choose_ptm2 = st.selectbox(
            "Pilih Data",
            ["Penelitian", "Pengabdian Masyarakat"],
            key="ptm2"
        )
        # Sample data for Penelitian (research)
        penelitian_data = {}
        years = list(range(2016, 2025))  # Last 10 years
        for category in fields:
            # Generate random funding data with an increasing trend
            base_value = np.random.randint(50, 200)
            trend = np.random.uniform(1.05, 1.15)  # Slight upward trend
            fluctuation = np.random.uniform(0.8, 1.2, size=len(years))
            values = [int(base_value * (trend ** i) * fluctuation[i]) for i in range(len(years))]
            penelitian_data[category] = values

        # Sample data for Pengabdian Masyarakat (community service)
        pengabdian_data = {}
        for category in fields:
            # Generate different random funding data with an increasing trend
            base_value = np.random.randint(30, 150)
            trend = np.random.uniform(1.03, 1.12)  # Slight upward trend
            fluctuation = np.random.uniform(0.85, 1.15, size=len(years))
            values = [int(base_value * (trend ** i) * fluctuation[i]) for i in range(len(years))]
            pengabdian_data[category] = values

        def create_plotly_stacked_bar(df, title):
            fig = go.Figure()
            
            # Define a colorful palette
            colors = [
                "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
                "#FFA15A", "#19D3F3", "#FF6692"
            ]
            
            # Add each category as a separate trace
            for i, category in enumerate(fields):
                fig.add_trace(go.Bar(
                    x=df.index,
                    y=df[category],
                    name=category,
                    marker_color=colors[i % len(colors)],
                    hovertemplate='%{y:,.0f} juta rupiah<extra></extra>'  # Hover text format
                ))
            
            # Update layout for better appearance
            fig.update_layout(
                title={
                    'text': f"Total Dana {title} per Kategori (2015-2024)",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 17}
                },
                xaxis_title="Tahun",
                yaxis_title="Dana (dalam Juta Rupiah)",
                barmode='stack',
                legend_title="Kategori",
                hovermode="closest",
                height=300,
                xaxis=dict(
                    tickmode='linear',
                    tickvals=years
                ),
                yaxis=dict(
                    tickformat=',d'
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=14
                )
            )
            
            return fig
        # Convert to DataFrames
        df_penelitian = pd.DataFrame(penelitian_data, index=years)
        df_pengabdian = pd.DataFrame(pengabdian_data, index=years)
        if choose_ptm2 == "Penelitian":
            fig_penelitian_fund = create_plotly_stacked_bar(df_penelitian, "Penelitian")
            st.plotly_chart(fig_penelitian_fund, use_container_width=True)
        else:
            fig_pengmas_fund = create_plotly_stacked_bar(df_pengabdian, "Pengabdian Masyarakat")
            st.plotly_chart(fig_pengmas_fund, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Membuat figure kosong
    fig = go.Figure()

    # Fungsi untuk menambahkan trace untuk legend
    def add_trace_to_legend(name, color):
        fig.add_trace(go.Scatter(
            x=[None],  # Tidak ada data, hanya legend
            y=[None],
            name=name,
            mode="lines",
            line=dict(color=color, width=4)  # Warna sesuai
        ))

    # Menambahkan traces untuk setiap field secara otomatis
    for field, color in zip(fields, colors):
        add_trace_to_legend(field, color)

    # Update layout untuk hanya menampilkan legend di tengah
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="middle",  # Vertikal center
            y=0.5,             # Posisi tengah secara vertikal
            xanchor="center",  # Horizontal center
            x=0.5,             # Posisi tengah secara horizontal
            font=dict(size=12)  # Ukuran font
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper
        xaxis=dict(visible=False),      # Hide x-axis
        yaxis=dict(visible=False),      # Hide y-axis
        margin=dict(l=0, r=0, t=0, b=0, pad=0),  # Remove margins
        height=100  # Adjust height as needed
    )

    # Menampilkan plot
    st.plotly_chart(fig,use_container_width=True)

elif main_menu == "Klasifikasi Penelitian":
    # st.markdown("<h2 style='text-align: center; color: #323b4f;'>Klasifikasi Penelitian</h1>", unsafe_allow_html=True)
    show_table(data_penelitian, "Penelitian")

elif main_menu == "Klasifikasi Pengabdian Masyarakat":
    # st.markdown("<h2 style='text-align: center; color: #323b4f;'>Klasifikasi Pengabdian Masyarakat</h1>", unsafe_allow_html=True)
    show_table(data_pengmas, "Pengabdian Masyarakat")

elif main_menu == "Klasifikasi Judul":
    st.markdown("<h1 style='text-align: center; color: #323b4f;'>Klasifikasi Judul</h1>", unsafe_allow_html=True)

    # Create tabs
    tab1, tab2 = st.tabs(["Manual Input", "File Upload"])

    # Tab 1: Manual Input
    with tab1:
        st.header("Manual Data Input")
        
        # Create form for manual input
        with st.form(key="manual_input_form"):
            # Form fields based on specified requirements
            judul = st.text_input("Judul (Judul Penelitian/Pengabdian) *")
            
            # Year selection
            current_year = datetime.datetime.now().year
            years = list(range(current_year-10, current_year+1))
            tahun = st.selectbox("Tahun *", years)
            
            # ketua = st.text_input("Ketua *")
            
            # # Multiline input for anggota
            # anggota = st.text_area("Anggota (Tulis satu anggota per baris jika lebih dari satu) *")
            
            # Jenis selection
            jenis = st.selectbox("Jenis *", ["Penelitian", "Pengabdian Masyarakat"])
            
            st.markdown("**Semua field harus diisi*")
            
            # Submit button
            submit_button = st.form_submit_button(label="Clasify")
        
        # Handle form submission
        if submit_button:
            # Validate all fields are filled
            if not judul:
                st.error("Judul harus diisi!")
            # elif not ketua:
            #     st.error("Ketua harus diisi!")
            # elif not anggota:
            #     st.error("Anggota harus diisi!")
            else:
                # # Process anggota - split by newline
                # anggota_list = [a.strip() for a in anggota.split('\n') if a.strip()]
                
                # if not anggota_list:
                #     st.error("Anggota harus diisi dengan benar!")
                # else:
                #     anggota_str = ', '.join(anggota_list)
                    
                    # Create DataFrame from inputs
                    data = {
                        "Judul": [judul],
                        "Tahun": [tahun],
                        # "Ketua": [ketua],
                        # "Anggota": [anggota_str],
                        "Jenis": [jenis]
                    }
                    

                    
                    # Show anggota as a list for clearer display
                    # if anggota_list:
                    #     st.subheader("Daftar Anggota:")
                    #     for i, ang in enumerate(anggota_list, 1):
                    #         st.write(f"{i}. {ang}")
                    
                    # CSS untuk mempercantik tampilan
                    st.markdown("""
                        <style>
                            .success-box {
                                background-color: #d4edda;
                                border-left: 5px solid #28a745;
                                padding: 1rem;
                                border-radius: 10px;
                                margin-bottom: 20px;
                            }
                            .section-header {
                                font-size: 24px;
                                font-weight: 600;
                                color: #2c3e50;
                                margin-top: 30px;
                                margin-bottom: 10px;
                            }
                            .result-box {
                                background-color: #f0f8ff;
                                border-left: 5px solid #1e90ff;
                                padding: 1rem;
                                border-radius: 10px;
                            }
                        </style>
                    """, unsafe_allow_html=True)

                    # Show the entered data
                    st.markdown('<div class="success-box">✅ <strong>Data berhasil disubmit!</strong></div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-header">📋 Data yang Dimasukkan</div>', unsafe_allow_html=True)
                    # st.dataframe(df)
                    st.markdown(f"""
                        <div class="result-box">
                            <strong>Judul:</strong> {judul}<br>
                            <strong>Jenis Data:</strong> {jenis}<br>
                            <strong>Tahun:</strong> {tahun}<br>
                        </div>
                    """, unsafe_allow_html=True)

                    # Clasify the title
                    if jenis == "Penelitian":
                        preds = load_model_and_predict(str(judul), model_path='rf_model_penelitian.joblib', vectorizer_path='tfidf_vectorizer_penelitian.joblib')
                        st.write(preds)

                    else:
                        # Load the model for Pengabdian Masyarakat
                        # model = load_model("path_to_pengmas_model")
                        # result = model.predict(df)
                        result = "Klasifikasi Pengabdian Masyarakat"

                    result = "Artificial Intelligence and Data Science"  # Dummy result for testing
                    st.markdown('<div class="section-header">📚 Hasil Klasifikasi</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-box"><strong>{result}</strong></div>', unsafe_allow_html=True)


    # Tab 2: File Upload
    with tab2:
        st.header("File Upload")
        
        # File type selection
        file_type = st.radio("Pilih Jenis File", ["CSV", "Excel"])
        
        # File uploader based on selected type
        if file_type == "CSV":
            uploaded_file = st.file_uploader("Pilih file CSV", type="csv")
        else:
            uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            # Read the file
            try:
                # Load the data based on file type
                if file_type == "CSV":
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Display file info
                st.subheader("Informasi File")
                st.write(f"Jumlah Baris: {df.shape[0]}, Jumlah Kolom: {df.shape[1]}")
                
                # Display data preview
                st.subheader("Preview Data")
                st.dataframe(df.head(5))
                
                # Column mapping
                st.subheader("Pemetaan Kolom")
                st.write("Pilih kolom dari file yang sesuai dengan field yang diperlukan:")
                
                # Get column names from the dataframe
                column_options = ["-- Pilih Kolom --"] + list(df.columns)
                
                # Create column mapping form
                with st.form(key="column_mapping_form"):
                    judul_col = st.selectbox("Kolom untuk Judul *", column_options)
                    tahun_col = st.selectbox("Kolom untuk Tahun *", column_options)
                    ketua_col = st.selectbox("Kolom untuk Ketua *", column_options)
                    anggota_col = st.selectbox("Kolom untuk Anggota *", column_options)
                    jenis_col = st.selectbox("Kolom untuk Jenis *", column_options)
                    
                    st.markdown("**Semua field harus dipilih*")
                    
                    map_button = st.form_submit_button(label="Proses Data")
                
                if map_button:
                    # Validate all fields are selected
                    if judul_col == "-- Pilih Kolom --" or tahun_col == "-- Pilih Kolom --" or ketua_col == "-- Pilih Kolom --" or anggota_col == "-- Pilih Kolom --" or jenis_col == "-- Pilih Data --":
                        st.error("Semua field harus dipilih!")
                    else:
                        # Create new dataframe with mapped columns
                        mapped_df = pd.DataFrame({
                            "Judul": df[judul_col],
                            "Tahun": df[tahun_col],
                            "Ketua": df[ketua_col],
                            "Anggota": df[anggota_col],
                            "Jenis": df[jenis_col]
                        })
                        
                        # Check for empty values
                        empty_values = False
                        for col in ["Judul", "Tahun", "Ketua", "Anggota", "Jenis"]:
                            if mapped_df[col].isna().any():
                                empty_values = True
                                st.warning(f"Kolom {col} memiliki nilai kosong. Semua nilai harus diisi.")
                        
                        if empty_values:
                            st.error("Data berisi nilai kosong. Semua field harus diisi.")
                        
                        # Display processed data
                        st.subheader("Data yang Dipetakan")
                        st.dataframe(mapped_df.head(10))
                        
                        # Basic statistics
                        st.subheader("Ringkasan Data")
                        
                        # Count by year
                        st.write("Jumlah Proyek per Tahun:")
                        year_counts = mapped_df["Tahun"].value_counts().sort_index()
                        st.bar_chart(year_counts)
                        
                        # Count by Jenis
                        st.write("Jumlah Proyek berdasarkan Jenis:")
                        jenis_counts = mapped_df["Jenis"].value_counts()                      
                        st.write(jenis_counts)
                        
                        # Data processing options
                        st.subheader("Pengolahan Data")
                        
                        # Example actions with the data
                        if st.button("Hapus Data Duplikat"):
                            original_count = mapped_df.shape[0]
                            mapped_df = mapped_df.drop_duplicates(subset=["Judul", "Tahun", "Ketua"])
                            new_count = mapped_df.shape[0]
                            st.write(f"Menghapus {original_count - new_count} baris duplikat.")
                            st.dataframe(mapped_df.head(10))
                        
                        # Download processed data
                        csv = mapped_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Data yang Telah Diolah (CSV)",
                            data=csv,
                            file_name="data_proyek_diolah.csv",
                            mime="text/csv"
                        )
                        
                        # # Also provide Excel download option
                        # buffer = io.BytesIO()
                        # with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        #     mapped_df.to_excel(writer, sheet_name='Sheet1', index=False)
                        
                        # st.download_button(
                        #     label="Download Data yang Telah Diolah (Excel)",
                        #     data=buffer.getvalue(),
                        #     file_name="data_proyek_diolah.xlsx",
                        #     mime="application/vnd.ms-excel"
                        # )
                        
            except Exception as e:
                st.error(f"Error: {e}")
                st.write("Pastikan file Anda diformat dengan benar.")
