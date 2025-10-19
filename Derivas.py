import oficina as of
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

Coef=0.75
R=1.5

print("ADMINISTRACION - BLQOUE 4")

Deplazamiento_Nodo_X=np.array([0.0,0.00112,0.001685,0.001822])
Deplazamiento_Nodo_Y=np.array([0.0,0.002719,0.004034,0.004298])

Pisos=np.array([0.0,3.0,5.7,7.25])
DerivaX=of.Deriva(Pisos,Deplazamiento_Nodo_X,1)
DerivaY=of.Deriva(Pisos,Deplazamiento_Nodo_Y,1)
print("SENTIDO X", DerivaX*Coef*R)
print("SENTIDO Y", DerivaY*Coef*R)

print("Teatros EA -BLQOUE 2")

Deplazamiento_Nodo_X=np.array([0.0,0.025]) # pico de las paredes
Deplazamiento_Nodo_Y=np.array([0.0,0.046315]) # alto del arco

Pisos=np.array([0.0,4.7])
DerivaX=of.Deriva(Pisos,Deplazamiento_Nodo_X,1)
Pisos=np.array([0.0,3.5])
DerivaY=of.Deriva(Pisos,Deplazamiento_Nodo_Y,1)
print("SENTIDO X", DerivaX*Coef*R)
print("SENTIDO Y", DerivaY*Coef*R)