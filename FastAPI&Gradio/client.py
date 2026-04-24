import httpx
from bs4 import BeautifulSoup
import sqlite3

async def 명언_수집():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM quotes")
    현재_개수 = cursor.fetchone()[0]
    페이지 = (현재_개수 // 10) + 1
    
    추가된_항목_수 = 0
    
    async with httpx.AsyncClient() as client:
        URL = f"https://quotes.toscrape.com/page/{페이지}/"
        try:
            응답 = await client.get(URL, timeout=10.0)
            
            if 응답.status_code != 200:
                return "✓ 더 이상 가져올 페이지가 없습니다."
                
            소스 = BeautifulSoup(응답.text, "html.parser")
            명언_리스트 = 소스.find_all("div", class_="quote")
            
            if not 명언_리스트:
                return "✓ 해당 페이지에 명언이 없습니다."
                
            for 항목 in 명언_리스트:
                내용 = 항목.find("span", class_="text").get_text(strip=True)
                저자 = 항목.find("small", class_="author").get_text(strip=True)
                
                cursor.execute("SELECT 1 FROM quotes WHERE text = ?", (내용,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO quotes (text, author, category) 
                        VALUES (?, ?, ?)
                    """, (내용, 저자, "일반"))
                    추가된_항목_수 += 1
            
            conn.commit()
            print(f"DEBUG: {페이지}페이지 수집 완료 (신규: {추가된_항목_수}개)")
            
        except Exception as e:
            print(f"오류 발생: {e}")
            return f"❌ 오류 발생: {e}"
    
    conn.close()
    
    if 추가된_항목_수 > 0:
        return f"✓ {페이지}페이지에서 {추가된_항목_수}개의 명언을 추가했습니다!"
    else:
        return "✓ 이미 해당 페이지의 데이터를 가지고 있습니다."