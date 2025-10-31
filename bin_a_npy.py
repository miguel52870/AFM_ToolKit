import numpy as np
import struct
import os
import glob

# Configuración de rutas
carpeta_bin = r"C:/PATH/TO/CARPETA_CON_AFMS/canales_separados_gwy/canales_separados_bin"
carpeta_npy = r"C:/PATH/TO/CARPETA_CON_AFMS/canales_separados_gwy/canales_separados_npy"

def bin_a_npy(carpeta_bin, carpeta_npy):
    """
    Convierte todos los archivos .bin en una carpeta a .npy
    """
    if not os.path.exists(carpeta_npy):
        os.makedirs(carpeta_npy)
        print(f"✓ Carpeta creada: {carpeta_npy}")
    
    # Encontrar todos los archivos .bin
    archivos_bin = glob.glob(os.path.join(carpeta_bin, "*.bin"))
    
    if not archivos_bin:
        print("✗ No se encontraron archivos .bin en la carpeta")
        return
    
    print(f"Encontré {len(archivos_bin)} archivos .bin")
    print("Convirtiendo a .npy...")
    print("=" * 50)
    
    for archivo_bin in archivos_bin:
        try:
            nombre_base = os.path.splitext(os.path.basename(archivo_bin))[0]
            archivo_npy = os.path.join(carpeta_npy, nombre_base + ".npy")
            
            # Cargar archivo .bin
            with open(archivo_bin, 'rb') as f:
                # Leer dimensiones
                xres, yres = struct.unpack('ii', f.read(8))
                # Leer datos
                data = np.fromfile(f, dtype=np.float64).reshape(yres, xres)
            
            # Guardar como .npy
            np.save(archivo_npy, data)
            
            # Estadísticas
            stats = f"[{np.min(data):.2e} to {np.max(data):.2e}]"
            print(f"✓ {nombre_base:30} {yres:4d}x{xres:<4d} {stats}")
            
        except Exception as e:
            print(f"✗ Error con {os.path.basename(archivo_bin)}: {str(e)}")
    
    print("=" * 50)
    print(f"¡Conversión completada! {len(archivos_bin)} archivos convertidos a .npy")
    print(f"Archivos .npy guardados en: {carpeta_npy}")

def verificar_carga_npy(carpeta_npy):
    """
    Verifica que los archivos .npy se pueden cargar correctamente
    """
    print("\n" + "=" * 50)
    print("VERIFICANDO ARCHIVOS .NPY...")
    
    archivos_npy = glob.glob(os.path.join(carpeta_npy, "*.npy"))
    
    for archivo_npy in archivos_npy[:3]:  # Verificar solo los primeros 3
        try:
            data = np.load(archivo_npy)
            nombre = os.path.basename(archivo_npy)
            print(f"✓ {nombre:30} {data.shape} - Carga exitosa")
        except Exception as e:
            print(f"✗ Error cargando {os.path.basename(archivo_npy)}: {str(e)}")

# Ejecutar conversión
if __name__ == "__main__":
    print("CONVERSOR BIN → NPY")
    print("=" * 50)
    
    # Convertir bin → npy
    bin_a_npy(carpeta_bin, carpeta_npy)
    
    # Verificar resultados
    verificar_carga_npy(carpeta_npy)
    
    print("\n ¡Proceso completado exitosamente!")
    print("\nPara usar los archivos .npy:")
    print("  import numpy as np")
    print("  data = np.load('archivo.npy')")