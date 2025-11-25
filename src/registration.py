import cv2
import numpy as np

def estimate_homography(kp1, kp2, matches, reproj_thresh=4.0):
    """
    Calcula la matriz de homografía usando RANSAC.
    
    Args:
        kp1, kp2: Keypoints de imagen origen y destino.
        matches: Lista de matches buenos.
        reproj_thresh: Umbral de error en píxeles (RANSAC).
        
    Returns:
        H (numpy.ndarray): Matriz 3x3.
        mask (numpy.ndarray): Máscara de inliers.
    """
    if len(matches) < 4:
        print("No hay suficientes matches para calcular homografía (min 4).")
        return None, None

    # Extraer coordenadas (x, y) de los matches
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Calcular Homografía con RANSAC
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, reproj_thresh)

    return H, mask

def calculate_transform_error(H_est, H_true):
    """
    Calcula el error RMSE entre la matriz estimada y la real (Ground Truth).
    """
    if H_est is None:
        return float('inf')
        
    # Normalizar matrices (hacer que H[2,2] = 1) para comparación justa
    # Evitar división por cero
    if abs(H_est[2, 2]) > 1e-10: H_est = H_est / H_est[2, 2]
    if abs(H_true[2, 2]) > 1e-10: H_true = H_true / H_true[2, 2]
    
    rmse = np.sqrt(np.mean((H_est - H_true) ** 2))
    return rmse

def warp_image(img, H, shape):
    """
    Aplica la transformación de perspectiva a una imagen.
    """
    return cv2.warpPerspective(img, H, shape)