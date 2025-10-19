import oficina as of
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
#Punto_Linea=np.array([7.472,6.46])
#Punto2=np.array([-0.029,3.787])



R=0.4

Pi=np.array([9.212,-4.638])
Pf=np.array([9.972,-4.637])

Dist=np.array([1.32,0.42,0.76])
Puntos_Lineas2=of.Puntos_Lineales(Pi,Pf,Dist,2.5)


X,Y,Z,JOINT,CORDSYS,CORDTYPE,SPE,TX=of.arco(R,Pi,Pf,20,1,0)
#print(np.array([JOINT,CORDSYS,CORDTYPE,X,Y,[],Z,SPE]))

Puntos_Arcos=np.transpose(np.array([X,Y,Z+1.4]))
print(Puntos_Arcos)


#Arreglo=of.relleno_para_sap(30,Puntos_Lineas2)
Arreglo=of.relleno_para_sap(30,Puntos_Arcos)

alExcel=pd.DataFrame(Arreglo,columns=["Joint","CoordSys","CoordType","XorR","Y","T","Z","SpecialJt"])
alExcel.to_excel("Archivo_puntos_ARCO.xlsx",index=False)