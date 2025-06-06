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

# Membaca data dari file CSV
data_penelitian = pd.read_excel("E:/kuliah/Tugas Akhir/code/fix code/data_revisi/penelitian_categorized.xlsx")
data_pengmas = pd.read_excel("E:/kuliah/Tugas Akhir/code/fix code/fix_data/pengmas_categorized.xlsx",'Sheet1')

# Set page config
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",  # Biarkan "wide" untuk tampilan luas
    initial_sidebar_state="expanded"  # Sidebar tetap muncul
)

# Warna untuk kategori
colors = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
    "#FFA15A", "#19D3F3", "#FF6692"
]

# Custom CSS - versi default dinamis
st.markdown("""
<style>
    /* Latar belakang utama */
    .main {
        background-color: #f8fafc;
    }

    /* Sidebar default, tidak dikunci */
    [data-testid="stSidebar"] {
        background-color: white;
    }

    /* Container halaman tanpa pembatas max-width */
    .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Card metrik */
    .metric-card {
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 0.5rem 0;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

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

    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        color: #1e293b;
    }

    .metric-label {
        text-align: center;
        color: #475569;
        font-size: 1rem;
        margin-top: 0.25rem;
    }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.7rem;
        padding: 1rem 0;
    }

    .stPlotlyChart {
        outline: 10px solid #b8f9fc;
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2), 0 6px 20px rgba(0,0,0,0.3);
    }

    .plot-title {
        color: black;
        text-align: center;
        padding: 5px;
        margin-bottom: 25px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


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
        open_all=True,
        index=2
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
                    hovertemplate='<b>%{fullData.name}</b><br>%{y:,.0f} juta rupiah<extra></extra>'
                ))
            
            # Hitung total per tahun (bar)
            totals = df[fields].sum(axis=1)

            # Tambahkan trace untuk menampilkan total di atas bar
            fig.add_trace(go.Scatter(
                x=df.index,
                y=totals,
                mode='text',
                text=[f"{val:,.0f} juta" for val in totals],
                textposition='top center',
                showlegend=False,
                textfont=dict(size=12, color='black')
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
                showlegend=False, 
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
                ),
                margin=dict(l=10, r=10,t=40, b=5),  # Margin bawah kecil karena legend dipisah

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

