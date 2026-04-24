import httpx
from bs4 import BeautifulSoup
import sqlite3

async def crawl_quotes():
    url = "https://quotes.toscrape.com"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.find_all("div", class_="quote")[:20]
    
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quotes") 
    for item in items:
        text = item.find("span", class_="text").text
        author = item.find("small", class_="author").text
        cursor.execute("INSERT INTO quotes (text, author, category) VALUES (?, ?, ?)", 
                       (text, author, "General"))
    conn.commit()
    conn.close()
    return "✅ 20개의 명언 수집 완료!"
