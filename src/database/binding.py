import sqlite3
import datetime
import os

from .objects import (
    Relayed,
    RestartInfo
)

"""
INITIALIZE EVERYTHING
"""

RESET_ANYWAYS = True

DB_FILE = "snow.db"
initialize = not os.path.exists(DB_FILE)
if RESET_ANYWAYS and os.path.exists(DB_FILE):
    os.remove(DB_FILE)

connection = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = connection.cursor()

if initialize or RESET_ANYWAYS:
    with open("structure.sql", "r") as structure_file:
        query = structure_file.read()

    cursor.executescript(query)
    connection.commit()

"""
WRITING
"""


def add_relayed_data(relayed: Relayed):
    """
    :param relayed:
    :return:
    """

    insert_query = "INSERT INTO Relayed VALUES (?, ?, ?, ?);"
    cursor.executemany(insert_query, relayed.get_database_values())
    connection.commit()


def add_restart(restarts: RestartInfo):
    """
    :param restarts:
    :return:
    """

    insert_query = "INSERT INTO Restart VALUES (?);"
    cursor.executemany(insert_query, restarts.get_database_values())
    connection.commit()
