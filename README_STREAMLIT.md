# 🐉 Golden Dragon Wok - Enterprise Resource Planning System (Streamlit)

Modern web-based ERP system untuk restoran Golden Dragon Wok yang dibuat dengan **Streamlit** - memberikan interface dashboard yang interaktif dan mudah digunakan.

## 🌟 Keunggulan Streamlit Version

### 🌐 **Web-Based Modern Interface**
- **Beautiful dashboard** dengan tema merah-emas Chinese restaurant
- **Responsive design** yang mobile-friendly  
- **Interactive charts** dengan Plotly untuk visualisasi data
- **Real-time updates** dan auto-refresh

### 📊 **Built-in Dashboard Components**
- **Metrics cards** dengan delta indicators untuk KPI
- **Interactive charts** (line, bar, pie) untuk analytics
- **Data tables** dengan search & filter functionality
- **Multi-tab interface** untuk navigasi yang mudah

### 🚀 **Easy Development & Deployment**
- **Zero CSS/HTML** knowledge needed
- **Pure Python** - familiar syntax
- **Auto-deployment** ready untuk cloud
- **Share via URL** untuk remote access

## 🎯 Fitur Lengkap ERP

### 🔐 **Sistem Autentikasi**
- Login dan registrasi user dengan validasi
- Session management yang aman
- Role-based access (admin, staff, chef, kasir)
- Profile management lengkap

### 📊 **Dashboard Analytics**
- Real-time metrics (penjualan, pesanan, stok, karyawan)
- Interactive charts untuk trend analysis
- Quick stats di sidebar untuk overview cepat
- Recent orders tracking

### 🍜 **Manajemen Menu**
- CRUD operations untuk menu items
- Kategori menu (Nasi, Mie, Ayam, Sup, Minuman)
- Search dan filter functionality
- Status management (Tersedia/Habis)

### 📝 **Manajemen Pesanan**
- Order tracking dengan status real-time
- Multi-status workflow (Menunggu → Dimasak → Siap → Selesai)
- Support untuk berbagai jenis order (Dine-in, Takeaway, Delivery)
- Order metrics dan analytics

### 📦 **Inventori Management**
- Stock monitoring dengan alert system
- Low stock warnings otomatis
- Kategori bahan baku
- Supplier information

### 👥 **Manajemen Karyawan**
- Employee database lengkap
- Shift management
- Position-based organization
- Contact information tracking

### 💰 **Financial Management**
- Revenue dan expense tracking
- Profit calculation real-time
- Interactive financial charts
- Transaction history detailed

### 📈 **Reports & Analytics**
- Sales analytics dengan visualisasi
- Menu performance reports
- Hourly sales patterns
- Export functionality (PDF, Excel, Email)

### ⚙️ **System Settings**
- Restaurant configuration
- User management
- System preferences
- Security settings

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- Modern web browser

### Quick Start
```bash
# Clone atau download project
cd "Enterprise Resource Planning untuk restoran Golden Dragon Wok"

# Install dependencies
pip3 install streamlit pandas plotly

# Run application
streamlit run main_streamlit.py

# Atau gunakan launcher script
./run_streamlit.sh
```

### Alternative Installation
```bash
# Install dari requirements.txt
pip3 install -r requirements.txt

# Run dengan custom port
streamlit run main_streamlit.py --server.port 8502
```

## 🎨 Interface Overview

### **Login Page**
- Modern form dengan tema Chinese restaurant
- Demo accounts tersedia
- Registration form untuk user baru
- Responsive design untuk semua device

### **Main Dashboard**
- Header dengan user info dan logout button
- Sidebar navigation dengan quick stats
- Content area dengan interactive widgets
- Real-time data visualization

### **Navigation**
- Sidebar menu untuk semua modul
- Breadcrumb navigation
- Quick access buttons
- Search functionality

## 👤 Demo Accounts

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| Admin | `admin` | `admin123` | Full system access |
| Staff | `staff01` | `staff123` | General operations |
| Chef | `chef01` | `chef123` | Kitchen management |
| Kasir | `kasir01` | `kasir123` | Point of sale |

## 📱 Access Methods

### **Local Access**
```
http://localhost:8501
```

### **Network Access**
```
http://YOUR_IP_ADDRESS:8501
```

### **Mobile Access**
- Responsive design works on all devices
- Touch-friendly interface
- Optimized for tablets dan smartphones

## 🛠️ Development

### **Project Structure**
```
├── main_streamlit.py           # Main Streamlit application
├── src/
│   ├── database_tk.py          # Database & user management
│   └── __init__.py             # Package initialization
├── run_streamlit.sh            # Launcher script
├── requirements.txt            # Dependencies
└── README_STREAMLIT.md         # This documentation
```

### **Key Technologies**
- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive charts
- **Python**: Core language

### **Architecture**
- **Session Management**: Streamlit session state
- **Data Storage**: In-memory dictionaries
- **UI Components**: Streamlit widgets
- **Charts**: Plotly visualizations

## 📊 Sample Data

### **Menu Items**
- 20+ menu items across 5 categories
- Realistic pricing untuk Chinese restaurant
- Stock status management

### **Financial Data**
- Weekly sales trends
- Expense breakdown
- Profit calculations
- Transaction history

### **Operational Data**
- Employee schedules
- Inventory levels
- Order status tracking
- Customer data

## 🔧 Customization

### **Theme Modification**
Edit CSS dalam `st.markdown()` untuk mengubah:
- Color scheme
- Font styles
- Layout spacing
- Component styling

### **Data Integration**
Replace dictionary storage dengan:
- SQLite database
- PostgreSQL
- MySQL
- MongoDB

### **Feature Extension**
Tambah modul baru:
- Customer management
- Loyalty program
- Online ordering
- Payment integration

## 🚀 Deployment Options

### **Streamlit Cloud** (Recommended)
```bash
# Push to GitHub
git add .
git commit -m "Initial commit"
git push origin main

# Deploy via Streamlit Cloud
# Visit: share.streamlit.io
```

### **Heroku**
```bash
# Create Procfile
echo "web: streamlit run main_streamlit.py --server.port $PORT" > Procfile

# Deploy to Heroku
heroku create golden-dragon-wok-erp
git push heroku main
```

### **Docker**
```dockerfile
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "main_streamlit.py"]
```

## 🎯 Performance Tips

### **Optimization**
- Use `@st.cache_data` untuk expensive operations
- Minimize data reloading dengan session state
- Optimize chart rendering dengan sampling

### **Scalability**
- Implement proper database backend
- Add caching layer (Redis)
- Use load balancer untuk multiple instances

## 🔒 Security Considerations

### **Authentication**
- Implement proper password hashing
- Add session timeout
- Enable HTTPS dalam production

### **Data Protection**
- Validate all user inputs
- Sanitize database queries
- Implement audit logging

## 📞 Support & Contact

- **Development Team**: Golden Dragon Wok IT
- **Email**: support@goldendragonwok.com
- **Documentation**: Lihat README files untuk detail

## 🏆 Benefits Over Traditional Desktop Apps

### **Accessibility**
- ✅ Access dari any device dengan browser
- ✅ No installation required
- ✅ Automatic updates
- ✅ Cross-platform compatibility

### **Collaboration**
- ✅ Multiple users simultaneously
- ✅ Real-time data sharing
- ✅ Central data management
- ✅ Remote access capability

### **Maintenance**
- ✅ Easy updates dan patches
- ✅ Central configuration
- ✅ Simplified backup
- ✅ Cloud deployment ready

---

**Golden Dragon Wok ERP System** - *Empowering Restaurant Excellence Through Modern Technology* 🐉✨

## 🌟 Quick Commands

```bash
# Start application
streamlit run main_streamlit.py

# With custom configuration
streamlit run main_streamlit.py --server.port 8502 --server.address 0.0.0.0

# Background mode
nohup streamlit run main_streamlit.py &

# Stop application
pkill -f streamlit
```