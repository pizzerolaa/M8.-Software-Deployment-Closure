from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import os
import time

app = FastAPI()

class Input(BaseModel):
    dividendo: float
    divisor: float

class Equation(BaseModel):
    a: float
    b: float
    c: float
    d: float
    resultado: float

def wait_for_db():
    max_retries = 30
    retries = 0
    while retries < max_retries:
        try:
            conn = mysql.connector.connect(
                host = os.getenv("MYSQL_HOST", "db"),
                user = os.getenv("MYSQL_USER", "user"),
                password = os.getenv("MYSQL_PASSWORD", "password"),
                database = os.getenv("MYSQL_DATABASE", "ecuaciones")
            )
            if conn.is_connected():
                conn.close()
                return True
        except Error:
            retries += 1
            time.sleep(2)
    return False

@app.on_event("startup")
async def startup():
    if not wait_for_db():
        raise Exception("No se pudo conectar a la base de datos")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "db"),
            user=os.getenv("MYSQL_USER", "user"),
            password=os.getenv("MYSQL_PASSWORD", "password"),
            database=os.getenv("MYSQL_DATABASE", "ecuaciones")
        )
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resultados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                a FLOAT NOT NULL,
                b FLOAT NOT NULL,
                c FLOAT NOT NULL,
                d FLOAT NOT NULL,
                resultado FLOAT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    except Error as e:
        print(f"Error al crear tabla: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.post('/dividir')
def dividir(valores: Input):
    if valores.divisor == 0:
        raise HTTPException(status_code=400, detail="El divisor no puede ser cero")
    res = valores.dividendo / valores.divisor
    return {'resultado': res}

@app.post('/guardar')
def guardar_resultado(ecuacion: Equation):
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "db"),
            user=os.getenv("MYSQL_USER", "user"),
            password=os.getenv("MYSQL_PASSWORD", "password"),
            database=os.getenv("MYSQL_DATABASE", "ecuaciones")
        )
        cursor = conn.cursor()
        query = """
        INSERT INTO resultados (a, b, c, d, resultado)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (ecuacion.a, ecuacion.b, ecuacion.c, ecuacion.d, ecuacion.resultado)
        cursor.execute(query, values)
        conn.commit()
        return {"mensaje": "Resultado guardado correctamente", "id": cursor.lastrowid}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@app.get('/historial')
def obtener_historial():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "db"),
            user=os.getenv("MYSQL_USER", "user"),
            password=os.getenv("MYSQL_PASSWORD", "password"),
            database=os.getenv("MYSQL_DATABASE", "ecuaciones")
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resultados ORDER BY fecha_creacion DESC")
        resultados = cursor.fetchall()
        return {"resultados": resultados}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()