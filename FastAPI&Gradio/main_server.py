from fastapi import FastAPI
from main_CRUD import db_get_all
import client

app = FastAPI(title="중간고사 API 서버")

@app.get("/api/quotes")
async def read_quotes():
    data = db_get_all()
    return [{"id": r[0], "text": r[1], "author": r[2]} for r in data]

@app.post("/api/scrape")
async def run_scraper():
    result = await client.crawl_quotes()
    return {"message": result}

from fastapi import HTTPException
from main_CRUD import db_delete_quote 

@app.delete("/api/quotes/{quote_id}", tags=["삭제"])
async def delete_quote(quote_id: int):
    """데이터베이스에서 특정 명언을 삭제합니다."""
    success = db_delete_quote(quote_id)
    if not success:
        raise HTTPException(status_code=404, detail="해당 ID의 명언을 찾을 수 없습니다.")
    return {"message": f"ID {quote_id} 명언이 성공적으로 삭제되었습니다."}

from main_CRUD import db_update_quote, ItemCreate 

@app.put("/api/quotes/{quote_id}", tags=["수정"])
async def update_quote(quote_id: int, item: ItemCreate):
    """기존 명 admission의 내용을 수정합니다."""
    success = db_update_quote(quote_id, item.text, item.author, item.category)
    if not success:
        raise HTTPException(status_code=404, detail="수정할 명언을 찾을 수 없습니다.")
    return {"message": f"ID {quote_id} 명언이 성공적으로 수정되었습니다."}