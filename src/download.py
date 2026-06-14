import flet as ft
from sqlalchemy import create_engine
from fastapi.responses import FileResponse
import flet.fastapi as flet_fastapi
from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()
    #app = flet_fastapi()

@app.get("/api/download_local/{filename}")
async def download_local_file(filename: str):
    file_path = os.path.join(os.getcwd(), 'excels', filename)
    if os.path.exists(filename):
        return FileResponse(path=file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        return {"error": "File not found"}
