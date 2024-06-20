import mysql.connector
import pandas as pd

def create_connection():
    return mysql.connector.connect(
        host="kubela.id",
        port="3306",         
        user="davis2024irwan",            
        password="wh451n9m@ch1n3",      
        database="aw"  
    
    )

def get_data_from_db(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
