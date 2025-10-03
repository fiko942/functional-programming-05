#!/usr/bin/env python3
"""
Golden Dragon Wok - Enterprise Resource Planning System
Menggunakan Tkinter untuk GUI yang lebih reliable
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from src.database_tk import user_manager, init_demo_data

class GoldenDragonERP:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Golden Dragon Wok - ERP System")
        self.root.geometry("800x900")
        self.root.configure(bg='#FFFFFF')
        
        # macOS optimizations
        self.setup_macos_optimizations()
        
        # Initialize database
        init_demo_data()
        
        # Setup styles
        self.setup_styles()
        
        # Create login window
        self.create_login_window()
        
    def setup_macos_optimizations(self):
        """Setup optimizations for macOS"""
        import platform
        if platform.system() == 'Darwin':  # macOS
            # Enable native look and feel
            try:
                self.root.tk.call('tk', 'appname', 'Golden Dragon Wok')
                # Force focus and raise window
                self.root.lift()
                self.root.attributes('-topmost', True)
                self.root.after_idle(lambda: self.root.attributes('-topmost', False))
                
                # Improve responsiveness
                self.root.update_idletasks()
                
            except Exception as e:
                print(f"macOS optimization warning: {e}")
                
    def create_responsive_button(self, parent, text, command, bg_color=None, fg_color=None, **kwargs):
        """Create a button with enhanced responsiveness for macOS"""
        if bg_color is None:
            bg_color = self.colors['primary_red']
        if fg_color is None:
            fg_color = self.colors['white']
            
        # Set default relief if not provided in kwargs
        if 'relief' not in kwargs:
            kwargs['relief'] = 'flat'
        
        button = tk.Button(parent, text=text, command=command,
                          bg=bg_color, fg=fg_color,
                          font=self.fonts['button'],
                          cursor='hand2',
                          activebackground=self.colors['dark_red'],
                          activeforeground=self.colors['white'],
                          **kwargs)
        
        # Add enhanced event handling for macOS
        def on_enter(e):
            button.configure(bg=self.colors['dark_red'])
            self.root.update_idletasks()
            
        def on_leave(e):
            button.configure(bg=bg_color)
            self.root.update_idletasks()
            
        def on_click(e):
            # Force focus and update
            button.focus_set()
            self.root.update_idletasks()
            # Execute command directly without delay to avoid double execution
            command()
            
        # Bind events - but disable default command to avoid double execution
        button.configure(command=None)
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        button.bind('<Button-1>', on_click)
        
        # Also bind to space and return for keyboard accessibility
        def on_key(e):
            if e.keysym in ['Return', 'space']:
                try:
                    command()
                except Exception as ex:
                    print(f"Button command error: {ex}")
                    
        button.bind('<KeyPress>', on_key)
        
        return button
        
    def setup_styles(self):
        """Setup custom styles"""
        self.style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'primary_red': '#D32F2F',
            'dark_red': '#B71C1C',
            'gold': '#FFD700',
            'light_gold': '#FFF8DC',
            'white': '#FFFFFF',
            'black': '#000000',
            'gray': '#BDBDBD'
        }
        
        # Custom fonts
        self.fonts = {
            'title': font.Font(family="Arial", size=24, weight="bold"),
            'subtitle': font.Font(family="Arial", size=14),
            'label': font.Font(family="Arial", size=12, weight="bold"),
            'button': font.Font(family="Arial", size=14, weight="bold"),
            'entry': font.Font(family="Arial", size=12)
        }
        
    def create_login_window(self):
        """Create login/register window"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['white'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title frame with border
        title_frame = tk.Frame(main_frame, bg=self.colors['white'], 
                              relief='solid', bd=3, highlightbackground=self.colors['gold'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(title_frame, text="🐉 Golden Dragon Wok", 
                              font=self.fonts['title'], fg=self.colors['primary_red'], 
                              bg=self.colors['white'])
        title_label.pack(pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Enterprise Resource Planning System", 
                                 font=self.fonts['subtitle'], fg=self.colors['dark_red'], 
                                 bg=self.colors['white'])
        subtitle_label.pack(pady=(0, 15))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Login tab
        login_frame = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(login_frame, text="🔑 Login")
        self.create_login_tab(login_frame)
        
        # Register tab
        register_frame = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(register_frame, text="📝 Register")
        self.create_register_tab(register_frame)
        
    def create_login_tab(self, parent):
        """Create login tab content"""
        # Main container
        container = tk.Frame(parent, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # User ID
        tk.Label(container, text="User ID:", font=self.fonts['label'], 
                fg=self.colors['black'], bg=self.colors['white']).pack(anchor='w', pady=(0, 5))
        
        self.login_userid = tk.Entry(container, font=self.fonts['entry'], 
                                    relief='solid', bd=2, width=40)
        self.login_userid.pack(fill='x', pady=(0, 15), ipady=8)
        self.login_userid.insert(0, "admin")  # Default value
        # Add focus binding for better macOS support
        self.login_userid.bind('<Button-1>', lambda e: self.login_userid.focus_set())
        
        # Password
        tk.Label(container, text="Password:", font=self.fonts['label'], 
                fg=self.colors['black'], bg=self.colors['white']).pack(anchor='w', pady=(0, 5))
        
        self.login_password = tk.Entry(container, font=self.fonts['entry'], 
                                      relief='solid', bd=2, width=40, show='*')
        self.login_password.pack(fill='x', pady=(0, 20), ipady=8)
        self.login_password.insert(0, "admin123")  # Default value
        # Add focus binding for better macOS support  
        self.login_password.bind('<Button-1>', lambda e: self.login_password.focus_set())
        # Add enter key binding
        self.login_password.bind('<Return>', lambda e: self.handle_login())
        
        # Login button dengan responsive handling
        login_btn = self.create_responsive_button(container, "🔓 MASUK", self.handle_login, pady=12)
        login_btn.pack(fill='x', pady=(0, 20))
        
        # Demo info
        demo_frame = tk.Frame(container, bg=self.colors['light_gold'], 
                             relief='solid', bd=1)
        demo_frame.pack(fill='x', pady=10)
        
        demo_text = """Demo Accounts:
• Admin: admin / admin123
• Staff: staff01 / staff123"""
        
        tk.Label(demo_frame, text=demo_text, font=self.fonts['subtitle'],
                fg=self.colors['dark_red'], bg=self.colors['light_gold'],
                justify='left').pack(pady=10)
        
    def create_register_tab(self, parent):
        """Create register tab content"""
        # Scrollable frame
        canvas = tk.Canvas(parent, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Container with padding
        container = tk.Frame(scrollable_frame, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Form fields
        fields = [
            ("User ID:", "reg_userid", "Pilih User ID unik"),
            ("Password:", "reg_password", "Buat password"),
            ("Konfirmasi Password:", "reg_confirm_password", "Konfirmasi password"),
            ("Nama Lengkap:", "reg_nama", "Nama lengkap"),
            ("Alamat:", "reg_alamat", "Alamat lengkap"),
            ("No. HP:", "reg_hp", "Nomor HP")
        ]
        
        self.register_entries = {}
        
        for label_text, field_name, placeholder in fields:
            # Label
            tk.Label(container, text=label_text, font=self.fonts['label'], 
                    fg=self.colors['black'], bg=self.colors['white']).pack(anchor='w', pady=(10, 5))
            
            # Entry
            entry = tk.Entry(container, font=self.fonts['entry'], 
                           relief='solid', bd=2, width=40)
            entry.pack(fill='x', pady=(0, 5), ipady=8)
            
            # Add placeholder text
            entry.insert(0, placeholder)
            entry.configure(fg='gray')
            
            # Bind events for placeholder
            def on_focus_in(event, e=entry, p=placeholder):
                if e.get() == p:
                    e.delete(0, tk.END)
                    e.configure(fg='black')
                    
            def on_focus_out(event, e=entry, p=placeholder):
                if e.get() == '':
                    e.insert(0, p)
                    e.configure(fg='gray')
                    
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
            
            # Configure password fields
            if 'password' in field_name:
                entry.configure(show='*')
                
            self.register_entries[field_name] = entry
        
        # Role combobox
        tk.Label(container, text="Role:", font=self.fonts['label'], 
                fg=self.colors['black'], bg=self.colors['white']).pack(anchor='w', pady=(10, 5))
        
        self.reg_role = ttk.Combobox(container, font=self.fonts['entry'], 
                                    values=['staff', 'admin', 'manager'], 
                                    state='readonly', width=37)
        self.reg_role.pack(fill='x', pady=(0, 20), ipady=8)
        self.reg_role.set('staff')
        
        # Register button dengan responsive handling
        register_btn = self.create_responsive_button(container, "📝 DAFTAR", self.handle_register, pady=12)
        register_btn.pack(fill='x', pady=20)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def handle_login(self):
        """Handle login process"""
        user_id = self.login_userid.get().strip()
        password = self.login_password.get()
        
        if not user_id or not password:
            messagebox.showerror("Error", "Mohon isi semua field!")
            return
            
        success, message = user_manager.login(user_id, password)
        
        if success:
            messagebox.showinfo("Sukses", f"Selamat datang, {user_id}!")
            self.create_main_window(user_id)
        else:
            messagebox.showerror("Error", message)
            
    def handle_register(self):
        """Handle register process"""
        # Get values from entries
        user_id = self.register_entries['reg_userid'].get().strip()
        password = self.register_entries['reg_password'].get()
        confirm_password = self.register_entries['reg_confirm_password'].get()
        nama = self.register_entries['reg_nama'].get().strip()
        alamat = self.register_entries['reg_alamat'].get().strip()
        hp = self.register_entries['reg_hp'].get().strip()
        role = self.reg_role.get()
        
        # Remove placeholder texts
        if user_id == "Pilih User ID unik":
            user_id = ""
        if nama == "Nama lengkap":
            nama = ""
        if alamat == "Alamat lengkap":
            alamat = ""
        if hp == "Nomor HP":
            hp = ""
            
        # Validation
        if not all([user_id, password, nama, alamat, hp]):
            messagebox.showerror("Error", "Mohon isi semua field!")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Password tidak cocok!")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password minimal 6 karakter!")
            return
            
        # Register user
        profile_data = {
            'nama': nama,
            'alamat': alamat,
            'hp': hp,
            'role': role,
            'tanggal_daftar': '2024-10-03'
        }
        
        success, message = user_manager.register(user_id, password, profile_data)
        
        if success:
            messagebox.showinfo("Sukses", "Registrasi berhasil! Silakan login.")
            # Clear form and switch to login tab
            self.clear_register_form()
            self.notebook.select(0)  # Switch to login tab
        else:
            messagebox.showerror("Error", message)
            
    def clear_register_form(self):
        """Clear register form"""
        placeholders = {
            'reg_userid': "Pilih User ID unik",
            'reg_password': "Buat password",
            'reg_confirm_password': "Konfirmasi password",
            'reg_nama': "Nama lengkap",
            'reg_alamat': "Alamat lengkap",
            'reg_hp': "Nomor HP"
        }
        
        for field_name, entry in self.register_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, placeholders[field_name])
            entry.configure(fg='gray')
            
        self.reg_role.set('staff')
        
    def create_main_window(self, user_id):
        """Create main ERP window after successful login"""
        # Clear login window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Main window setup
        self.root.title(f"Golden Dragon Wok ERP - {user_id}")
        self.root.geometry("1200x800")
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['primary_red'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['primary_red'])
        header_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(header_content, text="🐉 Golden Dragon Wok - ERP System", 
                font=self.fonts['title'], fg=self.colors['white'], 
                bg=self.colors['primary_red']).pack(side='left')
        
        # Logout button dengan responsive handling
        logout_btn = self.create_responsive_button(header_content, "🚪 LOGOUT", self.logout,
                                                  bg_color=self.colors['white'], 
                                                  fg_color=self.colors['dark_red'],
                                                  relief='solid', bd=2, padx=15, pady=8)
        logout_btn.pack(side='right', padx=15, pady=15)
        
        # User info
        profile = user_manager.get_current_profile()
        user_info = f"👤 {profile['nama']} ({profile['role'].title()})" if profile else f"👤 {user_id}"
        tk.Label(header_content, text=user_info, font=self.fonts['subtitle'], 
                fg=self.colors['white'], bg=self.colors['primary_red']).pack(side='right', padx=20)
        
        # Main content area
        content_frame = tk.Frame(self.root, bg=self.colors['white'])
        content_frame.pack(fill='both', expand=True)
        
        # Sidebar
        sidebar_frame = tk.Frame(content_frame, bg=self.colors['light_gold'], width=250)
        sidebar_frame.pack(side='left', fill='y')
        sidebar_frame.pack_propagate(False)
        
        # Menu items
        menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("🍜 Manajemen Menu", "menu"),
            ("📝 Pesanan", "orders"),
            ("📦 Inventori", "inventory"),
            ("👥 Karyawan", "employees"),
            ("💰 Keuangan", "finance"),
            ("📈 Laporan", "reports"),
            ("⚙️ Pengaturan", "settings")
        ]
        
        # Menu title
        tk.Label(sidebar_frame, text="Menu Navigasi", font=self.fonts['label'],
                fg=self.colors['dark_red'], bg=self.colors['light_gold']).pack(pady=20)
        
        for menu_text, menu_id in menu_items:
            btn = self.create_responsive_button(sidebar_frame, menu_text, 
                                               lambda m=menu_id: self.switch_page(m),
                                               bg_color=self.colors['white'], 
                                               fg_color=self.colors['black'],
                                               relief='flat', anchor='w', pady=10)
            btn.pack(fill='x', padx=10, pady=2)
            
        # Main content area
        self.main_content = tk.Frame(content_frame, bg=self.colors['white'])
        self.main_content.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        # Show dashboard by default
        self.switch_page('dashboard')
        
    def switch_page(self, page_id):
        """Switch to different page with optimized loading"""
        # Show loading state
        self.root.configure(cursor='watch')
        self.root.update_idletasks()
        
        # Clear current content
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
        # Force update before loading new content
        self.root.update_idletasks()
        
        # Load new page content
        try:
            if page_id == 'dashboard':
                self.create_dashboard()
            elif page_id == 'menu':
                self.create_menu_page()
            elif page_id == 'orders':
                self.create_orders_page()
            elif page_id == 'inventory':
                self.create_inventory_page()
            elif page_id == 'employees':
                self.create_employees_page()
            elif page_id == 'finance':
                self.create_finance_page()
            elif page_id == 'reports':
                self.create_reports_page()
            else:
                self.create_settings_page()
        finally:
            # Restore normal cursor and force update
            self.root.configure(cursor='')
            self.root.update_idletasks()
            # Additional delay for macOS
            self.root.after(100, lambda: self.root.update_idletasks())
            
    def create_dashboard(self):
        """Create dashboard page"""
        tk.Label(self.main_content, text="📊 Dashboard", font=self.fonts['title'],
                fg=self.colors['primary_red'], bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        # Stats cards
        stats_frame = tk.Frame(self.main_content, bg=self.colors['white'])
        stats_frame.pack(fill='x', pady=10)
        
        stats = [
            ("Total Penjualan Hari Ini", "Rp 2,450,000", self.colors['primary_red']),
            ("Pesanan Aktif", "23 pesanan", "#4CAF50"),
            ("Stok Menipis", "8 item", "#FF9800"),
            ("Karyawan Aktif", "12 orang", "#2196F3")
        ]
        
        for i, (title, value, color) in enumerate(stats):
            col = i % 2
            row = i // 2
            
            card_frame = tk.Frame(stats_frame, bg=color, relief='solid', bd=2)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            tk.Label(card_frame, text=title, font=self.fonts['subtitle'],
                    fg=self.colors['white'], bg=color).pack(pady=(10, 5))
            tk.Label(card_frame, text=value, font=self.fonts['title'],
                    fg=self.colors['white'], bg=color).pack(pady=(0, 10))
                    
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        
    def create_menu_page(self):
        """Create menu management page"""
        tk.Label(self.main_content, text="🍜 Manajemen Menu", font=self.fonts['title'],
                fg=self.colors['primary_red'], bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        # Sample menu data
        menu_data = [
            ["001", "Nasi Goreng Special", "Nasi", "Rp 35,000", "Tersedia"],
            ["002", "Ayam Kung Pao", "Ayam", "Rp 45,000", "Tersedia"],
            ["003", "Mie Ayam Canton", "Mie", "Rp 30,000", "Tersedia"],
            ["004", "Es Teh Manis", "Minuman", "Rp 8,000", "Tersedia"],
            ["005", "Sup Kimlo", "Sup", "Rp 25,000", "Habis"]
        ]
        
        self.create_table(["ID", "Nama Menu", "Kategori", "Harga", "Status"], menu_data)
        
    def create_orders_page(self):
        """Create orders page"""
        tk.Label(self.main_content, text="📝 Pesanan", font=self.fonts['title'],
                fg=self.colors['primary_red'], bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        orders_data = [
            ["ORD001", "Meja 5", "19:30", "Rp 85,000", "Dimasak"],
            ["ORD002", "Meja 12", "19:45", "Rp 120,000", "Siap"],
            ["ORD003", "Takeaway", "20:00", "Rp 65,000", "Menunggu"],
            ["ORD004", "Meja 8", "20:15", "Rp 95,000", "Dimasak"]
        ]
        
        self.create_table(["No. Pesanan", "Meja", "Waktu", "Total", "Status"], orders_data)
        
    def create_inventory_page(self):
        """Create inventory page"""
        tk.Label(self.main_content, text="📦 Inventori", font=self.fonts['title'],
                fg=self.colors['primary_red'], bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        inventory_data = [
            ["BHN001", "Beras Premium", "50", "Kg", "Aman"],
            ["BHN002", "Ayam Fillet", "15", "Kg", "Menipis"],
            ["BHN003", "Mie Telur", "25", "Kg", "Aman"],
            ["BHN004", "Kecap Manis", "8", "Botol", "Menipis"],
            ["BHN005", "Bawang Putih", "5", "Kg", "Habis"]
        ]
        
        self.create_table(["Kode", "Nama Bahan", "Stok", "Satuan", "Status"], inventory_data)
        
    def create_employees_page(self):
        """Create employees page"""
        tk.Label(self.main_content, text="👥 Karyawan", font=self.fonts['title'],
                fg=self.colors['primary_red'], bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        employees_data = [
            ["EMP001", "Li Wei", "Chef", "Siang", "Aktif"],
            ["EMP002", "Wang Ming", "Pelayan", "Malam", "Aktif"],
            ["EMP003", "Chen Lu", "Kasir", "Siang", "Aktif"],
            ["EMP004", "Liu Han", "Pelayan", "Siang", "Libur"]
        ]
        
        self.create_table(["ID", "Nama", "Posisi", "Shift", "Status"], employees_data)
        
    def create_finance_page(self):
        """Create finance page"""
        tk.Label(self.main_content, text="💰 Keuangan", font=self.fonts['title'],
                fg=self.colors['primary_red'], bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        finance_data = [
            ["03/10/2024", "Rp 2,450,000", "Rp 800,000", "Rp 1,650,000", "Tunai"],
            ["02/10/2024", "Rp 2,200,000", "Rp 750,000", "Rp 1,450,000", "Tunai"],
            ["01/10/2024", "Rp 2,800,000", "Rp 900,000", "Rp 1,900,000", "Campuran"]
        ]
        
        self.create_table(["Tanggal", "Pemasukan", "Pengeluaran", "Profit", "Metode"], finance_data)
        
    def create_reports_page(self):
        """Create reports page"""
        tk.Label(self.main_content, text="📈 Laporan", font=self.fonts['title'],
                fg=self.colors['primary_red'], bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        reports_data = [
            ["Nasi Goreng Special", "45", "Rp 1,575,000", "Nasi", "⭐⭐⭐⭐⭐"],
            ["Ayam Kung Pao", "32", "Rp 1,440,000", "Ayam", "⭐⭐⭐⭐"],
            ["Mie Ayam Canton", "28", "Rp 840,000", "Mie", "⭐⭐⭐⭐"],
            ["Es Teh Manis", "67", "Rp 536,000", "Minuman", "⭐⭐⭐⭐⭐"]
        ]
        
        self.create_table(["Menu", "Terjual", "Pendapatan", "Kategori", "Popularitas"], reports_data)
        
    def create_settings_page(self):
        """Create settings page"""
        tk.Label(self.main_content, text="⚙️ Pengaturan", font=self.fonts['title'],
                fg=self.colors['primary_red'], bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        settings_text = """Pengaturan sistem ERP Golden Dragon Wok:

• Konfigurasi database
• Pengaturan printer
• Manajemen pengguna
• Backup data
• Tema aplikasi
• Notifikasi"""
        
        tk.Label(self.main_content, text=settings_text, font=self.fonts['entry'],
                fg=self.colors['black'], bg=self.colors['white'], justify='left').pack(anchor='w')
        
    def create_table(self, headers, data):
        """Create a table with given headers and data"""
        # Table frame
        table_frame = tk.Frame(self.main_content, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True)
        
        # Create Treeview
        tree = ttk.Treeview(table_frame, columns=headers, show='headings', height=15)
        
        # Define headings
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, width=150, anchor='center')
            
        # Insert data
        for row in data:
            tree.insert('', 'end', values=row)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def logout(self):
        """Logout and return to login screen"""
        # Konfirmasi logout
        result = messagebox.askyesno("Konfirmasi Logout", 
                                   "Apakah Anda yakin ingin logout?",
                                   icon='question')
        
        if result:
            # Clear user session
            user_manager.logout()
            
            # Clear all main window widgets
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Reset window properties
            self.root.geometry("800x900")
            self.root.title("Golden Dragon Wok - ERP System")
            
            # Recreate login window
            self.create_login_window()
            
            # Show success message
            messagebox.showinfo("Logout Berhasil", 
                               "Session telah dibersihkan.\nSilakan login kembali.")
        
    def run(self):
        """Run the application with macOS optimizations"""
        # Final macOS optimizations
        self.root.update_idletasks()
        self.root.deiconify()  # Ensure window is visible
        
        # Start the main loop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

if __name__ == "__main__":
    app = GoldenDragonERP()
    app.run()