import cv2
from config import CAMERA_INDEX
from camera import Camera
from detector import ArUcoDetector

def main():
    print("Iniciando el Ojo... (Presiona 'q' en la ventana de video para salir)")
    cam = Camera(camera_index=CAMERA_INDEX)
    detector = ArUcoDetector()

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                print("Fallo al capturar frame. Revisa la terminal.")
                break

            corners, ids = detector.detect(frame)

            if ids is not None:
                # Dibuja un cuadrito verde alrededor del ArUco detectado
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                print(f"IDs detectados: {ids.flatten()}")

            cv2.imshow("Visión - Infovis", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()
        print("Cámara apagada. Todo clean.")

if __name__ == "__main__":
    main()