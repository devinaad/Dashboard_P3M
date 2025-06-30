import streamlit as st
import plotly.graph_objects as go

def show_legend(fields, colors, has_uncategorized=False):
    """
    Show enhanced legend that includes uncategorized category when present
    
    Parameters:
        fields (list): List of category names
        colors (list): List of colors for each category  
        has_uncategorized (bool): Whether to include uncategorized category in legend
    """
    fig = go.Figure()
    
    # Add traces for main categories
    for field, color in zip(fields, colors):
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            name=field,
            mode="lines",
            line=dict(color=color, width=4)
        ))
    
    # Add uncategorized category if needed
    if has_uncategorized:
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None], 
            name='Belum Terklasifikasi',
            mode="lines",
            line=dict(color='#6B7280', width=4)  # Gray color
        ))
    
    # Update layout for horizontal legend
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="middle",
            y=0.5,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        height=100
    )
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)