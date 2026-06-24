import cv2
from config import CAMERA_INDEX, REFERENCE_IDS, POINTER_ID
from camera import Camera
from detector import ArUcoDetector
from calibrator import Calibrator

def main():
    print("Iniciando el Ojo y el Calibrador...")
    cam = Camera(camera_index=CAMERA_INDEX)
    detector = ArUcoDetector()
    calibrator = Calibrator(REFERENCE_IDS)

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                break

            corners, ids = detector.detect(frame)

            if ids is not None:
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                
                # 1. Intentar actualizar la calibración si vemos las 4 esquinas
                is_calibrated = calibrator.update_matrix(corners, ids)
                
                if is_calibrated:
                    cv2.putText(frame, "TABLERO CALIBRADO", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # 2. Buscar el puntero
                    for i, marker_id in enumerate(ids.flatten()):
                        if marker_id == POINTER_ID:
                            # Obtener posición (x, y) normalizada
                            pos = calibrator.get_normalized_position(corners[i])
                            if pos:
                                x, y = pos
                                texto_pos = f"Puntero: X={x:.2f}, Y={y:.2f}"
                                cv2.putText(frame, texto_pos, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 2)
                                print(texto_pos)
                else:
                    cv2.putText(frame, "Buscando esquinas (0,1,2,3)...", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Visión - Infovis", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()