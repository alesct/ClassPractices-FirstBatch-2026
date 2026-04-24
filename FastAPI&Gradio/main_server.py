from fastapi import FastAPI, HTTPException, Query
from client import 명언_수집
from main_CRUD import 모든_명언_가져오기, 명언_삭제하기, 명언_수정하기, 명언_추가하기, 명언_생성_모델

app = FastAPI(title=" ⋆⭒˚.⋆ 명언 분석 시스템 (중간고사) ⋆⭒˚.⋆")

@app.post("/api/scrape", tags=["수집"])
async def 자동_명언_수집():
    result = await 명언_수집() 
    return {"status": "success", "message": result}

@app.post("/api/quotes", tags=["추가"])
async def 명언_추가(
    text: str = Query(..., description="text"), 
    author: str = Query(..., description="author"), 
    category: str = Query(default="General", description="category")
): 
    item = 명언_생성_모델(text=text, author=author, category=category)
    명언_추가하기(item)
    return {"status": "success", "message": "성공적으로 추가되었습니다."}

@app.get("/api/quotes", tags=["조회"])
async def 명언_조회():
    return 모든_명언_가져오기()

@app.delete("/api/quotes/{quote_id}", tags=["삭제"])
async def 명언_삭제(quote_id: int):
    success = 명언_삭제하기(quote_id)
    if not success:
        raise HTTPException(status_code=404, detail="해당 ID의 명언을 찾을 수 없습니다.")
    return {"message": f"ID {quote_id} 명언이 성공적으로 삭제되었습니다."}

@app.put("/api/quotes/{quote_id}", tags=["수정"])
async def 명언_수정(quote_id: int, text: str, author: str, category: str):
    success = 명언_수정하기(quote_id, text, author, category)
    if not success:
        raise HTTPException(status_code=404, detail="수정할 명언을 찾을 수 없습니다.")
    return {"message": f"ID {quote_id} 명언이 성공적으로 수정되었습니다."}