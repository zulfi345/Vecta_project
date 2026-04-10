"""
VECTA KASIR - Versi Sederhana
Aplikasi kasir dengan menu makanan
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import sqlite3
from datetime import datetime

# === DATABASE ===
def init_database():
    conn = sqlite3.connect('vecta_kasir.db')
    cursor = conn.cursor()
    
    # Tabel produk
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            harga INTEGER NOT NULL,
            stok INTEGER DEFAULT 0,
            tersedia INTEGER DEFAULT 1
        )
    ''')
    
    # Tabel karyawan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS karyawan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'kasir'
        )
    ''')
    
    # Tabel transaksi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            total INTEGER NOT NULL,
            kasir_id INTEGER NOT NULL,
            FOREIGN KEY (kasir_id) REFERENCES karyawan (id)
        )
    ''')
    
    # Tabel detail transaksi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detail_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaksi_id INTEGER NOT NULL,
            produk_id INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            harga_satuan INTEGER NOT NULL,
            subtotal INTEGER NOT NULL,
            FOREIGN KEY (transaksi_id) REFERENCES transaksi (id),
            FOREIGN KEY (produk_id) REFERENCES produk (id)
        )
    ''')
    
    # Cek apakah ada produk, jika tidak tambahkan contoh
    cursor.execute("SELECT COUNT(*) FROM produk")
    if cursor.fetchone()[0] == 0:
        contoh_produk = [
            ('VEGETARIAN MENU', 15000, 100),
            ('VEDIC CHICKEN', 8000, 100),
            ('VEDIC RICE', 10000, 100),
            ('SAMBHAR KORMA', 12000, 100),
            ('SAMBHAR LAMB', 13000, 100),
            ('TANDOORI MASALA', 15000, 100),
        ]
        cursor.executemany("INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)", contoh_produk)
    
    # Cek apakah ada admin, jika tidak tambahkan
    cursor.execute("SELECT COUNT(*) FROM karyawan")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO karyawan (nama, username, password, role) VALUES (?, ?, ?, ?)",
                      ('Administrator', 'admin', 'admin', 'admin'))
        cursor.execute("INSERT INTO karyawan (nama, username, password, role) VALUES (?, ?, ?, ?)",
                      ('Kasir 1', 'kasir1', 'kasir1', 'kasir'))
    
    conn.commit()
    conn.close()

# === SCREEN LOGIN ===
class LoginScreen(Screen):
    def do_login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        
        conn = sqlite3.connect('vecta_kasir.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama, username, role FROM karyawan WHERE username=? AND password=?", 
                      (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            app = App.get_running_app()
            app.kasir_aktif = {
                'id': user[0],
                'nama': user[1],
                'username': user[2],
                'role': user[3]
            }
            self.manager.current = 'menu'
        else:
            self.ids.error_label.text = "Username atau password salah!"

# === SCREEN MENU ===
class MenuScreen(Screen):
    def on_enter(self):
        self.load_products()
        self.update_kasir_info()
    
    def load_products(self):
        conn = sqlite3.connect('vecta_kasir.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama, harga FROM produk WHERE tersedia=1")
        products = cursor.fetchall()
        conn.close()
        
        grid = self.ids.product_grid
        grid.clear_widgets()
        
        for p in products:
            item = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=5, padding=10)
            
            nama = Label(text=p[1], font_size='16sp', bold=True, size_hint_y=0.4)
            harga = Label(text=f"Rp {p[2]:,}", font_size='14sp', size_hint_y=0.3)
            
            btn = Button(text='+ Beli', size_hint_y=0.3, background_color=(0.2, 0.6, 0.2, 1))
            btn.product_id = p[0]
            btn.product_name = p[1]
            btn.product_price = p[2]
            btn.bind(on_press=self.add_to_cart)
            
            item.add_widget(nama)
            item.add_widget(harga)
            item.add_widget(btn)
            grid.add_widget(item)
    
    def update_kasir_info(self):
        app = App.get_running_app()
        if hasattr(app, 'kasir_aktif'):
            self.ids.kasir_label.text = f"Kasir: {app.kasir_aktif['nama']}"
    
    def add_to_cart(self, instance):
        app = App.get_running_app()
        if not hasattr(app, 'cart'):
            app.cart = []
        
        for item in app.cart:
            if item['id'] == instance.product_id:
                item['qty'] += 1
                self.show_message(f"{instance.product_name} jumlah ditambah")
                return
        
        app.cart.append({
            'id': instance.product_id,
            'nama': instance.product_name,
            'harga': instance.product_price,
            'qty': 1
        })
        self.show_message(f"{instance.product_name} ditambahkan")
    
    def show_message(self, msg):
        from kivy.uix.popup import Popup
        popup = Popup(title='Info', content=Label(text=msg), size_hint=(0.6, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
    
    def go_to_cart(self):
        self.manager.current = 'cart'
    
    def go_to_products(self):
        self.manager.current = 'products'
    
    def logout(self):
        App.get_running_app().cart = []
        self.manager.current = 'login'

# === SCREEN KERANJANG ===
class CartScreen(Screen):
    def on_enter(self):
        self.load_cart()
    
    def load_cart(self):
        app = App.get_running_app()
        self.cart_items = getattr(app, 'cart', [])
        
        list_widget = self.ids.cart_list
        list_widget.clear_widgets()
        
        total = 0
        for item in self.cart_items:
            subtotal = item['harga'] * item['qty']
            total += subtotal
            
            item_widget = BoxLayout(size_hint_y=None, height=50, spacing=10)
            item_widget.add_widget(Label(text=item['nama'], size_hint_x=0.4))
            item_widget.add_widget(Label(text=f"Rp {item['harga']:,}", size_hint_x=0.2))
            
            btn_minus = Button(text='-', size_hint_x=0.1)
            btn_minus.item_id = item['id']
            btn_minus.bind(on_press=self.decrease_qty)
            
            qty_label = Label(text=str(item['qty']), size_hint_x=0.1)
            item_widget.qty_label = qty_label
            
            btn_plus = Button(text='+', size_hint_x=0.1)
            btn_plus.item_id = item['id']
            btn_plus.bind(on_press=self.increase_qty)
            
            item_widget.add_widget(btn_minus)
            item_widget.add_widget(qty_label)
            item_widget.add_widget(btn_plus)
            item_widget.add_widget(Label(text=f"Rp {subtotal:,}", size_hint_x=0.2))
            
            list_widget.add_widget(item_widget)
        
        self.ids.total_label.text = f"Total: Rp {total:,}"
        app.total_bayar = total
    
    def increase_qty(self, instance):
        app = App.get_running_app()
        for item in app.cart:
            if item['id'] == instance.item_id:
                item['qty'] += 1
                break
        self.load_cart()
    
    def decrease_qty(self, instance):
        app = App.get_running_app()
        for i, item in enumerate(app.cart):
            if item['id'] == instance.item_id:
                item['qty'] -= 1
                if item['qty'] <= 0:
                    app.cart.pop(i)
                break
        self.load_cart()
    
    def checkout(self):
        app = App.get_running_app()
        if not hasattr(app, 'cart') or len(app.cart) == 0:
            self.show_message("Keranjang kosong!")
            return
        
        conn = sqlite3.connect('vecta_kasir.db')
        cursor = conn.cursor()
        
        # Simpan transaksi
        cursor.execute("INSERT INTO transaksi (tanggal, total, kasir_id) VALUES (?, ?, ?)",
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), app.total_bayar, app.kasir_aktif['id']))
        transaksi_id = cursor.lastrowid
        
        # Simpan detail
        for item in app.cart:
            cursor.execute("INSERT INTO detail_transaksi (transaksi_id, produk_id, qty, harga_satuan, subtotal) VALUES (?, ?, ?, ?, ?)",
                          (transaksi_id, item['id'], item['qty'], item['harga'], item['harga'] * item['qty']))
        
        conn.commit()
        conn.close()
        
        # Cetak struk
        self.print_struk(transaksi_id)
        
        # Kosongkan keranjang
        app.cart = []
        self.manager.current = 'menu'
    
    def print_struk(self, transaksi_id):
        conn = sqlite3.connect('vecta_kasir.db')
        cursor = conn.cursor()
        cursor.execute("SELECT tanggal, total FROM transaksi WHERE id=?", (transaksi_id,))
        transaksi = cursor.fetchone()
        
        struk = "="*30 + "\n"
        struk += "   VECTA KASIR\n"
        struk += "="*30 + "\n"
        struk += f"Tanggal: {transaksi[0]}\n"
        struk += f"Kasir: {App.get_running_app().kasir_aktif['nama']}\n"
        struk += "-"*30 + "\n"
        
        cursor.execute("""
            SELECT p.nama, d.qty, d.harga_satuan, d.subtotal 
            FROM detail_transaksi d 
            JOIN produk p ON d.produk_id = p.id 
            WHERE d.transaksi_id=?
        """, (transaksi_id,))
        
        for item in cursor.fetchall():
            struk += f"{item[0][:15]:15} {item[1]:>3} x Rp{item[2]:>8,} = Rp{item[3]:>10,}\n"
        
        struk += "-"*30 + "\n"
        struk += f"TOTAL: Rp {transaksi[1]:,}\n"
        struk += "="*30 + "\n"
        struk += "Terima kasih!\n"
        
        conn.close()
        
        # Simpan ke file
        with open(f"struk_{transaksi_id}.txt", "w") as f:
            f.write(struk)
        
        self.show_message("Struk tersimpan!\nCek folder aplikasi")
    
    def show_message(self, msg):
        from kivy.uix.popup import Popup
        popup = Popup(title='Info', content=Label(text=msg), size_hint=(0.7, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    
    def back_to_menu(self):
        self.manager.current = 'menu'

# === SCREEN KELOLA PRODUK ===
class ProductsScreen(Screen):
    def on_enter(self):
        self.load_products()
    
    def load_products(self):
        conn = sqlite3.connect('vecta_kasir.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama, harga, stok FROM produk")
        products = cursor.fetchall()
        conn.close()
        
        grid = self.ids.product_list
        grid.clear_widgets()
        
        for p in products:
            item = BoxLayout(size_hint_y=None, height=50, spacing=10)
            item.add_widget(Label(text=p[1], size_hint_x=0.4))
            item.add_widget(Label(text=f"Rp {p[2]:,}", size_hint_x=0.2))
            item.add_widget(Label(text=f"Stok: {p[3]}", size_hint_x=0.2))
            
            btn_edit = Button(text='Edit', size_hint_x=0.1, background_color=(0.3, 0.5, 0.8, 1))
            btn_edit.product = p
            btn_edit.bind(on_press=self.edit_product)
            
            btn_delete = Button(text='Hapus', size_hint_x=0.1, background_color=(0.8, 0.3, 0.3, 1))
            btn_delete.product_id = p[0]
            btn_delete.bind(on_press=self.delete_product)
            
            item.add_widget(btn_edit)
            item.add_widget(btn_delete)
            grid.add_widget(item)
    
    def add_product(self):
        self.show_product_dialog()
    
    def edit_product(self, instance):
        self.show_product_dialog(instance.product)
    
    def show_product_dialog(self, product=None):
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        nama = TextInput(hint_text='Nama produk', text=product[1] if product else '')
        harga = TextInput(hint_text='Harga', text=str(product[2]) if product else '')
        stok = TextInput(hint_text='Stok', text=str(product[3]) if product else '')
        
        layout.add_widget(nama)
        layout.add_widget(harga)
        layout.add_widget(stok)
        
        btn_layout = BoxLayout(spacing=10)
        btn_simpan = Button(text='Simpan')
        btn_batal = Button(text='Batal')
        
        def simpan(instance):
            conn = sqlite3.connect('vecta_kasir.db')
            cursor = conn.cursor()
            if product:
                cursor.execute("UPDATE produk SET nama=?, harga=?, stok=? WHERE id=?", 
                              (nama.text, int(harga.text), int(stok.text), product[0]))
            else:
                cursor.execute("INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)",
                              (nama.text, int(harga.text), int(stok.text)))
            conn.commit()
            conn.close()
            popup.dismiss()
            self.load_products()
        
        btn_simpan.bind(on_press=simpan)
        btn_batal.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(btn_simpan)
        btn_layout.add_widget(btn_batal)
        layout.add_widget(btn_layout)
        
        popup = Popup(title='Tambah/Edit Produk', content=layout, size_hint=(0.9, 0.5))
        popup.open()
    
    def delete_product(self, instance):
        from kivy.uix.popup import Popup
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(Label(text='Hapus produk ini?'))
        
        btn_layout = BoxLayout(spacing=10)
        btn_ya = Button(text='Ya')
        btn_tidak = Button(text='Tidak')
        
        def confirm(instance):
            conn = sqlite3.connect('vecta_kasir.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produk WHERE id=?", (instance.product_id,))
            conn.commit()
            conn.close()
            popup.dismiss()
            self.load_products()
        
        btn_ya.bind(on_press=confirm)
        btn_tidak.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(btn_ya)
        btn_layout.add_widget(btn_tidak)
        layout.add_widget(btn_layout)
        
        popup = Popup(title='Konfirmasi', content=layout, size_hint=(0.7, 0.3))
        popup.open()
    
    def back_to_menu(self):
        self.manager.current = 'menu'

# === KV LAYOUT ===
KV = '''
ScreenManager:
    LoginScreen:
    MenuScreen:
    CartScreen:
    ProductsScreen:

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 40
        
        Label:
            text: 'VECTA KASIR'
            font_size: '32sp'
            bold: True
        
        TextInput:
            id: username
            hint_text: 'Username'
            multiline: False
        
        TextInput:
            id: password
            hint_text: 'Password'
            password: True
            multiline: False
        
        Button:
            text: 'LOGIN'
            background_color: 0.2,0.7,0.2,1
            on_press: root.do_login()
        
        Label:
            id: error_label
            text: ''
            color: 1,0.3,0.3,1

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: 0.1
            padding: 10
            Label:
                text: 'VECTA'
                font_size: '24sp'
                bold: True
            Label:
                id: kasir_label
                text: 'Kasir: -'
            Button:
                text: 'Logout'
                size_hint_x: 0.2
                on_press: root.logout()
        
        Label:
            text: 'MENU MAKANAN'
            font_size: '18sp'
            size_hint_y: 0.05
        
        ScrollView:
            GridLayout:
                id: product_grid
                cols: 2
                spacing: 10
                padding: 10
                size_hint_y: None
                height: self.minimum_height
        
        BoxLayout:
            size_hint_y: 0.08
            padding: 10
            spacing: 10
            Button:
                text: '🛒 Keranjang'
                on_press: root.go_to_cart()
            Button:
                text: '📦 Kelola Produk'
                on_press: root.go_to_products()

<CartScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: 0.08
            padding: 10
            Button:
                text: '← Kembali'
                size_hint_x: 0.3
                on_press: root.back_to_menu()
            Label:
                text: 'KERANJANG'
                font_size: '20sp'
                bold: True
        
        ScrollView:
            GridLayout:
                id: cart_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
        
        BoxLayout:
            size_hint_y: 0.12
            padding: 10
            spacing: 10
            Label:
                id: total_label
                text: 'Total: Rp 0'
                font_size: '18sp'
                bold: True
            Button:
                text: 'BAYAR'
                background_color: 0.2,0.7,0.2,1
                on_press: root.checkout()

<ProductsScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: 0.08
            padding: 10
            Button:
                text: '← Kembali'
                size_hint_x: 0.3
                on_press: root.back_to_menu()
            Label:
                text: 'KELOLA PRODUK'
                font_size: '20sp'
                bold: True
            Button:
                text: '+ Tambah'
                size_hint_x: 0.3
                on_press: root.add_product()
        
        ScrollView:
            GridLayout:
                id: product_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
'''

# === MAIN APP ===
class VectaKasirApp(App):
    def build(self):
        init_database()
        self.cart = []
        self.kasir_aktif = None
        return Builder.load_string(KV)
    
    def on_start(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

if __name__ == '__main__':
    VectaKasirApp().run()
