import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="",
        database="sistema_cuestionarios" 
    )
    return conn


def inicialitzar_base_dades():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3307,
            user="root",
            password=""
        )

        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS sistema_cuestionarios")
        conn.close()

        conn = get_connection()
        cursor = conn.cursor()

        with open("database/database.sql", "r", encoding="utf-8") as f:
            schema = f.read()

        for statement in schema.split(";"):
            if statement.strip():
                cursor.execute(statement)

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error conectando a MySQL: {e}")