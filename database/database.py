import mysql

def get_connection():
    conn = mysql.connector.connect(
        host="onejar",
        port=3307,
        user="root",
        password="",
        database="sistema_cuestionarios",
        auth_plugin='mysql_native_password'
    )