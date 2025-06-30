import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def show_fund_viz(df, title, colors, fields, uncategorized_data=None):
    """
    Create enhanced stacked bar chart for fund visualization that includes uncategorized data
    
    Parameters:
        df (pd.DataFrame): DataFrame with years as index and categories as columns
        title (str): Chart title
        colors (list): Color list for each category
        fields (list): Category names list
        uncategorized_data (pd.DataFrame, optional): Uncategorized data grouped by year
    
    Returns:
        fig: Plotly Figure object
    """
    
    # Check if main data is empty
    if df.empty and (uncategorized_data is None or uncategorized_data.empty):
        # Create empty chart with message
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
    
    # Add categorized data traces
    if not df.empty:
        for i, category in enumerate(fields):
            if category in df.columns:
                fig.add_trace(go.Bar(
                    x=df.index,
                    y=df[category],
                    name=category,
                    marker_color=colors[i % len(colors)],
                    hovertemplate=f'<b>{category}</b><br>Tahun: %{{x}}<br>Dana: %{{y:,.0f}} juta rupiah<extra></extra>'
                ))
    
    # Add uncategorized data if it exists
    if uncategorized_data is not None and not uncategorized_data.empty:
        fig.add_trace(go.Bar(
            x=uncategorized_data.index,
            y=uncategorized_data['Dana'],
            name='Belum Terklasifikasi',
            marker_color='#6B7280',  # Gray color
            hovertemplate='<b>Belum Terklasifikasi</b><br>Tahun: %{x}<br>Dana: %{y:,.0f} juta rupiah<extra></extra>'
        ))
    
    # Calculate and display totals
    all_years = set()
    if not df.empty:
        all_years.update(df.index)
    if uncategorized_data is not None and not uncategorized_data.empty:
        all_years.update(uncategorized_data.index)
    
    if all_years:
        totals = []
        years_list = sorted(list(all_years))
        
        for year in years_list:
            total = 0
            # Add categorized data total
            if not df.empty and year in df.index:
                total += df.loc[year, fields].sum()
            # Add uncategorized data total
            if uncategorized_data is not None and not uncategorized_data.empty and year in uncategorized_data.index:
                total += uncategorized_data.loc[year, 'Dana']
            totals.append(total)
        
        # Add total labels on top of bars
        fig.add_trace(go.Scatter(
            x=years_list,
            y=totals,
            mode='text',
            text=[f"{val:,.0f}" for val in totals],
            textposition='top center',
            showlegend=False,
            textfont=dict(size=10, color='black'),
            hoverinfo='skip'
        ))
    
    # Update layout
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
            tickvals=years_list if 'years_list' in locals() else []
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
