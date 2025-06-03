# Metrics Cards 
import streamlit as st

def tampilkan_kartu_summary(
    total_penelitian: int,
    total_pengmas: int,
    top_kategori_penelitian: str,
    top_kategori_pengmas: str
):
    st.markdown(f"""
        <div class="card-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div class="metric-card blue" style="border-radius: 0.5rem; padding: 1rem; background-color: #dbeafe; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <div class="metric-value" style="font-size: 2rem; font-weight: bold; text-align: center; color: #1e3a8a;">{total_penelitian}</div>
                <div class="metric-label" style="text-align: center; color: #475569;">Total Penelitian</div>
            </div>
            <div class="metric-card green" style="border-radius: 0.5rem; padding: 1rem; background-color: #dcfce7; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <div class="metric-value" style="font-size: 2rem; font-weight: bold; text-align: center; color: #166534;">{total_pengmas}</div>
                <div class="metric-label" style="text-align: center; color: #475569;">Total Pengabdian Masyarakat</div>
            </div>
            <div class="metric-card blue" style="border-radius: 0.5rem; padding: 1rem; background-color: #dbeafe; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <div style="font-size: 1.1rem; font-weight: 700; text-align: center; color: #1e293b;">
                    {top_kategori_penelitian}
                </div>
                <div class="metric-label" style="text-align: center; color: #475569; font-size: 0.85rem; margin-top: 0.5rem;">
                    Top 1 Kategori Penelitian
                </div>
            </div>
            <div class="metric-card green" style="border-radius: 0.5rem; padding: 1rem; background-color: #dcfce7; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                <div style="font-size: 1.1rem; font-weight: 700; text-align: center; color: #1e293b;">
                    {top_kategori_pengmas}
                </div>
                <div class="metric-label" style="text-align: center; color: #475569; font-size: 0.85rem; margin-top: 0.5rem;">
                    Top 1 Kategori Pengabdian Masyarakat
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
