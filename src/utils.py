import cv2
import numpy as np
import os

def generate_synthetic_image(image, angle=0, scale=1.0, tx=0, ty=0):
    """
    Aplica transformaciones afines a una imagen y devuelve la imagen transformada
    junto con la matriz de homografía (Ground Truth).
    """
    h, w = image.shape[:2]
    center = (w // 2, h // 2)

    # 1. Obtener matriz de rotación y escala
    # cv2.getRotationMatrix2D devuelve una matriz 2x3
    M_rot = cv2.getRotationMatrix2D(center, angle, scale)

    # 2. Agregar traslación (modificando la columna 2 de la matriz)
    M_rot[0, 2] += tx
    M_rot[1, 2] += ty

    # 3. Convertir a matriz de Homografía 3x3 (para que sea compatible con findHomography después)
    # Agregamos la fila [0, 0, 1] al final
    H_true = np.vstack([M_rot, [0, 0, 1]])

    # 4. Aplicar la transformación
    transformed_image = cv2.warpPerspective(image, H_true, (w, h))

    return transformed_image, H_true

def save_synthetic_data(image_name, original_img, output_dir):
    """
    Genera variaciones de una imagen y guarda los resultados y las matrices GT.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Definir experimentos: (ángulo, escala, tx, ty)
    experiments = [
        {"params": (10, 1.0, 0, 0), "suffix": "rot10"},        # Solo rotación
        {"params": (0, 1.2, 0, 0), "suffix": "scale1.2"},      # Solo escala
        {"params": (0, 1.0, 20, -30), "suffix": "trans"},      # Solo traslación
        {"params": (15, 0.9, 10, 10), "suffix": "mix"},        # Mezcla
    ]

    results_log = []

    print(f"--- Generando sintéticos para {image_name} ---")
    
    for exp in experiments:
        angle, scale, tx, ty = exp["params"]
        suffix = exp["suffix"]
        
        # Generar
        syn_img, H_gt = generate_synthetic_image(original_img, angle, scale, tx, ty)
        
        # Nombres de archivo
        base_name = os.path.splitext(image_name)[0]
        img_filename = f"{base_name}_{suffix}.jpg"
        mat_filename = f"{base_name}_{suffix}_H.npy"
        
        # Guardar imagen
        cv2.imwrite(os.path.join(output_dir, img_filename), syn_img)
        
        # Guardar matriz Ground Truth (usamos numpy para preservar precisión)
        np.save(os.path.join(output_dir, mat_filename), H_gt)
        
        print(f"Generado: {img_filename}")
        print(f"Matriz guardada en: {mat_filename}")

    return True