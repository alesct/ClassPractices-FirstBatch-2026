from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 웹페이지에 필요한 CSS 스타일시트, 자바스크립트, 이미지 파일 등을 넣어둘 static 폴더를 서버와 연결
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates 폴더 안의 파일들을 템플릿으로 쓰겠다고 선언하는 것
templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("jinja_2:app", host="127.0.0.1", port=8000, reload=True)