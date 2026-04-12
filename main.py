from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

import sqlite3
import os

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('produk.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            harga INTEGER,
            gambar TEXT
        )
    ''')

    # DATA CONTOH (biar langsung tampil)
    if not c.execute("SELECT * FROM produk").fetchone():
        c.execute("INSERT INTO produk (nama,harga,gambar) VALUES ('Ayam Goreng',15000,'')")
        c.execute("INSERT INTO produk (nama,harga,gambar) VALUES ('Nasi Putih',5000,'')")
        c.execute("INSERT INTO produk (nama,harga,gambar) VALUES ('Sambal Ayam',20000,'')")
        c.execute("INSERT INTO produk (nama,harga,gambar) VALUES ('Sambal Tempe',10000,'')")

    conn.commit()
    conn.close()

# ================= SCREEN =================
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.goto_home, 2)

    def goto_home(self, dt):
        self.manager.current = 'home'

class HomeScreen(Screen):
    total = 0

    def on_enter(self):
        self.load_produk()

    def load_produk(self):
        self.ids.produk_list.clear_widgets()
        self.total = 0
        self.update_total()

        conn = sqlite3.connect('produk.db')
        c = conn.cursor()
        data = c.execute("SELECT * FROM produk").fetchall()
        conn.close()

        for item in data:
            nama, harga, gambar = item[1], item[2], item[3]

            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=250,
                padding=10,
                spacing=5
            )

            # CARD STYLE
            with card.canvas.before:
                Color(1,1,1,1)
                rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[20])

            def update_rect(instance, value):
                rect.pos = instance.pos
                rect.size = instance.size

            card.bind(pos=update_rect, size=update_rect)

            # IMAGE
            if gambar and os.path.exists(gambar):
                img = Image(source=gambar, size_hint_y=0.6)
            else:
                img = Image(size_hint_y=0.6)

            card.add_widget(img)

            # NAMA
            card.add_widget(Label(text=nama, size_hint_y=0.2))

            # HARGA
            card.add_widget(Label(text=f"Rp {harga}", size_hint_y=0.2))

            # TOMBOL +
            def tambah(instance, harga=harga):
                self.total += harga
                self.update_total()

            btn = Button(
                text="+",
                size_hint=(None,None),
                size=(40,40),
                pos_hint={"right":1}
            )
            btn.bind(on_press=tambah)
            card.add_widget(btn)

            self.ids.produk_list.add_widget(card)

    def update_total(self):
        self.ids.total_label.text = f"Total: Rp {self.total}"

# ================= KV =================
KV = '''
#:import dp kivy.metrics.dp

ScreenManager:
    SplashScreen:
    HomeScreen:

<SplashScreen>:
    name: 'splash'

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)

        canvas.before:
            Color:
                rgba: 0.1,0.2,0.4,1
            Rectangle:
                pos: self.pos
                size: self.size

        Image:
            source: 'logo.png'

        Label:
            text: 'VECTA PROJECT'
            font_size: '28sp'
            color: 1,1,1,1

<HomeScreen>:
    name: 'home'

    BoxLayout:
        orientation: 'vertical'

        # ===== BACKGROUND =====
        canvas.before:
            Color:
                rgba: 0.95,0.95,0.95,1
            Rectangle:
                pos: self.pos
                size: self.size

        # ===== HEADER =====
        BoxLayout:
            size_hint_y: None
            height: dp(80)
            padding: dp(10)

            canvas.before:
                Color:
                    rgba: 0.1,0.2,0.4,1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: 'VECTA KASIR'
                color: 1,1,1,1
                font_size: '18sp'

        # ===== GRID PRODUK =====
        ScrollView:
            GridLayout:
                id: produk_list
                cols: 2
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height

        # ===== TOTAL + BAYAR =====
        BoxLayout:
            size_hint_y: None
            height: dp(70)
            padding: dp(10)
            spacing: dp(10)

            canvas.before:
                Color:
                    rgba: 1,1,1,1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [20]

            Label:
                id: total_label
                text: 'Total: Rp 0'

            Button:
                text: 'Bayar'
                size_hint_x: 0.4
                background_color: 0.1,0.2,0.4,1

        # ===== NAVBAR =====
        BoxLayout:
            size_hint_y: None
            height: dp(70)

            Button:
                text: '🏠\\nHome'
            Button:
                text: '⬛\\nProduk'
            Button:
                text: '🛒\\nTransaksi'
            Button:
                text: '📊\\nLaporan'
'''

# ================= APP =================
class VectaApp(App):
    def build(self):
        init_db()
        Window.clearcolor = (1,1,1,1)
        return Builder.load_string(KV)

if __name__ == "__main__":
    VectaApp().run()
