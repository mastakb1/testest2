import mysql.connector
import pandas as pd
import os

def create_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        port=os.getenv('MYSQL_PORT'),         
        user=os.getenv('MYSQL_USER'),            
        password=os.getenv('MYSQL_PASSWORD'),      
        database=os.getenv('MYSQL_DATABASE')  
    )

def get_data_from_db(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
