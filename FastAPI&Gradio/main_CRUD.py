from pydantic import BaseModel
from typing import List
import sqlite3

class 명언_모델(BaseModel):
    id: int
    text: str
    author: str
    category: str

class 명언_생성_모델(BaseModel):
    text: str
    author: str
    category: str

def 명언_추가하기(명언: 명언_생성_모델):
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quotes (text, author, category) 
        VALUES (?, ?, ?)
    """, (명언.text, 명언.author, 명언.category))
    conn.commit()
    conn.close()

def 모든_명언_가져오기():
    conn = sqlite3.connect("quotes.db")
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes ORDER BY id DESC")
    rows = cursor.fetchall()
    print(f"★ DB DEBUG: 데이터베이스에 총 {len(rows)}개의 명언이 있습니다.")
    결과 = [dict(row) for row in rows]
    conn.close()
    return 결과

def 명언_삭제하기(명언_id: int):
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quotes WHERE id = ?", (명언_id,))
    성공 = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return 성공

def 명언_수정하기(명언_id: int, text: str, author: str, category: str):
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE quotes SET text = ?, author = ?, category = ? WHERE id = ?
    """, (text, author, category, 명언_id))
    성공 = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return 성공