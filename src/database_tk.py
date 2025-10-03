"""
Database module untuk Golden Dragon Wok ERP System
Menggunakan dictionary storage yang simple dan reliable
"""

from datetime import datetime

# Dictionary untuk menyimpan akun
accounts_db = {}

# Dictionary untuk menyimpan profil user
user_profiles = {}

class UserAccount:
    def __init__(self):
        self.current_user = None
        
    def register(self, user_id, password, profile_data):
        """Register user baru"""
        if user_id in accounts_db:
            return False, "User ID sudah terdaftar!"
        
        if len(user_id) < 3:
            return False, "User ID minimal 3 karakter!"
        
        if len(password) < 6:
            return False, "Password minimal 6 karakter!"
        
        # Simpan akun
        accounts_db[user_id] = password
        user_profiles[user_id] = profile_data
        
        return True, "Registrasi berhasil!"
    
    def login(self, user_id, password):
        """Login user"""
        if user_id not in accounts_db:
            return False, "User ID tidak ditemukan!"
        
        if accounts_db[user_id] != password:
            return False, "Password salah!"
        
        self.current_user = user_id
        return True, "Login berhasil!"
    
    def logout(self):
        """Logout user dan clear session"""
        old_user = self.current_user
        self.current_user = None
        if old_user:
            print(f"✅ User {old_user} berhasil logout - session cleared")
        return True
    
    def get_current_user(self):
        """Dapatkan user yang sedang login"""
        return self.current_user
    
    def get_current_profile(self):
        """Dapatkan profil user yang sedang login"""
        if self.current_user and self.current_user in user_profiles:
            return user_profiles[self.current_user]
        return None
    
    def update_profile(self, user_id, profile_data):
        """Update profil user"""
        if user_id in user_profiles:
            user_profiles[user_id].update(profile_data)
            return True, "Profil berhasil diupdate!"
        return False, "User tidak ditemukan!"
    
    def get_all_users(self):
        """Dapatkan semua user (untuk admin)"""
        return list(accounts_db.keys())
    
    def get_user_profile(self, user_id):
        """Dapatkan profil user tertentu"""
        if user_id in user_profiles:
            return user_profiles[user_id]
        return None

# Instance global
user_manager = UserAccount()

def init_demo_data():
    """Inisialisasi data demo"""
    # Clear existing data
    accounts_db.clear()
    user_profiles.clear()
    
    # Admin account
    accounts_db['admin'] = 'admin123'
    user_profiles['admin'] = {
        'nama': 'Administrator Golden Dragon',
        'alamat': 'Jl. Merdeka No. 123, Jakarta',
        'hp': '081234567890',
        'role': 'admin',
        'tanggal_daftar': '2024-01-01',
        'status': 'aktif'
    }
    
    # Staff accounts
    accounts_db['staff01'] = 'staff123'
    user_profiles['staff01'] = {
        'nama': 'Li Wei Chen',
        'alamat': 'Jl. Sudirman No. 45, Jakarta', 
        'hp': '082345678901',
        'role': 'staff',
        'tanggal_daftar': '2024-02-15',
        'status': 'aktif'
    }
    
    accounts_db['chef01'] = 'chef123'
    user_profiles['chef01'] = {
        'nama': 'Wang Ming Lu',
        'alamat': 'Jl. Kemang No. 67, Jakarta',
        'hp': '083456789012', 
        'role': 'chef',
        'tanggal_daftar': '2024-03-01',
        'status': 'aktif'
    }
    
    accounts_db['kasir01'] = 'kasir123'
    user_profiles['kasir01'] = {
        'nama': 'Chen Lu Mei',
        'alamat': 'Jl. Blok M No. 89, Jakarta',
        'hp': '084567890123',
        'role': 'kasir', 
        'tanggal_daftar': '2024-03-15',
        'status': 'aktif'
    }
    
    print("✅ Demo data berhasil diinisialisasi!")
    print(f"📊 Total akun: {len(accounts_db)}")
    print(f"📊 Total profil: {len(user_profiles)}")

# Menu data untuk restaurant
menu_data = {
    'nasi': [
        ('001', 'Nasi Goreng Special', 35000, 'Nasi goreng dengan telur, ayam, dan udang'),
        ('002', 'Nasi Goreng Ayam', 30000, 'Nasi goreng dengan potongan ayam'),
        ('003', 'Nasi Goreng Udang', 40000, 'Nasi goreng dengan udang segar'),
        ('004', 'Nasi Goreng Seafood', 45000, 'Nasi goreng dengan aneka seafood'),
        ('005', 'Nasi Putih', 8000, 'Nasi putih hangat')
    ],
    'mie': [
        ('101', 'Mie Ayam Canton', 30000, 'Mie dengan potongan ayam dan sayuran'),
        ('102', 'Mie Goreng Special', 35000, 'Mie goreng dengan telur dan daging'),
        ('103', 'Kwetiau Goreng', 32000, 'Kwetiau goreng dengan daging dan sayur'),
        ('104', 'Bihun Goreng', 28000, 'Bihun goreng dengan sayuran segar'),
        ('105', 'Mie Kuah Ayam', 25000, 'Mie kuah dengan ayam dan sayuran')
    ],
    'ayam': [
        ('201', 'Ayam Kung Pao', 45000, 'Ayam dengan saus pedas manis khas Sichuan'),
        ('202', 'Ayam Sweet & Sour', 42000, 'Ayam dengan saus asam manis'),
        ('203', 'Ayam Szechuan', 48000, 'Ayam pedas khas Szechuan'),
        ('204', 'Ayam Teriyaki', 40000, 'Ayam dengan saus teriyaki'),
        ('205', 'Ayam Goreng Tepung', 35000, 'Ayam goreng dengan tepung crispy')
    ],
    'minuman': [
        ('301', 'Es Teh Manis', 8000, 'Es teh manis segar'),
        ('302', 'Es Jeruk', 10000, 'Es jeruk segar'),
        ('303', 'Teh Hijau Panas', 12000, 'Teh hijau hangat'),
        ('304', 'Kopi Hitam', 15000, 'Kopi hitam original'),
        ('305', 'Jus Jambu', 18000, 'Jus jambu segar')
    ],
    'sup': [
        ('401', 'Sup Kimlo', 25000, 'Sup khas dengan tahu dan jamur'),
        ('402', 'Sup Jagung', 20000, 'Sup jagung dengan telur'),
        ('403', 'Sup Wonton', 30000, 'Sup dengan pangsit isi daging'),
        ('404', 'Sup Sayuran', 18000, 'Sup sayuran segar'),
        ('405', 'Hot & Sour Soup', 28000, 'Sup asam pedas khas China')
    ]
}

def get_menu_by_category(category):
    """Dapatkan menu berdasarkan kategori"""
    return menu_data.get(category.lower(), [])

def get_all_menu():
    """Dapatkan semua menu"""
    all_menu = []
    for category, items in menu_data.items():
        for item in items:
            all_menu.append((item[0], item[1], category.title(), f"Rp {item[2]:,}", item[3]))
    return all_menu

def search_menu(keyword):
    """Cari menu berdasarkan keyword"""
    results = []
    for category, items in menu_data.items():
        for item in items:
            if keyword.lower() in item[1].lower():
                results.append((item[0], item[1], category.title(), f"Rp {item[2]:,}", item[3]))
    return results