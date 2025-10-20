import numpy as np
import pandas as pd
import oficina as of
import sys
#Para hacerlo mas rapido se exporta desde la tabla
Zin=9
PPP=of.Leer_Frames("Book1.xlsx")
AAA=of.Leer_Area("Book1.xlsx")

AAA.set_index("ID",inplace=True)



PLS=[]
for i in AAA.index:
    P1=AAA.loc[i,["P1","P1x","P1y","P1z"]].values
    P2=AAA.loc[i,["P2","P2x","P2y","P2z"]].values
    P3=AAA.loc[i,["P3","P3x","P3y","P3z"]].values
    P4=AAA.loc[i,["P4","P4x","P4y","P4z"]].values
    
    PLS.append(P1),PLS.append(P2),PLS.append(P3),PLS.append(P4)



PLS2=pd.DataFrame(PLS,columns=["ID","X","Y","Z"])

PLS2["Zconf"]=PLS2["Z"].apply(lambda x: "OK" if x==Zin else "NO")

PuntosOk=PLS2[PLS2["Zconf"]=="OK"]

PuntosOk.drop(columns="ID",axis=1, inplace=True)
PuntosOk.drop(columns="Zconf",axis=1, inplace=True)
PuntosOk.insert(loc=2, column='Comentario', value='')
print(PuntosOk)
PuntosOk.to_csv("Puntos_En_Plano.csv",sep="\t",index=False)
print("Ok en replicate - replicar una linea " + str(len(PuntosOk)/2-1) + "veces")

print(AAA.index)


SECCIONESAREA=pd.read_excel("Book1.xlsx",sheet_name="Area Section Assignments",usecols=[0,1],skiprows=[0,2])

print(SECCIONESAREA)

Secciones_Shell=np.unique(SECCIONESAREA["Section"])

Secciones_Frames=np.array(['Viga 10x30','Viga 20x30','Viga 25x30','Viga 30x30','Viga 40x30','Viga 45x30','Viga 55x30'])

reemplazos = dict(zip(Secciones_Shell, Secciones_Frames))

print(reemplazos)

SeccionesFRAM=SECCIONESAREA.applymap(lambda x: reemplazos.get(x,x))
SeccionesFRAM=SeccionesFRAM.drop(columns=["Area"])
SeccionesFRAM.to_csv("Secciones de Remplazo.csv",index=False)
