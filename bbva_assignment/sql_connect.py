import traceback
from pathlib import Path
from typing import Any, Dict, List, Tuple

import psycopg2

from .config import config

RAW_DATA_PATH = Path(".").absolute().parent / "data" / "raw"

# read connection parameters
params = config(filename=Path(".").absolute().parent / "database.ini")


def get_connection(connection_params: Dict[str, Any]) -> psycopg2.extensions.connection:
    """Get a connection to the database

    Parameters
    ----------
    connection_params : Dict[str, Any]
        Parameters to pass to `psycopg2.connect` to connect to the database

    Returns
    -------
    psycopg2.extensions.connection
        Connection to the database
    """
    return psycopg2.connect(**connection_params)


def run_sql_command(
    query: str,
    connection: psycopg2.extensions.connection = None,
    connection_params: Dict[str, Any] = None,
) -> List[Tuple]:
    """Run a SQL command

    Parameters
    ----------
    query : str
        SQL query
    connection : psycopg2.extensions.connection
        Connection to the database. When set to None, a new connection is created
        with ``connection_params``. Defaults to None
    connection_params : Dict[str, Any]
        Parameters to pass to `psycopg2.connect` to connect to the database,
        when the ``connection`` is not provided. Defaults to None

    Returns
    -------
    List[Tuple]
        List of tuples with the results of the query

    Raises
    ------
    Tuple[Exception, psycopg2.DatabaseError]
        If the query fails
    """
    if connection is None or connection.closed:
        connection = get_connection(connection_params)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            record = cursor.fetchall()
    except Exception as error:
        print(type(error))
        traceback.print_exception(error)
        print(f"Connection failed. Starting a new connection and trying again...")

        connection.close()
        with get_connection(connection_params).cursor() as cursor:
            cursor.execute(query)
            record = cursor.fetchall()

    return record