import numpy as np
import cv2

class Calibrator:
    def __init__(self):
        self.pixels_per_cm = None
        self.image = None # Variable para guardar la imagen visualmente

    def set_image(self, image):
        """Carga la imagen sobre la cual se trabajará."""
        self.image = image.copy()

    def calibrate(self, point1, point2, real_distance_cm):
        """
        Calcula el factor de escala basado en una distancia real conocida.
        """
        p1 = np.array(point1)
        p2 = np.array(point2)
        
        dist_pixels = np.linalg.norm(p1 - p2)
        
        if real_distance_cm > 0 and dist_pixels > 0:
            self.pixels_per_cm = dist_pixels / real_distance_cm
            print(f"✅ Sistema Calibrado: {dist_pixels:.2f} px = {real_distance_cm} cm")
            print(f"   Factor: {self.pixels_per_cm:.4f} px/cm")
            return self.pixels_per_cm
        return 0

    def measure(self, point1, point2):
        """
        Devuelve la distancia real entre dos puntos nuevos.
        """
        if self.pixels_per_cm is None:
            print("Error: El sistema no está calibrado.")
            return None
            
        p1 = np.array(point1)
        p2 = np.array(point2)
        dist_pixels = np.linalg.norm(p1 - p2)
        
        # Distancia en cm = Distancia pixeles / pixeles_por_cm
        return dist_pixels / self.pixels_per_cm

    # --- NUEVO: Parte Interactiva (GUI) ---
    def seleccionar_puntos_interactivo(self, titulo_ventana="Seleccionar Puntos", n_puntos=2):
        """
        Abre una ventana de OpenCV y permite al usuario hacer clic para obtener coordenadas.
        """
        if self.image is None:
            print("Error: Carga una imagen primero usando set_image()")
            return []

        puntos = []
        img_temp = self.image.copy()

        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                puntos.append((x, y))
                # Dibujar marca visual (Círculo rojo)
                cv2.circle(img_temp, (x, y), 8, (0, 0, 255), -1)
                # Dibujar texto
                cv2.putText(img_temp, f"P{len(puntos)}", (x+10, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.imshow(titulo_ventana, img_temp)

        print(f"👉 Haz clic en {n_puntos} puntos en la ventana '{titulo_ventana}'.")
        print("   (Presiona cualquier tecla para confirmar cuando termines)")

        cv2.imshow(titulo_ventana, img_temp)
        cv2.setMouseCallback(titulo_ventana, click_event)
        
        # Esperar hasta presionar tecla
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return puntos[:n_puntos]