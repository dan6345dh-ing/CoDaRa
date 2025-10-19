import ezdxf
from ezdxf import bbox
from ezdxf.math import Vec3
import numpy as np

def polilinea_adaptativa_centroide(archivo_entrada, archivo_salida):
    """Crea una polilínea que se adapta a la forma del solid"""
    
    doc = ezdxf.readfile(archivo_entrada)
    msp = doc.modelspace()
    solids = msp.query('3DSOLID')
    
    for i, solid in enumerate(solids):
        try:
            solid_bbox = bbox.extents([solid])
            min_point = solid_bbox.extmin
            max_point = solid_bbox.extmax
            centroide = (min_point + max_point) / 2
            
            # Calcular relación de aspecto
            ancho = max_point.x - min_point.x
            alto = max_point.y - min_point.y
            relacion_aspecto = ancho / alto if alto != 0 else 1
            
            # Determinar forma basada en relación de aspecto
            if relacion_aspecto > 1.5:
                # Forma horizontal - rectángulo alargado
                puntos = crear_polilinea_rectangular(min_point, max_point, centroide)
            elif relacion_aspecto < 0.67:
                # Forma vertical - rectángulo alargado
                puntos = crear_polilinea_rectangular(min_point, max_point, centroide)
            else:
                # Forma cuadrada - usar octágono
                puntos = crear_polilinea_octagonal(min_point, max_point, centroide)
            
            polilinea = msp.add_lwpolyline(puntos, format='xy', close=True)
            polilinea.dxf.color = i % 7 + 1  # Ciclo de colores
            
            # Agregar marcador de centroide
            msp.add_circle(centroide, radius=min(ancho, alto)*0.05).dxf.color = polilinea.dxf.color
            
        except Exception as e:
            print(f"Error procesando solid {i}: {e}")
    
    doc.saveas(archivo_salida)
    print(f"Archivo con polilíneas adaptativas guardado: {archivo_salida}")

def crear_polilinea_rectangular(min_point, max_point, centroide):
    """Crea polilínea rectangular redondeada"""
    ancho = max_point.x - min_point.x
    alto = max_point.y - min_point.y
    radio_esquina = min(ancho, alto) * 0.1
    
    puntos = []
    # Puntos en sentido antihorario
    puntos.extend(crear_arco_esquina(
        centroide.x - ancho/2 + radio_esquina, 
        centroide.y - alto/2 + radio_esquina, 
        radio_esquina, 180, 270, 4
    ))
    puntos.extend(crear_arco_esquina(
        centroide.x + ancho/2 - radio_esquina, 
        centroide.y - alto/2 + radio_esquina, 
        radio_esquina, 270, 360, 4
    ))
    puntos.extend(crear_arco_esquina(
        centroide.x + ancho/2 - radio_esquina, 
        centroide.y + alto/2 - radio_esquina, 
        radio_esquina, 0, 90, 4
    ))
    puntos.extend(crear_arco_esquina(
        centroide.x - ancho/2 + radio_esquina, 
        centroide.y + alto/2 - radio_esquina, 
        radio_esquina, 90, 180, 4
    ))
    
    return puntos

def crear_polilinea_octagonal(min_point, max_point, centroide):
    """Crea polilínea octagonal"""
    ancho = max_point.x - min_point.x
    alto = max_point.y - min_point.y
    
    puntos = []
    for i in range(8):
        angulo = 2 * np.pi * i / 8
        # Octágono irregular basado en dimensiones reales
        x = centroide.x + (ancho/2 * 0.8) * np.cos(angulo)
        y = centroide.y + (alto/2 * 0.8) * np.sin(angulo)
        puntos.append((x, y))
    
    return puntos

def crear_arco_esquina(centro_x, centro_y, radio, ang_inicio, ang_fin, segmentos):
    """Crea puntos para un arco de esquina"""
    puntos = []
    for i in range(segmentos + 1):
        angulo = np.radians(ang_inicio + (ang_fin - ang_inicio) * i / segmentos)
        x = centro_x + radio * np.cos(angulo)
        y = centro_y + radio * np.sin(angulo)
        puntos.append((x, y))
    return puntos

# Uso
polilinea_adaptativa_centroide('Archivos_Ingreso/PolyDxf.dxf', 'Archivos_Salida/salida_adaptativa.dxf')