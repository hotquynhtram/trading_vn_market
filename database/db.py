import sqlite3
from sqlite3 import Error
import pandas as pd
from lambda_logging import logger


class DataBase(object):
    """
    contains methods to build the Ebay dataset
    param db_file: database filename. E.g: "ebay_training_data.db"

    """

    def __init__(self, db_file):

        self.db_file = db_file

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database filename
        :return: Connection object or None
        """
        try:
            connection = sqlite3.connect(self.db_file)
            logger.info("Connected to database successfully")
            return connection
        except Error as e:
            logger.error("Connect Failed")
            return None

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return: create a table object or None
        """
        try:
            c = conn.cursor()  # Interface of database
            c.execute(create_table_sql)
            logger.info("Table created")
        except Error as e:
            logger.error("Can not create table")

    def insert_table(self, conn, record, insert_record_sql):
        """
        Insert a new record into table
        :param conn: Connection object
        :param record: a list consists of Ebay Product Info
        :return: a new record in database or ignore it due to already existance. 
        """

        cur = conn.cursor()
        cur.execute(insert_record_sql, record)
        conn.commit()
        logger.info("Insert record successfully")

        return cur.lastrowid

    def update_table(self, conn, record,sql):
        """
        update task by task id
        task id: item number
        param: record is a list consists of ebay_report_category_id and label
        param conn: connection object

        """

        
        cur = conn.cursor()
        cur.execute(sql, record)
        conn.commit()
        logger.info("Update record successfully")

    def delete_table(self, conn, item_number, table_name):
        """
        Delete a task by task id
        :param conn:  connection object
        :param id: id of the task
        :return:
        """
        sql = "DELETE FROM {} WHERE item_number=?".format(table_name)
        cur = conn.cursor()
        cur.execute(sql, (item_number,))
        conn.commit()
        
    def select_data(self, conn, sql, value, option):       
        cur = conn.cursor()
        cur.execute(sql, value)
        if option == 1:
            rows = cur.fetchone()
        else:
            rows = cur.fetchall()
        return rows
            
    def select_column(self, conn, column_name, table_name):       
        cur = conn.cursor()
        cur.execute("SELECT {} FROM {}".format(column_name, table_name))
        rows = cur.fetchall()
        return rows
    
    def select_table(self, conn, q):

        df = pd.read_sql_query(q, conn)

        return df
