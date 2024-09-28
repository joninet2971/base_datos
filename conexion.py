import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = mysql.connector.connect(
        host="143.198.156.171",
        user="BD2021",
        password="BD2021itec",
        database="db_desplats2"
    )
    return connection