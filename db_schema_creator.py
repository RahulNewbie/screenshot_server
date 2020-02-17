import sqlite3
from sqlite3 import Error
import db_api


def create_db_schema():
    """
    Create database schema for the database
    """
    con = db_api.connect_to_database()
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS screenshot_data "
                    "(id, url,address);")
        print("database creation finished")
    except Error as err:
        print("Error while creating database" + str(err))
    con.commit()
    con.close()
