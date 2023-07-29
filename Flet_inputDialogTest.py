import flet as ft
import joblib
#import sqlite3
import pandas as pd
import jgb_rates

#class Initial_Inputs(ft.UserControl):
#    def __init__(self):
#        super().__init__()
    
#    def build(self):
#        return ft.column([])
def main(page: ft.Page):
    
    def button_clicked(e):        
        jgb_rates.JGB_rates_conv()
        JGB_rates_df = pd.read_csv('JGB_rates.csv', sep='\t', encoding='shift_jis', header=None, names=['year', 'rate'])
        #JRB_rates_df = pd.read_csv('JRB_rates.csv', sep='\t', encoding='shift_jis', header=None, names=['year', 'rate'])

        year_select = ['10年', '10年', '10年', '15年', '15年', '15年', '15年', '15年', '20年', '20年', '20年', '20年', '20年', '25年', '25年', '25年', '25年', '25年', '30年', '30年', '30年']

        y = int(dd5.value) - 10
        r_idx = year_select[y]
        r1 = float(JGB_rates_df[JGB_rates_df['year']==r_idx]['rate'].iloc[0])
        #r2 = float(JRB_rates_df[JRB_rates_df['year']==r_idx]['rate'].iloc[0])
        r2 = 0.729

        if dd1.value == '国':
            zei_modori = 27.8
        elif dd1.value == '都道府県':
            zei_modori = 5.78
        elif dd1.value == '市町村':
            zei_modori = 8.4

        Initail_Inputs = {
            "mgmt_type":dd1.value, 
            "proj_ctgry":dd2.value, 
            "proj_type":dd3.value,
            "proj_years":dd4.value,
            "const_years":dd5.value,
            "kijun_kinri":r1,
            "chisai_kinri":r2,
            "zei_modori":zei_modori,
            "lg_spread":1.5,
            "zei_total":41.98,
            "growth":0.0,
            "kitai_bukka":2.0,
            "shisetsu_seibi":2000.0,
            "ijikanri_unnei":50.0,
            "reduc_shisetsu":90.0,
            "reduc_ijikanri":90.0,
            "pre_kyoukouka":False,
            "kisai_jutou":0.0,
            "kisai_koufu":0.0,
            "zeimae_rieki":8.5,
            "SPC_keihi":15.0,
            "hojo":0.0
            }
        
        joblib.dump(Initail_Inputs, 'Initial_Inputs.pkl')
        page.client_storage.set("Initial_Inputs", Initail_Inputs)


    dd1 = ft.Dropdown(
        label="管理者の種別",
        hint_text="管理者の種別を選択してください", 
        width=400,
        options=[
            ft.dropdown.Option("国"),
            ft.dropdown.Option("都道府県"),
            ft.dropdown.Option("市町村"),
        ],
    )
 
    dd2 = ft.Dropdown(
        label="事業の方式",
        hint_text="事業の方式を選択してください", 
        width=400,
        options=[
            ft.dropdown.Option("サービス購入型"),
            #ft.dropdown.Option("独立採算型"),
            #ft.dropdown.Option("混合型"),
        ],
    )
    
    dd3 = ft.Dropdown(
        label="事業の類型",
        hint_text="事業の類型を選択してください", 
        width=400,
        options=[
            ft.dropdown.Option("BTO"),
            #ft.dropdown.Option("BOT"),
            #ft.dropdown.Option("BT"),
        ],
    )

    dd4 = ft.Dropdown(
        label="事業期間",
        hint_text="事業期間を選択してください", 
        width=400,
        value="20",
        options=[
            ft.dropdown.Option("10"),
            ft.dropdown.Option("11"),#ft.dropdown.Option("BOT"),
            ft.dropdown.Option("12"),#ft.dropdown.Option("BT"),
            ft.dropdown.Option("13"),
            ft.dropdown.Option("14"),
            ft.dropdown.Option("15"),
            ft.dropdown.Option("16"),
            ft.dropdown.Option("17"),
            ft.dropdown.Option("18"),
            ft.dropdown.Option("19"),
            ft.dropdown.Option("20"),
            ft.dropdown.Option("21"),
            ft.dropdown.Option("22"),
            ft.dropdown.Option("23"),
            ft.dropdown.Option("24"),
            ft.dropdown.Option("25"),
            ft.dropdown.Option("26"),
            ft.dropdown.Option("27"),
            ft.dropdown.Option("28"),
            ft.dropdown.Option("29"),
            ft.dropdown.Option("30")
        ],
    )

    dd5 = ft.Dropdown(
        label="施設整備期間",
        hint_text="施設整備期間を選択してください", 
        width=400,
        value="1",
        options=[
            ft.dropdown.Option("1"),
            ft.dropdown.Option("2"),#ft.dropdown.Option("BOT"),
            ft.dropdown.Option("3")
        ],
    )
    
    b = ft.ElevatedButton(text="選択", on_click=button_clicked)

    page.add(dd1, dd2, dd3, dd4, dd5, b)

ft.app(target=main)
#
#def main(page: ft.Page):
#    page.add(
#        ft.TextField(label="Underlined", border="underline", hint_text="Enter text here"),
#        ft.TextField(
#            label="Underlined filled",
#            border=ft.InputBorder.UNDERLINE,
#            filled=True,
#            hint_text="Enter text here",
#       ),
#        ft.TextField(label="Borderless", border="none", hint_text="Enter text here"),
#        ft.TextField(
#            label="Borderless filled",
#            border=ft.InputBorder.NONE,
#            filled=True,
#            hint_text="Enter text here",
#        ),
#    )

#t = ft.Text()
#    tb1 = ft.TextField(label="Standard")
#    tb2 = ft.TextField(label="Disabled", disabled=True, value="First name")
#    tb3 = ft.TextField(label="Read-only", read_only=True, value="Last name")
#    tb4 = ft.TextField(label="With placeholder", hint_text="Please enter text here")
#    tb5 = ft.TextField(label="With an icon", icon=ft.icons.EMOJI_EMOTIONS)
#    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
#    page.add(tb1, tb2, tb3, tb4, tb5, b, t)

#    def checkbox_changed(e):
#        output_text.value = (
#            f"You have learned how to ski :  {todo_check.value}."
#        )
#        page.update()
#
#    output_text = ft.Text()
#    todo_check = ft.Checkbox(label="ToDo: Learn how to use ski", value=False, on_change=checkbox_changed)
#    page.add(todo_check, output_text)

#def main(page):
#    def btn_click(e):
#        if not txt_name.value:
#            txt_name.error_text = "Please enter your name"
#            page.update()
#        else:
#            name = txt_name.value
#            page.clean()
#            page.add(ft.Text(f"Hello, {name}!"))
#
#    txt_name = ft.TextField(label="Your name")
#
#    page.add(txt_name, ft.ElevatedButton("Say hello!", on_click=btn_click))

#    txt_number = ft.TextField(value="0", text_align="right", width=100)
#
#    def minus_click(e):
#        txt_number.value = str(int(txt_number.value) - 1)
#        page.update()
#
#    def plus_click(e):
#        txt_number.value = str(int(txt_number.value) + 1)
#        page.update()
#
#    page.add(
#        ft.Row(
#            [
#                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
#                txt_number,
#                ft.IconButton(ft.icons.ADD, on_click=plus_click),
#            ],
#            alignment=ft.MainAxisAlignment.CENTER,
#        )
#    )
