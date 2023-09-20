from application import db

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    description = db.Column(db.String(200))
    isbn = db.Column(db.String(9))
    __table_args__ = (db.UniqueConstraint('isbn'),)

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.name == other.name and self.author == other.author and \
                  self.description == other.description and self.isbn == other.isbn
        return False

    def __repr__(self):
        return f"Book name: {self.name}\nAuthor: {self.author}\nDescription: {self.description}\nfake_isbn: {self.isbn}\n"