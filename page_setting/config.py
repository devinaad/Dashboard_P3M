import streamlit as st

def setup_page():
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Sistem Klasifikasi & Analisis P3M",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Injeksi CSS khusus untuk desain responsif dan dinamis
    st.markdown("""
    <style>
        /* Latar belakang utama */
        .main {
            background-color: #f8fafc;
        }

        /* Container utama */
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* Kartu metrik */
        .metric-card {
            border-radius: 0.5rem;
            padding: 0.5rem;
            margin: 0.5rem 0;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }

        .metric-card.blue { background-color: #dbeafe; }
        .metric-card.green { background-color: #dcfce7; }
        .metric-card.yellow { background-color: #fef9c3; }
        .metric-card.purple { background-color: #f3e8ff; }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            text-align: center;
            color: #1e293b;
        }

        .metric-label {
            text-align: center;
            color: #475569;
            font-size: 1rem;
            margin-top: 0.25rem;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.7rem;
            padding: 1rem 0;
        }

        .stPlotlyChart {
            outline: 10px solid #b8f9fc;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2), 0 6px 20px rgba(0,0,0,0.3);
        }

        .plot-title {
            color: black;
            text-align: center;
            padding: 5px;
            margin-bottom: 25px;
            border-radius: 5px;
            font-weight: bold;
        }

        .upload-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            color: white;
        }

        .data-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 0.5rem 0;
            border-left: 2px solid #667eea;
            transition: 0.2s ease;
        }

        .data-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        .feature-card {
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
            padding: 1rem;
            border-radius: 8px;
            margin: 0.3rem;
            color: white;
            text-align: center;
            transition: 0.2s ease;
        }

        .feature-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        .stats-card {
            background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
            padding: 0.7rem;
            border-radius: 6px;
            text-align: center;
            color: white;
            margin: 0.3rem 0;
            font-size: 0.9rem;
        }

        .title-gradient {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.8rem;
        }

        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }

        /* Flex Utility */
        .flex-row {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: space-between;
        }

        .flex-item {
            flex: 1 1 200px;
        }

        /* Responsif */
        @media (max-width: 768px) {
            .title-gradient {
                font-size: 2rem;
            }

            .subtitle {
                font-size: 1rem;
            }

            .upload-container,
            .data-card,
            .feature-card,
            .stats-card {
                padding: 1rem;
                font-size: 0.9rem;
            }

            .metric-value {
                font-size: 1.2rem;
            }

            .metric-label {
                font-size: 0.85rem;
            }
        }

        @media (max-width: 480px) {
            .card-grid {
                grid-template-columns: 1fr !important;
            }

            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Warna default (opsional untuk grafik)
fields = [
            "Robotics and Mechatronics",
            "Telecommunications and Networking",
            "Power and Energy Systems",
            "Artificial Intelligence and Data Science",
            "Sensors and Embedded Systems",
            "Digital Media and Entertainment",
            "Software Development",
        ]
colors = [
    "#636EFA",  # Blue
    "#EF553B",  # Red
    "#00CC96",  # Green
    "#AB63FA",  # Purple
    "#FFA15A",  # Orange
    "#19D3F3",  # Cyan
    "#FF6692",  # Pink
    "#B6E880",  # Light Green
    "#FF97FF",  # Light Pink
    "#FECB52"   # Yellow
]
