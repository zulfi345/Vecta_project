from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# ======================
# SCREEN
# ======================
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.goto_home, 2)

    def goto_home(self, dt):
        self.manager.current = 'home'


class HomeScreen(Screen):
    pass


# ======================
# KV DESIGN
# ======================
KV = '''
ScreenManager:
    SplashScreen:
    HomeScreen:

<SplashScreen>:
    name: 'splash'

    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 40

        Image:
            source: 'logo.png'

        Label:
            text: '[b]VECTA PROJECT[/b]'
            markup: True
            font_size: '30sp'

        Label:
            text: 'Loading...'
            font_size: '16sp'


<HomeScreen>:
    name: 'home'

    BoxLayout:
        orientation: 'vertical'

        # ================= HEADER =================
        BoxLayout:
            size_hint_y: 0.2
            padding: 10
            spacing: 10
            canvas.before:
                Color:
                    rgba: 0.1, 0.3, 0.5, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            # LEFT (Nama toko)
            BoxLayout:
                orientation: 'vertical'

                Label:
                    text: 'VECTA JAYA GROUP'
                    bold: True
                    color: 1,1,1,1

                Label:
                    text: 'Jl. Contoh Alamat No.1'
                    font_size: '12sp'
                    color: 1,1,1,1

            # RIGHT (Menu 3 garis)
            Button:
                text: '☰'
                size_hint_x: 0.2
                on_press: app.menu()

        # ================= CONTENT =================
        BoxLayout:
            padding: 20

            Label:
                text: 'Selamat Datang di Aplikasi Kasir'
'''


# ======================
# APP
# ======================
class VectaKasirApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        return Builder.load_string(KV)

    def menu(self):
        print("Menu diklik!")


if __name__ == "__main__":
    VectaKasirApp().run()
