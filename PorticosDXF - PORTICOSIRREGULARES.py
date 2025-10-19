import tkinter as tk
from mayavi import mlab
from tkinter import filedialog, messagebox
import oficina as of
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import uuid
from tvtk.api import tvtk
from collections import Counter
from shapely.geometry import Point, LineString, Polygon
import ast, random

def seleccionar_archivos():
    archivos = filedialog.askopenfilenames(
        title="Seleccionar archivos",
        filetypes=[("Archivos de texto", "*.xlsx"), ("Todos los archivos", "*.*")]
    )
    if archivos:
        lista.delete(0, tk.END)  # limpiar la lista
        for archivo in archivos:
            lista.insert(tk.END, archivo)


def obtener_seleccion():
    global archivo_rut, archivo, FramesDF, PX, PY
    PX=[]
    PY=[]
    FramesDF=[]
    seleccion = lista.curselection()  # devuelve una tupla con los índices seleccionados
    if seleccion:
        archivo_rut = lista.get(seleccion[0])  # obtener el texto (ruta) del primer índice
        messagebox.showinfo("Archivo seleccionado", f"Ruta:\n{archivo_rut}")
    else:
        messagebox.showwarning("Atención", "No has seleccionado ningún archivo.")

    archivo=of.Leer_Puntos(archivo_rut)
    archivo.set_index("Joint")
        
## FUNCIONES PROPIAS 

def graficar_excel():
    print(archivo)
    fig
    ax.scatter(archivo["XorR"],archivo["Y"])
    ax.set_xlabel("XorR")
    ax.set_ylabel("Y")
    ax.grid()
    canvas.draw()
    
def Limpiar():
    ax.clear()
    canvas.draw()
 

def contar_decimales(numero):
    """Cuenta el número de decimales de un número flotante."""
    # Convierte el número a cadena y busca el punto decimal.
    # Si no hay punto, busca -1, así que manejamos ese caso.
    s_numero = str(numero)
    if '.' in s_numero:
        # Divide la cadena en la parte entera y decimal
        parte_entera, parte_decimal = s_numero.split('.')
        return len(parte_decimal)
    else:
        return 0 # No tiene parte decimal

def cargar_frames():
    global FramesDF,Puntos
    FramesDF,_,Puntos =of.Leer_Frames_vs2(archivo_rut)
    
    print(FramesDF)


def Exportar_dxf():
    global Guias, FramesTotales
    i=0
    Max=0.0
    dfxTT=[]
    for dfx in FramesTotales:
        i=i+1
        

        dfx["Pz1"]=dfx.apply(lambda x: x["Pz1"]+Max,axis=1)
        dfx["Pz2"]=dfx.apply(lambda x: x["Pz2"]+Max,axis=1)
        
        dfx["P1tupla"]=dfx.apply(lambda x: (x["Px1"],x["Pz1"]),axis=1)
        dfx["P2tupla"]=dfx.apply(lambda x: (x["Px2"],x["Pz2"]),axis=1)
        #print(dfx[["P1tupla","P2tupla"]])
        dfx["Lineatupla"]=dfx.apply(lambda x: LineString([x["P1tupla"],x["P2tupla"]]),axis=1)

        dfxTT.append(dfx)

        Max=dfx[["Pz1", "Pz2"]].to_numpy().max() + Max*1.1

    

    import ezdxf
    # Crear un nuevo documento DXF
    Secciones=pd.read_excel(archivo_rut,sheet_name="Frame Section Assignments",usecols=[0,3],skiprows=[0,2])
    Secciones.set_index("Frame",inplace=True)

    doc = ezdxf.new()
    msp = doc.modelspace()

    n=0
    for capa in Secciones['AnalSect'].unique():
        n=1+n
        capa=str(capa)
        doc.layers.new(name=capa, dxfattribs={'color': n})
        

    n=0
   
        

    # Agregar la línea
    for dfxT in dfxTT:

        for j in dfxT.index:
            lay=Secciones.loc[j,"AnalSect"]
            lay=str(lay)
            i=dfxT.loc[j,"Lineatupla"]
            msp.add_lwpolyline(i.coords,    
                            dxfattribs={'layer': lay}
    )
        
    doc.saveas("Archivos_Salida/DXF_Irregular.dxf")
    print("--DOCUMENTO GUARDADO--")
    messagebox.showinfo("Guardado" ,"'DFX_Irregular.dxf'")
    

def Graficar3D():
    global FramesDF
    mlab.points3d(archivo["XorR"],archivo["Y"],archivo["Z"],scale_factor=0.1)
    print(FramesDF)
    points = []
    lines = []
    point_id = 0

    if len(FramesDF)>0:
        for i in FramesDF.index:
            # nodo inicial
            p1 = (FramesDF.loc[i, "Px1"],
                FramesDF.loc[i, "Py1"],
                FramesDF.loc[i, "Pz1"])
            # nodo final
            p2 = (FramesDF.loc[i, "Px2"],
                FramesDF.loc[i, "Py2"],
                FramesDF.loc[i, "Pz2"])
            
            points.extend([p1, p2])
            lines.append([point_id, point_id+1])  # conecta los 2 puntos
            point_id += 2

        # convertir a arrays
        points = np.array(points)
        lines = np.array(lines)

        # crear PolyData
        poly = tvtk.PolyData(points=points)
        poly.lines = lines

        # mostrar en mayavi
        mlab.pipeline.surface(
            mlab.pipeline.stripper(
                mlab.pipeline.poly_data_normals(
                    mlab.pipeline.add_dataset(poly)
                )
            ),
            color=(0,0,1)
        )
    mlab.show()            

def LineaGuia():
    global FramesDF, Puntos, Guias, df_SinVert

    ninicial=ast.literal_eval(box_Frames.get())
    

    n_dir=ast.literal_eval(box_dir.get())
    print(ninicial)
    print(n_dir)
    #Frames sin los verticales
    df_SinVert=FramesDF.copy()

    df_SinVert=df_SinVert[~((df_SinVert["Px1"]==df_SinVert["Px2"]) & (df_SinVert["Py1"]==df_SinVert["Py2"]))]

    Guias=[]

    nporticos=0
    for i in range(len(ninicial)):
        
        FramesX=pd.DataFrame()

        df4=df_SinVert.copy()

        if n_dir[i]==1:
            FramesX[["JointI","JointJ"]]=df4[["P1","P2"]].copy()
        else:
            FramesX[["JointI","JointJ"]]=df4[["P2","P1"]].copy()

        LineasContinuas=[]

        FramesConcatenado=FramesX.copy()     
        
        FrameInicial=FramesConcatenado.loc[ninicial[i]].copy()

        FramesConcatenado.drop(ninicial[i],inplace=True)

        Inicial=FrameInicial["JointI"]
        Final=FrameInicial["JointJ"]

        LineasContinuas.append({"Pi":ninicial[i],"I":Inicial,"J":Final})

        for j in range(len(FramesX)):
            A=FramesConcatenado[FramesConcatenado["JointI"]==Final]
            B=FramesConcatenado[FramesConcatenado["JointJ"]==Final]

            if len(A)==1:
                ind=A.index
                Inicial=FramesConcatenado.loc[ind,"JointI"].values[0]
                Final=FramesConcatenado.loc[ind,"JointJ"].values[0]
            elif len(B)==1:
                ind=B.index
                Inicial=FramesConcatenado.loc[ind,"JointJ"].values[0]
                Final=FramesConcatenado.loc[ind,"JointI"].values[0]
            else:
                print("--OK--",i,"-",ninicial[i])
                break

            FramesConcatenado.drop(ind,inplace=True)

            LineasContinuas.append({"Pi":ind[0],"I":Inicial,"J":Final})

        df0=pd.DataFrame(LineasContinuas,columns=["Pi","I","J"])
        print(Puntos)
        puntos_indexados=Puntos.copy()

        if i==0:
            ax.scatter(puntos_indexados["XorR"],puntos_indexados["Y"],marker="+",color="blue")

        df0[["Xi","Yi"]]=df0.apply(lambda x: puntos_indexados.loc[x["I"],["XorR","Y"]],axis=1)
        df0[["Xf","Yf"]]=df0.apply(lambda x: puntos_indexados.loc[x["J"],["XorR","Y"]],axis=1)

        df0["Nporticos"]=nporticos
        nporticos=nporticos+1
        
        colorx=np.random.rand(1,3)

        Guias.append(df0)
        for j in df0.index:
            if j == df0.index[0]:
                ax.plot(df0.loc[j,["Xi","Xf"]],df0.loc[j,["Yi","Yf"]],color="black")
                ax.text(df0.loc[j,["Xi"]],df0.loc[j,["Yi"]],s=ninicial[i])
            else:
                ax.plot(df0.loc[j,["Xi","Xf"]],df0.loc[j,["Yi","Yf"]],color=colorx)
                
        canvas.draw()
    print(Guias)


def Crear_Porticos():
    global Guias, FramesDF, FramesTotales
    FramesGuia=[]
    # Definir tolerancia
    tol = ast.literal_eval(box_tol.get())
    for guia in Guias:
        # Calcular distancia de cada punto a la línea
        Linea=[]
        for i in range(len(guia)):
            Linea.append(tuple(guia.loc[i,["Xi","Yi"]]))
            if i==len(guia):
                Linea.append(tuple(guia.loc[i,["Xf","Yf"]]))

        Linea=LineString(Linea)

        FramesDF["distI"] = FramesDF.apply(lambda row: Point(row["Px1"], row["Py1"]).distance(Linea), axis=1)
        FramesDF["distF"] = FramesDF.apply(lambda row: Point(row["Px2"], row["Py2"]).distance(Linea), axis=1)

        # Filtrar puntos que estén dentro de la tolerancia
        df_filtrado = FramesDF[(FramesDF["distI"] <= tol) & (FramesDF["distF"] <= tol)]
        FramesGuia.append(df_filtrado)

    
    FramesTotales=[]
    
    for Frames,guia in zip(FramesGuia,Guias):
        PRT=[]
        print(len(Frames))
        print(len(guia))
        for i in range(len(guia)):
            Punto1=guia.loc[i,["Xi","Yi"]].values
            Punto2=guia.loc[i,["Xf","Yf"]].values
                
            guia[["Xi","Yi"]]=of.Traslacion_de_Eje_vs2(Punto1,Punto2,guia,"Especial",["Xi","Yi"],ContenerX="Si")
            guia[["Xf","Yf"]]=of.Traslacion_de_Eje_vs2(Punto1,Punto2,guia,"Especial",["Xf","Yf"],ContenerX="Si")

            SobreEje="Especial"
            VectorXY=["Px1","Py1"]
            Frames[["Px1","Py1"]]=of.Traslacion_de_Eje_vs2(Punto1,Punto2,Frames,SobreEje,VectorXY,ContenerX="Si")
            VectorXY=["Px2","Py2"]
            Frames[["Px2","Py2"]]=of.Traslacion_de_Eje_vs2(Punto1,Punto2,Frames,SobreEje,VectorXY,ContenerX="Si")
            
            Punto1=guia.loc[i,["Xi","Yi"]].values
            Punto2=guia.loc[i,["Xf","Yf"]].values

            Y1=Punto1[1]
            Y2=Punto2[1]

            X1=Punto1[0]
            X2=Punto2[0]



            guia.drop(i,inplace=True)

            
            PRot_Selec = Frames[Frames["Py1"].between(Y1 - tol, Y2 + tol) & Frames["Py2"].between(Y1 - tol, Y2 + tol) &
                                    Frames["Px1"].between(X1 - tol, X2 + tol) & Frames["Px2"].between(X1 - tol, X2 + tol)
                                    ].copy()
            Frames=Frames.drop(PRot_Selec.index)
            print(i,"--",len(Frames))
            
            PRT.append(PRot_Selec)
            if len(Frames)==0:
                break

        FramesRotados=pd.concat(PRT)
        print(FramesRotados)
        FramesTotales.append(FramesRotados)
    


def Graficar3DSel():
    global FramesTotales

    print(FramesTotales)
    
    for FramesDFS in FramesTotales:
        points = []
        lines = []
        point_id = 0

        for i in FramesDFS.index:
            # nodo inicial
            p1 = (FramesDFS.loc[i, "Px1"],
                FramesDFS.loc[i, "Py1"],
                FramesDFS.loc[i, "Pz1"])
            # nodo final
            p2 = (FramesDFS.loc[i, "Px2"],
                FramesDFS.loc[i, "Py2"],
                FramesDFS.loc[i, "Pz2"])

            points.extend([p1, p2])
            # Formato correcto: [n_puntos, idx1, idx2]
            lines.append([point_id, point_id + 1])
            point_id += 2

        # convertir a arrays
        points = np.array(points)
        lines = np.array(lines)

        # crear PolyData
        poly = tvtk.PolyData(points=points)
        poly.lines = lines

        # mostrar en mayavi
        mlab.pipeline.surface(
            mlab.pipeline.stripper(
                mlab.pipeline.poly_data_normals(
                    mlab.pipeline.add_dataset(poly)
                )
            ),
            color=tuple(np.random.rand(3)),
            line_width=2
        )

    mlab.show()  




global FramesDF



# Ventana principal
root = tk.Tk()
root.title("PORTICOS DXF")
root.geometry("1000x800")

Frame1=tk.Frame(root)
Frame2=tk.Frame(root)
Frame3=tk.Frame(root)
Frame4=tk.Frame(root)

# GRAFICO
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side="bottom")

# Botones
btn_archivos = tk.Button(root, text="Seleccionar Excel", command=seleccionar_archivos)
btn_graficar = tk.Button(Frame1, text="Graficar", command=graficar_excel)

btn_graf3D = tk.Button(Frame1, text="Graficar 3D", command= Graficar3D )
btn_cargarFrames = tk.Button(Frame1, text="CargaFrames", command= cargar_frames)

btn_crearPorticos = tk.Button(root, text="Crear Porticos", command=Crear_Porticos)
btn_exportarDXF = tk.Button(root, text="Exportar DXF", command=Exportar_dxf)


btn_get = tk.Button(Frame1, text="Obtener archivo seleccionado", command=obtener_seleccion)
btn_clean = tk.Button(Frame1,text="Limpiar Graficos",command=Limpiar)

btn_eval_lineas = tk.Button(root, text="Evaluar Lineas",command=LineaGuia)

btn_grafsel3D = tk.Button(root, text="Graf Seleccion",command=Graficar3DSel)

# Labels


LToleracia = tk.Label(Frame4,text="Tolerancia (Si los puntos no estan en exactos): ")
# Datos ingresables

box_Frames= tk.Entry(root)

box_dir= tk.Entry(Frame4)

box_tol= tk.Entry(Frame4)
# LISTA
lista = tk.Listbox(root,height=3)



# UBICACIONES
btn_archivos.pack()
lista.pack(fill="x")

Frame1.pack(side="top",pady=5)
btn_get.pack(side="left")
btn_graficar.pack(side="left")
btn_clean.pack(side="left")

btn_graf3D.pack(side="left")
btn_cargarFrames.pack(side="left")

Frame2.pack(side="top",pady=5)

box_Frames.pack(side="top",pady=1,fill=tk.X,expand=True)


Frame3.pack(side="top",pady=5)



Frame4['borderwidth'] = 2
Frame4['relief'] = 'sunken'
Frame4.pack(side="top",pady=5)

box_dir.pack(side="left")


LToleracia.pack(side="left")
box_tol.pack(side="left")



btn_exportarDXF.pack(side="bottom")

btn_grafsel3D.pack(side="bottom")
btn_crearPorticos.pack(side="bottom")
btn_eval_lineas.pack(side="bottom")
# MODIFICACIONES POSTERIORES

box_Frames.insert(0,"[236,205]")
box_dir.insert(0,"[1,1]")

box_tol.insert(0,"0.00001")

root.mainloop()
