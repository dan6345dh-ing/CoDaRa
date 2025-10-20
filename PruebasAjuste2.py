import os
import sys
import comtypes.client
import numpy as np

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


    
def IgualarPuntos():
    punt,_,_=obtenerselecion()
    puntos=[]
    for i in punt:
        [x,y,z,_]=mySapObject.SapModel.PointObj.GetCoordCartesian(i,0,0,0)
        puntos.append([x,y,z])
    puntos=np.array(puntos)
    
    puntos[puntos[:, 2].argsort()]
    
    puntos=puntos[:, :2]
    print(puntos)
    
    from sklearn.cluster import DBSCAN
    import matplotlib.pyplot as plt

    R = 100  # radio
    db = DBSCAN(eps=R, min_samples=1).fit(puntos)
    labels = db.labels_

    n_clusters = len(set(labels))
    print(f"Se detectaron {n_clusters} grupos")

    # Visualizar
    colores = plt.cm.tab10(np.linspace(0, 1, n_clusters))
    for i, c in enumerate(np.unique(labels)):
        plt.scatter(puntos[labels == c, 0], puntos[labels == c, 1],
                    color=colores[i % len(colores)], s=20, label=f'Grupo {i+1}')
    print(labels)
    print(puntos)
    plt.legend()
    plt.axis('equal')
    plt.show()

    
    Punto,_,_=obtenerselecion()
    PuntosUnicos=[]
    for i, c in enumerate(np.unique(labels)):
        Modificador=puntos[labels == c]
        nmp=np.array(punt)
        Nombre=nmp[labels == c]
        x,y=Modificador[0]
        PuntosUnicos.append([x,y])
        for k in Nombre:
            [_,_,z,_]=mySapObject.SapModel.PointObj.GetCoordCartesian(k,0,0,0)
            ret = mySapModel.EditPoint.ChangeCoordinates_1(k, x, y, z,True)

    return PuntosUnicos


    

    
    





#Python Running example code
initialize_helper()
attach()


PuntosUnicos=IgualarPuntos()
Zmin=0
Zmax=12000
n=0
for i in PuntosUnicos:
    n=n+1
    borrar="Borrar "+str(n)
    x,y=i
    ret = mySapModel.FrameObj.AddByCoord(x, y, Zmin, x, y, Zmax, borrar)


ret=mySapObject.SapModel.View.RefreshView()

