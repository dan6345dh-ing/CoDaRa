import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Ejemplo: tus resultados de ensayos
valores = [53.59,28.90,30.79,31.01,34.64,67.26]
valores = [1021.44,879.39,1252.25,1144.65,879.39,1021.44,1252.25,989.39]
valores = [3.4,3.5,4.3,2.6,4.2]

media = np.mean(valores)
desv = np.std(valores)
x = np.linspace(media - 4*desv, media + 4*desv, 300)
y = norm.pdf(x, media, desv)

plt.plot(x, y, 'r-', linewidth=2, label='Campana de Gauss')
plt.fill_between(x, y, 0, where=(x >= media-desv) & (x <= media+desv), color='orange', alpha=0.3, label='68% confianza')
plt.fill_between(x, y, 0, where=(x >= media-2*desv) & (x <= media+2*desv), color='yellow', alpha=0.2, label='95% confianza')
print(f"Media = {media:.2f}")
print(f"Desviación estándar = {desv:.2f}")

plt.title(f"Distribución normal (μ={media:.2f}, σ={desv:.2f})")
plt.xlabel('Valor')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.grid(alpha=0.3)
plt.show()