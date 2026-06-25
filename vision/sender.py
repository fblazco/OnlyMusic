import socketio
import base64
import cv2

class VisionSender:
    def __init__(self, server_url="http://localhost:3000"):
        self.sio = socketio.Client()
        self.server_url = server_url
        self.is_connected = False

        # Eventos de Socket.IO
        @self.sio.event
        def connect():
            self.is_connected = True
            print("🟢 [Sender] Conectado al Cerebro (Backend)")

        @self.sio.event
        def disconnect():
            self.is_connected = False
            print("🔴 [Sender] Desconectado del Cerebro")

    def connect_to_server(self):
        try:
            print(f"[Sender] Intentando conectar a {self.server_url}...")
            self.sio.connect(self.server_url)
        except socketio.exceptions.ConnectionError:
            print("⚠️ [Sender] El servidor Node.js aún no está levantado. Iniciando en modo offline.")

    def send_state(self, x, y, genre_id):
        if self.is_connected:
            # Casteamos (transformamos) obligatoriamente a float y a int nativos de Python
            payload = {
                "pointer": {
                    "x": round(float(x), 3), 
                    "y": round(float(y), 3)
                },
                "genreId": int(genre_id) if genre_id is not None else None
            }
            # Enviamos la data cruda del sensor
            self.sio.emit('vision_data', payload)

    def send_frame(self, frame):
        if self.is_connected:
            # Achicamos la resolución a 640x360 para que el WebSocket no sufra lag
            small_frame = cv2.resize(frame, (640, 360))
            
            # Comprimimos a JPG con calidad al 50% para hacerlo ultraligero
            _, buffer = cv2.imencode('.jpg', small_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            
            # Convertimos los bytes de la imagen a texto plano (Base64)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            
            # Emitimos el frame de video al backend
            self.sio.emit('video_frame', jpg_as_text)

    def disconnect(self):
        if self.is_connected:
            self.sio.disconnect()