import pandas as pd
import flet as ft
from simpledt import DataFrame
import openpyxl
from styleframe import StyleFrame

def main(page: ft.Page):
    page.title = "Excel読み込み"
    print("Initial Inputs", page.route)

    def route_change(e):
        print("Route changed to:", e.route)
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Excel読み込み")),
                    ft.ElevatedButton("Read Excel", on_click=show_excel),
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
        )
        page.update()
        if page.route == "/show_excel":
            page.views.append(
                ft.View(
                    "/show_excel",
                    [
                        ft.AppBar(title=ft.Text("Excel読み込み")),
                        read_excel("vfm_outputs/VFM_result_sheet_2025-02-09_01_06_39.xlsx"),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
            )
            page.update()



    def view_pop(e):
        print("View popped:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def open_index_page(e):
        page.go("/")
    
    def show_excel(e):
        page.go("/show_excel")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    def read_excel(path):
        with open(path, 'rb') as s:
            df = pd.read_excel(s)
            simpledt_df = DataFrame(df)
            simpledt_dt = simpledt_df.datatable
            table = simpledt_dt

            lv_01 = ft.ListView(
                expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
            )
            lv_01.controls.append(table)

            return ft.View(
                content=ft.Column(
                    controls=[
                        lv_01,
                    ],
                ),
            )


ft.app(target=main)


#def excel_to_cs():
#    df.to_excel('result.xlsx', index=False)
#    file_name = 'VFM_result_sheet_' + dtime_w + '.xlsx'
#    save_path = 'vfm_output/' + file_name

#    wb = openpyxl.Workbook()
#    ws = wb['Sheet']
#    ws.title = '算定結果概要'
#    wb.save(save_path)

#    with StyleFrame.ExcelWriter(save_path, if_sheet_exists='overlay', mode='a') as writer:    
#        sf_final_inputs_df.to_excel(writer, sheet_name='最終入力等', index=False, startrow=1, startcol=1)

if __name__ == '__main__':
    main()