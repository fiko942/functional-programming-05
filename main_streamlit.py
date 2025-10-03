#!/usr/bin/env python3
"""
Golden Dragon Wok - Enterprise Resource Planning System
Streamlit Web-Based Version
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from src.database_tk import user_manager, init_demo_data

# Page config
st.set_page_config(
    page_title="Golden Dragon Wok ERP",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_demo_data()

# Custom CSS for Chinese restaurant theme
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #D32F2F 0%, #B71C1C 100%);
    padding: 1rem 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #D32F2F;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}

.gold-border {
    border: 2px solid #FFD700;
    border-radius: 10px;
    padding: 1rem;
    background: #FFF8DC;
}

.sidebar-metric {
    background: #FFF8DC;
    padding: 0.5rem;
    border-radius: 5px;
    border-left: 3px solid #D32F2F;
    margin: 0.5rem 0;
}

.stSelectbox > div > div > select {
    color: #D32F2F;
}

/* Hide Streamlit style */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

def login_page():
    """Login interface"""
    st.markdown('<div class="main-header"><h1>🐉 Golden Dragon Wok</h1><h3>Enterprise Resource Planning System</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="gold-border">', unsafe_allow_html=True)
        
        # Login Form
        with st.form("login_form"):
            st.subheader("🔑 Login ke Sistem")
            
            user_id = st.text_input("User ID", placeholder="Masukkan User ID", value="admin")
            password = st.text_input("Password", type="password", placeholder="Masukkan Password", value="admin123")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                login_button = st.form_submit_button("🔓 MASUK", use_container_width=True)
            
            if login_button:
                if user_id and password:
                    success, message = user_manager.login(user_id, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.user_profile = user_manager.get_current_profile()
                        st.success(f"Selamat datang, {user_id}!")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Mohon isi semua field!")
        
        # Register Form
        with st.expander("📝 Registrasi Akun Baru"):
            with st.form("register_form"):
                st.subheader("Daftar Akun Baru")
                
                reg_user_id = st.text_input("User ID Baru", placeholder="Pilih User ID unik")
                reg_password = st.text_input("Password Baru", type="password", placeholder="Minimal 6 karakter")
                reg_confirm = st.text_input("Konfirmasi Password", type="password")
                reg_nama = st.text_input("Nama Lengkap", placeholder="Nama lengkap Anda")
                reg_alamat = st.text_area("Alamat", placeholder="Alamat lengkap")
                reg_hp = st.text_input("No. HP", placeholder="Nomor HP")
                reg_role = st.selectbox("Role", ["staff", "admin", "manager"])
                
                register_button = st.form_submit_button("📝 DAFTAR", use_container_width=True)
                
                if register_button:
                    if all([reg_user_id, reg_password, reg_nama, reg_alamat, reg_hp]):
                        if reg_password != reg_confirm:
                            st.error("Password tidak cocok!")
                        elif len(reg_password) < 6:
                            st.error("Password minimal 6 karakter!")
                        else:
                            profile_data = {
                                'nama': reg_nama,
                                'alamat': reg_alamat,
                                'hp': reg_hp,
                                'role': reg_role,
                                'tanggal_daftar': str(date.today())
                            }
                            success, message = user_manager.register(reg_user_id, reg_password, profile_data)
                            if success:
                                st.success("Registrasi berhasil! Silakan login.")
                            else:
                                st.error(message)
                    else:
                        st.error("Mohon isi semua field!")
        
        # Demo accounts info
        st.info("""
        **Demo Accounts:**
        - Admin: `admin` / `admin123`
        - Staff: `staff01` / `staff123`
        - Chef: `chef01` / `chef123`
        - Kasir: `kasir01` / `kasir123`
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main_app():
    """Main ERP application"""
    # Header
    profile = st.session_state.get('user_profile', {})
    user_name = profile.get('nama', st.session_state.user_id)
    user_role = profile.get('role', 'user').title()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="main-header"><h2>🐉 Golden Dragon Wok - ERP System</h2><p>Selamat datang, {user_name} ({user_role})</p></div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 LOGOUT", use_container_width=True):
            user_manager.logout()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Sidebar Navigation
    st.sidebar.markdown("## 🧭 Menu Navigasi")
    
    menu_options = {
        "📊 Dashboard": "dashboard",
        "🍜 Manajemen Menu": "menu",
        "📝 Pesanan": "orders",
        "📦 Inventori": "inventory",
        "👥 Karyawan": "employees",
        "💰 Keuangan": "finance",
        "📈 Laporan": "reports",
        "⚙️ Pengaturan": "settings"
    }
    
    selected_page = st.sidebar.selectbox("Pilih Menu:", list(menu_options.keys()))
    page_id = menu_options[selected_page]
    
    # Quick stats in sidebar
    st.sidebar.markdown("### 📈 Quick Stats")
    st.sidebar.markdown('<div class="sidebar-metric"><b>Penjualan Hari Ini</b><br/>Rp 2,450,000</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-metric"><b>Pesanan Aktif</b><br/>23 pesanan</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-metric"><b>Stok Menipis</b><br/>8 item</div>', unsafe_allow_html=True)
    
    # Load selected page
    if page_id == "dashboard":
        dashboard_page()
    elif page_id == "menu":
        menu_page()
    elif page_id == "orders":
        orders_page()
    elif page_id == "inventory":
        inventory_page()
    elif page_id == "employees":
        employees_page()
    elif page_id == "finance":
        finance_page()
    elif page_id == "reports":
        reports_page()
    else:
        settings_page()

def dashboard_page():
    """Dashboard with key metrics and charts"""
    st.header("📊 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Penjualan Hari Ini",
            value="Rp 2,450,000",
            delta="12% dari kemarin"
        )
    
    with col2:
        st.metric(
            label="📝 Pesanan Aktif",
            value="23",
            delta="5 pesanan baru"
        )
    
    with col3:
        st.metric(
            label="📦 Stok Menipis",
            value="8 item",
            delta="-2 dari kemarin"
        )
    
    with col4:
        st.metric(
            label="👥 Karyawan Aktif",
            value="12 orang",
            delta="Shift siang"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Penjualan Mingguan")
        # Sample data for sales chart
        sales_data = pd.DataFrame({
            'Hari': ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'],
            'Penjualan': [2100000, 1950000, 2300000, 2450000, 2800000, 3200000, 2900000]
        })
        
        fig_sales = px.line(sales_data, x='Hari', y='Penjualan', 
                           title="Tren Penjualan 7 Hari Terakhir",
                           color_discrete_sequence=['#D32F2F'])
        fig_sales.update_layout(yaxis_title="Penjualan (Rp)")
        st.plotly_chart(fig_sales, use_container_width=True)
    
    with col2:
        st.subheader("🥘 Menu Terpopuler")
        # Sample data for popular menu
        menu_data = pd.DataFrame({
            'Menu': ['Nasi Goreng Special', 'Ayam Kung Pao', 'Mie Canton', 'Es Teh Manis', 'Sup Kimlo'],
            'Terjual': [45, 32, 28, 67, 18]
        })
        
        fig_menu = px.bar(menu_data, x='Menu', y='Terjual',
                         title="Menu Terlaris Hari Ini",
                         color_discrete_sequence=['#FFD700'])
        fig_menu.update_xaxes(tickangle=45)
        st.plotly_chart(fig_menu, use_container_width=True)
    
    # Recent orders
    st.subheader("📋 Pesanan Terbaru")
    recent_orders = pd.DataFrame({
        'No. Pesanan': ['ORD001', 'ORD002', 'ORD003', 'ORD004'],
        'Meja': ['Meja 5', 'Meja 12', 'Takeaway', 'Meja 8'],
        'Waktu': ['19:30', '19:45', '20:00', '20:15'],
        'Total': ['Rp 85,000', 'Rp 120,000', 'Rp 65,000', 'Rp 95,000'],
        'Status': ['🍳 Dimasak', '✅ Siap', '⏳ Menunggu', '🍳 Dimasak']
    })
    st.dataframe(recent_orders, use_container_width=True, hide_index=True)

def menu_page():
    """Menu management page"""
    st.header("🍜 Manajemen Menu")
    
    # Add new menu item
    with st.expander("➕ Tambah Menu Baru"):
        col1, col2 = st.columns(2)
        with col1:
            menu_name = st.text_input("Nama Menu")
            menu_category = st.selectbox("Kategori", ["Nasi", "Mie", "Ayam", "Sup", "Minuman", "Dessert"])
            menu_price = st.number_input("Harga", min_value=0, step=1000)
        with col2:
            menu_description = st.text_area("Deskripsi")
            menu_status = st.selectbox("Status", ["Tersedia", "Habis", "Tidak Aktif"])
            
        if st.button("Tambah Menu"):
            st.success(f"Menu '{menu_name}' berhasil ditambahkan!")
    
    # Menu list
    st.subheader("📋 Daftar Menu")
    menu_data = pd.DataFrame({
        'ID': ['001', '002', '003', '004', '005'],
        'Nama Menu': ['Nasi Goreng Special', 'Ayam Kung Pao', 'Mie Ayam Canton', 'Es Teh Manis', 'Sup Kimlo'],
        'Kategori': ['Nasi', 'Ayam', 'Mie', 'Minuman', 'Sup'],
        'Harga': ['Rp 35,000', 'Rp 45,000', 'Rp 30,000', 'Rp 8,000', 'Rp 25,000'],
        'Status': ['✅ Tersedia', '✅ Tersedia', '✅ Tersedia', '✅ Tersedia', '❌ Habis']
    })
    
    # Search and filter
    col1, col2, col3 = st.columns(3)
    with col1:
        search_menu = st.text_input("🔍 Cari Menu", placeholder="Nama menu...")
    with col2:
        filter_category = st.selectbox("Filter Kategori", ["Semua", "Nasi", "Mie", "Ayam", "Sup", "Minuman"])
    with col3:
        filter_status = st.selectbox("Filter Status", ["Semua", "Tersedia", "Habis"])
    
    # Apply filters
    filtered_data = menu_data.copy()
    if search_menu:
        filtered_data = filtered_data[filtered_data['Nama Menu'].str.contains(search_menu, case=False)]
    if filter_category != "Semua":
        filtered_data = filtered_data[filtered_data['Kategori'] == filter_category]
    
    st.dataframe(filtered_data, use_container_width=True, hide_index=True)

def orders_page():
    """Orders management page"""
    st.header("📝 Manajemen Pesanan")
    
    # Order status summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⏳ Menunggu", "8", "2 baru")
    with col2:
        st.metric("🍳 Dimasak", "12", "5 berlangsung")
    with col3:
        st.metric("✅ Siap", "3", "Siap disajikan")
    with col4:
        st.metric("🍽️ Selesai", "45", "Hari ini")
    
    # Add new order
    with st.expander("➕ Tambah Pesanan Baru"):
        col1, col2 = st.columns(2)
        with col1:
            order_table = st.selectbox("Meja/Jenis", ["Meja 1", "Meja 2", "Meja 3", "Takeaway", "Delivery"])
            order_items = st.multiselect("Pilih Menu", 
                                       ["Nasi Goreng Special", "Ayam Kung Pao", "Mie Canton", "Es Teh Manis"])
        with col2:
            order_notes = st.text_area("Catatan Khusus")
            order_priority = st.selectbox("Prioritas", ["Normal", "Urgent", "VIP"])
            
        if st.button("Buat Pesanan"):
            st.success("Pesanan berhasil dibuat!")
    
    # Orders table
    st.subheader("📋 Daftar Pesanan")
    orders_data = pd.DataFrame({
        'No. Pesanan': ['ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005'],
        'Meja': ['Meja 5', 'Meja 12', 'Takeaway', 'Meja 8', 'Delivery'],
        'Waktu Pesan': ['19:30', '19:45', '20:00', '20:15', '20:30'],
        'Items': ['2 items', '4 items', '1 item', '3 items', '2 items'],
        'Total': ['Rp 85,000', 'Rp 120,000', 'Rp 65,000', 'Rp 95,000', 'Rp 55,000'],
        'Status': ['🍳 Dimasak', '✅ Siap', '⏳ Menunggu', '🍳 Dimasak', '⏳ Menunggu']
    })
    
    # Status filter
    status_filter = st.selectbox("Filter Status", ["Semua", "Menunggu", "Dimasak", "Siap", "Selesai"])
    
    st.dataframe(orders_data, use_container_width=True, hide_index=True)

def inventory_page():
    """Inventory management page"""
    st.header("📦 Manajemen Inventori")
    
    # Inventory alerts
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🟢 Stok Aman", "25 item", "Normal")
    with col2:
        st.metric("🟡 Stok Menipis", "8 item", "Perlu restok")
    with col3:
        st.metric("🔴 Stok Habis", "3 item", "Segera beli")
    
    # Low stock alerts
    st.warning("⚠️ **Peringatan Stok Menipis:** Bawang Putih, Kecap Manis, Ayam Fillet")
    
    # Add inventory item
    with st.expander("➕ Tambah Item Inventori"):
        col1, col2 = st.columns(2)
        with col1:
            item_name = st.text_input("Nama Bahan")
            item_category = st.selectbox("Kategori", ["Bahan Utama", "Bumbu", "Sayuran", "Protein", "Minuman"])
            item_unit = st.selectbox("Satuan", ["Kg", "Gram", "Liter", "Botol", "Pack", "Buah"])
        with col2:
            item_stock = st.number_input("Stok Awal", min_value=0)
            item_min_stock = st.number_input("Minimum Stok", min_value=0)
            item_supplier = st.text_input("Supplier")
            
        if st.button("Tambah Item"):
            st.success(f"Item '{item_name}' berhasil ditambahkan!")
    
    # Inventory table
    st.subheader("📋 Daftar Inventori")
    inventory_data = pd.DataFrame({
        'Kode': ['BHN001', 'BHN002', 'BHN003', 'BHN004', 'BHN005'],
        'Nama Bahan': ['Beras Premium', 'Ayam Fillet', 'Mie Telur', 'Kecap Manis', 'Bawang Putih'],
        'Kategori': ['Bahan Utama', 'Protein', 'Bahan Utama', 'Bumbu', 'Bumbu'],
        'Stok': [50, 15, 25, 8, 5],
        'Satuan': ['Kg', 'Kg', 'Kg', 'Botol', 'Kg'],
        'Min. Stok': [20, 10, 15, 5, 3],
        'Status': ['🟢 Aman', '🟡 Menipis', '🟢 Aman', '🟡 Menipis', '🔴 Habis']
    })
    
    # Filter by status
    status_filter = st.selectbox("Filter Status", ["Semua", "Aman", "Menipis", "Habis"])
    
    st.dataframe(inventory_data, use_container_width=True, hide_index=True)

def employees_page():
    """Employee management page"""
    st.header("👥 Manajemen Karyawan")
    
    # Employee summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👨‍🍳 Chef", "3", "Shift aktif")
    with col2:
        st.metric("🧑‍💼 Pelayan", "6", "Shift aktif")
    with col3:
        st.metric("💰 Kasir", "2", "Shift aktif")
    with col4:
        st.metric("📋 Manager", "1", "Aktif")
    
    # Add employee
    with st.expander("➕ Tambah Karyawan Baru"):
        col1, col2 = st.columns(2)
        with col1:
            emp_name = st.text_input("Nama Lengkap")
            emp_position = st.selectbox("Posisi", ["Chef", "Pelayan", "Kasir", "Manager", "Cleaning"])
            emp_phone = st.text_input("No. HP")
        with col2:
            emp_shift = st.selectbox("Shift", ["Pagi (06:00-14:00)", "Siang (14:00-22:00)", "Malam (22:00-06:00)"])
            emp_salary = st.number_input("Gaji Pokok", min_value=0, step=100000)
            emp_start_date = st.date_input("Tanggal Mulai Kerja")
            
        if st.button("Tambah Karyawan"):
            st.success(f"Karyawan '{emp_name}' berhasil ditambahkan!")
    
    # Employee table
    st.subheader("📋 Daftar Karyawan")
    employees_data = pd.DataFrame({
        'ID': ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005'],
        'Nama': ['Li Wei', 'Wang Ming', 'Chen Lu', 'Liu Han', 'Zhang Mei'],
        'Posisi': ['Chef', 'Pelayan', 'Kasir', 'Pelayan', 'Manager'],
        'Shift': ['Siang', 'Malam', 'Siang', 'Siang', 'Siang'],
        'No. HP': ['081234567890', '081234567891', '081234567892', '081234567893', '081234567894'],
        'Status': ['✅ Aktif', '✅ Aktif', '✅ Aktif', '🏖️ Libur', '✅ Aktif']
    })
    
    # Position filter
    position_filter = st.selectbox("Filter Posisi", ["Semua", "Chef", "Pelayan", "Kasir", "Manager"])
    
    st.dataframe(employees_data, use_container_width=True, hide_index=True)

def finance_page():
    """Finance management page"""
    st.header("💰 Manajemen Keuangan")
    
    # Financial summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Pemasukan Hari Ini", "Rp 2,450,000", "12%")
    with col2:
        st.metric("💸 Pengeluaran Hari Ini", "Rp 800,000", "-5%")
    with col3:
        st.metric("📈 Profit Hari Ini", "Rp 1,650,000", "18%")
    with col4:
        st.metric("💳 Saldo Kas", "Rp 15,750,000", "3%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Pemasukan vs Pengeluaran")
        finance_data = pd.DataFrame({
            'Tanggal': ['01/10', '02/10', '03/10', '04/10', '05/10'],
            'Pemasukan': [2800000, 2200000, 2450000, 2600000, 2300000],
            'Pengeluaran': [900000, 750000, 800000, 850000, 700000]
        })
        
        fig_finance = go.Figure()
        fig_finance.add_trace(go.Bar(name='Pemasukan', x=finance_data['Tanggal'], y=finance_data['Pemasukan'], marker_color='#4CAF50'))
        fig_finance.add_trace(go.Bar(name='Pengeluaran', x=finance_data['Tanggal'], y=finance_data['Pengeluaran'], marker_color='#F44336'))
        fig_finance.update_layout(barmode='group', title="Trend Keuangan 5 Hari Terakhir")
        st.plotly_chart(fig_finance, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Pembagian Pengeluaran")
        expense_data = pd.DataFrame({
            'Kategori': ['Bahan Baku', 'Gaji Karyawan', 'Utilitas', 'Operasional'],
            'Jumlah': [450000, 200000, 100000, 50000]
        })
        
        fig_expense = px.pie(expense_data, values='Jumlah', names='Kategori',
                           title="Pengeluaran Hari Ini",
                           color_discrete_sequence=['#D32F2F', '#FF9800', '#2196F3', '#4CAF50'])
        st.plotly_chart(fig_expense, use_container_width=True)
    
    # Transaction table
    st.subheader("📋 Transaksi Terbaru")
    transactions_data = pd.DataFrame({
        'Tanggal': ['03/10/2024', '02/10/2024', '01/10/2024'],
        'Jenis': ['Pemasukan', 'Pengeluaran', 'Pemasukan'],
        'Deskripsi': ['Penjualan Menu', 'Pembelian Bahan', 'Penjualan Menu'],
        'Jumlah': ['+ Rp 2,450,000', '- Rp 800,000', '+ Rp 2,200,000'],
        'Metode': ['Tunai + Transfer', 'Tunai', 'Tunai'],
        'Saldo': ['Rp 15,750,000', 'Rp 14,100,000', 'Rp 14,900,000']
    })
    
    st.dataframe(transactions_data, use_container_width=True, hide_index=True)

def reports_page():
    """Reports and analytics page"""
    st.header("📈 Laporan & Analisis")
    
    # Report filters
    col1, col2, col3 = st.columns(3)
    with col1:
        report_type = st.selectbox("Jenis Laporan", ["Penjualan", "Menu", "Karyawan", "Keuangan"])
    with col2:
        date_range = st.selectbox("Periode", ["Hari Ini", "Minggu Ini", "Bulan Ini", "Kustom"])
    with col3:
        if st.button("📊 Generate Laporan"):
            st.success("Laporan berhasil di-generate!")
    
    # Sales analytics
    st.subheader("📊 Analisis Penjualan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Best selling items
        bestselling_data = pd.DataFrame({
            'Menu': ['Nasi Goreng Special', 'Ayam Kung Pao', 'Mie Canton', 'Es Teh Manis'],
            'Terjual': [45, 32, 28, 67],
            'Pendapatan': [1575000, 1440000, 840000, 536000]
        })
        
        fig_bestselling = px.bar(bestselling_data, x='Menu', y='Terjual',
                               title="Menu Terlaris",
                               color='Pendapatan',
                               color_continuous_scale='Reds')
        fig_bestselling.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bestselling, use_container_width=True)
    
    with col2:
        # Hourly sales
        hourly_data = pd.DataFrame({
            'Jam': ['11:00', '12:00', '13:00', '18:00', '19:00', '20:00', '21:00'],
            'Pesanan': [5, 12, 8, 15, 23, 18, 10]
        })
        
        fig_hourly = px.line(hourly_data, x='Jam', y='Pesanan',
                           title="Pesanan per Jam",
                           color_discrete_sequence=['#FFD700'])
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Detailed reports table
    st.subheader("📋 Laporan Detail")
    reports_data = pd.DataFrame({
        'Menu': ['Nasi Goreng Special', 'Ayam Kung Pao', 'Mie Ayam Canton', 'Es Teh Manis', 'Sup Kimlo'],
        'Terjual': [45, 32, 28, 67, 18],
        'Pendapatan': ['Rp 1,575,000', 'Rp 1,440,000', 'Rp 840,000', 'Rp 536,000', 'Rp 450,000'],
        'Kategori': ['Nasi', 'Ayam', 'Mie', 'Minuman', 'Sup'],
        'Popularitas': ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐⭐'],
        'Margin': ['45%', '52%', '38%', '75%', '40%']
    })
    
    st.dataframe(reports_data, use_container_width=True, hide_index=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Export PDF"):
            st.info("Laporan akan didownload sebagai PDF")
    with col2:
        if st.button("📊 Export Excel"):
            st.info("Laporan akan didownload sebagai Excel")
    with col3:
        if st.button("📧 Email Laporan"):
            st.info("Laporan akan dikirim via email")

def settings_page():
    """Settings and configuration page"""
    st.header("⚙️ Pengaturan Sistem")
    
    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏪 Restoran", "👥 Pengguna", "🔧 Sistem", "🔒 Keamanan"])
    
    with tab1:
        st.subheader("Pengaturan Restoran")
        rest_name = st.text_input("Nama Restoran", value="Golden Dragon Wok")
        rest_address = st.text_area("Alamat", value="Jl. Raya Chinese Food No. 88, Jakarta")
        rest_phone = st.text_input("No. Telepon", value="021-12345678")
        rest_email = st.text_input("Email", value="info@goldendragonwok.com")
        
        col1, col2 = st.columns(2)
        with col1:
            rest_open = st.time_input("Jam Buka", value=datetime.strptime("10:00", "%H:%M").time())
        with col2:
            rest_close = st.time_input("Jam Tutup", value=datetime.strptime("22:00", "%H:%M").time())
            
        if st.button("💾 Simpan Pengaturan Restoran"):
            st.success("Pengaturan restoran berhasil disimpan!")
    
    with tab2:
        st.subheader("Manajemen Pengguna")
        st.info("Pengguna yang terdaftar dalam sistem:")
        
        users_data = pd.DataFrame({
            'User ID': ['admin', 'staff01', 'chef01', 'kasir01'],
            'Nama': ['Administrator', 'Staff Utama', 'Chef Utama', 'Kasir Utama'],
            'Role': ['Admin', 'Staff', 'Chef', 'Kasir'],
            'Status': ['Aktif', 'Aktif', 'Aktif', 'Aktif'],
            'Last Login': ['03/10/2024 20:30', '03/10/2024 19:15', '03/10/2024 18:00', '03/10/2024 17:30']
        })
        
        st.dataframe(users_data, use_container_width=True, hide_index=True)
        
        if st.button("➕ Tambah Pengguna Baru"):
            st.info("Gunakan menu Register untuk menambah pengguna baru")
    
    with tab3:
        st.subheader("Pengaturan Sistem")
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Tema Aplikasi", ["Light", "Dark", "Auto"])
            st.selectbox("Bahasa", ["Indonesia", "English", "中文"])
            st.checkbox("Notifikasi Push", value=True)
            st.checkbox("Auto Backup", value=True)
        
        with col2:
            st.number_input("Timeout Session (menit)", min_value=5, max_value=120, value=30)
            st.selectbox("Format Tanggal", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
            st.selectbox("Format Mata Uang", ["Rp", "$", "¥"])
            
        if st.button("💾 Simpan Pengaturan Sistem"):
            st.success("Pengaturan sistem berhasil disimpan!")
    
    with tab4:
        st.subheader("Pengaturan Keamanan")
        
        st.info("🔒 **Kebijakan Password:**")
        st.write("- Minimal 6 karakter")
        st.write("- Kombinasi huruf dan angka direkomendasikan")
        st.write("- Ganti password secara berkala")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Require Strong Password", value=False)
            st.checkbox("Two-Factor Authentication", value=False)
            st.checkbox("Login Logging", value=True)
        
        with col2:
            st.number_input("Max Login Attempts", min_value=3, max_value=10, value=5)
            st.number_input("Password Expiry (hari)", min_value=30, max_value=365, value=90)
            
        if st.button("💾 Simpan Pengaturan Keamanan"):
            st.success("Pengaturan keamanan berhasil disimpan!")

def main():
    """Main application flow"""
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Show appropriate page
    if st.session_state.logged_in:
        main_app()
    else:
        login_page()

if __name__ == "__main__":
    main()