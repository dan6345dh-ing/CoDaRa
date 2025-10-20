import os
import sys
import comtypes.client
import numpy as np

# Initialize global variables
def VariablesIniciales():
    myHelper = None
    mySapObject = None
    mySapModel = None
    ret = 0
    program_id="CSI.SAP2000.API.SapObject"
    program_path=r"C:\Program Files\Computers and Structures\SAP2000 26\SAP2000.exe" 
    return myHelper,mySapModel,mySapObject,ret,program_id,program_path

def initialize_helper(myHelper,mySapModel,mySapObject,ret,program_id,program_path):
    #Initialize the API helper object.        

    try:            
        #create API helper object        
        myHelper = comtypes.client.CreateObject('SAP2000v1.Helper')
        myHelper = myHelper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
    except Exception as e:
        print(f"Error: Cannot create an instance of the Helper object: {e}")
    
    return myHelper


def attach(myHelper,mySapModel,mySapObject,ret,program_id,program_path):
    #Attach to an active instance of the program.

    if not myHelper:
        raise RuntimeError("Helper is not initialized. Cannot attach to an instance.")

    try:
        # Get the active application object
        mySapObject = myHelper.GetObject(program_id)
        # Get a reference to cSapModel
        mySapModel = mySapObject.SapModel
        return mySapModel, mySapObject
    except Exception as e:
        raise RuntimeError(f"Error: Failed to attach to an active instance: {e}")
    
    

#-----------------------------------------------------#
#-----------------------------------------------------#
#-----------------------------------------------------#
#-----------------------------------------------------#

def obtenerseleccion(mySapModel, mySapObject, ret):
    
    Tipo=["Nada","Punto","Frame","Cable","Tendon","Area","Solido","Link"]
    ret = mySapObject.SapModel.SelectObj.GetSelected()
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

def obtenerCoor(mySapModel, mySapObject, ret, PuntoTF=False, FrameTF=False, AreaTF=False, EliminarRepetidos=False):
    Punto,Frame,Area=obtenerseleccion(mySapModel, mySapObject, ret)

    # Casos Puntos, Frames, Area
    Puntos=[]
    PuntosFrame=[]
    PuntosArea=[]

    if PuntoTF!=False:
        Puntos=Punto
    if FrameTF!=False:
        
        for i in Frame:
            [P1,P2,ret] = mySapObject.SapModel.FrameObj.GetPoints(i,'','')
            PuntosFrame.append((P1,P2))

        PuntosFrame=[x for t in PuntosFrame for x in t]
    if AreaTF!=False:
        
        for i in Area:
            [Cantidad,PuntosTupla,ret] = mySapObject.SapModel.AreaObj.GetPoints(i,0,())
            PuntosArea.append(PuntosTupla)
        
        PuntosArea=[x for t in PuntosArea for x in t]

    PointName=Puntos+PuntosFrame+PuntosArea

    if EliminarRepetidos==True:
        PointName=np.unique(PointName)

    print(PointName)

    PointCoord=[]
    for i in PointName:
        [x,y,z,ret]=mySapObject.SapModel.PointObj.GetCoordCartesian(i,0,0,0)
        PointCoord.append([x,y,z])
    
    PointCoord=np.array(PointCoord)

    return PointCoord

def DibujarLinea(PointCoordINI,PointCoordFIN,Nombre,mySapModel):
     
        xi,yi,zi=PointCoordINI
        xf,yf,zf=PointCoordFIN
        ret = mySapModel.FrameObj.AddByCoord(xi, yi, zi, xf, yf, zf, Nombre)