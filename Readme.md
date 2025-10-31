# Convertidor de Archivos AFM a GWY y PNG

Este proyecto contiene scripts para convertir archivos de Microscopía de Fuerza Atómica (AFM) a varios formatos utilizando Gwyddion.

## Requisitos Previos

- Gwyddion (versión 32 bits)
- Python 2.7
- Consola pygwy de Gwyddion

> **Nota**: Debido a las limitaciones de Gwyddion, solo funciona con la versión de 32 bits y Python 2.7.

## Instalación del Entorno Virtual

1. Crear un entorno virtual:
   ```powershell
   python -m venv env
   ```

2. Activar el entorno virtual:
   - En Windows (PowerShell):
     ```powershell
     .\env\Scripts\Activate.ps1
     ```

3. Instalar las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

## Flujo de Trabajo

### 1. Conversión de AFM a GWY
Ejecutar en la consola pygwy de Gwyddion:
```python
exec(open("C:/PATH/TO/AFM_ToolKit/afm_a_gwy.py").read())
```

### 2. Separación de Canales
Ejecutar en la consola pygwy:
```python
exec(open("C:/PATH/TO/AFM_ToolKit/separar_canales.py").read())
```

### 3. Conversión a PNG
Ejecutar en la consola pygwy:
```python
exec(open("C:/PATH/TO/AFM_ToolKit/gwy_a_png.py").read())
```

## Conversión Alternativa a NumPy Array

Si prefieres convertir los archivos a formato NumPy array en lugar de PNG, sigue estos pasos:

1. Convierte los archivos `.gwy` a binarios usando el script `gwy_a_bin.py` en la consola de Gwyddion:
   ```python
   exec(open("C:/PATH/TO/AFM_ToolKit/gwy_a_bin.py").read())
   ```

2. Ejecuta el script `bin_a_npy.py` directamente en la terminal de Python (no requiere Gwyddion).

## Configuración de Rutas

Es importante configurar correctamente las rutas en cada script:

1. En `afm_a_gwy.py`: Configurar la ruta de los archivos con extensión `.000`
2. En `separar_canales.py`: Configurar la ruta de los archivos `.gwy` para separar en canales:
   - Superficie
   - Amplitud
   - Fase
3. En `gwy_a_png.py` o `gwy_a_bin.py`: Configurar la ruta donde se guardarán los archivos de salida

> **Importante**: Verifica que todas las rutas estén correctamente establecidas antes de ejecutar cada script.