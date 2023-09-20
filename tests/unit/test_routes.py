from unittest.mock import Mock, patch
from application.main.exceptions import BookServiceException

home_url = '/'
add_url = '/add'

home_page_string = b'Current time is'
add_page_string = b'Add new book'

add_post_invalid_form_flash_dict = {'message': {'isbn': ['Invalid fake ISBN']}}
add_post_service_error_flash_dict = {'message': 'Failed to add book'}

def test_home(client):
    response = client.get(home_url)
    assert response.status_code == 200
    assert home_page_string in response.data

def test_add_get_success(client):
    response = client.get(add_url)
    assert response.status_code == 200
    assert add_page_string in response.data

# how do i mock book_service.add_book to not call the function but
# instead just check if it has been called with sth like assert_called()
# also how do i make it throw an exception?

# def test_add_post_success(client,valid_add_form):
#     response = client.post(add_url, data = valid_add_form)
#     with client.session_transaction() as session:
#         flash_message = dict(session['_flashes'])
#     print (flash_message)
#     assert False

# def test_add_post_success(client,valid_add_form):

#     mock_flash = Mock()
    
#     with patch('application.main.routes.book_service', mock_flash):
#         mock_flash.add_book.assert_called()
#         response = client.post(add_url, data = valid_add_form)
#         mock_flash.add_book.assert_called()
#         print(response)

def test_add_post_invalid_form(client,invalid_add_form):
    response = client.post(add_url, data = invalid_add_form)
    with client.session_transaction() as session:
        flash_message_dict = dict(session['_flashes'])
    assert flash_message_dict == add_post_invalid_form_flash_dict

def test_add_post_service_error(client,valid_add_form):
    mock_book_service = Mock()
    mock_book_service.add_book.side_effect = BookServiceException()
    with patch('application.main.routes.book_service', mock_book_service):
        response = client.post(add_url, data = valid_add_form)
        with client.session_transaction() as session:
            flash_message_dict = dict(session['_flashes'])
    assert add_post_service_error_flash_dict == flash_message_dict