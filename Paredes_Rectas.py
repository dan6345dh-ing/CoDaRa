import oficina as of
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
#Punto_Linea=np.array([7.472,6.46])
#Punto2=np.array([-0.029,3.787])

Punto1=np.array([-0.054,6.467])
Punto2=np.array([7.472,6.46])

Dist=np.array([1.39,0.81,1.27,0.82,0.87,0.58])
Puntos_Lineas=of.Puntos_Lineales(Punto1,Punto2,Dist,2.5)
print(Puntos_Lineas)
Punto1=np.array([-0.054,6.467])
Punto2=np.array([0.006,-0.003])

Dist=np.array([1.95,1.66])
Puntos_Lineas1=of.Puntos_Lineales(Punto1,Punto2,Dist,2.5)

Punto1=np.array([0.006,-0.003])
Punto2=np.array([4.960,-0.003])

Dist=np.array([0.62,1.49,0.73,1.48])
Puntos_Lineas2=of.Puntos_Lineales(Punto1,Punto2,Dist,2.5)

Punto1=np.array([4.81,-4.644])
Punto2=np.array([4.848,-0.003])

Dist=np.array([0.3,1.9,0.22,0.37,0.63,0.83])
Puntos_Lineas3=of.Puntos_Lineales(Punto1,Punto2,Dist,2.5)

Pp=np.vstack((Puntos_Lineas,Puntos_Lineas1))
Pp=np.vstack((Pp,Puntos_Lineas2))
Pp=Puntos_Lineas3
print(Pp)

Arreglo=of.relleno_para_sap(142943,Pp)

alExcel=pd.DataFrame(Arreglo,columns=["Joint","CoordSys","CoordType","XorR","Y","T","Z","SpecialJt"])
alExcel.to_excel("Archivo_puntos.xlsx",index=False)

sys.exit()

# ARCOS 

R=2.38

Pi=np.array([11.742,0.564])
Pf=np.array([14.112,0.567])

X,Y,Z,JOINT,CORDSYS,CORDTYPE,SPE,TX=of.arco(R,Pi,Pf,20,0)
#print(np.array([JOINT,CORDSYS,CORDTYPE,X,Y,[],Z,SPE]))

Puntos_Arcos=np.transpose(np.array([X,Y,Z+2.5]))
print(Puntos_Arcos)


Pp=np.vstack((Puntos_Lineas,Puntos_Arcos))
print(Pp)

Arreglo=of.relleno_para_sap(30,Pp)

alExcel=pd.DataFrame(Arreglo,columns=["Joint","CoordSys","CoordType","XorR","Y","T","Z","SpecialJt"])
alExcel.to_excel("Archivo_puntos.xlsx",index=False)