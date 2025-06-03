import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def create_donut_chart(fields, values, title, colors=None):
    """
    Membuat donut chart menggunakan Plotly dengan hanya menampilkan persentase di dalamnya.
    
    Parameters:
        fields (list): Nama kategori dalam chart.
        values (list): Nilai kategori.
        title (str): Judul chart.
        colors (list, optional): Daftar warna untuk setiap kategori.
        
    Returns:
        fig: Objek Plotly Figure.
    """
    # Warna default jika tidak diberikan
    if colors is None:
        colors = [
            "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
            "#FFA15A", "#19D3F3", "#FF6692"
        ]
    
    # Membuat donut chart
    fig = go.Figure(data=[
          go.Pie(
            labels=fields,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo="percent",
            textposition="inside",
            textfont=dict(
                size=13,  # Ukuran font (bisa disesuaikan)
                weight='bold',  # Membuat teks menjadi bold
                color = 'black'
            )
        )
    ])

    
    # Update layout untuk judul
    fig.update_layout(
        width=100, 
        height=300,
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top"
        },
        margin=dict(l=10, r=10,t=40, b=5),  # Margin bawah kecil karena legend dipisah
        showlegend=False,  # Sembunyikan legend bawaan Plotly
    )
    
    return fig