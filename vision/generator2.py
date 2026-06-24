import cv2
import numpy as np
from config import REFERENCE_IDS, POINTER_ID, GENRES

def generar_hoja_arucos():
# Cambia el 50 por 250
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    ids_to_generate = REFERENCE_IDS + [POINTER_ID] + list(GENRES.keys())
    
    # Configuración visual de la grilla
    marker_size = 200
    padding = 60
    cols = 3  # Cuántos marcadores por fila queremos
    rows = (len(ids_to_generate) + cols - 1) // cols
    
    # Crear un lienzo blanco gigante (ancho y alto total)
    canvas_h = rows * (marker_size + padding * 2)
    canvas_w = cols * (marker_size + padding * 2)
    # np.ones crea una matriz de 1s, multiplicada por 255 da blanco puro
    canvas = np.ones((canvas_h, canvas_w), dtype=np.uint8) * 255
    
    print("Armando la grilla de marcadores...")
    
    for idx, aruco_id in enumerate(ids_to_generate):
        row = idx // cols
        col = idx % cols
        
        # Generar la imagen del marcador
        img = cv2.aruco.generateImageMarker(aruco_dict, aruco_id, marker_size)
        
        # Calcular en qué coordenadas X e Y lo vamos a pegar
        y_offset = row * (marker_size + padding * 2) + padding
        x_offset = col * (marker_size + padding * 2) + padding
        
        # Pegar el marcador en el lienzo
        canvas[y_offset:y_offset+marker_size, x_offset:x_offset+marker_size] = img
        
        # Preparar el texto de la etiqueta
        label = f"ID: {aruco_id}"
        if aruco_id in REFERENCE_IDS: 
            label += " (Esquina)"
        elif aruco_id == POINTER_ID: 
            label += " (Puntero)"
        else: 
            label += f" ({GENRES.get(aruco_id, '')})"
            
        # Dibujar el texto arriba del marcador
        cv2.putText(canvas, label, (x_offset, y_offset - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0, 2)
        
    # Guardar la imagen final
    cv2.imwrite("hoja_arucos.png", canvas)
    print("¡Listo! Se generó 'hoja_arucos.png' con todos los marcadores ordenados.")

if __name__ == "__main__":
    generar_hoja_arucos()