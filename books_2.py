from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(lt=2024)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Move fast with FastAPI',
                'author': 'No name',
                'description': 'The description of the book',
                'rating': 5,
                'published_date': 1900
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'Author 1', 'A very nice book!', 5, 1900),
    Book(2, 'Be Fast with FastAPI', 'Author 2', 'Good!', 4, 1999),
    Book(3, 'Master Endpoint', 'Author 3', 'A great book!', 4, 2021),
    Book(4, 'Ruby on Rails Microservice', 'Author 1', 'A awesome book!', 3, 2022),
    Book(5, 'Love Ruby but Python', 'Author 2', 'Description nice!', 3, 2023),
    Book(6, 'Master Vue', 'Author 3', 'Must buy when start learning Vue', 5, 2020)
]


@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):  # Path support validation for path parameters
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='The book was not found')


@app.get('/books/', status_code=status.HTTP_200_OK)
async def read_all_books_by_rating(rating: int = Query(gt=0, lt=6)):  # Query support validation for query parameters
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.get('/books/published', status_code=status.HTTP_200_OK)
async def read_all_books_by_published_date(published_date: int = Query(lt=2024)):  # Query support validation for
    # query parameters
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookRequest):
    new_book = Book(**new_book.model_dump())
    BOOKS.append(find_book_by_id(new_book))


def find_book_by_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_updated: BookRequest, book_id: int = Path(gt=0)):  # Path support validation for path
    # parameters
    book_changed = False
    for index, book in enumerate(BOOKS):  # enumerate() returns index and value of each element in the list
        if book.id == book_id:
            BOOKS[index] = Book(**book_updated.model_dump())
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='The book was not found')


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):  # Path support validation for path parameters
    book_changed = False
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='The book was not found')
