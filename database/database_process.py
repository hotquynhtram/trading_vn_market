import pickle
import pandas as pd
from db import DataBase
import os
import hashlib

def create_database(database_name, table_name):
    """
    Connect to the database,
    Create table if not exist, 
    Insert new record into table
    """

    # create a database instance
    db = DataBase(database_name)

    # Create database connection
    conn = db.create_connection()

    # create ebay_poc table if not exist
    create_table_sql = f"""CREATE TABLE IF NOT EXISTS {table_name} 
                    (id INT PRIMARY KEY ,
                     url TEXT,
                     title  TEXT ,
                     alltext TEXT ,
                     publish_date TEXT,
                     author TEXT )"""

    db.create_table(conn, create_table_sql)
    

    # Insert each row of dataframe as info of a product into database
if __name__ == '__main__':   
    create_database('newsdata.sqlite', 'news')

