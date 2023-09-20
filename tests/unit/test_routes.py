import unittest
from unittest.mock import Mock, patch
from application.main.exceptions import BookServiceException

class TestRoutes():

    home_url = '/'
    add_url = '/add'

    home_page_string = b'Current time is'
    add_page_string = b'Add new book'

    add_post_invalid_form_flash_dict = {'message': {'isbn': ['Invalid fake ISBN']}}
    add_post_service_error_flash_dict = {'message': 'Failed to add book'}

    def test_home(self, client):
        response = client.get(self.home_url)
        assert response.status_code == 200
        assert self.home_page_string in response.data
        
    def test_add_get_success(self, client):
        response = client.get(self.add_url)
        assert response.status_code == 200
        assert self.add_page_string in response.data

    @patch('application.main.services.BookService.add_book')
    def test_add_post_success(self, add_book,client,valid_add_form):
        add_book.return_value = Mock()
        response = client.post(self.add_url, data = valid_add_form)
        with client.session_transaction() as session:
            flash_message = dict(session['_flashes'])
        print (flash_message)
        add_book.assert_called()

    def test_add_post_invalid_form(self, client,invalid_add_form):
        response = client.post(self.add_url, data = invalid_add_form)
        with client.session_transaction() as session:
            flash_message_dict = dict(session['_flashes'])
        assert flash_message_dict == self.add_post_invalid_form_flash_dict

    def test_add_post_service_error(self,client,valid_add_form):
        mock_book_service = Mock()
        mock_book_service.add_book.side_effect = BookServiceException()
        with patch('application.main.routes.book_service', mock_book_service):
            response = client.post(self.add_url, data = valid_add_form)
            with client.session_transaction() as session:
                flash_message_dict = dict(session['_flashes'])
        assert self.add_post_service_error_flash_dict == flash_message_dict
