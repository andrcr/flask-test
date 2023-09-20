from application import db
from application.models import Book
from application.main.exceptions import BookServiceException
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select
from typing import List

class BookService():

    def add_book(self, name: str, author: str, description: str, isbn: str) -> None:
        '''
        Adds a new book to the database

            Args:
                name (str): Name of book to be added
                author (str): Author of book to be added
                description (str): Description of book to be added
                isbn (str): ISBN of book to be added

            Returns:
                None

            Raises:
                BookServiceException
        '''
        new_book = Book(name = name,
                        author = author, 
                        description = description, 
                        isbn = isbn)
        try:
            db.session.add(new_book)
            db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise BookServiceException(500,str(ex) +" "+ str(new_book)) from ex
        
    def get_all_books_list(self) -> List[Book]:
        try:
            books = Book.query.all()
            return books
        except SQLAlchemyError as ex:
            raise BookServiceException(500,ex._message) from ex
        
    def get_book_by_isbn(self, isbn: str) -> Book:
        try:
            book = db.session.execute(select(Book) \
                                     .filter_by(isbn=isbn)) \
                                     .scalar_one()
            return book
        except SQLAlchemyError as ex:
            error_code = 500
            if isinstance(ex, NoResultFound):
                error_code = 404
            raise BookServiceException(error_code,ex._message) from ex
    
    # validating field name in the form for immediate feedback to user
    # unsure if form validation is done with requests sent outside of the UI
    def update_book(self, isbn: str, field_name: str, new_value: str) -> None:
        try:
            book = db.session.execute(select(Book) \
                                     .filter_by(isbn=isbn)) \
                                     .scalar_one()
            setattr(book, field_name, new_value)
            db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise BookServiceException(500,ex._message) from ex
    
    def delete_book(self, isbn: str) -> None:
        try:
            book = db.session.execute(select(Book) \
                                     .filter_by(isbn=isbn)) \
                                     .scalar_one()
            db.session.delete(book)
            db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise BookServiceException(500,ex._message) from ex
