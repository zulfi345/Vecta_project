from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class VectaKasirApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        label = Label(text='VECTA KASIR\n\nBerhasil Terinstall!', 
                      font_size='24sp',
                      halign='center')
        
        button = Button(text='OK', size_hint_y=0.3)
        
        layout.add_widget(label)
        layout.add_widget(button)
        
        return layout

if __name__ == '__main__':
    VectaKasirApp().run()
