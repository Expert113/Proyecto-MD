from conecion import CConexion  # Corregido el nombre
import sqlite3
import hashlib
import re

def validar_correo(correo):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None

def registrar_usuario(nombre, correo, contraseña):
    # Validaciones
    if not nombre or not correo or not contraseña:
        return "Todos los campos son obligatorios"
    
    if not validar_correo(correo):
        return "El formato del correo no es válido"
    
    if len(contraseña) < 8:
        return "La contraseña debe tener al menos 8 caracteres"
    
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
            
            # Hash de la contraseña
            hash_contraseña = hashlib.sha256(contraseña.encode()).hexdigest()
            
            # Insertar nuevo usuario
            cursor.execute(
                'INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)',
                (nombre, correo, hash_contraseña)
            )
            
            conn.commit()
            return "Usuario registrado correctamente"
            
        except sqlite3.IntegrityError:
            conn.rollback()
            return "Error: El correo ya está registrado"
        except Exception as e:
            conn.rollback()
            return f"Error al registrar usuario: {str(e)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    return "Error de conexión a la base de datos"