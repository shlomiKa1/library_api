# Library API

## About the system
- The system show details of a library that saved on a database SQL
- The details is on books, members and report
- The choice like: 
- books -> like show, add, edit
- And the system runs system run on a server.

## Code for create to doker
```py
docker run --name mysql-w7 -e MYSQL_ROOT_PASSWORD=<passqord> -e MYSQL_DATABASE=soldiers_db -p 3306:3306 -d mysql:8

```

## FILES
```
library-api/
│
│
├── main.py <!-- run server -->
├── database/ 
│   ├── db_connection.py <!-- --> Connect to data base
│   ├── book_db.py <!-- CRUD for books -->
│   └── member_db.py <!-- CRUD for members -->
├── routes/
│   <!-- POST | PUT | PATCH | GET... -->
│   ├── book_routes.py
│   ├── member_routes.py  
│   └── report_routes.py 
├── logs/
│   └── logger_config.py <!-- logger defination -->
│
└── config.py <!-- Constant variables, Like app.log -->
├── README.md <!-- Describe the project -->
├── requirements.txt <!-- Installation file -->
└── .gitignore <!-- Files & folders that git ignore -->

```

# Table structure

## Books:
| name | detail |
| ------ | ------ |
| id |A unique integer that dynamically increases by 1 each time. |
| title | A string with 50 chars and can't be empty | 
| author | A string with 50 chars and can't be empty |
| genre | It's a word from the list (Fiction, Non-Fiction, Science, History, Other) |
| is_available | A boolean that the default is true |
| borrowed_by_member_id | A integer number and the default is empty.|

## members:

| name | detail |
| ------ | ------ |
| id |A unique integer that dynamically increases by 1 each time |
| name | A string with 50 chars and can't be empty |
| email | A string with 30 chars and can't be empty and most be unique |
| is_active | A boolean and the deafualt is true |
| total_borrows | A integer numbers |


# system
1. Create book - User send (title, author, genre) and the system (on server) add is_available = True & borrowed_by = NULL

2. Genre most be one of the word in the list [Fiction, Non-Fiction, Science, History, Other] - and we check that on PUT & POSt.

3. Create member - User send (name, email) and the system add (is_active = True, total_borrows=0).

4. email most be unique

5. If meber is not active (is_active = False) so he can't borrow a book.

6. A member can't borrow a book that already borrowed (is_available = False).

7. Any member can only borrow three books.

8. The return of book is only if the who is return this.


## Endpoints:
### books:
1. Create book - /books - POST
2. All books - /books - GET
3. Book by ID - /books/{id} - GET
4. Update book - /books/{id} - PATCH
5. Borrow book to member - /books/{id}/borrow/{member_id} - PATCH
6. Borrow book from member - /books/{id}/return/{member_id} - PATCH

### Members:
1. Creat member - /members - POST
2. All members - /members - GET
3. Member by ID - /members/{id} - GET
4. update member - /members/{id} - PATCH
5. Member deactivation - /members/{id}/deactivate - PATCH
6. Activate member - /members/{id}/activate - PATCH

### Reports:
1. Summary report - /reports/summary - GET
2. Books by genre - /reports/books-by-genre - GET
3. The most activate member - /reports/top-member - GET


## System flow
```text
Client -> books -> DB_books -> Database
Client -> members -> DB_members -> Database
Client -> reports -> DB_books/DB_members -> Database
```

## How to run the system
Step 1: Run the code command for to connect to the container from docker.

Step 2 Show which container is running:
```docker ps```

Step 3 Start the container:
```docker exec -it mysql-w7 mysql -uroot -proot```

Step 4 create a vitrual:
```python3/py -m venv .venv```

Step 5 Install python models:
```pip install -r requirements.txt```  

step 6 Run the main file like:
```uvicorn main:app```
