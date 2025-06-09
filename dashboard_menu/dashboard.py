import streamlit as st
from dashboard_menu.components.card import tampilkan_kartu_summary
from dashboard_menu.filter_dataset import filter_dataset_by_year
from dashboard_menu.components.classification_viz import create_donut_chart
from dashboard_menu.components.yearly_P3M import yearly_P3M_viz
from dashboard_menu.components.legend import show_legend
from dashboard_menu.components.fund_viz import show_fund_viz
from dashboard_menu.data_processing.data_processor import DataProcessor

def show_dashboard_page(fields, colors, data_penelitian, data_pengabdian):
    """
    Menampilkan halaman dashboard utama
    
    Parameters:
        fields (list): List kategori data
        colors (list): List warna untuk visualisasi
        data_penelitian (pd.DataFrame): Data penelitian
        data_pengabdian (pd.DataFrame): Data pengabdian masyarakat
    """
    
    st.markdown("<h1 style='text-align: center; color: #323b4f;'>Analytics Dashboard</h1>", unsafe_allow_html=True)

    # Filter dataset berdasarkan tahun
    filtered_penelitian, filtered_pengmas, label_tahun = filter_dataset_by_year(
        data_penelitian, data_pengabdian
    )
    
        # Tampilkan informasi filter
    if label_tahun != "Semua Tahun":
        st.info(f"📊 Data yang ditampilkan: {label_tahun}")
    else:
        st.info("📊 Menampilkan semua data yang tersedia")

    # Inisialisasi data processor
    processor = DataProcessor(data_penelitian, data_pengabdian, fields)
    
    # Proses semua data yang diperlukan
    processed_data = processor.process_all_data(filtered_penelitian, filtered_pengmas)
    
    # Extract processed data
    total_penelitian = processed_data['total_penelitian']
    total_pengmas = processed_data['total_pengmas']
    top_penelitian = processed_data['top_penelitian']
    top_pengmas = processed_data['top_pengmas']
    penelitian_values = processed_data['penelitian_values']
    pengmas_values = processed_data['pengmas_values']
    penelitian_fund_df = processed_data['penelitian_fund_df']
    pengmas_fund_df = processed_data['pengmas_fund_df']

    # Menampilkan Card summary data
    tampilkan_kartu_summary(total_penelitian, total_pengmas, top_penelitian, top_pengmas) 

    # Visualisasi perbandingan jumlah penelitian dan pengabdian masyarakat per tahun
    st.markdown("<br>", unsafe_allow_html=True)
    yearly_P3M_viz(filtered_penelitian, filtered_pengmas)

    # Layout Streamlit untuk donut charts dan fund visualization
    col1, col2 = st.columns(2, gap="large")

    with col1:
        choose_ptm1 = st.selectbox(
            "Pilih Data",
            ["Penelitian", "Pengabdian Masyarakat"],
            key="ptm1"
        )

        if choose_ptm1 == "Penelitian":
            fig1 = create_donut_chart(fields, penelitian_values, "Kategori Data Penelitian P3M", colors)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            fig2 = create_donut_chart(fields, pengmas_values, "Kategori Data Pengabdian Masyarakat P3M", colors)
            st.plotly_chart(fig2, use_container_width=True)

    with col2:
        choose_ptm2 = st.selectbox(
            "Pilih Data",
            ["Penelitian", "Pengabdian Masyarakat"],
            key="ptm2"
        )

        if choose_ptm2 == "Penelitian":
            fig_penelitian_fund = show_fund_viz(
                penelitian_fund_df, "Penelitian", colors, fields
            )
            st.plotly_chart(fig_penelitian_fund, use_container_width=True)
        else:
            fig_pengmas_fund = show_fund_viz(
                pengmas_fund_df, "Pengabdian Masyarakat", colors, fields
            )
            st.plotly_chart(fig_pengmas_fund, use_container_width=True)
            
    st.markdown("<br>", unsafe_allow_html=True)

    # Tampilkan legend
    show_legend(fields, colors)
    

