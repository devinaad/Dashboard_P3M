import pandas as pd
import numpy as np
from collections import Counter

class DataProcessor:
    """Class untuk memproses data penelitian dan pengabdian masyarakat"""
    
    def __init__(self, data_penelitian, data_pengabdian, fields):
        self.data_penelitian = data_penelitian
        self.data_pengabdian = data_pengabdian
        self.fields = fields
    
    def get_basic_counts(self, filtered_penelitian, filtered_pengmas):
        """Menghitung jumlah total penelitian dan pengabdian masyarakat"""
        total_penelitian = len(filtered_penelitian)
        total_pengmas = len(filtered_pengmas)
        return total_penelitian, total_pengmas
    
    def get_top_categories(self, filtered_penelitian, filtered_pengmas, category_column_penelitian, category_column_pengmas):
        """Mendapatkan kategori teratas untuk penelitian dan pengabdian masyarakat"""
        try:
            # Top kategori penelitian
            if not filtered_penelitian.empty and category_column_penelitian in filtered_penelitian.columns:
                top_penelitian = filtered_penelitian[category_column_penelitian].value_counts().index[0]
            else:
                top_penelitian = "Data tidak tersedia"
            
            # Top kategori pengabdian masyarakat
            if not filtered_pengmas.empty and category_column_pengmas in filtered_pengmas.columns:
                top_pengmas = filtered_pengmas[category_column_pengmas].value_counts().index[0]
            else:
                top_pengmas = "Data tidak tersedia"
                
        except (IndexError, KeyError):
            top_penelitian = "Data tidak tersedia"
            top_pengmas = "Data tidak tersedia"
        
        return top_penelitian, top_pengmas
    
    def get_category_distribution(self, data, category_column='Kategori'):
        """Menghitung distribusi kategori dalam data"""
        if data.empty or category_column not in data.columns:
            return [], []
        
        category_counts = data[category_column].value_counts()
        
        # Pastikan semua field ada, jika tidak ada set ke 0
        values = []
        for field in self.fields:
            values.append(category_counts.get(field, 0))
        
        return self.fields, values
    
    def prepare_fund_data(self, data, fund_column='Dana Disetujui', category_column='Kategori', year_column='Tahun'):
        """Mempersiapkan data untuk visualisasi dana per tahun dan kategori"""
        if data.empty:
            return pd.DataFrame()
        
        # Buat DataFrame kosong dengan tahun sebagai index
        years = sorted(data[year_column].unique()) if year_column in data.columns else []
        if not years:
            return pd.DataFrame()
        
        # Inisialisasi DataFrame dengan 0 untuk semua kombinasi tahun-kategori
        fund_df = pd.DataFrame(index=years, columns=self.fields).fillna(0)
        
        # Jika kolom dana dan kategori ada
        if fund_column in data.columns and category_column in data.columns:
            # Group by tahun dan kategori, sum dana
            grouped = data.groupby([year_column, category_column])[fund_column].sum().reset_index()
            
            # Isi DataFrame dengan data yang ada
            for _, row in grouped.iterrows():
                year = row[year_column]
                category = row[category_column]
                amount = row[fund_column]
                
                if category in fund_df.columns:
                    fund_df.loc[year, category] = amount
        
        # Konversi ke numeric dan handle NaN
        fund_df = fund_df.apply(pd.to_numeric, errors='coerce').fillna(0)
        
        return fund_df
    
    def get_yearly_counts(self, data, year_column='Tahun'):
        """Menghitung jumlah data per tahun"""
        if data.empty or year_column not in data.columns:
            return pd.DataFrame(columns=[year_column, 'Count'])
        
        yearly_counts = data[year_column].value_counts().reset_index()
        yearly_counts.columns = [year_column, 'Count']
        return yearly_counts.sort_values(year_column)
    
    def process_all_data(self, filtered_penelitian, filtered_pengmas):
        """Memproses semua data yang diperlukan untuk dashboard"""
        
        # Basic counts
        total_penelitian, total_pengmas = self.get_basic_counts(filtered_penelitian, filtered_pengmas)
        
        # Top categories
        top_penelitian, top_pengmas = self.get_top_categories(filtered_penelitian, filtered_pengmas, 'Bidang Penelitian','Bidang Pengabdian Masyarakat')
        
        # Category distributions
        penelitian_fields, penelitian_values = self.get_category_distribution(filtered_penelitian, category_column='Bidang Penelitian')
        pengmas_fields, pengmas_values = self.get_category_distribution(filtered_pengmas, category_column='Bidang Pengabdian Masyarakat')
        
        # Fund data
        penelitian_fund_df = self.prepare_fund_data(filtered_penelitian,fund_column='Dana Disetujui', category_column='Bidang Penelitian', year_column='Tahun')
        pengmas_fund_df = self.prepare_fund_data(filtered_pengmas, fund_column='Dana Disetujui', category_column='Bidang Pengabdian Masyarakat', year_column='Tahun')
        
        return {
            'total_penelitian': total_penelitian,
            'total_pengmas': total_pengmas,
            'top_penelitian': top_penelitian,
            'top_pengmas': top_pengmas,
            'penelitian_fields': penelitian_fields,
            'penelitian_values': penelitian_values,
            'pengmas_fields': pengmas_fields,
            'pengmas_values': pengmas_values,
            'penelitian_fund_df': penelitian_fund_df,
            'pengmas_fund_df': pengmas_fund_df
        }