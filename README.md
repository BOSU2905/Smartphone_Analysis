📱 Smartphone Market Analysis & Dashboard
🎯 Overview
Proyek ini bertujuan untuk menganalisis tren pasar smartphone global melalui pendekatan data-driven. Dengan menggunakan dataset yang mencakup berbagai brand, harga, dan spesifikasi, aplikasi ini menyediakan dashboard interaktif untuk mengungkap pola distribusi harga dan korelasi spesifikasi teknis.

Proyek ini sangat menitikberatkan pada integritas data, di mana teknik preprocessing tingkat lanjut diterapkan untuk memastikan model atau analisis yang dihasilkan tetap akurat dan tidak bias oleh nilai ekstrem.

🛠️ Key Features & Data Logic
Dashboard ini tidak hanya menampilkan grafik, tetapi juga menangani masalah fundamental dalam dataset:

Missing Value Handling: Menggunakan Median Imputation pada kolom numerik untuk menjaga volume data (100 baris) tanpa terpengaruh oleh outlier.

Outlier Handling (Winsorization): Menggunakan teknik IQR (Interquartile Range) untuk melakukan clipping pada nilai ekstrem (Upper & Lower Bound), memastikan distribusi data tetap simetris namun tetap mempertahankan hierarki brand premium.

Interactive Visualizations: Implementasi Plotly untuk grafik interaktif (Pie Charts, Box Plots, dan Heatmap Korelasi) guna memberikan pengalaman eksplorasi data yang dinamis.

Market Storytelling: Menganalisis dominasi pasar brand tertentu dibandingkan dengan segmen ultra-premium.

📂 Project Structure
Struktur folder diatur secara modular untuk memudahkan skalabilitas dan kolaborasi:

Plaintext
Smartphone_Analysis/
├── data/
│   ├── raw/           # Dataset asli (3 file kotor)
│   └── processed/     # Dataset final yang sudah dibersihkan
├── notebooks/         # Eksperimen analisis (EDA & Cleaning) dalam .ipynb
├── .venv/             # Virtual environment isolasi library
├── app.py             # Main engine Streamlit Dashboard
├── requirements.txt   # Daftar dependensi library
└── README.md          # Dokumentasi proyek
🚀 Getting Started
Prerequisites
Pastikan Anda memiliki Python 3.10+ (Direkomendasikan 3.14) terinstal di sistem Anda.

Installation
Clone repositori ini:

Bash
git clone https://github.com/username/smartphone-analysis.git
cd smartphone-analysis
Buat dan aktifkan Virtual Environment:

Bash
python -m venv .venv
source .venv/bin/activate  # Untuk Linux/Mac
# atau
.venv\Scripts\activate     # Untuk Windows
Instal library yang dibutuhkan:

Bash
pip install -r requirements.txt
Running the App
Jalankan dashboard melalui terminal:

Bash
streamlit run app.py
📊 Insights Captured
Hubungan antara kapasitas RAM dan harga jual global.

Distribusi harga smartphone yang cenderung skewed ke arah budget-entry level.

Visualisasi "Harga Sultan" sebagai outlier yang divalidasi melalui Box Plot.

✍️ Author
Benedictus Alfred Djaja

Undergraduate Data Science Student at Bina Nusantara University.

Connect with me on LinkedIn
