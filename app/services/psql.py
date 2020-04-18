import os
import sys

import psycopg2
from psycopg2.extras import execute_values, DictCursor

from app.config.prod import PSQL_DB, PSQL_USER, PSQL_HOST, PSQL_PORT, PSQL_PASSWORD
from app.constants import TABLE_NAME, TABLE_COLUMNS
from utilities.logger import LoggerManager

logger = LoggerManager.get_logger()


class PSQL:
    """
    PSQL service class
    """
    __conn = None

    def __init__(self):
        if PSQL.__conn != None:
            raise Exception("This class is a singleton!")
        else:
            # creating psql connection.
            conn = self._psql_connection()
            PSQL.__conn = conn

    @staticmethod
    def get_instance():
        """
        Constructor to initialize Db connection.
        """
        if PSQL.__conn == None:
            PSQL()
        return PSQL.__conn


    def _psql_connection(self):
        """
        :return: Receives credentials from environmen variables
                and returns a psql connection
        """
        psql_credentials = {
            'database': os.getenv('PSQL_DB'),
            'user':  os.getenv('PSQL_USER'),
            'password':  os.getenv('PSQL_PASSWORD'),
            'host': os.getenv('PSQL_HOST'),
            'port': int(os.getenv('PSQL_PORT'))
        }
        try:
            # connecting to psql server
            connection = psycopg2.connect(**psql_credentials)
            logger.info("Connected successfully to PostgreSQL Server.")
        except Exception as e:
            logger.error("ERROR: Unable to connect to PostgreSQL Server. - {}".format(e))
            sys.exit()

        return connection


class DBService:
    """
    DB service class act as layer between DB and views.
    """

    def __init__(self):
        self.conn = PSQL.get_instance()
        self.cur = self.conn.cursor()
    
    def add_record(self, add_record, table=TABLE_NAME):
        """
        Function to add a record into db.
        """

        if not add_record:
            return

        insert_query = "INSERT INTO {}{} VALUES %s".format(
            table, TABLE_COLUMNS)
        try:
            execute_values(self.cur, insert_query, [add_record])
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
        

    def search_query(self, query, table=TABLE_NAME, limit=3):
        """
        Returns list of record dictionaries.
        """
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT content, created_by FROM {} WHERE content like '%{}%' order by created_at DESC LIMIT {};".format(
            table, query, limit))
        result = cursor.fetchall()
        cursor.close()
        return result
