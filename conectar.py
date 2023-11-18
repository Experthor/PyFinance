from config import config
import psycopg2


def conectar():
    conexion = None
    try:
        params = config()
        print("Estableciendo conexión con la Base de Datos")
        conexion = psycopg2.connect(**params)

        conexion.autocommit = True

        cursor = conexion.cursor()
        cursor.execute("SELECT version();")
        datos = cursor.fetchone()
        print("La versión de PostgreSQL es", datos[0])
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    else:
        print("Conexión exitosa a la Base de Datos")

    finally:
        if conexion is not None:
            return conexion
