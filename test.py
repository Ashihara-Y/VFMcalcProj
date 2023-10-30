import flet as ft
from state import State, ReactiveState
from reactive_text import ReactiveText

text = State('')
text1, text2 = text, text
#text2 = State('')

class InfoArea1(ft.UserControl):
    def __init__(self):
        #self.text = State('')
        super().__init__(self)
        self.text_val = ReactiveState(lambda: f'テキストボックスに「{text1.get()}」と入力されています。', [text1])
    
    def build(self):
        return ft.Column([ReactiveText(self.text_val)])
class InfoArea2(ft.UserControl):
    def __init__(self):
        #self.text = State('')
        super().__init__(self)
        self.text_val = ReactiveState(lambda: f'テキストボックスに「{text2.get()}」と入力されています。', [text2])
        #　このReactiveStateは、上記のそれと同じインスタンスで、それぞれに渡しているLambda関数は、
        # 同じReactiveStateに登録されたFormulaになっているのか？
        # ２つめの引数は、RelianceState。このStateが変更されると、第１引数のFormulaが実行されて、Text_valの値が
        # 更新される。この時に、上記とここで、異なるStateを第２引数で渡していて、Formulaも一応異なる。
        # 問題は、Buildで返している部分が同じになっていることか？
    def build(self):
        return ft.Column([ReactiveText(self.text_val)])
    
def main(page: ft.Page):
    page.title = "Flet Test"
    tx1 = ft.TextField(on_change=lambda e: text1.set(e.control.value))
    tx2 = ft.TextField(on_change=lambda e: text2.set(e.control.value))
    ia1 = InfoArea1()
    ia2 = InfoArea2()
    #page.add(ft.Column([ft.TextField(on_change=lambda e: text.set(e.control.value)), InfoArea()]))
    page.add(ft.Column([tx1, tx2, ia1, ia2]))
    
ft.app(target=main)