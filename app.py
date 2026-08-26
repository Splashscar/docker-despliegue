from flask import Flask, request, render_template, redirect, url_for
import pymysql
import os

sample = Flask(__name__)

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
    'cursorclass': pymysql.cursors.DictCursor
}   


def inicializar_base_datos():
    """Crea la base de datos y la tabla 'aprendices' si no existen al iniciar la app"""
    try:
        # Nos conectamos primero sin especificar base de datos para asegurarnos de que exista
        conexion_temp = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor_temp = conexion_temp.cursor()
        cursor_temp.execute("CREATE DATABASE IF NOT EXISTS adso_db;")
        conexion_temp.close()

        # Ahora nos conectamos a 'adso_db' para crear la tabla
        conexion = pymysql.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aprendices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_completo VARCHAR(100) NOT NULL,
                numero_documento VARCHAR(20) NOT NULL,
                ficha VARCHAR(20) NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Base de datos y tabla 'aprendices' inicializadas correctamente.")
    except Exception as e:
        print(f"Advertencia al inicializar la BD (es posible que el contenedor de la BD aún esté iniciando): {e}")


# Ruta Principal (GET /): Muestra el formulario y la lista de aprendices registrados
@sample.route("/", methods=["GET"])
def home():
    db_status = ""
    aprendices = []
    
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Consultar los registros guardados
        cursor.execute("SELECT * FROM aprendices ORDER BY creado_en DESC;")
        aprendices = cursor.fetchall()
        
        cursor.close()
        conn.close()
        db_status = "Conexión exitosa a la base de datos"
    except Exception as e:
        db_status = f"Error al conectar a la base de datos: {str(e)}"

    # Renderiza el template y le pasa tanto el estado de la db como la lista de aprendices
    return render_template("index.html", db_status=db_status, aprendices=aprendices)


# Ruta de Registro (POST /registrar): Procesa el formulario y guarda en MySQL
@sample.route("/registrar", methods=["POST"])
def registrar():
    nombre_completo = request.form.get("nombre_completo")
    numero_documento = request.form.get("numero_documento")
    ficha = request.form.get("ficha")
    
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        sql = "INSERT INTO aprendices (nombre_completo, numero_documento, ficha) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre_completo, numero_documento, ficha))
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al registrar: {e}")
        
    return redirect(url_for("home"))

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT", "5050"))

if __name__ == "__main__":
    inicializar_base_datos()
    sample.run(host=HOST, port=PORT, debug=False)
