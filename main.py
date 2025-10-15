from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Кітапхана кітаптарының API")

# ===== Модель (кітап құрылымы) =====
class Book(BaseModel):
    title: str
    author: str
    year: int

# ===== Уақытша "дерекқор" — жадыдағы тізім =====
books = [
    {"id": 1, "title": "Абай жолы", "author": "М. Әуезов", "year": 1942},
    {"id": 2, "title": "Көшпенділер", "author": "І. Есенберлин", "year": 1978}
]

# Соңғы ID-ді бақылау
next_id = 3

# ===== 1. Барлық кітаптарды алу =====
@app.get("/books")
def get_books():
    return books

# ===== 2. Белгілі бір кітапты ID бойынша алу =====
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Кітап табылмады")

# ===== 3. Жаңа кітап қосу =====
@app.post("/books")
def add_book(new_book: Book):
    global next_id
    book_dict = new_book.dict()
    book_dict["id"] = next_id
    books.append(book_dict)
    next_id += 1
    return book_dict

# ===== 4. Кітаптың мәліметін жаңарту =====
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for book in books:
        if book["id"] == book_id:
            book.update(updated_book.dict())
            return book
    raise HTTPException(status_code=404, detail="Кітап табылмады")

# ===== 5. Кітапты жою =====
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Кітап жойылды"}
    raise HTTPException(status_code=404, detail="Кітап табылмады")
