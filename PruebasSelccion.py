import os
import sys
import comtypes.client

# Initialize global variables
myHelper = None
mySapObject = None
mySapModel = None
ret = 0
program_id="CSI.SAP2000.API.SapObject"
program_path=r"C:\Program Files\Computers and Structures\SAP2000 26\SAP2000.exe" 

def initialize_helper():
    #Initialize the API helper object.        
    global myHelper
    try:            
        #create API helper object        
        myHelper = comtypes.client.CreateObject('SAP2000v1.Helper')
        myHelper = myHelper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
    except Exception as e:
        print(f"Error: Cannot create an instance of the Helper object: {e}")

def open():
    #Open a new instance using the program ID.
    global myHelper, mySapObject, mySapModel, ret
    if not myHelper:
        raise RuntimeError("Helper is not initialized. Cannot start a new instance.")

    try:
        # Create an instance of the CSi object from the program ID
        mySapObject = myHelper.CreateObjectProgID(program_id)
        # Start the application
        ret = mySapObject.ApplicationStart()
        # Get a reference to cSapModel
        mySapModel = mySapObject.SapModel
        return mySapModel
    except Exception as e:
        raise RuntimeError(f"Error: Failed to start a new instance of the program: {e}")

def open_path():
    #Open a new instance using the specified program path.
    global myHelper, mySapObject, mySapModel, ret
    if not program_path:
        raise ValueError("Program path is not specified.")
    
    if not myHelper:
        raise RuntimeError("Helper is not initialized. Cannot start a new instance.")

    try:
        # Create an instance from the specified path
        mySapObject = myHelper.CreateObject(program_path)
        # Start the application
        ret = mySapObject.ApplicationStart()
        # Get a reference to cSapModel
        mySapModel = mySapObject.SapModel
        return mySapModel
    except Exception as e:
        raise RuntimeError(f"Error: Failed to start the program from the specified path: {e}")

def attach():
    #Attach to an active instance of the program.
    global myHelper, mySapObject, mySapModel
    if not myHelper:
        raise RuntimeError("Helper is not initialized. Cannot attach to an instance.")

    try:
        # Get the active application object
        mySapObject = myHelper.GetObject(program_id)
        # Get a reference to cSapModel
        mySapModel = mySapObject.SapModel
        return mySapModel
    except Exception as e:
        raise RuntimeError(f"Error: Failed to attach to an active instance: {e}")

def close():
    #Close the application and clean up resources.
    global mySapObject, mySapModel, ret
    if not mySapObject:
        raise RuntimeError("No active application instance to close.")

    try:
        # Close the application
        mySapObject.ApplicationExit(False)
        # Clean up variables
        mySapModel = None
        mySapObject = None

        if ret == 0:
            print("API script completed successfully.")
        else:
            print("API script FAILED to complete.")
    except Exception as e:
        raise RuntimeError(f"Error: Failed to close the application: {e}")

def obtenerselecion():
    global mySapModel, ret
    Tipo=["Nada","Punto","Frame","Cable","Tendon","Area","Solido","Link"]
    ret = mySapObject.SapModel.SelectObj.GetSelected()
    Cantidad,Elementos,Nombre,Zero = ret
    print("Hay "+str(Cantidad))
    Punto=[]
    Frame=[]
    Area=[]
    for i,j in zip(Elementos,Nombre):
        print(Tipo[i]+" "+j)
        #Separador
        if Tipo[i]=="Punto":
            Punto.append(j)
        elif Tipo[i]=="Frame":
            Frame.append(j)
        elif Tipo[i]=="Area":
            Area.append(j)

    return Punto,Frame,Area

def ajustarlinea(Punto,Frame,Area,caso):
    global mySapModel, ret
    import numpy as np
    from scipy.spatial import cKDTree
    import matplotlib.pyplot as plt
    
    PuntosArea=[]
    PuntosLinea=[]

    if caso==1 or caso==2:
        for i in Area:
            [Cantidad,PuntosTupla,ret] = mySapObject.SapModel.AreaObj.GetPoints(i,0,())
            PuntosArea.append(PuntosTupla)
        
    
    if caso==2 or caso==3:
        PuntosArea.append(tuple(Punto))
    print(PuntosArea) 

    PuntosArea = np.array([x for t in PuntosArea for x in t])
    PuntosArea=np.unique(PuntosArea)
    print(PuntosArea) 
    
    for i in Frame:
        [P1,P2,ret] = mySapObject.SapModel.FrameObj.GetPoints(i,'','')

        PuntosLinea.append((P1,P2))
    
    

    PuntosLinea = np.array([x for t in PuntosLinea for x in t])

    PuntosAreaCoord=[]
    PuntosLineaCoord=[]
    for i in PuntosArea:
        [x,y,z,ret]=mySapObject.SapModel.PointObj.GetCoordCartesian(i,0,0,0)
        PuntosAreaCoord.append([x,y,z])

    for i in PuntosLinea:
        [x,y,z,ret]=mySapObject.SapModel.PointObj.GetCoordCartesian(i,0,0,0)
        PuntosLineaCoord.append([x,y,z])
    
    



    PuntosLineaCoord=np.array(PuntosLineaCoord)
    linea=PuntosLineaCoord[:, :2]
    PuntosAreaCoord=np.array(PuntosAreaCoord)
    puntos=PuntosAreaCoord[:, :2]

    print(linea)
    LINEAT=[]
    for i in range(len(linea)-1):
        A = linea[i]
        B = linea[i + 1]
        lin= np.linspace(A, B, 1000, endpoint=False)
        LINEAT.append(lin)
    LINEAT = np.vstack(LINEAT + [linea[-1][None, :]])
    linea=LINEAT
    
    print(puntos)
    tree = cKDTree(linea)
    dist, idx = tree.query(puntos)
    print(idx)
    puntos_ajustados = linea[idx]
    print(puntos_ajustados)

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
    for i,j,k in zip(PuntosArea,puntos_ajustados,PuntosAreaCoord):
        #Nuevos x y z
        #print(i)
        #print(j)
        #print(k)
        [xn,yn]=j
        [xv,yv,zv]=k
        print(xn,yn,zv)
        # Modificacion
        ret = mySapModel.EditPoint.ChangeCoordinates_1(i, xn, yn, zv,True)
 

    
def IgualarPuntos():
    Punto,_,_=obtenerselecion()
    [x,y,z,ret]=mySapObject.SapModel.PointObj.GetCoordCartesian(Punto[0],0,0,0)
    input("Cambia Seleccion")
    Punto,_,_=obtenerselecion()
    for i in Punto:
        [_,_,z,_]=mySapObject.SapModel.PointObj.GetCoordCartesian(i,0,0,0)
        ret = mySapModel.EditPoint.ChangeCoordinates_1(i, x, y, z,True)

    
    





#Python Running example code
initialize_helper()
attach()
i=0
#while i == 0:
#    
    #i=int(input("Ingresa Valor Distinto de 0"))

i=int(input("Caso: \n 1 [Ajustar Areas a Frames] " \
"\n 2 [Ajustar Areas y Puntos a Frame] " \
"\n 3 [Ajustar Puntos a Frame] " \
"\n 4 [Alinear Puntos] \n"))

if i==1 or i==2 or i==3:
    Punto,Frame,Area=obtenerselecion()
    caso=i
    ajustarlinea(Punto,Frame,Area,caso)

elif i==4:
    for i in range(1):
        input("---")
        IgualarPuntos()
#IgualarPuntos()
ret=mySapObject.SapModel.View.RefreshView()


#input("Press Enter to continue and close the model.")
# Close the program
