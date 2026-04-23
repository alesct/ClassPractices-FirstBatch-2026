from pydantic import BaseModel
import sqlite3

# Pydantic 모델 
class Item(BaseModel):
    id: int
    text: str
    author: str
    category: str

class ItemCreate(BaseModel):
    text: str
    author: str
    category: str

# 데이터베이스 함수
def db_get_all():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes")
    rows = cursor.fetchall()
    conn.close()
    return rows

# 특정 ID의 명언을 삭제하는 함수
def db_delete_quote(quote_id: int):
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    # 해당 ID가 존재하는지 확인
    cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
    if cursor.fetchone() is None:
        conn.close()
        return False
    
    cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
    conn.commit()
    conn.close()
    return True

# 명언 내용을 수정하는 함수 (Función para actualizar)
def db_update_quote(quote_id: int, text: str, author: str, category: str):
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    
    # 해당 ID가 있는지 먼저 확인
    cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
    if cursor.fetchone() is None:
        conn.close()
        return False
    
    # 데이터 업데이트
    cursor.execute("""
        UPDATE quotes 
        SET text = ?, author = ?, category = ? 
        WHERE id = ?
    """, (text, author, category, quote_id))
    
    conn.commit()
    conn.close()
    return True