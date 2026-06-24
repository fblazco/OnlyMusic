import cv2
from config import REFERENCE_IDS, POINTER_ID, GENRES

def generar_arucos():
    # Usamos el mismo diccionario de tu detector
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    
    # Juntamos todos los IDs que tu sistema necesita
    ids_to_generate = REFERENCE_IDS + [POINTER_ID] + list(GENRES.keys())
    
    print("Generando marcadores...")
    for aruco_id in ids_to_generate:
        # Genera una imagen de 200x200 píxeles por cada ID
        img = cv2.aruco.generateImageMarker(aruco_dict, aruco_id, 200)
        filename = f"aruco_ID_{aruco_id}.png"
        cv2.imwrite(filename, img)
        print(f" Guardado: {filename}")
        
    print("¡Listo! Tienes todos los PNG en tu carpeta.")

if __name__ == "__main__":
    generar_arucos()