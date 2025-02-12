import flet as ft
from sqlalchemy import create_engine
from fastapi.responses import FileResponse
import flet.fastapi as flet_fastapi
import pandas as pd

def download():
    engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
    download_df = pd.read_sql_table('download_table', engine)

    filename = download_df['file_name'].iloc[0]
    save_path = download_df['save_path'].iloc[0]
    dtime_w = download_df['datetime'].iloc[0]

    #def s_h(page: ft.Page):
    #    page.add(ft.Text(""))

    #app = flet_fastapi.app(session_handler=s_h)

    #@app.get("/download/{filename}")
    path = f"vfm_output/{filename}"
    return FileResponse(path, filename=filename)

#download(filenamw  = filename)