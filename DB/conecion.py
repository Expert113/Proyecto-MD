import sqlite3
import os

class CConexion:
    @staticmethod
    def ConexionBaseDeDatos():
        try:
            # Aseguramos que la base de datos se cree en la carpeta DB
            db_path = os.path.join(os.path.dirname(__file__), 'DBusuariosSqlite.db')
            conexion = sqlite3.connect(db_path)
            print("Conexión exitosa a la base de datos")
            return conexion
        except sqlite3.Error as error:
            print("Error en la conexión:", error)
            return None




