import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Main title
st.title("Visualisasi Dana Penelitian dan Pengabdian Masyarakat")
st.subheader("Data 10 Tahun Terakhir (2016-2024)")

def create_plotly_stacked_bar(df, title, colors, fields):
    fig = go.Figure()
    
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
