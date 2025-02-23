import flet as ft
from state import StateProperty, bind_props, get_prop_value

class ReactiveText(ft.UserControl):
    def __init__(self, text: StateProperty[str]):
        super().__init__()
        self.control = ft.Text('')
        self.text = text

        self.set_props()
        bind_props([self.text], lambda: self.update())

    def set_props(self):
        self.control.value = get_prop_value(self.text)

    def update(self):
        self.set_props()
        self.control.update()

    def build(self):
        return self.control

    