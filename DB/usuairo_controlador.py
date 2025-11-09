from conecion import CConexion
import sqlite3

def registrar_usuario(nombre, correo, contraseña):
    if not nombre or not correo or not contraseña:
        return "Todos los campos son obligatorios"
    
    conn = CConexion.ConexionBaseDeDatos()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            
            # Crear tabla si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT UNIQUE NOT NULL,
                    contraseña TEXT NOT NULL
                )
            ''')
            
            # Insertar nuevo usuario
            cursor.execute(
                'INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)',
                (nombre, correo, contraseña)
            )
            
            conn.commit()
            return "Usuario registrado correctamente"
            
        except sqlite3.IntegrityError:
            return "Error: El correo ya está registrado"
        except Exception as e:
            return f"Error al registrar usuario: {str(e)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    return "Error de conexión a la base de datos"