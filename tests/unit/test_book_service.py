from application import db
from sqlalchemy import select
from application.models import Book
from application.main.services import book_service
from application.main.exceptions import BookServiceException
from unittest.mock import Mock, patch
import pytest
from sqlalchemy.exc import SQLAlchemyError

new_book_to_add = Book(name = "name",
                       author = "author", 
                       description = "description", 
                       isbn = "AAAA-0001")

def test_add_book_success(app,setup_and_teardown_database):
    with app.app_context():
        book_service.add_book(name = new_book_to_add.name,
                              author =  new_book_to_add.author,
                              description = new_book_to_add.description,
                              isbn = new_book_to_add.isbn)
        retrieved_book = db.session.execute(select(Book) \
                                  .filter_by(isbn = new_book_to_add.isbn)) \
                                  .scalar_one()
        assert retrieved_book == new_book_to_add

def test_add_book_fail_existing_book(existing_book,app,setup_and_teardown_database):
    with app.app_context(), pytest.raises(BookServiceException):
        book_service.add_book(name = existing_book.name,
                              author =  existing_book.author,
                              description = existing_book.description,
                              isbn = existing_book.isbn)
        
def test_get_all_books_success(existing_book,app,setup_and_teardown_database):
    with app.app_context():
        books = book_service.get_all_books_list()
        assert books == [existing_book]
        
def test_get_all_books_failure_database_error(app,setup_and_teardown_database):
    with app.app_context(), pytest.raises(BookServiceException) :
        mock_book_class = Mock()
        mock_book_class.query.all.side_effect = SQLAlchemyError()
        with patch('application.main.services.Book', mock_book_class):
            book_service.get_all_books_list()

def test_get_book_by_isbn_success():
    pass

def test_get_book_by_isbn_failure_not_found():
    pass

def test_get_book_by_isbn_failure_database_error():
    pass

# editing multiple fields
def test_update_book_success():
    pass

def test_update_book_failure_not_existing_book():
    pass

def test_update_book_failure_invalid_field_data():
    pass

def test_update_book_failure_database_error():
    pass

def test_delete_book_success():
    pass

def test_delete_book_failure_not_existing_book():
    pass

def test_delete_book_failure_database_error():
    pass