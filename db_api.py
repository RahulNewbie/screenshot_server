import sqlite3
from sqlite3 import Error
import os
import constant

# Global variable declaration
ID = 1
INCREMENT = 1


def connect_to_database():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param: None
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(constant.DB_FILE)
    except Error as e:
        print(e)
    return conn


def update_to_db(url, address):
    """
    inserts the records in the database
    """
    global ID
    con = connect_to_database()
    cur = con.cursor()
    try:
        cur.execute(r"INSERT INTO screenshot_data "
                    "(id, url,address) "
                    "VALUES (?, ?, ?)",
                    (ID, url, address,))
        # Incrementing sequence for the record identifier
        ID += INCREMENT
        print("database insertion finished")
    except Error as err:
        print("Error happened while inserting data into database " + str(err))
    con.commit()
    con.close()


def select_all_data_from_table():
    """
    Query all rows in the screenshot table
    :param: None
    :return: ALl rows of the table
    """
    conn = connect_to_database()
    cur = conn.cursor()
    # Select All the records from the Database
    cur.execute("SELECT * FROM screenshot_data")
    rows = cur.fetchall()
    return rows
