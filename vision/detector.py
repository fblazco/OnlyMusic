import cv2

class ArUcoDetector:
    def __init__(self):
        # DICT_4X4_50: 4x4 bits, hasta 50 IDs distintos. Perfecto para nosotros.
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)

    def detect(self, frame):
        # Escala de grises = procesamiento mucho más rápido
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = self.detector.detectMarkers(gray)
        return corners, ids