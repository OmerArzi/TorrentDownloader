import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: series name
    """
    sql = ''' INSERT INTO series(name,season,episode)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def init_database():
    database_path = r"C:\sqlite\db\pythonsqlite.db"
    sql_create_series_table = """ CREATE TABLE IF NOT EXISTS series (
                                            name integer PRIMARY KEY,
                                            season integer NOT NULL,
                                            episode integer NOT NULL
                                        ); """
    conn = create_connection(database_path)
    if conn is not None:
        # Execute creation of projects table
        create_table(conn, sql_create_series_table)
    else:
        print("Error: cannot create the database connection.")
