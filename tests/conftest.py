import pytest
import os
from flask import Flask
from config import Config
from application import db, create_app
from application.models import Book

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture
def existing_book():
    existing_book = Book(name = "name",
                    author = "author", 
                    description = "description", 
                    isbn = "AAAA-0000")
    return existing_book

@pytest.fixture
def setup_and_teardown_database(app,existing_book):
    with app.app_context():
        db.create_all()
        db.session.add(existing_book)
        db.session.commit()
        yield
        db.drop_all()

@pytest.fixture
def valid_add_form():
    return { 'name': 'name',
             'author': 'author',
             'description': 'description',
             'isbn': 'ABCD-0220'}

@pytest.fixture
def invalid_add_form():
    return { 'name': 'name',
             'author': 'author',
             'description': 'description',
             'isbn': 'wrong format '}