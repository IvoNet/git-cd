#!/usr/bin/env python3
import argparse
import os
import sqlite3
from pathlib import Path
from sqlite3 import Error

DATABASE = r"%s/.gcd/gcd.sqlite" % str(Path.home())
CACHE_FILE = r"%s/.gcd/gcd.cache" % str(Path.home())
ALIAS_FILE = r"%s/.gcd/gcd.alias" % str(Path.home())

SQL_CREATE_PROJECTS_TABLE = """
                            CREATE TABLE IF NOT EXISTS projects (
                            project text PRIMARY KEY,
                            alias text,
                            called integer NOT NULL DEFAULT 0
                            );
                            """


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return None


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
    """ Increment the called field on a project
    :param conn: Connection object
    :param project: project directory
    :return:
    """
    with conn:
        c = conn.cursor()
        c.execute("""INSERT OR REPLACE 
                     INTO projects (project, alias, called) 
                     VALUES 
                     (?,
                      (SELECT alias FROM projects WHERE project=?),
                      (SELECT called FROM projects WHERE project=?) + 1
                     )""", (project, project, project,))


def create_rows(conn, cache_file):
    """ Create project entries in the database if it does not yet exist.
    :param conn: Connection object
    :param cache_file: the cach_file to import
    :return:
    """
    with conn:
        c = conn.cursor()
        with open(cache_file) as fi:
            lines = fi.read().split("\n")
        for project in lines:
            if project:
                c.execute("""INSERT OR REPLACE 
                             INTO projects (project, alias, called) 
                             VALUES 
                             (?,
                              (SELECT alias FROM projects WHERE project=?),
                              (SELECT called FROM projects WHERE project=?)
                             )""", (project, project, project,))


def export_cache_file(conn, cache_file):
    """ Export the newly sorted cache file based. Sorted based on the metrix
    :param conn: Connection object
    :param cache_file: the cache_file location
    :return:
    """
    with conn:
        c = conn.cursor()
        with open(cache_file, "w") as fo:
            c.execute("SELECT project FROM projects ORDER BY called DESC, project")
            rows = c.fetchall()
            [fo.write(x[0] + "\n") for x in rows]


def delete(conn, project):
    """ Deletes a directory from the metrics db.
    :param conn: Connection object
    :param project:
    :return:
    """
    with conn:
        c = conn.cursor()
        c.execute("DELETE FROM projects WHERE project =?", (project,))


def zap_entries(conn):
    """ Zaps (deletes) entries from the metrics db if the project does not
    physically exist on the machine.
    :param conn: Connection object
    :return:
    """
    with conn:
        c = conn.cursor()
        c.execute("SELECT project FROM projects")
        rows = c.fetchall()
        rows = [x[0] for x in rows]
        for project in rows:
            if not os.path.isdir(project):
                print("Zapping from cache: %s" % project)
                delete(conn, project)


def add_directory(conn, add_dir):
    """
    Add a directory to the cache. This does not need to be a git managed directory
    :param conn: the db connection
    :param add_dir: the dir to add
    :return:
    """
    with conn:
        c = conn.cursor()
        c.execute("""INSERT OR REPLACE 
                     INTO projects (project, alias, called) 
                     VALUES 
                     (?,
                      (SELECT alias FROM projects WHERE project=?),
                      (SELECT called FROM projects WHERE project=?)
                     )""", (add_dir, add_dir, add_dir,))


def add_alias(conn, alias, directory):
    """
    Adds an alias to a directory for easy retrieval.
    :param conn: the db connection
    :param alias: the alias to set
    :param directory: on the directory provided here
    :return:
    """
    with conn:
        c = conn.cursor()
        c.execute("""INSERT OR REPLACE 
                     INTO projects (project, alias, called) 
                     VALUES 
                     (?, ?,
                      (SELECT called FROM projects WHERE project=?)
                     )""", (directory, alias, directory))


def remove_alias(conn, alias):
    """
    Removes a specific alias reference for all directories with that alias
    :param conn: the db connection
    :param alias: the alias to remove
    :return:
    """
    with conn:
        c = conn.cursor()
        c.execute("""UPDATE projects 
                     SET alias = null 
                     WHERE alias = '%(alias)s'
                     """ % locals())


def retrieve_alias(conn, alias):
    """Retrieve the sorted set of directories belonging to an alias
    :param alias: the alias to retrieve
    :param conn: Connection object
    :return:
    """
    with conn:
        c = conn.cursor()
        with open(ALIAS_FILE, "w") as fo:
            c.execute("SELECT alias, project FROM projects WHERE alias = '%(alias)s' ORDER BY called DESC, project" % locals())
            return c.fetchall()


def export_alias(conn, alias):
    """Export the sorted set of directories belonging to an alias
    :param conn: Connection object
    :return:
    """
    with open(ALIAS_FILE, "w") as fo:
        rows = retrieve_alias(conn, alias)
        [fo.write(x[1] + "\n") for x in rows]


def get_alias(conn, alias):
    """
    Get the sorted set of directories belonging to an alias and print it.
    :param conn: the db connection
    :param alias: the alias to get
    :return:
    """
    rows = retrieve_alias(conn, alias)
    [print("%-20s: %s" % x) for x in rows]


def show_aliases(conn):
    """
    Show all aliases with their directories sorted by alias and number of times called.
    :param conn: the db connection
    :return:
    """
    with conn:
        c = conn.cursor()
        c.execute("""SELECT alias, project FROM projects WHERE alias NOT NULL ORDER BY alias, called DESC""")
        rows = c.fetchall()
        [print("%-20s: %s" % x) for x in rows]


def main(args):
    if args.create_db and os.path.isfile(DATABASE):
        os.remove(DATABASE)

    conn = create_connection(DATABASE)

    with conn:
        if args.create_db:
            create_table(conn, SQL_CREATE_PROJECTS_TABLE)

        if args.import_cache:
            create_rows(conn, CACHE_FILE)

        if args.export_cache:
            export_cache_file(conn, CACHE_FILE)

        if args.zap:
            zap_entries(conn)

        if args.add_dir:
            add_directory(conn, args.add_dir)

        if args.alias:
            add_alias(conn, args.alias[0], args.alias[1])

        if args.aliases:
            show_aliases(conn)

        if args.get_alias:
            get_alias(conn, args.get_alias)

        if args.unalias:
            remove_alias(conn, args.unalias)

        if args.export_alias:
            export_alias(conn, args.export_alias)

        if args.increment:
            increment(conn, args.increment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("python3 gcd.py")
    parser.add_argument_group()
    parser.add_argument('--create-db', action='store_true', help="(Re-)Creates the database")
    parser.add_argument('--import-cache', action='store_true', help="Import the cache")
    parser.add_argument('--export-cache', action='store_true', help="Exports the database to cache")
    parser.add_argument('--add-dir', help="Add directory to database")
    parser.add_argument('--export-alias', help="Export alias to alias cache")
    parser.add_argument('--aliases', action='store_true', help="Print unique set of aliases")
    parser.add_argument('--get-alias', help="Select all directories with alias")
    parser.add_argument('--alias', nargs=2, metavar=('ALIAS', 'DIR'), help="Add alias to directory")
    parser.add_argument('--unalias', help="Remove alias")
    parser.add_argument('--zap', action='store_true', help="Zaps non existing directories from database")
    parser.add_argument('--increment', help="Increments the directory metrics")
    main(parser.parse_args())
