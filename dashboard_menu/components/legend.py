import streamlit as st
import plotly.graph_objects as go

def show_legend(fields, colors):     
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