import cv2
import numpy as np

def detect_features(image, method='SIFT'):
    """
    Detecta keypoints y calcula descriptores para una imagen dada.
    
    Args:
        image (numpy.ndarray): Imagen de entrada (BGR o Gray).
        method (str): 'SIFT' o 'ORB'.
        
    Returns:
        keypoints (list): Puntos clave detectados.
        descriptors (numpy.ndarray): Descriptores calculados.
    """
    if image is None:
        raise ValueError("La imagen proporcionada es None")

    # Convertir a escala de grises si es necesario
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    if method == 'SIFT':
        # SIFT: Invariante a escala, rotación e iluminación
        detector = cv2.SIFT_create()
    elif method == 'ORB':
        # ORB: Alternativa rápida y eficiente
        detector = cv2.ORB_create(nfeatures=2000)
    else:
        raise ValueError(f"Método '{method}' no soportado. Use 'SIFT' o 'ORB'.")

    keypoints, descriptors = detector.detectAndCompute(gray, None)
    
    return keypoints, descriptors