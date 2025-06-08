import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def show_fund_viz(df, title, colors, fields):
    """
    Membuat stacked bar chart untuk visualisasi dana per kategori dan tahun
    
    Parameters:
        df (pd.DataFrame): DataFrame dengan tahun sebagai index dan kategori sebagai kolom
        title (str): Judul untuk chart
        colors (list): List warna untuk setiap kategori
        fields (list): List nama kategori
    
    Returns:
        fig: Plotly Figure object
    """
    
    if df.empty:
        # Jika tidak ada data, buat chart kosong
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data untuk ditampilkan",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=f"Total Dana {title} per Kategori",
            height=300,
            showlegend=False
        )
        return fig
    
    fig = go.Figure()
    
    # Add each category as a separate trace
    for i, category in enumerate(fields):
        if category in df.columns:
            fig.add_trace(go.Bar(
                x=df.index,
                y=df[category],
                name=category,
                marker_color=colors[i % len(colors)],
                hovertemplate=f'<b>{category}</b><br>Tahun: %{{x}}<br>Dana: %{{y:,.0f}} juta rupiah<extra></extra>'
            ))
    
    # Hitung total per tahun (bar)
    if not df.empty:
        totals = df[fields].sum(axis=1)
        
        # Tambahkan trace untuk menampilkan total di atas bar
        fig.add_trace(go.Scatter(
            x=df.index,
            y=totals,
            mode='text',
            text=[f"{val:,.0f}" for val in totals],
            textposition='top center',
            showlegend=False,
            textfont=dict(size=10, color='black'),
            hoverinfo='skip'
        ))
    
    # Update layout for better appearance
    fig.update_layout(
        title={
            'text': f"Total Dana {title} per Kategori",
            'y': 0.95,
            'x': 0.5,
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
            tickvals=list(df.index) if not df.empty else []
        ),
        yaxis=dict(
            tickformat=',d'
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14
        ),
        margin=dict(l=10, r=10, t=40, b=5),
    )
    
    return fig