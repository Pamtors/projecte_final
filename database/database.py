import mysql.connector
import os

def get_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "quizzbattle")
    )
    return conn

def inicialitzar_base_dades():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "")
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS quizzbattle")
        conn.close()

        conn = get_connection()
        cursor = conn.cursor()
        
        with open("database/schema.sql", "r") as f:
            schema = f.read()
            
        for statement in schema.split(";"):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error connectant a MySQL: {e}")
        print("Recorda tenir el servidor MySQL encès i l'usuari configurat.")
