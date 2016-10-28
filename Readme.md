# Item Catalog

This is FSND "Item Catalog" project.

The result of this project is a backend for Item Catalog. In particular case - a list of books, recommended to read. It also contains a very basic HTML+CSS to provide user interface.
Authorized user can add new books and also edit and delete his books. An unauthorized person can only view list of books.

## Technologies
Backend: Python (Flask and SQLAlchemy mostly)
Frontend: HTML, CSS, JS

## Installation

##### Install Vagrant and VirtualBox

##### Clone the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository

##### Download this repository and move the repository to fullstack-nanodegree-vm/vagrant folder

##### Launch and connect to the Vagrant VM
```
    vagrant up
    vagrant ssh
```

##### Setup and initially populate the database
```
    # in the root directory for project:
    python database_setup.py
    python lotsofbooks.py
```

##### Run the application
```
    python project.py
```
##### Access the application

Visit [http://localhost:5000](http://localhost:5000)

## Main features
 
- CRUD
You can add, edit, delete and read items (books)

- Authentication
Support third-party (Google) authentication

- API
User can get all books from particular category:
[http://localhost:5000/categories/1/JSON](http://localhost:5000/categories/1/JSON)
and data about particular book:
[http://localhost:5000/categories/1/1/JSON](http://localhost:5000/categories/1/1/JSON)
