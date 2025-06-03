from itables import to_html_datatable
from streamlit.components.v1 import html
import pandas as pd
import streamlit as st
from dataset_menu.table_setting import get_datatable_options
from dataset_menu.table_css import custom_style


def show_table(dataframe, dataframe_name):
    st.markdown(f"<h2 style='text-align: center; color: #323b4f;'>Klasifikasi {dataframe_name}</h1>", unsafe_allow_html=True)

    # Get dynamic datatable options based on the dataframe
    datatable_options = get_datatable_options(dataframe)

    # Combine custom style with datatable
    table_html = custom_style + to_html_datatable(
        dataframe,
        classes="display",  # Remove nowrap from here
        options=datatable_options
    )
    return html(table_html, height=1000, scrolling=True)