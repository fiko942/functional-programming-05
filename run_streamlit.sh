#!/bin/bash
# Golden Dragon Wok ERP - Streamlit Launcher
# Script untuk menjalankan aplikasi ERP dengan mudah

echo "🐉 Golden Dragon Wok ERP System - Streamlit Version"
echo "=============================================="
echo ""

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "import streamlit, pandas, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required dependencies..."
    pip3 install streamlit pandas plotly
fi

echo "✅ Dependencies ready!"
echo ""

# Launch Streamlit app
echo "🚀 Launching Golden Dragon Wok ERP..."
echo "📱 Application will open in your browser at:"
echo "   Local:   http://localhost:8501"
echo "   Network: http://$(ipconfig getifaddr en0):8501"
echo ""
echo "🔐 Demo Login Credentials:"
echo "   Admin:  admin / admin123"
echo "   Staff:  staff01 / staff123"
echo "   Chef:   chef01 / chef123"
echo "   Kasir:  kasir01 / kasir123"
echo ""
echo "🛑 Press Ctrl+C to stop the application"
echo "=============================================="

# Run Streamlit
streamlit run main_streamlit.py --server.port 8501 --server.address 0.0.0.0