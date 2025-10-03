# Golden Dragon Wok - Enterprise Resource Planning System

Sistem ERP untuk restoran Golden Dragon Wok yang dibuat dengan **Tkinter** - GUI yang simple, reliable, dan built-in di Python.

## 🎯 Fitur Utama

### 🔐 Sistem Autentikasi
- Login dan registrasi user
- Manajemen role (admin, staff, chef, kasir)
- Profile management

### 📊 Dashboard
- Overview penjualan harian
- Status pesanan aktif
- Monitor stok yang menipis
- Info karyawan aktif

### 🍜 Manajemen Menu
- Katalog menu lengkap
- Kategori: Nasi, Mie, Ayam, Minuman, Sup
- Harga dan deskripsi

### 📝 Manajemen Pesanan
- Tracking pesanan real-time
- Status: Menunggu, Dimasak, Siap
- Info meja dan takeaway

### 📦 Inventori
- Monitor stok bahan baku
- Alert stok menipis
- Satuan dan status

### 👥 Manajemen Karyawan
- Data karyawan lengkap
- Schedule shift
- Status kehadiran

### 💰 Keuangan
- Laporan harian
- Tracking pemasukan/pengeluaran
- Profit calculation

### 📈 Laporan
- Analisis penjualan
- Menu terpopuler
- Rating dan feedback

## 🚀 Cara Menjalankan

### Prerequisites
- Python 3.11+
- Tkinter (sudah built-in di Python)

### Install Dependencies
```bash
# Masuk ke direktori project
cd "Enterprise Resource Planning untuk restoran Golden Dragon Wok"

# Buat virtual environment
python3 -m venv .venv

# Aktifkan virtual environment
source .venv/bin/activate  # macOS/Linux
# atau
.venv\Scripts\activate     # Windows

# Install requirements (minimal karena menggunakan Tkinter)
pip install -r requirements.txt
```

### Jalankan Aplikasi
```bash
python3 main.py
```

## 🎨 Desain & UI

- **Framework**: Tkinter (built-in Python)
- **Theme**: Chinese restaurant (Red & Gold)
- **Colors**: 
  - Primary Red: #D32F2F
  - Gold: #FFD700
  - Clean white background
- **Typography**: Arial font family dengan berbagai ukuran

## 🏗️ Struktur Project

```
├── main.py                 # Entry point aplikasi (Tkinter)
├── src/
│   ├── database_tk.py      # Database & user management
│   └── __init__.py         # Package init
├── README.md               # Dokumentasi
└── requirements.txt        # Dependencies (minimal)
```

## 👤 Demo Accounts

### Admin
- **User ID**: admin
- **Password**: admin123
- **Role**: Administrator

### Staff
- **User ID**: staff01
- **Password**: staff123
- **Role**: Staff

### Chef
- **User ID**: chef01
- **Password**: chef123
- **Role**: Chef

### Kasir
- **User ID**: kasir01
- **Password**: kasir123
- **Role**: Kasir

## ✨ Keunggulan Tkinter Version

1. **Built-in**: Tidak perlu install library eksternal
2. **Reliable**: Stabil dan teruji
3. **Cross-platform**: Jalan di Windows, macOS, Linux
4. **Ringan**: Memory usage minimal
5. **Simple**: Mudah dipahami dan dimodifikasi

## 📋 Menu Restoran

### 🍚 Nasi
- Nasi Goreng Special - Rp 35,000
- Nasi Goreng Ayam - Rp 30,000
- Nasi Goreng Udang - Rp 40,000
- Nasi Goreng Seafood - Rp 45,000

### 🍜 Mie
- Mie Ayam Canton - Rp 30,000
- Mie Goreng Special - Rp 35,000
- Kwetiau Goreng - Rp 32,000
- Bihun Goreng - Rp 28,000

### 🐔 Ayam
- Ayam Kung Pao - Rp 45,000
- Ayam Sweet & Sour - Rp 42,000
- Ayam Szechuan - Rp 48,000
- Ayam Teriyaki - Rp 40,000

### 🥤 Minuman
- Es Teh Manis - Rp 8,000
- Es Jeruk - Rp 10,000
- Teh Hijau Panas - Rp 12,000
- Kopi Hitam - Rp 15,000

### 🍲 Sup
- Sup Kimlo - Rp 25,000
- Sup Jagung - Rp 20,000
- Sup Wonton - Rp 30,000
- Hot & Sour Soup - Rp 28,000

## 🛠️ Development

### Database
- Dictionary-based storage (in-memory)
- User accounts & profiles
- Menu data dengan kategori
- Session management

### Security
- Basic password validation
- User session management
- Role-based access (siap untuk dikembangkan)

## 📞 Support

Untuk bantuan dan pertanyaan, silakan hubungi tim development.

---

**Golden Dragon Wok ERP System** - *Powering Chinese Cuisine Excellence* 🐉# functional-programming-05
