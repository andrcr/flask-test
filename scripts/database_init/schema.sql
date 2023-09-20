DROP TABLE IF EXISTS books;
create table books (
                         id INTEGER PRIMARY KEY,
                         name VARCHAR(50) NOT NULL,
                         author VARCHAR(50) NOT NULL,
                         description VARCHAR(200) NOT NULL,
                         isbn VARCHAR(9) UNIQUE NOT NULL
);