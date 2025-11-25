# Trabajo 2: Fusión de Perspectivas - Registro de Imágenes y Medición del Mundo Real

Este proyecto implementa un pipeline completo de visión por computador para fusionar tres imágenes parciales de un comedor en una única vista panorámica coherente. El objetivo principal es demostrar la robustez del algoritmo de registro mediante validación con imágenes sintéticas y, finalmente, calibrar el sistema para extraer mediciones del mundo real a partir de objetos de referencia.

---

## 1. Estructura del Repositorio

El proyecto utiliza una estructura modular para separar el código de la lógica, los datos y los resultados:

| Carpeta/Archivo | Contenido |
| :--- | :--- |
| **`data/`** | Imágenes originales (`original/`) y variantes generadas para la validación (`synthetic/`). |
| **`src/`** | Contiene todos los módulos de lógica (`.py`) para detección, emparejamiento, registro, calibración (`measurement.py`) y utilidades. |
| **`notebooks/`** | Contiene el flujo de trabajo de ejecución (`01`, `02`, `03`). |
| **`results/`** | Almacena el panorama final fusionado y la tabla de mediciones. |
| `requirements.txt` | Dependencias del entorno. |

---

## 2. Instalación y Configuración

El proyecto requiere **Python 3.8+** y las dependencias listadas en `requirements.txt` (incluyendo `opencv-contrib-python`, `numpy`, y `pandas`).

### **Configuración en MacOS y Linux**

Ejecute los siguientes comandos en el terminal:

```bash
# Crear entorno virtual
python3 -m venv .venv
# Activar entorno
source .venv/bin/activate
# Instalar dependencias
pip install -r requirements.txt

### **Configuración en Windows**

# Crear entorno virtual
python -m venv .venv
# Activar entorno
.venv\Scripts\activate
# Instalar dependencias
pip install -r requirements.txt