#!/usr/bin/env python3
import argparse
import os
import sqlite3
from pathlib import Path
from sqlite3 import Error

DATABASE = r"%s/.gcd/gcd.sqlite" % str(Path.home())
CACHE_FILE = r"%s/.gcd/gcd.cache" % str(Path.home())

SQL_CREATE_PROJECTS_TABLE = """
                            CREATE TABLE IF NOT EXISTS projects (
                            project text PRIMARY KEY,
                            called integer NOT NULL DEFAULT 0
                            );
                            """


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def increment(conn, project):
    with conn:
        c = conn.cursor()
        c.execute("""INSERT OR REPLACE 
                     INTO projects (project, called) 
                     VALUES 
                     (?,
                      (SELECT called FROM projects WHERE project=?) + 1
                     )""", (project, project,))


def create_rows(conn, cache_file):
    with conn:
        c = conn.cursor()
        with open(cache_file) as fi:
            lines = fi.read().split("\n")
        for project in lines:
            if project:
                c.execute("""INSERT OR REPLACE 
                             INTO projects (project, called) 
                             VALUES 
                             (?,
                              (SELECT called FROM projects WHERE project=?)
                             )""", (project, project,))


def export_cache_file(conn, cache_file):
    with conn:
        c = conn.cursor()
        with open(cache_file, "w") as fo:
            c.execute("SELECT project FROM projects ORDER BY called DESC, project ASC")
            rows = c.fetchall()
            [fo.write(x[0] + "\n") for x in rows]


def delete(conn, project):
    with conn:
        c = conn.cursor()
        c.execute("DELETE FROM projects WHERE project =?", (project,))


def zap_entries(conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT project FROM projects")
        rows = c.fetchall()
        rows = [x[0] for x in rows]
        for project in rows:
            if not os.path.isdir(project):
                print("Deleting project entry: %s" % project)
                delete(conn, project)


def main(args):
    if args.create_db:
        if os.path.isfile(DATABASE):
            os.remove(DATABASE)

    conn = create_connection(DATABASE)

    with conn:
        if args.create_db:
            create_table(conn, SQL_CREATE_PROJECTS_TABLE)
            create_rows(conn, CACHE_FILE)

        if args.import_cache:
            create_rows(conn, CACHE_FILE)

        if args.export_cache:
            export_cache_file(conn, CACHE_FILE)

        if args.zap:
            zap_entries(conn)

        if args.project:
            increment(conn, args.project)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("python3 gcd.py")
    parser.add_argument_group()
    parser.add_argument('-i', '--import-cache', action='store_true', help="Import the cache")
    parser.add_argument('-c', '--create-db', action='store_true', help="(Re-)Creates the database")
    parser.add_argument('-e', '--export-cache', action='store_true', help="Exports the database to cache")
    parser.add_argument('-z', '--zap', action='store_true', help="Zaps non existing projects from database")
    parser.add_argument('-p', '--project', help="Increments the project")
    main(parser.parse_args())
