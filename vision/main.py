import cv2
from config import CAMERA_INDEX, REFERENCE_IDS, POINTER_ID, GENRES
from camera import Camera
from detector import ArUcoDetector
from calibrator import Calibrator
from sender import VisionSender

def main():
    print("Iniciando el Ojo, Calibrador y Transmisor...")
    cam = Camera(camera_index=CAMERA_INDEX)
    detector = ArUcoDetector()
    calibrator = Calibrator(REFERENCE_IDS)
    
    # Inicializamos y conectamos el emisor de WebSockets
    sender = VisionSender()
    sender.connect_to_server()

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                break

            corners, ids = detector.detect(frame)

            if ids is not None:
                # Dibujamos los cuadritos verdes en el frame local
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                
                # 1. Intentar actualizar la calibración si vemos las 4 esquinas
                is_calibrated = calibrator.update_matrix(corners, ids)
                
                if is_calibrated:
                    cv2.putText(frame, "TABLERO CALIBRADO", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    pointer_pos = None
                    active_genre_id = None
                    
                    # 2. Analizar la mesa (buscar puntero y géneros)
                    for i, marker_id in enumerate(ids.flatten()):
                        if marker_id == POINTER_ID:
                            pointer_pos = calibrator.get_normalized_position(corners[i])
                        elif marker_id in GENRES.keys():
                            active_genre_id = marker_id
                    
                    # 3. Si encontramos el puntero, enviamos la data al Node.js
                    if pointer_pos:
                        x, y = pointer_pos
                        sender.send_state(x, y, active_genre_id)
                        
                        texto_pos = f"Puntero: X={x:.2f}, Y={y:.2f} | Genero ID: {active_genre_id}"
                        cv2.putText(frame, texto_pos, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 0), 2)
                else:
                    cv2.putText(frame, "Buscando esquinas (0,1,2,3)...", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Mostramos la ventana en el Mac
            cv2.imshow("Visión - Infovis", frame)
            
            # 4. NUEVO: Enviamos el frame comprimido a la página web en React
            sender.send_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        sender.disconnect()
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()