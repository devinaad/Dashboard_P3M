import streamlit as st
from components.card import tampilkan_kartu_summary
from filter_dataset import filter_dataset_by_year
from components.classification_viz import create_donut_chart
from components.yearly_P3M import yearly_P3M_viz
from components.legend import show_legend

def show_dashboard_page(fields, colors, data_penelitian, data_pengabdian):


        st.markdown("<h1 style='text-align: center; color: #323b4f;'>Analytics Dashboard</h1>", unsafe_allow_html=True)

        filtered_penelitian, filtered_pengmas, label_tahun = filter_dataset_by_year(
            data_penelitian, data_pengabdian
        )

        # Menampilkan Card summary data
        tampilkan_kartu_summary(total_penelitian, total_pengmas, top_penelitian, top_pengmas) 

        #Visualisasi perbandingan jumlah penelitian dan pengabdian masyarakat per tahun
        yearly_P3M_viz(filtered_penelitian, filtered_pengmas)

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

 
            if choose_ptm2 == "Penelitian":
                fig_penelitian_fund = create_plotly_stacked_bar(data_penelitian, "Penelitian")
                st.plotly_chart(fig_penelitian_fund, use_container_width=True)
            else:
                fig_pengmas_fund = create_plotly_stacked_bar(data_pengabdian, "Pengabdian Masyarakat")
                st.plotly_chart(fig_pengmas_fund, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        show_legend(fields, colors)
