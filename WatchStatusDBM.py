import sqlite3
from sqlite3 import Error
import os


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
    Select series by name
    :param conn: the Connection object
    :param series_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM series WHERE name=?", (series_name,))
    query_result = cur.fetchall()
    return query_result


def select_episodes_by_name(conn: sqlite3.Connection, series_name: str):
    """
    Query series by name
    :param conn: the Connection object
    :param series_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM episode WHERE name=?", (series_name,))
    query_result = cur.fetchall()
    return query_result


def select_all_tv_shows(conn: sqlite3.Connection):
    """
    Query series by name
    :param conn: the Connection object
    :return: List of all unique tv-shows names in database
    """
    # TODO: check if works
    cur = conn.cursor()
    cur.execute("SELECT distinct * FROM series")
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
                  episode = ?
              WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, updated_series_status)
    conn.commit()


def delete_series(conn: sqlite3.Connection, series_name: str):
    """
    Delete a series by series name
    :param conn:  Connection to the SQLite database
    :param series_name:
    :return:
    """
    sql = 'DELETE FROM series WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (series_name,))
    conn.commit()


def delete_episodes(conn: sqlite3.Connection, series_name: str):
    """
    Delete all episodes' record on database (by series name)
    :param conn:  Connection to the SQLite database
    :param series_name:
    :return:
    """
    sql = 'DELETE FROM episode WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (series_name,))
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


def create_episode(conn: sqlite3.Connection, episode: tuple):
    """
    Create a new project into the series table
    :param conn:
    :param episode:
    :return: series name
    """
    sql = ''' INSERT INTO episode(name,season,episode,torrent_name,path)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, episode)
    conn.commit()
    return cur.lastrowid


def create_database_file():
    user_dir_path = os.path.join("C:\\", "sqlite", "db", "watchstatus.db")
    f = open(user_dir_path, "a")
    f.close()
    return user_dir_path


def init_database():
    database_path = create_database_file()
    sql_create_series_table = """ CREATE TABLE IF NOT EXISTS series (
                                            name text PRIMARY KEY,
                                            season integer NOT NULL,
                                            episode integer NOT NULL); """

    sql_create_extended_data = """CREATE TABLE IF NOT EXISTS episode (
                                    name text NOT NULL,
                                    season integer NOT NULL,
                                    episode integer NOT NULL,
                                    torrent_name text,
                                    path text,                               
                                    FOREIGN KEY (name) REFERENCES series (name),
                                    FOREIGN KEY (season) REFERENCES series (season),
                                    FOREIGN KEY (episode) REFERENCES series (episode),
                                    PRIMARY KEY(name,season,episode)
                                );"""
    conn = create_connection(database_path)
    if conn is not None:
        # Execute creation of projects table
        create_table(conn, sql_create_series_table)
        create_table(conn, sql_create_extended_data)
        return conn
    else:
        print("Error: cannot create the database connection.")
