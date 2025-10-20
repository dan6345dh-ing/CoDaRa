import os
import sys
import comtypes.client
import Libreria_SAP2000 as SP20
import numpy as np
import pandas as pd


myHelper,mySapModel,mySapObject,ret,program_id,program_path=SP20.VariablesIniciales()
myHelper=SP20.initialize_helper(myHelper,mySapModel,mySapObject,ret,program_id,program_path)
mySapModel, mySapObject=SP20.attach(myHelper,mySapModel,mySapObject,ret,program_id,program_path)
#-----------------------------------#
Caso=2
#Punto,Frame,Area=SP20.obtenerseleccion(mySapModel, mySapObject, ret)
if Caso==1: #DIBUJO LINEAS EN LA ZONA SUPERIOR DE LAS AREAS
    PC=SP20.obtenerCoor(mySapModel, mySapObject, ret, PuntoTF=False, FrameTF=False, AreaTF=True)

    AreasCoord=np.array_split(PC,len(PC)/4)
    n=0
    for i in AreasCoord:
        n=n+1
        Areaspd=pd.DataFrame(i, columns=["X","Y","Z"])
        
        Areaspd.sort_values(by="Z",inplace=True)
        Areaspd.reset_index(inplace=True,drop=True)
        print(Areaspd)
        #print(Areaspd.loc[[1,2]])
        CoordLineaSuperior=Areaspd.loc[[2,3]].to_numpy()
        PointCoordINI=CoordLineaSuperior[0]
        PointCoordFIN=CoordLineaSuperior[1]

        SP20.DibujarLinea(PointCoordINI,PointCoordFIN,"SuperiorP1"+str(),mySapModel)
        
    ret=mySapObject.SapModel.View.RefreshView()

elif Caso==2: # SELECCIONO Y REPLICO EN TODOS LOS Z UNICOS

    input("--PUNTOS CON Z UNICOS--")
    PC=SP20.obtenerCoor(mySapModel, mySapObject, ret, PuntoTF=True, FrameTF=False, AreaTF=False)
    Z=np.unique(PC[:,2])
    
    print(Z)

    input("SELECCIONA A REPLICAR")
    ZBase=-2000
    
    print(Z)
    for i in Z:

        ret = mySapModel.EditGeneral.ReplicateLinear(0,0, i-ZBase, 1, 0, "", ())
        
        ret = mySapModel.SelectObj.PreviousSelection()

    ret=mySapObject.SapModel.View.RefreshView()

elif Caso==3: #Redondear Z
    input("--PUNTOS CON Z UNICOS--")
    Puntos_Name,_,_=SP20.obtenerseleccion(mySapModel, mySapObject, ret)
    for i in Puntos_Name:
        [x,y,z,ret]=mySapObject.SapModel.PointObj.GetCoordCartesian(i,0,0,0)
        ret = mySapModel.EditPoint.ChangeCoordinates_1(i, x, y, np.round(z,-2),True)

    ret=mySapObject.SapModel.View.RefreshView()

    


     
        

ret=mySapObject.SapModel.View.RefreshView()