import gradio as gr
from main_server import app
import pandas as pd
import sqlite3

def get_stats():
    conn = sqlite3.connect("quotes.db")
    df = pd.read_sql_query("SELECT author, COUNT(*) as count FROM quotes GROUP BY author", conn)
    conn.close()
    return df

with gr.Blocks() as ui:
    gr.Markdown("# 🎓 명언 분석 시스템 (Gradio Interface)")
    with gr.Tab("데이터"):
        data_table = gr.DataFrame(label="DB 내용")
        refresh_btn = gr.Button("데이터 새로고침")
    
    # Aquí puedes añadir más funciones de análisis
    refresh_btn.click(get_stats, outputs=data_table)

# Gradio 마운트 및 실행
app = gr.mount_gradio_app(app, ui, path="/ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)