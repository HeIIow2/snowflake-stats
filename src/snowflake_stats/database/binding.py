import sqlite3
import os

from ..objects import (
    RelayedData,
    RestartData,
    Relayed,
    Restart
)

"""
INITIALIZE EVERYTHING
"""

RESET_ANYWAYS = False

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


def write_relayed_data(relayed: RelayedData):
    """
    :param relayed:
    :return:
    """

    insert_query = "INSERT OR IGNORE INTO Relayed VALUES (?, ?, ?, ?);"
    cursor.executemany(insert_query, relayed.get_database_values())
    connection.commit()


def write_restarts(restarts: RestartData):
    """
    :param restarts:
    :return:
    """

    insert_query = "INSERT OR IGNORE INTO Restart VALUES (?);"
    cursor.executemany(insert_query, restarts.get_database_values())
    connection.commit()


"""
READING
"""


def get_relayed_data() -> RelayedData:
    relayed_data = RelayedData()

    cursor.execute("SELECT * FROM Relayed;")
    for row in cursor.fetchall():
        relayed_data.append(Relayed(row[0], row[1], row[2], row[3]))

    return relayed_data


def get_restart_data() -> RestartData:
    restart_list = RestartData()

    cursor.execute("SELECT * FROM Restart;")
    for row in cursor.fetchall():
        restart_list.append(Restart(row[0]))

    return restart_list
