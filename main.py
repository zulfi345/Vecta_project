from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from plyer import filechooser

import sqlite3, os, shutil, csv
from datetime import datetime

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('kasir.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS produk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT, harga INTEGER, gambar TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal TEXT, total INTEGER, detail TEXT)''')

    c.execute("INSERT OR IGNORE INTO user VALUES (1,'admin','1234')")

    conn.commit()
    conn.close()

# ================= LOGIN =================
class LoginScreen(Screen):
    def login(self):
        u = self.ids.user.text
        p = self.ids.passw.text

        conn = sqlite3.connect('kasir.db')
        data = conn.execute("SELECT * FROM user WHERE username=? AND password=?", (u,p)).fetchone()
        conn.close()

        if data:
            self.manager.current = 'main'
        else:
            Popup(title="Error", content=Label(text="Login gagal"), size_hint=(0.6,0.4)).open()

# ================= MAIN =================
class MainScreen(Screen):
    total = 0
    keranjang = []

    def on_enter(self):
        self.load_produk()

    def load_produk(self):
        self.ids.grid.clear_widgets()
        self.total = 0
        self.keranjang = []
        self.update_total()

        conn = sqlite3.connect('kasir.db')
        data = conn.execute("SELECT * FROM produk").fetchall()
        conn.close()

        for item in data:
            nama, harga, gambar = item[1], item[2], item[3]

            box = BoxLayout(orientation='vertical', size_hint_y=None, height=280)

            img = Image(source=gambar if gambar else "")
            box.add_widget(img)

            box.add_widget(Label(text=nama))
            box.add_widget(Label(text=f"Rp {harga}"))

            qty = TextInput(text='0', input_filter='int')

            def tambah(x):
                qty.text = str(int(qty.text)+1)
                self.total += harga
                self.keranjang.append((nama,harga))
                self.update_total()

            def kurang(x):
                if int(qty.text)>0:
                    qty.text = str(int(qty.text)-1)
                    self.total -= harga
                    self.update_total()

            row = BoxLayout(size_hint_y=None, height=40)
            b1 = Button(text='-')
            b2 = Button(text='+')
            b1.bind(on_press=kurang)
            b2.bind(on_press=tambah)

            row.add_widget(b1)
            row.add_widget(qty)
            row.add_widget(b2)

            box.add_widget(row)
            self.ids.grid.add_widget(box)

    def update_total(self):
        self.ids.total.text = f"Total: {self.total}"

    # ================= BAYAR =================
    def bayar(self):
        detail = "\n".join([f"{n} - {h}" for n,h in self.keranjang])

        conn = sqlite3.connect('kasir.db')
        conn.execute("INSERT INTO transaksi VALUES (NULL,?,?,?)",
                     (datetime.now().strftime("%Y-%m-%d"), self.total, detail))
        conn.commit()
        conn.close()

        Popup(title="Struk", content=Label(text=detail), size_hint=(0.8,0.6)).open()

        self.print_bluetooth(detail)

        self.load_produk()

    # ================= BLUETOOTH PRINT =================
    def print_bluetooth(self, text):
        try:
            import bluetooth
            devices = bluetooth.discover_devices()
            if devices:
                addr = devices[0]
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((addr,1))
                sock.send(text)
                sock.close()
        except:
            print("Printer tidak tersedia")

    # ================= TAMBAH PRODUK =================
    def pilih_gambar(self):
        filechooser.open_file(on_selection=self.set_img)

    def set_img(self, sel):
        if sel:
            path = sel[0]
            new = os.path.basename(path)
            shutil.copy(path,new)
            self.img = new

    def tambah(self):
        nama = self.ids.nama.text
        harga = self.ids.harga.text

        conn = sqlite3.connect('kasir.db')
        conn.execute("INSERT INTO produk VALUES (NULL,?,?,?)",
                     (nama,int(harga),getattr(self,'img','')))
        conn.commit()
        conn.close()

        self.load_produk()

    # ================= LAPORAN =================
    def laporan(self):
        conn = sqlite3.connect('kasir.db')
        data = conn.execute("SELECT total FROM transaksi").fetchall()
        conn.close()

        popup = Popup(title="Grafik", size_hint=(0.8,0.6))
        box = BoxLayout()

        with box.canvas:
            Color(0,0,1,1)
            x = 10
            for d in data:
                Line(points=[x,10,x,10+d[0]/100])
                x += 30

        popup.content = box
        popup.open()

    def export(self):
        conn = sqlite3.connect('kasir.db')
        data = conn.execute("SELECT * FROM transaksi").fetchall()
        conn.close()

        with open("laporan.csv","w") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def backup(self):
        shutil.copy("kasir.db","backup.db")

# ================= UI =================
KV = '''
ScreenManager:
    LoginScreen:
    MainScreen:

<LoginScreen>:
    name:'login'
    BoxLayout:
        orientation:'vertical'
        TextInput:
            id:user
            hint_text:'Username'
        TextInput:
            id:passw
            hint_text:'Password'
        Button:
            text:'Login'
            on_press:root.login()

<MainScreen>:
    name:'main'
    BoxLayout:
        orientation:'vertical'

        BoxLayout:
            TextInput:
                id:nama
                hint_text:'Nama'
            TextInput:
                id:harga
                hint_text:'Harga'

        Button:
            text:'Pilih Gambar'
            on_press:root.pilih_gambar()

        Button:
            text:'Tambah Produk'
            on_press:root.tambah()

        ScrollView:
            GridLayout:
                id:grid
                cols:2
                size_hint_y:None
                height:self.minimum_height

        Label:
            id:total
            text:'Total: 0'

        Button:
            text:'Bayar'
            on_press:root.bayar()

        BoxLayout:
            Button:
                text:'Grafik'
                on_press:root.laporan()
            Button:
                text:'Export'
                on_press:root.export()
            Button:
                text:'Backup'
                on_press:root.backup()
'''

class VectaApp(App):
    def build(self):
        init_db()
        Window.clearcolor=(1,1,1,1)
        return Builder.load_string(KV)

VectaApp().run()
