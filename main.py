from ctypes import c_float
from typing import Text

import compile_c_code
import kivy
from kivy.event import EventDispatcher
from kivy.app import App
from kivy.uix.label import Label

game = compile_c_code.compile_c_file("./game.c")


class State(EventDispatcher):
    pass

class MyApp(App):
    def build(self):
        return Label(text="nice")




MyApp().run()