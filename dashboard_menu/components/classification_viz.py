import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_donut_chart(fields, values, title, colors=None, uncategorized_count=0):
    """
    Create enhanced donut chart that includes uncategorized data when present
    
    Parameters:
        fields (list): Category names in chart
        values (list): Category values  
        title (str): Chart title
        colors (list, optional): Color list for each category
        uncategorized_count (int): Count of uncategorized items
        
    Returns:
        fig: Plotly Figure object
    """
    # Default colors if not provided
    if colors is None:
        colors = [
            "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
            "#FFA15A", "#19D3F3", "#FF6692", "#B6E880",
            "#FF97FF", "#FECB52"
        ]
    
    # Prepare data for the chart
    chart_fields = fields.copy()
    chart_values = values.copy()
    chart_colors = colors.copy()
    
    # Add uncategorized data if it exists
    if uncategorized_count > 0:
        chart_fields.append("Belum Terklasifikasi")
        chart_values.append(uncategorized_count)
        chart_colors.append("#6B7280")  # Gray color for uncategorized
    
    # Only create chart if there's data to display
    if sum(chart_values) == 0:
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
            title=title,
            height=300,
            showlegend=False
        )
        return fig
    
    # Create the donut chart
    fig = go.Figure(data=[
        go.Pie(
            labels=chart_fields,
            values=chart_values,
            hole=0.4,
            marker=dict(colors=chart_colors),
            textinfo="percent",
            textposition="inside",
            textfont=dict(
                size=13,
                color='white',
                family='Arial Black'
            ),
            hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>'
        )
    ])
    
    # Update layout
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
        margin=dict(l=10, r=10, t=40, b=5),
        showlegend=False,
    )
    
    return fig