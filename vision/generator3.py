import cv2
import numpy as np
from config import REFERENCE_IDS, POINTER_ID, GENRES


def generar_hoja(ids_to_generate, nombre_archivo):
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

    marker_size = 200
    padding = 60
    text_space = 40

    cols = 3
    rows = (len(ids_to_generate) + cols - 1) // cols

    cell_w = marker_size + padding * 2
    cell_h = marker_size + padding * 2 + text_space

    canvas = np.ones(
        (rows * cell_h, cols * cell_w),
        dtype=np.uint8
    ) * 255

    for idx, aruco_id in enumerate(ids_to_generate):

        row = idx // cols
        col = idx % cols

        marker = cv2.aruco.generateImageMarker(
            aruco_dict,
            aruco_id,
            marker_size
        )

        x = col * cell_w + padding
        y = row * cell_h + padding + text_space

        canvas[y:y+marker_size, x:x+marker_size] = marker

        if aruco_id in REFERENCE_IDS:
            texto = f"ID {aruco_id} - Esquina"
        elif aruco_id == POINTER_ID:
            texto = f"ID {aruco_id} - Puntero"
        else:
            texto = f"{aruco_id} - {GENRES[aruco_id]}"

        cv2.putText(
            canvas,
            texto,
            (x, y - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            0,
            2,
            cv2.LINE_AA
        )

    cv2.imwrite(nombre_archivo, canvas)
    print(f"✔ {nombre_archivo} generado.")


def generar_hojas_arucos():

    ids = REFERENCE_IDS + [POINTER_ID] + sorted(GENRES.keys())

    n_hojas = 2
    tam = (len(ids) + n_hojas - 1) // n_hojas  # redondeo hacia arriba

    for i in range(n_hojas):
        inicio = i * tam
        fin = min((i + 1) * tam, len(ids))

        generar_hoja(
            ids[inicio:fin],
            f"hoja_arucos_{i+1}.png"
        )


if __name__ == "__main__":
    generar_hojas_arucos()
