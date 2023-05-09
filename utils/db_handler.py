import sqlite3

DB_NAME = "db.sqlite"

schema = [
    """CREATE TABLE users(
    userID varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    hash varchar(255) NOT NULL,
    role varchar(255) NOT NULL,
    PRIMARY KEY(userID)
   );"""
]

default_users = [
    "INSERT INTO users(userID, name, hash, role) VALUES('12cc9c91-6174-4cbd-aef5-5b4859c340d6', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Application')",
    "INSERT INTO users(userID, name, hash, role) VALUES('258a9465-119a-4562-9d58-b7a43e1c88d8', 'operate', '2c29d39181de8f853de5e48ba983a5c88612b9dbaa5ab32c7748800a0840aeb8', 'Operate')"
]

def create_schema():
    with sqlite3.connect(DB_NAME) as conn:
        for table in schema:
            conn.execute(table)
        return "200"

def test():
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT * FROM users;")
        return result.fetchall()

def reset_db(): 
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DROP TABLE users;")
        create_schema()
        for user in default_users:
            conn.execute(user)
    return "200"


def new_user(user_id, name, defined_hash, role):
    """ Creates a New User"""
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("INSERT INTO users(userID, name, hash, role) VALUES(?, ?, ?, ?)", (user_id, name, defined_hash, role))
        return result.fetchall()


def get_passhash(name):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT userID, hash FROM users WHERE name = ?;", (name,)).fetchall()
        if len(result) > 0: # If there is a value
            return result[0]
        else:
            return "500", "User doesnt exist"

def verify_user(userID):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT name, hash, role FROM users WHERE userID = ?", (userID,)).fetchall()[0]
        return (result[0], result[1], result[2])

def is_username_taken(username):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT userID FROM users WHERE name = ?", (username,)).fetchall()
        return len(result) > 0