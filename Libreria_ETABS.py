import os
import sys
import comtypes.client
import numpy as np

# Initialize global variables
def VariablesIniciales():
    myHelper = None
    myEtabsObject = None
    myEtabsModel = None
    ret = 0
    program_id="CSI.ETABS.API.ETABSObject"
    program_path=r"C:\Program Files\Computers and Structures\ETABS 22\ETABS.exe" 
    return myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path

def initialize_helper(myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path):
    #Initialize the API helper object.        

    try:            
        #create API helper object        
        myHelper = comtypes.client.CreateObject('ETABSv1.Helper')
        myHelper = myHelper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    except Exception as e:
        print(f"Error: Cannot create an instance of the Helper object: {e}")

    return myHelper


def attach(myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path):
    #Attach to an active instance of the program.

    if not myHelper:
        raise RuntimeError("Helper is not initialized. Cannot attach to an instance.")

    try:
        # Get the active application object
        myEtabsObject = myHelper.GetObject(program_id)
        # Get a reference to cSapModel
        myEtabsModel = myEtabsObject.SapModel
        return myEtabsModel
    except Exception as e:
        raise RuntimeError(f"Error: Failed to attach to an active instance: {e}")

    

#-----------------------------------------------------#
#-----------------------------------------------------#
#-----------------------------------------------------#
#-----------------------------------------------------#

def obtenerseleccion(myEtabsModel, myEtabsObject, ret):
    
    Tipo=["Nada","Punto","Frame","Cable","Tendon","Area","Solido","Link"]
    ret = myEtabsModel.SelectObj.GetSelected()
    Cantidad,Elementos,Nombre,Zero = ret
    print("Seleccionaste "+str(Cantidad) + " entidades")
    Punto=[]
    Frame=[]
    Area=[]
    for i,j in zip(Elementos,Nombre):
        #print(Tipo[i]+" "+j)
        #Separador
        if Tipo[i]=="Punto":
            Punto.append(j)
        elif Tipo[i]=="Frame":
            Frame.append(j)
        elif Tipo[i]=="Area":
            Area.append(j)

    print(str(len(Punto))+" Puntos")
    print(str(len(Frame))+" Frames")
    print(str(len(Area))+" Areas")
    return Punto,Frame,Area

def obtenerCoor(myEtabsModel, myEtabsObject, ret, PuntoTF=False, FrameTF=False, AreaTF=False, EliminarRepetidos=False,AgregarID="False"):
    Punto,Frame,Area=obtenerseleccion(myEtabsModel, myEtabsObject, ret)

    # Casos Puntos, Frames, Area
    Puntos=[]
    PuntosFrame=[]
    PuntosArea=[]

    if PuntoTF!=False:
        Puntos=Punto
    if FrameTF!=False:
        
        for i in Frame:
            [P1,P2,ret] = myEtabsObject.SapModel.FrameObj.GetPoints(i,'','')
            PuntosFrame.append((P1,P2))

        PuntosFrame=[x for t in PuntosFrame for x in t]
    if AreaTF!=False:
        
        for i in Area:
            [Cantidad,PuntosTupla,ret] = myEtabsObject.SapModel.AreaObj.GetPoints(i,0,())
            PuntosArea.append(PuntosTupla)
        
        PuntosArea=[x for t in PuntosArea for x in t]

    PointName=Puntos+PuntosFrame+PuntosArea

    if EliminarRepetidos==True:
        PointName=np.unique(PointName)

    print(PointName)

    PointCoord=[]
    for i in PointName:
        [x,y,z,ret]=myEtabsModel.PointObj.GetCoordCartesian(i,0,0,0)
        
        if AgregarID==True:
            PointCoord.append([x,y,z,int(i)])
        else:
            PointCoord.append([x,y,z])
    
    PointCoord=np.array(PointCoord)

    return PointCoord