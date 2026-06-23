import cv2
import numpy as np

class Calibrator:
    def __init__(self, reference_ids):
        self.reference_ids = reference_ids
        # Mapeamos el tablero a un plano cuadrado virtual de 1000x1000 píxeles
        self.target_size = 1000 
        
        # Las 4 esquinas perfectas de nuestro plano virtual
        self.dst_points = np.array([
            [0, 0],                                     # Top-Left (ID 0)
            [self.target_size, 0],                      # Top-Right (ID 1)
            [self.target_size, self.target_size],       # Bottom-Right (ID 2)
            [0, self.target_size]                       # Bottom-Left (ID 3)
        ], dtype="float32")
        
        self.matrix = None

    def _get_center(self, corner):
        # Transforma las 4 esquinas del marcador ArUco en un solo punto central
        pts = corner.reshape((4, 2))
        return pts.mean(axis=0)

    def update_matrix(self, corners, ids):
        # Buscar los centros de los ArUcos de referencia
        ref_centers = {}
        for i, marker_id in enumerate(ids.flatten()):
            if marker_id in self.reference_ids:
                ref_centers[marker_id] = self._get_center(corners[i])

        # Si no ve las 4 esquinas de calibración, no actualiza la matriz
        if len(ref_centers) < 4:
            return False

        try:
            # Ordenamos los puntos de la cámara según nuestros IDs (0, 1, 2, 3)
            src_points = np.array([
                ref_centers[self.reference_ids[0]],
                ref_centers[self.reference_ids[1]],
                ref_centers[self.reference_ids[2]],
                ref_centers[self.reference_ids[3]]
            ], dtype="float32")
            
            # Calcula la matriz de transformación de perspectiva
            self.matrix = cv2.getPerspectiveTransform(src_points, self.dst_points)
            return True
        except KeyError:
            return False

    def get_normalized_position(self, corner):
        if self.matrix is None:
            return None
        
        center = self._get_center(corner)
        
        # Aplicamos la matriz de homografía al punto del puntero
        pt = np.array([[[center[0], center[1]]]], dtype="float32")
        transformed = cv2.perspectiveTransform(pt, self.matrix)
        
        # Retornamos x, y como porcentajes (entre 0.0 y 1.0)
        x = transformed[0][0][0] / self.target_size
        y = transformed[0][0][1] / self.target_size
        
        # Limitar valores entre 0 y 1 por si el puntero sale un poco del tablero
        return max(0.0, min(1.0, x)), max(0.0, min(1.0, y))