import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Create sample data
years = list(range(2016, 2025))  # Last 10 years
categories = [
        "Robotics and Mechatronics",
        "Telecommunications and Networking",
        "Power and Energy Systems",
        "Artificial Intelligence and Data Science",
        "Sensors and Embedded Systems",
        "Digital Media and Entertainment",
        "Software Development",
    ]
# Generate random data for demonstration
np.random.seed(42)  # For reproducibility

# Sample data for Penelitian (research)
penelitian_data = {}
for category in categories:
    # Generate random funding data with an increasing trend
    base_value = np.random.randint(50, 200)
    trend = np.random.uniform(1.05, 1.15)  # Slight upward trend
    fluctuation = np.random.uniform(0.8, 1.2, size=len(years))
    values = [int(base_value * (trend ** i) * fluctuation[i]) for i in range(len(years))]
    penelitian_data[category] = values

# Sample data for Pengabdian Masyarakat (community service)
pengabdian_data = {}
for category in categories:
    # Generate different random funding data with an increasing trend
    base_value = np.random.randint(30, 150)
    trend = np.random.uniform(1.03, 1.12)  # Slight upward trend
    fluctuation = np.random.uniform(0.85, 1.15, size=len(years))
    values = [int(base_value * (trend ** i) * fluctuation[i]) for i in range(len(years))]
    pengabdian_data[category] = values

# Convert to DataFrames
df_penelitian = pd.DataFrame(penelitian_data, index=years)
df_pengabdian = pd.DataFrame(pengabdian_data, index=years)

# Main title
st.title("Visualisasi Dana Penelitian dan Pengabdian Masyarakat")
st.subheader("Data 10 Tahun Terakhir (2016-2024)")

# Create tabs
tab1, tab2 = st.tabs(["Penelitian", "Pengabdian Masyarakat"])

# Function to create interactive stacked bar chart with Plotly
def create_plotly_stacked_bar(df, title):
    fig = go.Figure()
    
    # Define a colorful palette
    colors = [
        '#636EFA', '#EF553B', '#00CC96', '#AB63FA', 
        '#FFA15A', '#19D3F3', '#FF6692'
    ]
    
    # Add each category as a separate trace
    for i, category in enumerate(categories):
        fig.add_trace(go.Bar(
            x=df.index,
            y=df[category],
            name=category,
            marker_color=colors[i % len(colors)],
            hovertemplate='%{y:,.0f} juta rupiah<extra></extra>'  # Hover text format
        ))
    
    # Update layout for better appearance
    fig.update_layout(
        title={
            'text': f"Total Dana {title} per Kategori (2015-2024)",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20}
        },
        xaxis_title="Tahun",
        yaxis_title="Dana (dalam Juta Rupiah)",
        barmode='stack',
        legend_title="Kategori",
        hovermode="closest",
        height=600,
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
        )
    )
    
    return fig

# Tab 1: Penelitian
with tab1:
    st.header("Visualisasi Dana Penelitian")
    
    # # Show data table with expander
    # with st.expander("Lihat Data Penelitian"):
    #     st.dataframe(df_penelitian)
        
    #     # Add download button for CSV
    #     csv_penelitian = df_penelitian.to_csv().encode('utf-8')
    #     st.download_button(
    #         label="Download Data Penelitian (CSV)",
    #         data=csv_penelitian,
    #         file_name='data_penelitian.csv',
    #         mime='text/csv'
    #     )
    
    # Show interactive plotly stacked bar chart
    fig_penelitian = create_plotly_stacked_bar(df_penelitian, "Penelitian")
    st.plotly_chart(fig_penelitian, use_container_width=True)
    
    # Add some analysis
    st.subheader("Analisis Dana Penelitian")
    
    col1, col2 = st.columns(2)
    
    # Calculate total funding per year
    yearly_total = df_penelitian.sum(axis=1)
    
    # Find year with highest funding
    max_year = yearly_total.idxmax()
    max_funding = yearly_total.max()
    
    # Calculate growth
    growth = ((yearly_total.iloc[-1] / yearly_total.iloc[0]) - 1) * 100
    
    with col1:
        st.metric(
            label="Total Dana Penelitian Tertinggi", 
            value=f"Rp {max_funding:,.0f} juta",
            delta=f"Tahun {max_year}"
        )
        
        st.metric(
            label="Pertumbuhan Dana (2015-2024)", 
            value=f"{growth:.2f}%"
        )
    
    # Find category with highest funding
    category_total = df_penelitian.sum()
    top_category = category_total.idxmax()
    top_funding = category_total.max()
    
    category_percent = (top_funding / category_total.sum()) * 100
    
    with col2:
        st.metric(
            label="Kategori Dengan Dana Tertinggi", 
            value=top_category,
            delta=f"Rp {top_funding:,.0f} juta"
        )
        
        st.metric(
            label="Persentase Dari Total Dana", 
            value=f"{category_percent:.2f}%"
        )

# Tab 2: Pengabdian Masyarakat
with tab2:
    st.header("Visualisasi Dana Pengabdian Masyarakat")
    
    # Show data table with expander
    # with st.expander("Lihat Data Pengabdian Masyarakat"):
    #     st.dataframe(df_pengabdian)
        
    #     # Add download button for CSV
    #     csv_pengabdian = df_pengabdian.to_csv().encode('utf-8')
    #     st.download_button(
    #         label="Download Data Pengabdian Masyarakat (CSV)",
    #         data=csv_pengabdian,
    #         file_name='data_pengabdian.csv',
    #         mime='text/csv'
    #     )
    
    # Show interactive plotly stacked bar chart
    fig_pengabdian = create_plotly_stacked_bar(df_pengabdian, "Pengabdian Masyarakat")
    st.plotly_chart(fig_pengabdian, use_container_width=True)
    
    # Add some analysis
    st.subheader("Analisis Dana Pengabdian Masyarakat")
    
    col1, col2 = st.columns(2)
    
    # Calculate total funding per year
    yearly_total = df_pengabdian.sum(axis=1)
    
    # Find year with highest funding
    max_year = yearly_total.idxmax()
    max_funding = yearly_total.max()
    
    # Calculate growth
    growth = ((yearly_total.iloc[-1] / yearly_total.iloc[0]) - 1) * 100
    
    with col1:
        st.metric(
            label="Total Dana Pengabdian Tertinggi", 
            value=f"Rp {max_funding:,.0f} juta",
            delta=f"Tahun {max_year}"
        )
        
        st.metric(
            label="Pertumbuhan Dana (2015-2024)", 
            value=f"{growth:.2f}%"
        )
    
    # Find category with highest funding
    category_total = df_pengabdian.sum()
    top_category = category_total.idxmax()
    top_funding = category_total.max()
    
    category_percent = (top_funding / category_total.sum()) * 100
    
    with col2:
        st.metric(
            label="Kategori Dengan Dana Tertinggi", 
            value=top_category,
            delta=f"Rp {top_funding:,.0f} juta"
        )
        
        st.metric(
            label="Persentase Dari Total Dana", 
            value=f"{category_percent:.2f}%"
        )
