# script: convertir_y_renombrar.py (Version Compatible)
import os, sys, gwy

# --- CONFIGURACIÓN ---
# 1. Coloca la ruta a la carpeta con tus archivos originales de extension .000.
input_dir = r'C:/PATH/TO/CARPETA_CON_AFMS'

# 2. El nombre base que quieres para tus archivos de salida.
output_base_name = 'bifeo_training_'
# ---------------------

print("Iniciando proceso en la carpeta: {}".format(input_dir))

# Creamos una carpeta para los resultados si no existe
output_dir = os.path.join(input_dir, 'convertidos_gwy')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print("Carpeta de salida creada: {}".format(output_dir))

# Iteramos sobre todos los archivos en la carpeta de entrada
for filename in sorted(os.listdir(input_dir)):
    base, ext = os.path.splitext(filename)
    
    if ext.startswith('.') and ext[1:].isdigit():
        
        # --- LÓGICA DE RENOMBRADO ---
        numero_extension = int(ext[1:])
        nuevo_numero = numero_extension + 1
        
        # Formateamos el nuevo nombre del archivo (formato compatible)
        output_filename = "{}{:02d}.gwy".format(output_base_name, nuevo_numero)
        
        # --- PROCESO DE CONVERSIÓN ---
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, output_filename)
        
        print("Procesando: {}  ->  {}".format(filename, output_filename))

        # Cargamos el archivo original
        container = gwy.gwy_file_load(input_path, gwy.RUN_NONINTERACTIVE)
        if not container:
            print("  -> Error al cargar el archivo {}. Saltando.".format(filename))
            continue

        # Guardamos el archivo con su nuevo nombre y formato
        gwy.gwy_file_save(container, output_path, gwy.RUN_NONINTERACTIVE)

print("\n¡Proceso de conversion y renombrado completado!")
print("Los archivos nuevos estan en: {}".format(output_dir))