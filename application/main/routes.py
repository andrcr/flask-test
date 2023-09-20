from application import db
from application.models import Book
from application.main import bp
from application.main.forms import (AddingBooksForm, 
                                    UpdatingBooksForm,
                                    DeleteBooksForm)
from application.main.services import BookService
from application.main.exceptions import HTTPError404, BookServiceException
from flask import render_template, request, flash, redirect
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select

import datetime
import os

book_service = BookService()

@bp.route("/")
def home():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("index.html",current_time = current_time)

@bp.route("/add", methods=['GET', 'POST'])
def add():
    form = AddingBooksForm(request.form)
    if request.method == 'GET':
        return render_template("add.html",form=form)
    else: 
        if form.validate():
            try:
                book_service.add_book(name = form.name.data, 
                                      author = form.author.data, 
                                      description = form.description.data, 
                                      isbn = form.isbn.data )
                flash("Book added")
            except BookServiceException as ex:
                flash("Failed to add book")
                print(str(ex.message))
        else:
            flash(form.errors)
        return redirect("/add")
    

@bp.route("/books", methods=['GET'])
def list_all_books():
    try:
        books = book_service.get_all_books_list()
    except BookServiceException as ex:
        flash("Operation failed")
        print(str(ex))
    return render_template("list_books.html",books = books)

@bp.route("/books/<isbn>", methods=['GET'])
def list_single_book(isbn):
    try:
        book = book_service.get_book_by_isbn(isbn)
        return render_template("list_books.html",books = [book])
    except BookServiceException as ex:
        if isinstance(ex, NoResultFound):
            raise HTTPError404()
        else:
            flash("Operation failed")
        
@bp.route("/update", methods=['GET','POST'])
def update_book():
    form = UpdatingBooksForm(request.form)
    if request.method == 'GET':
        return render_template("update_book.html",form=form)
    else: 
        if form.validate():
            try:
                book_service.update_book(form.isbn.data, form.field_name.data,\
                                         form.new_value.data)
            except BookServiceException as ex:
                flash("Operation failed")
                print(str(ex))   
        else: 
            flash(form.errors)
        return redirect("/update")


@bp.route("/delete", methods=['GET','POST'])
def delete_book():
    form = DeleteBooksForm(request.form)
    if request.method == 'GET':
        return render_template("delete_book.html",form=form)
    else: 
        if form.validate():
            try:
                book_service.delete_book(form.isbn.data)
            except BookServiceException as ex:
                flash("Operation failed")
                print(str(ex))  
        else: 
            flash(form.errors)
        return redirect("/delete")
