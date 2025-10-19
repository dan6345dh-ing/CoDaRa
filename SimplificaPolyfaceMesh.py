
import ezdxf
import numpy as np
import open3d as o3d

# Leer el archivo DXF
doc = ezdxf.readfile("Amabto.dxf")
msp = doc.modelspace()
i=1
# Buscar el primer POLYFACE MESH
mesh_entity = None
for e in msp:
    if e.dxftype() == "POLYLINE" and e.is_poly_face_mesh :
        mesh_entity = e
        i=i+1
        if i==1:
            break


if not mesh_entity:
    raise Exception("No se encontró un POLYFACE MESH en el archivo.")

# Extraer vértices y caras
vertex_map = []
face_indices = []

for v in mesh_entity.vertices:
    if v.is_face_record:
        # Es una cara: contiene índices de vértices
        indices = [v.dxf.vtx0, v.dxf.vtx1, v.dxf.vtx2, v.dxf.vtx3]
        face = [abs(i) - 1 for i in indices if i is not None and i != 0]
  # eliminar ceros, convertir a 0-based
        if len(face) >= 3:
            face_indices.append(face[:3])  # solo triángulos
    else:
        # Es un vértice geométrico
        loc = v.dxf.location
        vertex_map.append([loc.x, loc.y, loc.z])

vertices = np.array(vertex_map)
triangles = np.array(face_indices)

# Crear y mostrar la malla con Open3D
mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(vertices)
mesh.triangles = o3d.utility.Vector3iVector(triangles)
mesh.compute_vertex_normals()

target_faces = 300  # o ajusta según tu necesidad
mesh_simplified = mesh.simplify_quadric_decimation(target_number_of_triangles=target_faces)

# Mostrar ambas (opcional)
print(f"Malla original: {len(mesh.triangles)} caras")
print(f"Malla simplificada: {len(mesh_simplified.triangles)} caras")

# Visualizar
o3d.visualization.draw_geometries([mesh_simplified],mesh_show_wireframe=True)

print(mesh_simplified)

doc = ezdxf.new()
msp = doc.modelspace()

vertices = np.asarray(mesh_simplified.vertices)
triangles = np.asarray(mesh_simplified.triangles)

for tri in triangles:
    p1, p2, p3 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]
    # 3DFACE acepta 3 o 4 puntos, si solo 3 repetimos el último punto
    msp.add_3dface([p1, p2, p3, p3])


doc.saveas("malla_simplificada.dxf")