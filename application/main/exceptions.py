class HTTPError404(Exception):
    pass

class BookServiceException(Exception):
    def __init__(self, error_code, message = "Book service exception"):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)