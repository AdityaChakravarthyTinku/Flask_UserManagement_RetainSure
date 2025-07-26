## Change is Initaialisation is also done wth Hashed passwords for improved security

import sqlite3
from app.utils import hash_password

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS users')

cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

users = [
    ("John Doe", "john@example.com", "password123"),
    ("Jane Smith", "jane@example.com", "secret456"),
    ("Bob Johnson", "bob@example.com", "qwerty789")
]

for name, email, pwd in users:
    hashed_pwd = hash_password(pwd)
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   (name, email, hashed_pwd))

conn.commit()
conn.close()

print("Database initialized with hashed passwords for sample users.")

## Previous Initialisation 


# import sqlite3

# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     password TEXT NOT NULL
# )
# ''')

# cursor.execute("INSERT INTO users (name, email, password) VALUES ('John Doe', 'john@example.com', 'password123')")
# cursor.execute("INSERT INTO users (name, email, password) VALUES ('Jane Smith', 'jane@example.com', 'secret456')")
# cursor.execute("INSERT INTO users (name, email, password) VALUES ('Bob Johnson', 'bob@example.com', 'qwerty789')")

# conn.commit()
# conn.close()

# print("Database initialized with sample data")