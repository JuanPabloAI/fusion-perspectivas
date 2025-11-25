import cv2
import numpy as np

def match_features(desc1, desc2, method='SIFT', ratio_thresh=0.75):
    """
    Empareja descriptores de dos imágenes y filtra usando el Lowe's Ratio Test.
    
    Args:
        desc1, desc2: Descriptores de las dos imágenes.
        method (str): Debe coincidir con el detector usado ('SIFT' usa L2, 'ORB' usa Hamming).
        ratio_thresh (float): Umbral para considerar un match como "bueno" (0.7-0.8).
        
    Returns:
        good_matches (list): Lista de objetos DMatch filtrados.
    """
    if desc1 is None or desc2 is None:
        return []

    if method == 'SIFT':
        # NORM_L2 es la métrica de distancia para descriptores basados en gradientes
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    elif method == 'ORB':
        # NORM_HAMMING es necesario para descriptores binarios
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    else:
        raise ValueError("Método desconocido. Use 'SIFT' o 'ORB'.")

    # knnMatch busca los k=2 mejores vecinos para aplicar el ratio test
    try:
        raw_matches = bf.knnMatch(desc1, desc2, k=2)
    except cv2.error:
        return []

    good_matches = []
    # Aplicar Ratio Test de Lowe:
    # El match es bueno si la distancia del primero es < ratio * distancia del segundo
    for m, n in raw_matches:
        if m.distance < ratio_thresh * n.distance:
            good_matches.append(m)

    return good_matches