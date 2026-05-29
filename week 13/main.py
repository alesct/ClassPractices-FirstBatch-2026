from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import uvicorn
import gradio as gr

from database import get_db, SessionLocal
import models
import crud

app = FastAPI(title="도서 관리 시스템")

@app.get("/", response_class=HTMLResponse)
def read_main_page():
    return """
    <html>
        <head>
            <title>도서 관리 시스템 홈</title>
            <style>
                body { font-family: 'Arial', sans-serif; text-align: center; padding: 50px; background-color: #f4f6f9; }
                .container { background: white; padding: 40px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                h1 { color: #333; }
                p { color: #666; font-size: 18px; }
                .btn { display: inline-block; margin: 15px; padding: 15px 30px; font-size: 18px; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; transition: background 0.2s; }
                .btn-ui { background-color: #2196F3; }
                .btn-ui:hover { background-color: #0b7dda; }
                .btn-docs { background-color: #4CAF50; }
                .btn-docs:hover { background-color: #45a049; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>( ^_^ )/ 도서 관리 시스템에 오신 것을 환영합니다</h1>
                <p>FastAPI 백엔드와 Gradio 웹 인터페이스로 구동되는 시스템입니다.</p>
                <hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;">
                <a href="/ui" class="btn btn-ui">[ o_o ] 웹 UI 화면 접속 (Gradio)</a>
                <a href="/docs" class="btn btn-docs">⚙__⚙ API 명세서 접속 (Swagger)</a>
            </div>
        </body>
    </html>
    """

@app.get("/api/books")
def get_books_api(db: Session = Depends(get_db)):
    return crud.get_all_books(db)

@app.post("/api/books")
def add_book_api(title: str, author: str, db: Session = Depends(get_db)):
    return crud.add_book(db, title, author)

@app.delete("/api/books/{book_id}")
def delete_book_api(book_id: int, db: Session = Depends(get_db)):
    success = crud.delete_book(db, book_id)
    if success:
        return {"status": "성공"}
    return {"status": "찾을 수 없음"}, 404

def get_db_session():
    return SessionLocal()

def update_table():
    db = get_db_session()
    try:
        books = crud.get_all_books(db)
        return [[b.id, b.title, b.author, b.status] for b in books]
    finally:
        db.close()

def add_book_handler(title, author):
    if not title or not author:
        return update_table(), "오류: ( T_T ) 제목과 저자를 모두 입력해주세요."
    db = get_db_session()
    try:
        crud.add_book(db, title, author)
        return update_table(), f"성공: ( ^_^ )v '{title}' 도서가 등록되었습니다."
    finally:
        db.close()

def delete_book_handler(book_id):
    try:
        bid = int(book_id)
    except ValueError:
        return update_table(), "오류: ( •_• ) 올바른 숫자 형식의 ID를 입력해주세요."
    db = get_db_session()
    try:
        success = crud.delete_book(db, bid)
        if success:
            return update_table(), f"성공: (x_x) ID {bid}번 도서가 삭제되었습니다."
        return update_table(), "오류: ( o_o ) 해당 ID의 도서를 찾을 수 없습니다."
    finally:
        db.close()

with gr.Blocks(title="도서 관리 시스템") as gradio_ui:
    gr.Markdown("# (=^·^=) 도서 관리 시스템")
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### [ o_o ] 도서 목록")
            book_table = gr.Dataframe(
                headers=["ID", "제목", "저자", "상태"],
                datatype=["number", "str", "str", "str"],
                value=update_table(),
                interactive=False
            )
            refresh_btn = gr.Button("새로고침")
        with gr.Column(scale=1):
            gr.Markdown("### ( +_+) 도서 등록")
            title_input = gr.Textbox(label="제목")
            author_input = gr.Textbox(label="저자")
            add_btn = gr.Button("등록", variant="primary")
            gr.Markdown("---")
            gr.Markdown("### (x_x) 도서 삭제")
            id_input = gr.Textbox(label="도서 ID")
            delete_btn = gr.Button("삭제", variant="stop")
            gr.Markdown("---")
            status_output = gr.Markdown("준비 완료 ( -_- )_旦")

    refresh_btn.click(fn=update_table, outputs=book_table)
    add_btn.click(fn=add_book_handler, inputs=[title_input, author_input], outputs=[book_table, status_output])
    delete_btn.click(fn=delete_book_handler, inputs=id_input, outputs=[book_table, status_output])

app = gr.mount_gradio_app(app, gradio_ui, path="/ui")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)