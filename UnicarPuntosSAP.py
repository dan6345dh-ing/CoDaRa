from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

R = 110  # radio
db = DBSCAN(eps=R, min_samples=1).fit(puntos)
labels = db.labels_

n_clusters = len(set(labels))
print(f"Se detectaron {n_clusters} grupos")

# Visualizar
colores = plt.cm.tab10(np.linspace(0, 1, n_clusters))
for i, c in enumerate(np.unique(labels)):
    plt.scatter(puntos[labels == c, 0], puntos[labels == c, 1],
                color=colores[i % len(colores)], s=20, label=f'Grupo {i+1}')
plt.legend()
plt.axis('equal')
plt.show()
