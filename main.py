from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from plyer import filechooser
import sqlite3

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
    conn.commit()
    conn.close()

# ================= SCREEN =================
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.goto_home, 2)

    def goto_home(self, dt):
        self.manager.current = 'home'

class HomeScreen(Screen):
    pass

class ProdukScreen(Screen):
    def on_enter(self):
        self.load_produk()

    def load_produk(self):
        self.ids.produk_list.clear_widgets()

        conn = sqlite3.connect('produk.db')
        c = conn.cursor()
        data = c.execute("SELECT * FROM produk").fetchall()
        conn.close()

        for item in data:
            nama, harga, gambar = item[1], item[2], item[3]

            self.ids.produk_list.add_widget(
                Builder.load_string(f'''
BoxLayout:
    size_hint_y: None
    height: 120
    spacing: 10

    Image:
        source: '{gambar if gambar else ""}'

    BoxLayout:
        orientation: 'vertical'

        Label:
            text: '{nama}'
        Label:
            text: 'Rp {harga}'

    Button:
        text: '+'
    Button:
        text: '-'
'''))

    def pilih_gambar(self):
        filechooser.open_file(on_selection=self.set_gambar)

    def set_gambar(self, selection):
        if selection:
            self.ids.img_preview.source = selection[0]
            self.selected_image = selection[0]

    def tambah_produk(self):
        nama = self.ids.input_nama.text
        harga = self.ids.input_harga.text
        gambar = getattr(self, 'selected_image', '')

        conn = sqlite3.connect('produk.db')
        c = conn.cursor()
        c.execute("INSERT INTO produk (nama,harga,gambar) VALUES (?,?,?)",
                  (nama, harga, gambar))
        conn.commit()
        conn.close()

        self.load_produk()

# ================= KV =================
KV = '''
ScreenManager:
    SplashScreen:
    HomeScreen:
    ProdukScreen:

<SplashScreen>:
    name: 'splash'
    BoxLayout:
        orientation: 'vertical'
        spacing: 20

        Image:
            source: 'logo.png'

        Label:
            text: 'VECTA PROJECT'
            font_size: '28sp'

<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: 'Beranda'

        BoxLayout:
            size_hint_y: 0.1

            Button:
                text: 'Home'
                on_press: app.root.current = 'home'
            Button:
                text: 'Produk'
                on_press: app.root.current = 'produk'
            Button:
                text: 'Kasir'
            Button:
                text: 'Laporan'

<ProdukScreen>:
    name: 'produk'

    BoxLayout:
        orientation: 'vertical'

        # === INPUT PRODUK ===
        TextInput:
            id: input_nama
            hint_text: 'Nama Produk'

        TextInput:
            id: input_harga
            hint_text: 'Harga'

        Image:
            id: img_preview
            size_hint_y: 0.3

        Button:
            text: 'Pilih Gambar'
            on_press: root.pilih_gambar()

        Button:
            text: 'Tambah Produk'
            on_press: root.tambah_produk()

        # === LIST PRODUK ===
        ScrollView:
            BoxLayout:
                id: produk_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

        # === MENU BAWAH ===
        BoxLayout:
            size_hint_y: 0.1

            Button:
                text: 'Home'
                on_press: app.root.current = 'home'
            Button:
                text: 'Produk'
            Button:
                text: 'Kasir'
            Button:
                text: 'Laporan'
'''

# ================= APP =================
class VectaApp(App):
    def build(self):
        init_db()
        Window.clearcolor = (1,1,1,1)
        return Builder.load_string(KV)

if __name__ == "__main__":
    VectaApp().run()
