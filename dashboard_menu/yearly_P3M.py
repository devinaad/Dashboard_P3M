import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Fungsi menghitung jumlah penelitian per tahun
def hitung_penelitian_per_tahun(data_penelitian):
    penelitian_count = data_penelitian["Tahun"].value_counts().reset_index()
    penelitian_count.columns = ["Tahun", "Jumlah Penelitian"]
    return penelitian_count.sort_values("Tahun")

# Fungsi menghitung jumlah pengabdian masyarakat per tahun
def hitung_pengmas_per_tahun(data_pengmas):
    pengmas_count = data_pengmas["Tahun"].value_counts().reset_index()
    pengmas_count.columns = ["Tahun", "Jumlah Pengmas"]
    return pengmas_count.sort_values("Tahun")

# Fungsi menggabungkan data penelitian dan pengmas
def gabungkan_data(penelitian_count, pengmas_count):
    combined_data = pd.merge(
        penelitian_count,
        pengmas_count,
        on="Tahun",
        how="outer"
    ).fillna(0)
    combined_data["Tahun"] = combined_data["Tahun"].astype(str)
    return combined_data

# Fungsi untuk membuat visualisasi menggunakan Plotly
def buat_plot(combined_data):
    fig = go.Figure()

    # Bar untuk Penelitian
    fig.add_trace(go.Bar(
        x=combined_data["Tahun"],
        y=combined_data["Jumlah Penelitian"],
        name="Penelitian",
        marker_color="#636EFA"
    ))

    # Bar untuk Pengmas
    fig.add_trace(go.Bar(
        x=combined_data["Tahun"],
        y=combined_data["Jumlah Pengmas"],
        name="Pengabdian Masyarakat",
        marker_color="#00CC96"
    ))

    # Garis rata-rata
    avg_penelitian = round(combined_data["Jumlah Penelitian"].mean())
    avg_pengmas = round(combined_data["Jumlah Pengmas"].mean())

    fig.add_trace(go.Scatter(
        x=combined_data["Tahun"],
        y=[avg_penelitian] * len(combined_data["Tahun"]),
        name=f"Rata-rata Penelitian ({avg_penelitian:.1f})",
        mode="lines",
        line=dict(color="#636EFA", width=2, dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=combined_data["Tahun"],
        y=[avg_pengmas] * len(combined_data["Tahun"]),
        name=f"Rata-rata Pengmas ({avg_pengmas:.1f})",
        mode="lines",
        line=dict(color="#00CC96", width=2, dash="dash")
    ))

    # Update layout
    fig.update_layout(
        title={"text": "Distribusi Penelitian dan Pengabdian Masyarakat per Tahun",
               "y": 0.95, "x": 0.5, "xanchor": "center", "yanchor": "top"},
        xaxis_title="Tahun",
        yaxis_title="Jumlah",
        barmode="group",
        legend=dict(
            title="Kategori",
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=20, r=20, t=50, b=50),
        height=300
    )

    return fig

# Fungsi utama yang menjalankan semua langkah
def yearly_P3M_viz(data_penelitian, data_pengmas):
    penelitian_count = hitung_penelitian_per_tahun(data_penelitian)
    pengmas_count = hitung_pengmas_per_tahun(data_pengmas)
    combined_data = gabungkan_data(penelitian_count, pengmas_count)
    fig = buat_plot(combined_data)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
