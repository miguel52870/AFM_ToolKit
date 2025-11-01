import gwy
import os
import sys
import struct
import zlib

# Configurar carpetas
carpeta_origen = r'C:\Users\migue\Desktop\training_afm\canales_separados_gwy'
carpeta_destino = os.path.join(carpeta_origen, "canales_separados_png")

if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Función para crear PNG manualmente
def save_as_png(data, width, height, filename):
    """Guarda una matriz de datos como PNG, añadiendo el byte de filtro requerido."""
    
    # 1. Crear datos RGB (escala de grises) CON BYTES DE FILTRO
    image_data_with_filters = bytearray()
    for y in range(height):
        # AÑADIR BYTE DE FILTRO (0 = None) AL INICIO DE CADA FILA
        image_data_with_filters.append(0) 
        
        for x in range(width):
            value = data[y][x]
            # RGB igual para escala de grises
            image_data_with_filters.extend([value, value, value]) 
    
    # Comprimir los datos con los bytes de filtro
    compressed_data = zlib.compress(bytes(image_data_with_filters), 9)
    
    # Escribir archivo PNG (el resto del código IHDR/IDAT/IEND está bien)
    with open(filename, 'wb') as f:
        # Signature
        f.write(b'\x89PNG\r\n\x1a\n')
        
        # IHDR chunk (igual)
        f.write(struct.pack('>I', 13))
        f.write(b'IHDR')
        f.write(struct.pack('>I', width))
        f.write(struct.pack('>I', height))
        f.write(b'\x08\x02\x00\x00\x00')  # 8-bit RGB
        f.write(struct.pack('>I', zlib.crc32(b'IHDR' + struct.pack('>II', width, height) + b'\x08\x02\x00\x00\x00') & 0xffffffff))
        
        # IDAT chunk
        f.write(struct.pack('>I', len(compressed_data)))
        f.write(b'IDAT')
        f.write(compressed_data)
        f.write(struct.pack('>I', zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff))
        
        # IEND chunk (igual)
        f.write(b'\x00\x00\x00\x00IEND\xaeB`\x82')

archivos_gwy = [f for f in os.listdir(carpeta_origen) if f.endswith('.gwy')]
print "Encontré " + str(len(archivos_gwy)) + " archivos .gwy"

for archivo in archivos_gwy:
    try:
        print "Procesando: " + archivo
        ruta_gwy = os.path.join(carpeta_origen, archivo)
        nombre_base = os.path.splitext(archivo)[0]
        ruta_png = os.path.join(carpeta_destino, nombre_base + ".png")
        
        # Cargar archivo
        container = gwy.gwy_file_load(ruta_gwy, gwy.RUN_NONINTERACTIVE)
        
        # Buscar DataField
        data_field = None
        for key in container.keys():
            if isinstance(container[key], gwy.DataField):
                data_field = container[key]
                break
        
        if data_field:
            # Extraer dimensiones
            xres = data_field.get_xres()
            yres = data_field.get_yres()
            
            # Extraer datos y normalizar
            data_min = data_field.get_min()
            data_max = data_field.get_max()
            
            # Crear matriz de datos normalizados (0-255)
            image_data = []
            for y in range(yres):
                row = []
                for x in range(xres):
                    value = data_field.get_val(x, y)
                    # Normalizar a 0-255
                    if data_max > data_min:
                        normalized = int(255 * (value - data_min) / (data_max - data_min))
                    else:
                        normalized = 128  # Valor medio si no hay variación
                    row.append(max(0, min(255, normalized)))
                image_data.append(row)
            
            # Guardar como PNG
            save_as_png(image_data, xres, yres, ruta_png)
            print "✓ Convertido: " + archivo + " (" + str(xres) + "x" + str(yres) + ")"
            
        else:
            print "✗ No se encontró DataField en: " + archivo
            
    except Exception as e:
        print "✗ Error procesando " + archivo + ": " + str(e)

print "¡Conversión completada!"