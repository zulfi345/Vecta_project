from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button

from plyer import filechooser

import sqlite3
import os
import shutil
from datetime import datetime

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('kasir.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            harga INTEGER,
            gambar TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            total INTEGER
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS setting (
            id INTEGER PRIMARY KEY,
            nama_toko TEXT
        )
    ''')

    c.execute("INSERT OR IGNORE INTO setting (id, nama_toko) VALUES (1, 'VECTA KASIR')")

    conn.commit()
    conn.close()

# ================= SCREEN =================
class MainScreen(Screen):
    total = 0

    def on_enter(self):
        self.load_toko()
        self.load_produk()

    def load_toko(self):
        conn = sqlite3.connect('kasir.db')
        c = conn.cursor()
        nama = c.execute("SELECT nama_toko FROM setting WHERE id=1").fetchone()[0]
        conn.close()
        self.ids.nama_toko.text = nama

    def load_produk(self):
        self.ids.produk_grid.clear_widgets()
        self.total = 0
        self.update_total()

        conn = sqlite3.connect('kasir.db')
        c = conn.cursor()
        data = c.execute("SELECT * FROM produk").fetchall()
        conn.close()
    for item in data:
    nama, harga, gambar = item[1], item[2], item[3]

    box = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=280,
        padding=8,
        spacing=5
    )

    # 🔥 background rounded
    with box.canvas.before:
        Color(1,1,1,1)
        box.rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[15])

    def update_rect(instance, value):
        box.rect.pos = instance.pos
        box.rect.size = instance.size

    box.bind(pos=update_rect, size=update_rect)

    # 🔥 gambar
    img = Image(
        source=gambar if gambar else "",
        size_hint_y=None,
        height=140
    )
    box.add_widget(img)

    # 🔥 nama
    box.add_widget(Label(text=nama, bold=True))

    # 🔥 harga
    box.add_widget(Label(
        text=f"Rp {harga}",
        color=(0.2,0.6,0.2,1)
    ))

    # 🔥 qty
    qty = TextInput(text='0', size_hint_y=None, height=40)

    def tambah(x, harga=harga, qty=qty):
        val = int(qty.text)
        val += 1
        qty.text = str(val)
        self.total += harga
        self.update_total()

    def kurang(x, harga=harga, qty=qty):
        val = int(qty.text)
        if val > 0:
            val -= 1
            qty.text = str(val)
            self.total -= harga
            self.update_total()

    row = BoxLayout(size_hint_y=None, height=40)

    btn_minus = Button(text='-')
    btn_plus = Button(text='+')

    btn_minus.bind(on_press=kurang)
    btn_plus.bind(on_press=tambah)

    row.add_widget(btn_minus)
    row.add_widget(qty)
    row.add_widget(btn_plus)

    box.add_widget(row)

    self.ids.produk_grid.add_widget(box)

            

    def update_total(self):
        self.ids.total_label.text = f"Total: Rp {self.total}"

    def bayar(self):
        conn = sqlite3.connect('kasir.db')
        c = conn.cursor()

        c.execute("INSERT INTO transaksi (tanggal,total) VALUES (?,?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M"), self.total))

        conn.commit()
        conn.close()

        popup = Popup(
            title='Struk',
            content=Label(text=f"Total Bayar: Rp {self.total}"),
            size_hint=(0.8,0.5)
        )
        popup.open()

        self.total = 0
        self.update_total()

    def ganti_nama(self):
        def simpan(instance):
            conn = sqlite3.connect('kasir.db')
            c = conn.cursor()
            c.execute("UPDATE setting SET nama_toko=?", (input_nama.text,))
            conn.commit()
            conn.close()
            self.load_toko()
            popup.dismiss()

        input_nama = TextInput()
        btn = Button(text="Simpan", on_press=simpan)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(input_nama)
        layout.add_widget(btn)

        popup = Popup(title="Nama Toko", content=layout, size_hint=(0.8,0.5))
        popup.open()

    def pilih_gambar(self):
        filechooser.open_file(on_selection=self.set_gambar)

    def set_gambar(self, selection):
        if selection:
            path = selection[0]
            new_path = os.path.join('.', os.path.basename(path))
            if not os.path.exists(new_path):
                shutil.copy(path, new_path)
            self.selected_image = new_path

    def tambah_produk(self):
        nama = self.ids.input_nama.text
        harga = self.ids.input_harga.text
        gambar = getattr(self, 'selected_image', '')

        if not nama or not harga.isdigit():
            return

        conn = sqlite3.connect('kasir.db')
        c = conn.cursor()
        c.execute("INSERT INTO produk (nama,harga,gambar) VALUES (?,?,?)",
                  (nama, int(harga), gambar))
        conn.commit()
        conn.close()

        self.load_produk()

# ================= UI =================
KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'

    BoxLayout:
        orientation: 'vertical'
        spacing: 10

        # ================= HEADER =================
        BoxLayout:
            size_hint_y: 0.15
            padding: 10
            spacing: 10
            canvas.before:
                Color:
                    rgba: 0.1,0.2,0.35,1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Image:
                source: 'icon.png'
                size_hint_x: 0.2

            BoxLayout:
                orientation: 'vertical'

                Label:
                    id: nama_toko
                    text: 'VECTA KASIR'
                    color: 1,1,1,1
                    bold: True

                Label:
                    text: 'Alamat toko'
                    color: 1,1,1,0.7
                    font_size: 12

            Button:
                text: '☰'
                size_hint_x: 0.2
                on_press: root.ganti_nama()

        # ================= PRODUK =================
        ScrollView:
            GridLayout:
                id: produk_grid
                cols: 2
                spacing: 10
                padding: 10
                size_hint_y: None
                height: self.minimum_height

        # ================= TOTAL =================
        BoxLayout:
            size_hint_y: 0.1
            padding: 10
            spacing: 10

            Label:
                id: total_label
                text: 'Total: Rp 0'
                bold: True

            Button:
                text: 'Bayar'
                background_color: 0.1,0.3,0.6,1
                on_press: root.bayar()

        # ================= NAVBAR =================
        BoxLayout:
            size_hint_y: 0.1
            spacing: 5

            Button:
                text: '🏠\nHome'

            Button:
                text: '📦\nProduk'

            Button:
                text: '🛒\nKasir'

            Button:
                text: '📊\nLaporan'
'''

# ================= APP =================
class VectaApp(App):
    def build(self):
        init_db()
        Window.clearcolor = (1,1,1,1)
        return Builder.load_string(KV)

if __name__ == "__main__":
    VectaApp().run()
