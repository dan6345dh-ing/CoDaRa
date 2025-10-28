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
Caso=6

#Punto,Frame,Area=SP20.obtenerseleccion(mySapModel, mySapObject, ret)
if Caso==0:
    Puntos=["23750","23106","23751"]
    for i in Puntos:
        ret = mySapModel.PointObj.SetSelected(i, True)

    Areas=["8176","24687"]
    for i in Areas:
        ret = mySapModel.AreaObj.SetSelected(i, True, 0)
elif Caso==1: #DIBUJO LINEAS EN LA ZONA SUPERIOR DE LAS AREAS
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

elif Caso == 4: # Cambiar Seccion de un material por otro material
    _,_,Area=SP20.obtenerseleccion(mySapModel, mySapObject, ret)
    AreaProp=[]
    Inicial="M"
    Reemplazo="La"
    for i in Area:
        Prop, ret = mySapModel.AreaObj.GetProperty(i, "")
        Prop=Prop.replace(Inicial, Reemplazo)
        AreaProp.append(Prop)

    for i,j in zip(AreaProp, Area):
        ret = mySapModel.AreaObj.SetProperty(j, i)

    print(AreaProp)
 
elif Caso==5: #ExportarLineasDeAutocadASap
    Reescribir=input("Reescribir los frames SI 1 /NO 0:\n")
    if Reescribir==1:
        import win32com.client
        import time
        import os
        path_actual = os.path.dirname(os.path.abspath(__file__))
        print(path_actual)

        # Conecta a AutoCAD
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument

        # Carga y ejecuta un archivo LISP

        lisp_path = path_actual+"\Lisp\ConexionPython.lsp"
        print("PATH")
        print(lisp_path)

        doc.SendCommand(f'(load "{lisp_path}") ')

        time.sleep(2)
        doc.SendCommand('(c:ObteneryExportarLineas)\n')


    f = open('Lisp/txtpoint.txt')
    contenido=f.read()

    contenido=contenido.split('\n')
    PuntoRef=[]
    PuntosLinea=[]
    n=0
    for i in contenido:
        n=n+1      
        if n==len(contenido):
            break
        if n==1:  
            PuntosRef=eval(i)
        else:
            Puntos=i.split(";")
            print(Puntos)
            
            Pi=eval(Puntos[0])
            Pf=eval(Puntos[1])
            PuntosLinea.append([Pi,Pf])
    PuntoRef=np.array(PuntosRef)
    PuntosLinea=np.array(PuntosLinea)
        
    Punto=SP20.obtenerCoor(mySapModel, mySapObject, ret, PuntoTF=True, FrameTF=False, AreaTF=False, EliminarRepetidos=False)
    print("----- PUNTO DE REFERENCIA AUTOCAD -----")
    print(PuntoRef, "\n")
    print("----- PUNTO DE LINEA AUTOCAD -----")
    print(PuntosLinea, "\n")
    print("----- PUNTO DE REFERENCIA SAP2000 -----")
    print(Punto[0].astype(tuple))

    Deltas=-PuntoRef+Punto[0]
    print(Deltas)
    n=0
    for i in PuntosLinea:
        n=n+1
        print(i)
        PointCoordINI=i[0]+Deltas
        PointCoordFIN=i[1]+Deltas
        SP20.DibujarLinea(PointCoordINI,PointCoordFIN,"DeSap"+str(n),mySapModel)

elif Caso==6: #Obtener Derivas del Sap

    
    Numero_de_Piso=input("Ingrese Número de Pisos:")
    HPisos=[]
    DesplazamientoEX=[]
    DesplazamientoEY=[]
    NodoMAXIMOEx=[]
    NodoMAXIMOEy=[]
    ret = mySapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    ret = mySapModel.Results.Setup.SetCaseSelectedForOutput("Ex")
    ret = mySapModel.Results.Setup.SetCaseSelectedForOutput("Ey")
    
    CasoSeleccion=input("1) Seleccion Manual de Nodos \n2) Seleccion por piso \n Caso: ")
    
    for i in range(int(Numero_de_Piso)):
        
        if CasoSeleccion=="2":
            ret = mySapModel.SelectObj.ClearSelection()
            h=float(input("\nIngrese Altura de Piso "+str(i+1)+"[m]:  "))
            HPisos.append(h)
            ret = mySapModel.SelectObj.CoordinateRange(float('-inf'), float('inf'), float('-inf'), float('inf'), h, h,False,"GLOBAL",False, True ,False , False, False , False)


            NumberResults = 0;    Obj = [];    Elm = [];    ACase = [];    StepType = [];    StepNum = []
            U1 = [];    U2 = [];    U3 = [];    R1 = [];    R2 = [];    R3 = []
            ObjectElm = 3
            #0-> ObjetoElm 1-> Group ELem 2->  3-> Seleccion
        elif CasoSeleccion =="1":
            ret = mySapModel.SelectObj.ClearSelection()
            input("Seleccione Nodo " + str(i+1) + " : (Enter)")
            PP=SP20.obtenerCoor(mySapModel, mySapObject, ret, PuntoTF=True, FrameTF=False, AreaTF=False, EliminarRepetidos=False)
            print(PP)
            x,y,h=PP[0]
            HPisos.append(h)

            NumberResults = 0;    Obj = [];    Elm = [];    ACase = [];    StepType = [];    StepNum = []
            U1 = [];    U2 = [];    U3 = [];    R1 = [];    R2 = [];    R3 = []
            ObjectElm = 3



        
        [NumberResults, Obj, Elm, ACase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret] = mySapModel.Results.JointDispl("ALL", ObjectElm, NumberResults, Obj, Elm, ACase, StepType, StepNum,U1, U2, U3, R1, R2, R3)
        # U1 -> X ||| U2 -> Y
        Datos=[]
        Datos=pd.DataFrame(zip(Obj,ACase,U1,U2),columns=["Label J","Caso","Ux","Uy"])
        #print(Datos)
        Ex=Datos[Datos["Caso"]=="Ex"]
        Ey=Datos[Datos["Caso"]=="Ey"]
        Ex.reset_index(inplace=True,drop=True)
        Ey.reset_index(inplace=True,drop=True)
        ValoresMaximosEx=Ex.loc[int(Ex["Ux"].argmax()),["Ux","Uy"]].values
        ValoresMaximosEy=Ey.loc[int(Ey["Uy"].argmax()),["Ux","Uy"]].values
        NodoMAXIMOEx.append(Ex.loc[int(Ex["Ux"].argmax()),"Label J"])
        NodoMAXIMOEy.append(Ey.loc[int(Ey["Uy"].argmax()),"Label J"])

        DesplazamientoEX.append(ValoresMaximosEx)
        DesplazamientoEY.append(ValoresMaximosEy)

        #print(DesplazamientoEX)
    print(NodoMAXIMOEx)
    print(NodoMAXIMOEy)
    ret = mySapModel.SelectObj.ClearSelection()
    for i in NodoMAXIMOEx:
        ret = mySapModel.PointObj.SetSelected(i, True)
    ret=mySapObject.SapModel.View.RefreshView()
    input("Nodos de Mayor desplazamiento en X (Continuar)")
    ret = mySapModel.SelectObj.ClearSelection()
    for i in NodoMAXIMOEy:
        ret = mySapModel.PointObj.SetSelected(i, True)
    ret=mySapObject.SapModel.View.RefreshView()
    input("Nodos de Mayor desplazamiento en Y (Continuar)")
 

    import oficina as of
    R=1.5
    of.DibujarDerivas(HPisos,DesplazamientoEX,R,Deriva="X")
    of.DibujarDerivas(HPisos,DesplazamientoEY,R,Deriva="Y")
    

ret=mySapObject.SapModel.View.RefreshView()