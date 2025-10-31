import gwy
import os
import struct

# Configurar carpetas
carpeta_origen = r'C:/PATH/TO/CARPETA_CON_AFMS\canales_separados_gwy'
carpeta_bin = os.path.join(carpeta_origen, "canales_separados_bin")

if not os.path.exists(carpeta_bin):
    os.makedirs(carpeta_bin)
    print "Carpeta bin creada: " + carpeta_bin

print "Procesando archivos en: " + carpeta_origen
print "Guardando en: " + carpeta_bin

# Obtener lista de todos los archivos .gwy
archivos_gwy = [f for f in os.listdir(carpeta_origen) if f.endswith('.gwy')]
print "Encontré " + str(len(archivos_gwy)) + " archivos .gwy"

for archivo in archivos_gwy:
    try:
        print "Procesando: " + archivo
        ruta_gwy = os.path.join(carpeta_origen, archivo)
        nombre_base = os.path.splitext(archivo)[0]
        ruta_bin = os.path.join(carpeta_bin, nombre_base + ".bin")
        ruta_info = os.path.join(carpeta_bin, nombre_base + "_info.txt")
        
        # Cargar archivo
        container = gwy.gwy_file_load(ruta_gwy, gwy.RUN_NONINTERACTIVE)
        
        # Buscar DataField
        data_field = None
        for key in container.keys():
            if isinstance(container[key], gwy.DataField):
                data_field = container[key]
                break
        
        if data_field:
            # Extraer dimensiones y metadatos
            xres = data_field.get_xres()
            yres = data_field.get_yres()
            xreal = data_field.get_xreal()
            yreal = data_field.get_yreal()
            data_min = data_field.get_min()
            data_max = data_field.get_max()
            
            # Guardar datos binarios
            with open(ruta_bin, 'wb') as f:
                # Cabecera: dimensiones (2 ints, 8 bytes)
                f.write(struct.pack('ii', xres, yres))
                # Datos: todos los valores float64
                for y in range(yres):
                    for x in range(xres):
                        value = data_field.get_val(x, y)
                        f.write(struct.pack('d', value))  # 'd' = double (float64)
            
            # Guardar información de metadatos
            with open(ruta_info, 'w') as f:
                f.write("Archivo: {}\n".format(archivo))
                f.write("Dimensiones: {} x {}\n".format(xres, yres))
                f.write("Tamaño físico: {:.6e} x {:.6e} metros\n".format(xreal, yreal))
                f.write("Resolución X: {:.6e} metros/pixel\n".format(xreal/xres))
                f.write("Resolución Y: {:.6e} metros/pixel\n".format(yreal/yres))
                f.write("Valor mínimo: {:.6e}\n".format(data_min))
                f.write("Valor máximo: {:.6e}\n".format(data_max))
                f.write("Tipo de datos: float64\n")
                f.write("Formato: binario puro\n")
                f.write("Cabecera: 8 bytes (2 ints: xres, yres)\n")
                f.write("Datos: {} valores float64\n".format(xres * yres))
                f.write("Total bytes: {} bytes\n".format(8 + 8 * xres * yres))
            
            print "✓ Convertido: " + archivo + " (" + str(xres) + "x" + str(yres) + ")"
            
        else:
            print "✗ No se encontró DataField en: " + archivo
            
    except Exception as e:
        print "✗ Error procesando " + archivo + ": " + str(e)

print "=" * 60
print "¡Conversión a binarios completada!"
print "Archivos guardados en: " + carpeta_bin
print "\nAhora ejecuta el Script 2 en Python 3 para convertir a .npy"