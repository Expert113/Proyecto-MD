from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import json
from conecion import CConexion
from usuairo_controlador import registrar_usuario

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                # Ajustamos la ruta al archivo HTML
                html_path = os.path.join(os.path.dirname(__file__), '..', 'Vista', 'ACCESO WEB', 'Pg.Registro.html')
                with open(html_path, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                print(f"Error al servir HTML: {e}")
                self.send_error(404, "Página no encontrada")

    def do_POST(self):
        if self.path == '/registro':
            try:
                length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(length)
                datos = urllib.parse.parse_qs(post_data.decode('utf-8'))

                nombre = datos.get('nombre', [''])[0]
                correo = datos.get('correo', [''])[0]
                contraseña = datos.get('contraseña', [''])[0]

                mensaje = registrar_usuario(nombre, correo, contraseña)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"mensaje": mensaje}).encode())
            except Exception as e:
                print(f"Error en POST: {e}")
                self.send_error(500, str(e))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    try:
        server = HTTPServer(('localhost', 8000), Servidor)
        print("Servidor corriendo en http://localhost:8000")
        server.serve_forever()
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")