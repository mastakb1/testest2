import mysql.connector
import pandas as pd
import os

import toml

# Fungsi untuk membaca file konfigurasi TOML
def read_config(filename='config.toml'):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} tidak ditemukan.")
    with open(filename, 'r') as f:
        config = toml.load(f)
    return config

def create_connection():
    config = read_config()
    return mysql.connector.connect(
        host=config['database']['host'],
        port=config['database']['port'],
        user=config['database']['user'],
        password=config['database']['password'],
        database=config['database']['database_name']
    )


def get_data_from_db(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
