import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import qualitative
from itables import to_html_datatable
import streamlit.components.v1 as components

def create_prodi_bar_chart(data, title, prodi_column='Prodi', top_n=10):
    """
    Creates a horizontal bar chart showing distribution by study program (Prodi)
    
    Parameters:
        data (pd.DataFrame): DataFrame containing the data
        title (str): Title for the chart
        prodi_column (str): Column name for study program data
        top_n (int): Number of top programs to display
        
    Returns:
        fig: Plotly Figure object
    """
    
    if data.empty or prodi_column not in data.columns:
        # Create empty chart if no data
        fig = go.Figure()
        fig.add_annotation(
            text="Data Prodi tidak tersedia",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=title,
            height=400,
            showlegend=False
        )
        return fig
    
    # Count occurrences of each study program
    prodi_counts = data[prodi_column].value_counts().head(top_n)
    
    if prodi_counts.empty:
        # Handle case where no valid data exists
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data Prodi yang valid",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=title,
            height=400,
            showlegend=False
        )
        return fig
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Use a color palette
    colors = qualitative.Set3[:len(prodi_counts)]
    
    fig.add_trace(go.Bar(
        x=prodi_counts.values,
        y=prodi_counts.index,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(50, 50, 50, 0.2)', width=1)
        ),
        text=prodi_counts.values,
        textposition='outside',
        textfont=dict(size=12, color='black'),
        hovertemplate='<b>%{y}</b><br>Jumlah: %{x}<br><extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        },
        xaxis_title="Jumlah",
        yaxis_title="Program Studi",
        height=max(400, len(prodi_counts) * 30 + 100),  # Dynamic height based on data
        margin=dict(l=20, r=80, t=60, b=40),
        showlegend=False,
        xaxis=dict(
            tickformat=',d',
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        yaxis=dict(
            tickmode='linear',
            automargin=True
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_color="black"
        )
    )
    
    return fig


def create_prodi_table_itables(data, prodi_column='Prodi', bidang_column='Bidang Penelitian', ketua_column='Nama Ketua', top_n=20):
    """
    Creates an interactive table showing study program with most common category and top contributor.

    Parameters:
        data (pd.DataFrame): The dataset
        prodi_column (str): Column name for program study
        bidang_column (str): Column for category (e.g. 'Bidang Penelitian' or 'Bidang Pengabdian Masyarakat')
        ketua_column (str): Column name for contributors
        top_n (int): Number of top programs to show (based on frequency)

    Returns:
        str: HTML for the interactive itables table
    """
    import pandas as pd
    from itables import to_html_datatable

    if data.empty or prodi_column not in data.columns:
        empty_df = pd.DataFrame({
            "Program Studi": ["Data tidak tersedia"], 
            "Kategori Paling Banyak": ["-"],
            "Kontributor Terbanyak": ["-"]
        })
        return to_html_datatable(
            empty_df,
            table_id="empty_table",
            classes="display compact",
            style="width:100%",
            buttons=[]
        )

    # Hitung jumlah per prodi
    prodi_counts = data[prodi_column].value_counts().head(top_n)

    table_data = []

    for prodi in prodi_counts.index:
        subset = data[data[prodi_column] == prodi]

        # Ambil kategori terbanyak
        if bidang_column in subset.columns:
            kategori_terbanyak = subset[bidang_column].mode(dropna=True)
            kategori = kategori_terbanyak.iloc[0] if not kategori_terbanyak.empty else "-"
        else:
            kategori = "-"

        # Ambil kontributor terbanyak
        if ketua_column in subset.columns:
            top_ketua = subset[ketua_column].value_counts().idxmax()
        else:
            top_ketua = "-"

        table_data.append({
            "Program Studi": prodi,
            "Kategori Paling Banyak": kategori,
            "Kontributor Terbanyak": top_ketua
        })

    df_table = pd.DataFrame(table_data)

    # Render dengan itables
    html_table = to_html_datatable(
        df_table,
        table_id="prodi_table",
        classes="display compact stripe hover",
        style="width:100%",
        lengthMenu=[5, 10, 15, 20],
        pageLength=5,
        searching=True,
        ordering=True,
        info=True,
        paging=True
    )
    return html_table



def show_prodi_analysis(filtered_penelitian, filtered_pengmas):
    """
    Main function to display study program analysis section
    Simplified version with side-by-side plot and table
    
    Parameters:
        filtered_penelitian (pd.DataFrame): Filtered research data
        filtered_pengmas (pd.DataFrame): Filtered community service data
    """
    # Single selector for data type
    choose_data = st.selectbox(
        "Pilih Jenis Data untuk Analisis:",
        ["Penelitian", "Pengabdian Masyarakat"],
        key="prodi_data_select"
    )
    
    # Slider for top N programs
    top_n = st.slider(
        "Jumlah Program Studi Teratas:",
        min_value=5,
        max_value=20,
        value=10,
        key="prodi_top_n"
    )
    
    # Create two columns: one for chart, one for table
    st.info('''Jika terdapat Nama Prodi yang tidak sesuai atau berisi "lainnya", hal ini disebabkan oleh ketidak sesuain data nama dosen pada file yang 
        diupload dengan data nama yang ada pada PDDIKTI sehingga sistem tidak dapat mengidentifikasi nama prodi secara sempurna. ''')
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:        
        if choose_data == "Penelitian":
            fig = create_prodi_bar_chart(
                filtered_penelitian, 
                f"Top {top_n} Program Studi - Penelitian", 
                top_n=top_n
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            fig = create_prodi_bar_chart(
                filtered_pengmas, 
                f"Top {top_n} Program Studi - Pengabdian Masyarakat", 
                top_n=top_n
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:        
        if choose_data == "Penelitian":
            html_table = create_prodi_table_itables(filtered_penelitian, bidang_column="Bidang Penelitian")
        else:
            html_table = create_prodi_table_itables(filtered_penelitian, bidang_column="Bidang Pengabdian Masyarakat")
        
        # Display the interactive table
        components.html(html_table, height=500, scrolling=True)
    
