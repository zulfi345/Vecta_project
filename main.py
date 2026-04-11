from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import sqlite3
from datetime import datetime

# === DATABASE ===
def init_database():
    conn = sqlite3.connect('vecta_kasir.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            harga INTEGER
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM produk")
    if cursor.fetchone()[0] == 0:
        data = [
            ('Nasi Goreng', 15000),
            ('Mie Goreng', 12000),
            ('Ayam Goreng', 20000)
        ]
        cursor.executemany("INSERT INTO produk (nama, harga) VALUES (?,?)", data)

    conn.commit()
    conn.close()

# === SCREEN ===
class MainScreen(Screen):
    pass

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'VECTA KASIR'
            font_size: '30sp'

        Button:
            text: 'Klik Test'
            on_press: app.test()
'''

class VectaKasirApp(App):
    def build(self):
        init_database()
        Window.clearcolor = (0.1,0.1,0.1,1)
        return Builder.load_string(KV)

    def test(self):
        print("App jalan!")

if __name__ == "__main__":
    VectaKasirApp().run()
