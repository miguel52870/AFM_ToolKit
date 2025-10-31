# script: separar_canales.py
import os, sys, gwy

# --- CONFIGURACIÓN ---
# 1. ¡IMPORTANTE! La carpeta de entrada ahora debe ser la que contiene los archivos .gwy.
input_dir = r'C:/PATH/TO/CARPETA_CON_AFMS\convertidos_gwy'

# 2. El nombre base que quieres para tus archivos de salida.
output_base_name = 'bifeo_training_'
# ---------------------

print("Iniciando separacion de canales en: {}".format(input_dir))

# Creamos una carpeta para los resultados si no existe.
# Se creará al mismo nivel que la carpeta de entrada.
parent_dir = os.path.dirname(input_dir)
output_dir = os.path.join(parent_dir, 'canales_separados_gwy')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print("Carpeta de salida creada: {}".format(output_dir))

# Iteramos sobre todos los archivos en la carpeta de entrada
for filename in sorted(os.listdir(input_dir)):
    # Ahora buscamos archivos que terminen en .gwy
    if filename.endswith('.gwy'):
        input_path = os.path.join(input_dir, filename)
        print("\nProcesando archivo: {}".format(filename))

        container = gwy.gwy_file_load(input_path, gwy.RUN_NONINTERACTIVE)
        if not container:
            print("  -> Error al cargar el archivo. Saltando.")
            continue

        # Buscamos los canales de datos (misma lógica que antes)
        all_keys = container.keys_by_name()
        data_field_ids = []
        for key in all_keys:
            if key.endswith('/data'):
                data_field_ids.append(key)
        
        if not data_field_ids:
            print("  -> No se encontraron canales de datos en este archivo.")
            continue
            
        print("  -> Se encontraron {} canales.".format(len(data_field_ids)))
        
        # Iteramos sobre cada canal para guardarlo en un archivo nuevo
        for i, data_id in enumerate(data_field_ids):
            # Obtenemos el objeto del canal de datos
            data_field = container[data_id]
            
            # Construimos el nombre del nuevo archivo (ej. bifeo01_Canal_1.gwy)
            base_name_without_ext = os.path.splitext(filename)[0]
            channel_name = "Canal_{}".format(i + 1)
            output_filename = "{}_{}.gwy".format(base_name_without_ext, channel_name)
            output_path = os.path.join(output_dir, output_filename)
            
            # --- LÓGICA DE SEPARACIÓN ---
            # 1. Creamos un contenedor nuevo y vacío para el canal individual
            new_container = gwy.Container()
            # 2. Agregamos el canal actual a este nuevo contenedor
            new_container['/0/data'] = data_field
            # 3. Le ponemos un título
            new_container['/0/data/title'] = channel_name
            
            # 4. Guardamos el nuevo contenedor como un archivo .gwy independiente
            gwy.gwy_file_save(new_container, output_path, gwy.RUN_NONINTERACTIVE)
            print("    - Guardado: {}".format(output_filename))

print("\n¡Separacion de canales completada!")
print("Los archivos nuevos estan en la carpeta: {}".format(output_dir))