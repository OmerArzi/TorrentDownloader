import sqlite3
from sqlite3 import Error


def create_series(conn: sqlite3.Connection, series: tuple):
    """
    Create a new project into the series table
    :param conn:
    :param series:
    :return: series name
    """
    sql = ''' INSERT INTO series(name,season,episode)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()
    return cur.lastrowid


def select_series_by_name(conn: sqlite3.Connection, series_name: str):
    """
    Query series by name
    :param conn: the Connection object
    :param series_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM series WHERE name=?", (series_name,))
    query_result = cur.fetchall()
    return query_result


def update_series(conn: sqlite3.Connection, updated_series_status: tuple):
    """
    update season, and episode of a series
    :param conn:
    :param updated_series_status:
    :return:
    """
    sql = ''' UPDATE series
              SET season = ? ,
                  episode = ? ,
              WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, updated_series_status)
    conn.commit()


def create_table(conn: sqlite3.Connection, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def init_database():
    database_path = r"C:\sqlite\db\watchstatus.db"
    sql_create_series_table = """ CREATE TABLE IF NOT EXISTS series (
                                            name text PRIMARY KEY,
                                            season integer NOT NULL,
                                            episode integer NOT NULL); """
    conn = create_connection(database_path)
    if conn is not None:
        # Execute creation of projects table
        create_table(conn, sql_create_series_table)
        return conn
    else:
        print("Error: cannot create the database connection.")
