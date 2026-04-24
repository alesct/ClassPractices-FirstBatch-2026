import gradio as gr
from main_server import app
import pandas as pd
import sqlite3
from deep_translator import GoogleTranslator

def 데이터_가져오기():
    conn = sqlite3.connect("quotes.db")
    df = pd.read_sql_query("SELECT * FROM quotes ORDER BY id ASC", conn)
    conn.close()
    return df

def 명언_번역(text, target_lang):
    if not text or text.strip() == "":
        return "먼저 표에서 명언을 선택해주세요!"
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"번역 오류: {str(e)}"

def 클릭한_명언_가져오기(evt: gr.SelectData):
    text = evt.value
    word_count = len(text.split())
    return text, word_count

with gr.Blocks() as ui:
    
    with gr.Column(elem_classes="center-content"):
        gr.Markdown("# ⋆⭒˚.⋆ 글로벌 명언 분석 시스템 ⋆⭒˚.⋆ ")
        새로고침_버튼 = gr.Button("데이터 불러오기", variant="primary")
    
    with gr.Group():
        with gr.Column(elem_classes="center-content"):
            gr.Markdown("### .☘︎ ݁˖ 마음에 드는 명언을 골라보세요!.☘︎ ݁˖ ")
            gr.Markdown("(표에서 번역할 내용을 클릭하세요!)")
        
        데이터_표 = gr.DataFrame(
            label="명언 목록", 
            interactive=False,
            type="pandas"
        )
        
        gr.Markdown("---")
        
        with gr.Column(elem_classes="center-content"):
            gr.Markdown("### ⋆⭒˚.⋆실시간 번역기 ⋆⭒˚.⋆")
        
        입력_텍스트 = gr.Textbox(label="선택된 명언", lines=3)
        
        with gr.Row():
            한국어_버튼 = gr.Button("🇰🇷 한국어로 번역", variant="secondary")
            스페인어_버튼 = gr.Button("🇪🇸 스페인어로 번역", variant="secondary")
        
        with gr.Row():
            with gr.Column(scale=3):
                결과_텍스트 = gr.Textbox(label="번역 결과", lines=3)
            with gr.Column(scale=1):
                단어_카운트 = gr.Label(label="단어 수")

    ui.load(데이터_가져오기, outputs=데이터_표)
    새로고침_버튼.click(데이터_가져오기, outputs=데이터_표)
    데이터_표.select(클릭한_명언_가져오기, None, [입력_텍스트, 단어_카운트])
    한국어_버튼.click(lambda x: 명언_번역(x, 'ko'), inputs=입력_텍스트, outputs=결과_텍스트)
    스페인어_버튼.click(lambda x: 명언_번역(x, 'es'), inputs=입력_텍스트, outputs=결과_텍스트)

app = gr.mount_gradio_app(app, ui, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)