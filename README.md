# Dashboard Aplikasi P3M 📊

A comprehensive web application for analyzing and visualizing research (Penelitian) and community service (Pengabdian Masyarakat) data using Streamlit. This application provides automated text classification, data preprocessing, and interactive dashboards for academic research management.

## 🌟 Features

- **📤 Data Upload**: Support for CSV and Excel files
- **🔄 Automated Data Processing**: Text preprocessing and classification pipeline
- **📊 Interactive Dashboard**: Visual analytics with charts and metrics
- **🗂️ Dataset Management**: View and analyze classified research data
- **🎯 Smart Classification**: Automatic categorization of research fields
- **📱 Responsive Design**: Modern UI with streamlit-antd-components

## 🚀 Demo

![Dashboard Preview](demo-screenshot.png)

*Screenshot of the main dashboard showing research analytics*

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features Detail](#features-detail)
- [Data Format](#data-format)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/devinaad/Dashboard-Aplikasi-P3M.git
cd Dashboard-Aplikasi-P3M
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will be available at `https://dashboard-klasifikasi-p3m.streamlit.app/`

## 📦 Required Dependencies

Create a `requirements.txt` file with the following packages:

```txt
pandas
plotly
streamlit
streamlit-option-menu
streamlit-card
streamlit-antd-components
itables
joblib
numpy
nltk
sastrawi
scikit-learn
streamlit_date_picker
datetime
openpyxl>=3.1.0
xlrd>=2.0.0
```

## 🎯 Usage

### 1. Starting the Application

1. Launch the app using `streamlit run app.py`
2. Navigate to the **Beranda** (Home) page
3. Upload your research datasets

### 2. Data Upload

1. **Prepare Your Data**: Ensure your CSV/Excel files have a column named "Judul" (Title)
2. **Upload Files**: 
   - Upload Penelitian (Research) data file
   - Upload Pengabdian Masyarakat (Community Service) data file
3. **Submit Data**: Click "Submit & Proses Data" button

### 3. Data Processing

1. After upload, click "🚀 Start Data Processing"
2. Wait for the preprocessing and classification to complete
3. View processing results and statistics

### 4. Explore Analytics

- **Dashboard**: View comprehensive analytics and visualizations
- **Dataset**: Browse classified data in tabular format
- **Research Fields**: Analyze distribution of research categories

## 📁 Project Structure

```
Dashboard-Aplikasi-P3M/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
│
├── page_setting/
│   └── config.py                  # Page configuration and settings
│
├── beranda_menu/
│   ├── beranda.py                 # Home page logic
│   ├── components/
│   │   ├── header.py              # Header component
│   │   ├── features.py            # Features showcase
│   │   └── upload_section.py      # File upload interface
│   ├── sections/
│   │   ├── preview_data.py        # Data preview section
│   │   └── next_steps.py          # Next steps guide
│   └── templates/
│       └── template_download.py   # Template download feature
│
├── dashboard_menu/
│   └── dashboard.py               # Dashboard visualization logic
│
├── dataset_menu/
│   ├── show_dataset.py            # Dataset display functionality
│   └── load_data.py               # Data loading utilities
│
├── classify_data/
│   └── preprocessing_data.py      # Data preprocessing and classification  

```

## 💾 Data Format

### Expected Input Format

Your CSV/Excel files should contain at least the following columns:

#### For Penelitian (Research) Data:
```csv
Judul,Tahun,Dana Disetujui
"Analisis Machine Learning...",2023,1000000
```

#### For Pengabdian Masyarakat Data:
```csv
Judul,Tahun,Dana Disetujui
"Program Pelatihan IT...",2023,1000000
```

### Required Columns:
- **Judul** (Title): Main text for classification
- **Additional columns**: Any relevant metadata

### Output Format:
After processing, your data will include:
- **Bidang Penelitian/Pengabdian Masyarakat**: Classified research field
- **Processed_Text**: Cleaned text data

## ⚙️ Configuration

### Page Settings
Modify `page_setting/config.py` to customize:

```python
# Page configuration
PAGE_TITLE = "Dashboard P3M"
PAGE_ICON = "📊"
LAYOUT = "wide"
```

### Classification Settings
Customize classification parameters in `classify_data/preprocessing_data.py`

## 🎨 Customization

### Adding New Visualizations
1. Create new chart functions in `dashboard_menu/dashboard.py`
2. Add chart configurations to the dashboard layout
3. Update color schemes in `page_setting/config.py`

### Extending Classification
1. Update field mappings in configuration
2. Modify preprocessing pipeline as needed


### Adding New Features

1. **New Pages**: Add modules in respective menu folders
2. **New Components**: Create reusable components in `components/`
3. **New Data Sources**: Extend `load_data.py` functionality


## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/new-feature`
3. **Commit Changes**: `git commit -m 'Add new feature'`
4. **Push to Branch**: `git push origin feature/new-feature`
5. **Create Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex functions
- Update documentation for new features
- Test changes thoroughly before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Contributors to streamlit-antd-components
- Research community for inspiration and feedback

## 📞 Support

If you encounter any issues or have questions:

1. **Check the Issues**: Look for similar problems in [GitHub Issues](https://github.com/yourusername/Dashboard-Aplikasi-P3M/issues)
2. **Create New Issue**: Provide detailed information about your problem
3. **Contact**: Reach out via email or project discussions

---

**⭐ If this project helped you, please consider giving it a star!**

## 🔄 Changelog

### Version 1.0.0 (Current)
- Initial release with basic functionality
- Data upload and processing pipeline
- Interactive dashboard with visualizations
- Dataset management and classification
