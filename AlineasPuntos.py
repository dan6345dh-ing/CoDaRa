import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt

# --- Datos de ejemplo ---
# Puntos dispersos
puntos = np.random.rand(30, 2)
print(puntos)
# Línea (por ejemplo, una polilínea)
t = np.linspace(0, 1, 100)
linea = np.column_stack((t, 0.5 + 0.2*np.sin(4*np.pi*t)))
print(linea)
# --- Construir árbol KD con puntos de la línea ---
tree = cKDTree(linea)

# --- Encontrar el punto más cercano en la línea para cada punto ---
dist, idx = tree.query(puntos)
puntos_ajustados = linea[idx]

# --- Visualizar ---
plt.figure(figsize=(6, 4))
plt.plot(linea[:, 0], linea[:, 1], 'k-', label='Línea base')
plt.scatter(puntos[:, 0], puntos[:, 1], c='r', label='Puntos originales')
plt.scatter(puntos_ajustados[:, 0], puntos_ajustados[:, 1], c='b', label='Puntos ajustados')
for i in range(len(puntos)):
    plt.plot([puntos[i, 0], puntos_ajustados[i, 0]],
             [puntos[i, 1], puntos_ajustados[i, 1]], 'gray', lw=0.5)
plt.legend()
plt.axis('equal')
plt.show()

def Ajustealineaxynz(Linea,Puntos):
    import numpy as np
    from scipy.spatial import cKDTree
    tree = cKDTree(linea)
    dist, idx = tree.query(puntos)
    puntos_ajustados = linea[idx]
    #

    plt.figure(figsize=(6, 4))
    plt.plot(linea[:, 0], linea[:, 1], 'k-', label='Línea base')
    plt.scatter(puntos[:, 0], puntos[:, 1], c='r', label='Puntos originales')
    plt.scatter(puntos_ajustados[:, 0], puntos_ajustados[:, 1], c='b', label='Puntos ajustados')
    for i in range(len(puntos)):
        plt.plot([puntos[i, 0], puntos_ajustados[i, 0]],
                [puntos[i, 1], puntos_ajustados[i, 1]], 'gray', lw=0.5)
    plt.legend()
    plt.axis('equal')
    plt.show()  