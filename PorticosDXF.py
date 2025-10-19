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

def GraficarExterno():
    fig2, ax2 = plt.subplots()
    ax2.scatter(archivo["XorR"],archivo["Y"])
    ax2.set_xlabel("XorR")
    ax2.set_ylabel("Y")
    ax2.grid()
    
    fig2.show()

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
    global FramesDF
    FramesDF,_,_ =of.Leer_Frames_vs2(archivo_rut)
    
    print(FramesDF)

def limiteRangosX():
    global PX
    ini=float(box_X_ini.get())
    fin=float(box_X_fin.get())
    salto=float(box_X_salto.get())
    nd=np.max([contar_decimales(ini),contar_decimales(salto),contar_decimales(salto)])

    PX=np.arange(ini*nd,fin*nd+0.01,salto*nd)
    PX=PX/nd
    print(PX)
    ax.set_xticks(PX)
    ax.tick_params(axis='x',rotation=90)
    for i in PX:
        ax.plot([i,i],[archivo["Y"].min(),archivo["Y"].max()],color="yellow", linestyle='--')
    canvas.draw()

def limiteRangosY():
    global PY
    ini=float(box_Y_ini.get())
    fin=float(box_Y_fin.get())
    salto=float(box_Y_salto.get())
    nd=np.max([contar_decimales(ini),contar_decimales(salto),contar_decimales(salto)])

    PY=np.arange(ini,fin+0.01,salto)
    PY=PY/nd
    print(PY)
    ax.set_yticks(PY)
    for i in PY:
        ax.plot([archivo["XorR"].min(),archivo["XorR"].max()],[PY,PY],color="green", linestyle='--')
    canvas.draw()

def grafico_histograma():    
    figh, axh = plt.subplots(2)

    valores = archivo["XorR"].to_numpy()
    conteo = Counter(valores)


    axh[0].bar(conteo.keys(), conteo.values(), color='orange',width=0.02)
    axh[0].set_xlabel("Rango de valores")
    axh[0].set_ylabel("Frecuencia")
    axh[0].set_xticks(np.unique(valores))

    valores = archivo["Y"].to_numpy()
    conteo = Counter(valores)

    axh[1].bar(conteo.keys(), conteo.values(), color='orange',width=0.02)
    axh[1].set_xlabel("Rango de valores")
    axh[1].set_ylabel("Frecuencia")
    axh[1].set_xticks(np.unique(valores))

    figh.show()

def bordes(cuantos,esc,PS):

    MarcoDy=297
    MarcoDx=420

    Bx1=0
    Bx2=MarcoDx/esc
    By1=0
    By2=MarcoDy/esc
    Espacio=20
    BxT=[]
    ByT=[]
    PRefX=[]
    PRefY=[]

    MarcoDy=297/esc
    MarcoDx=420/esc
    
    n=np.ceil(len(PS)/cuantos)
    n=int(n)
    for i in range(n):        
        if cuantos==2:
            PRefX.append(Bx1+15/esc)
            PRefX.append(Bx1+15/esc)
            PRefY.append(By1+((By2-By1)/2+Espacio/esc))
            PRefY.append(By1+((By2-By1)/2-Espacio/esc))
        else:
            for i in range(cuantos):
                PRefX.append(Bx1+15/esc)
                PRefY.append(By1+15/esc+((By2-By1)/cuantos*i))

        BxT.append([Bx1,Bx2,Bx2,Bx1,Bx1])
        ByT.append([By1,By1,By2,By2,By1])
        
        By1=By1+MarcoDy+Espacio
        By2=By1+MarcoDy
    
    return BxT,ByT,PRefX,PRefY

def Portico(tol,PS,Sentido,cuantos,esc):
    global dfT,FramesDF
    BxT,ByT,PRefX,PRefY=bordes(cuantos,esc,PS)
    # TOL -> Toleracia para rangos
    # PS -> Numpy de porticos o rangoX, rangoY
    # dfra -> Excel con porticos
    # Sentido o X o Y
    dfra=FramesDF.copy()
    BordeCercha=[]
    dfT=[]
    n=0
    
    if Sentido=="x":
        Sel1="Py1"
        Sel2="Py2"
        Sel3="Px1"
        Sel4="Px2"
        
    elif Sentido=="y":
        Sel1="Px1"
        Sel2="Px2"
        Sel3="Py1"
        Sel4="Py2"

    for i in PS:
        
        dfx=dfra[(dfra[Sel1]>i-tol) & (dfra[Sel1]<i+tol) & (dfra[Sel2]>i-tol) & (dfra[Sel2]<i+tol)].copy()

        x1=dfx[[Sel3,Sel4]].min().min()
        y1=dfx[["Pz1","Pz2"]].min().min()
        x2=dfx[[Sel3,Sel4]].max().max()
        y2=dfx[["Pz1","Pz2"]].max().max()

        if np.isnan(x1):
            n=n+1
            dx=PRefX[n]
            dy=PRefY[n]
            BordeCercha.append([dx,dy,0,0])
            
            continue

            
        if n%2==0:
            dx=PRefX[n]-x1
            dy=PRefY[n]-y1
        else:
            dx=PRefX[n]-x1
            dy=PRefY[n]-y2

        n=n+1

        dfx[Sel3]=dfx.apply(lambda x: x[Sel3]+dx,axis=1)
        dfx[Sel4]=dfx.apply(lambda x: x[Sel4]+dx,axis=1)
        dfx["Pz1"]=dfx.apply(lambda x: x["Pz1"]+dy,axis=1)
        dfx["Pz2"]=dfx.apply(lambda x: x["Pz2"]+dy,axis=1)


        dfx["P1tupla"]=dfx.apply(lambda x: (x[Sel3],x["Pz1"]),axis=1)
        dfx["P2tupla"]=dfx.apply(lambda x: (x[Sel4],x["Pz2"]),axis=1)
        #print(dfx[["P1tupla","P2tupla"]])
        dfx["Lineatupla"]=dfx.apply(lambda x: LineString([x["P1tupla"],x["P2tupla"]]),axis=1)

        #print(dfx[["Lineatupla","P1tupla","P2tupla"]])
        x1=dfx[[Sel3,Sel4]].min().min()
        y1=dfx[["Pz1","Pz2"]].min().min()
        x2=dfx[[Sel3,Sel4]].max().max()
        y2=dfx[["Pz1","Pz2"]].max().max()
        BordeCercha.append([x1,x2,y1,y2])
        
        dfT.append(dfx[["Lineatupla","P1tupla","P2tupla"]].copy())
        
    dfT=pd.concat(dfT)

    figP, axP = plt.subplots(figsize=[20,80])
    axP.grid()
    axP.set_aspect("equal")
    # Dibujar polilínea original
    for i in dfT.index:
        polilinea=dfT.loc[i,"Lineatupla"]
        #print(polilinea)
        x, y = polilinea.xy
        
        axP.plot(x, y, color='black')

    for i in range(len(BxT)):
        axP.plot(BxT[i],ByT[i],color="r")
    n=0
    for i in BordeCercha:

        axP.plot([i[0],i[0],i[1],i[1],i[0]],[i[2],i[3],i[3],i[2],i[2]],color="g")   
        axP.text((i[1]-i[0])/2,i[3]+10/esc,PS[n])   
        n=n+1
    
    figP.show()
    if Sentido=="y":
        global dfTx,BordeCerchax,BXx,BYx
        dfTx=dfT.copy()
        BordeCerchax=BordeCercha.copy()
        BXx=BxT.copy()
        BYx=ByT.copy()
    elif Sentido=="x":
        global dfTy,BordeCerchay,BXy,BYy
        dfTy=dfT.copy()
        BordeCerchay=BordeCercha.copy()
        BXy=BxT.copy()
        BYy=ByT.copy()    
    
def Exportar_dxf(esc):
    global dfTx,dfTy,BordeCerchax,BordeCerchay,BXx,BYx,BXy,BYy,PX,PY
    
    import ezdxf
    # Crear un nuevo documento DXF

    Secciones=pd.read_excel(archivo_rut,sheet_name="Frame Section Assignments",usecols=[0,3],skiprows=[0,2])
    Secciones.set_index("Frame",inplace=True)

    if BordeCerchax:
        BordeCercha=BordeCerchax.copy()
        dfT=dfTx.copy()
        BxT=BXx.copy()
        ByT=BYx.copy()
        PS=PX.copy()

        doc = ezdxf.new()
        msp = doc.modelspace()

        n=0
        for i in BordeCercha:
            msp.add_text("Porticos X"+str(np.round(PS[n])), dxfattribs={'height': 5/esc,'insert': ((i[1]-i[0])/2,i[3]+10/esc) })
            n=n+1

        n=0
        for capa in Secciones['AnalSect'].unique():
            n=1+n
            capa=str(capa)
            doc.layers.new(name=capa, dxfattribs={'color': n})
            

        # Agregar la línea
        for j in dfT.index:
            lay=Secciones.loc[j,"AnalSect"]
            lay=str(lay)
            i=dfT.loc[j,"Lineatupla"]
            msp.add_lwpolyline(i.coords,    
                            dxfattribs={'layer': lay}
        )
            
        for i,j in zip(BxT,ByT):
            Poly=np.column_stack([np.transpose(i),np.transpose(j)])
            Poly=LineString(Poly)
            msp.add_lwpolyline(Poly.coords)
            
        doc.saveas("Archivos_Salida/DXF_por_X.dxf")
        print("--DOCUMENTO GUARDADO--X")
        messagebox.showinfo("Guardado" ,"'DFX_por_X.dxf'")

    if BordeCerchay:
        BordeCercha=BordeCerchay.copy()
        dfT=dfTy.copy()
        BxT=BXy.copy()
        ByT=BYy.copy()
        PS=PY.copy()

        doc = ezdxf.new()
        msp = doc.modelspace()

        n=0
        for i in BordeCercha:
            msp.add_text("Porticos Y "+str(np.round(PS[n])), dxfattribs={'height': 5/esc,'insert': ((i[1]-i[0])/2,i[3]+10/esc) })
            n=n+1

        n=0
        for capa in Secciones['AnalSect'].unique():
            n=1+n
            capa=str(capa)
            doc.layers.new(name=capa, dxfattribs={'color': n})
            

        # Agregar la línea
        for j in dfT.index:
            lay=Secciones.loc[j,"AnalSect"]
            lay=str(lay)
            i=dfT.loc[j,"Lineatupla"]
            msp.add_lwpolyline(i.coords,    
                            dxfattribs={'layer': lay}
        )
            
        for i,j in zip(BxT,ByT):
            Poly=np.column_stack([np.transpose(i),np.transpose(j)])
            Poly=LineString(Poly)
            msp.add_lwpolyline(Poly.coords)
            
        doc.saveas("Archivos_Salida/DXF_por_Y.dxf")
        print("--DOCUMENTO GUARDADO--Y")
        messagebox.showinfo("Guardado" ,"'DFX_por_Y.dxf'")


def D3_EXPORT():
    global FramesDF
    df=FramesDF.copy()
    df["P1tupla"]=df.apply(lambda x: (x["Px1"],x["Py1"],x["Pz1"]),axis=1)
    df["P2tupla"]=df.apply(lambda x: (x["Px2"],x["Py2"],x["Pz2"]),axis=1)

    df["Lineatupla"]=df.apply(lambda x: LineString([x["P1tupla"],x["P2tupla"]]),axis=1)
    dfT=df.copy()
    import ezdxf
    # Crear un nuevo documento DXF
    doc = ezdxf.new()
    msp = doc.modelspace()


    Secciones=pd.read_excel(archivo_rut,sheet_name="Frame Section Assignments",usecols=[0,3],skiprows=[0,2])
    Secciones.set_index("Frame",inplace=True)

    Secciones2=[]
    for j in dfT.index:
        
        lay=Secciones.loc[j,"AnalSect"]
        Secciones2.append(lay)

    Secciones2=np.unique(Secciones2)

    n=0
    for capa in Secciones2:
        n=1+n
        doc.layers.new(name=str(capa), dxfattribs={'color': n})

    # Agregar la línea
    for j in dfT.index:
        lay=Secciones.loc[j,"AnalSect"]
        i=dfT.loc[j,"Lineatupla"]
        msp.add_polyline3d(i.coords,    
                        dxfattribs={'layer': lay}
    )

    doc.saveas("Archivos_Salida/salida3D.dxf")
    print("-- DOCUMENTOS GUARDO -- 3D")
    messagebox.showinfo("Guardado", "'SALIDA 3D.dxf'")


# GLOBALES
global PX,PY,dfT,dfTx,dfTy,BordeCerchax,BordeCerchay,BXx,BYx,BXy,BYy

BordeCerchax=[]
BordeCerchay=[]
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
btn_grafuera = tk.Button(Frame1, text="Graficar Fuera", command= GraficarExterno )
btn_graf3D = tk.Button(Frame1, text="Graficar 3D", command= Graficar3D )
btn_cargarFrames = tk.Button(Frame1, text="CargaFrames", command= cargar_frames)
btn_Hist = tk.Button(Frame1, text="Hist", command= grafico_histograma )

btn_Porticos_viewX = tk.Button(Frame3, text="PorticosX", command=lambda: Portico(tol=float(box_tol.get()),
                                                                               PS=PX,
                                                                               Sentido="y",
                                                                               cuantos=int(box_cuantos.get()),
                                                                               esc=float(box_escala.get())
                                                                               ))

btn_Porticos_viewY = tk.Button(Frame3, text="PorticosY", command=lambda: Portico(tol=float(box_tol.get()),
                                                                               PS=PY,
                                                                               Sentido="x",
                                                                               cuantos=int(box_cuantos.get()),
                                                                               esc=float(box_escala.get())
                                                                               ))

btn_exportarDXF = tk.Button(root, text="Exportar DXF", command= lambda: Exportar_dxf(esc=float(box_escala.get())))
btn_exportard3 = tk.Button(root,text="Exportar 3D",command=D3_EXPORT)

btn_get = tk.Button(Frame1, text="Obtener archivo seleccionado", command=obtener_seleccion)
btn_clean = tk.Button(Frame1,text="Limpiar Graficos",command=Limpiar)

btn_Xsep = tk.Button(Frame2,text="Rangos X", command=limiteRangosX)
btn_Ysep = tk.Button(Frame2,text="Rangos Y", command=limiteRangosY)

# Labels

Lcuantos = tk.Label(Frame4,text="Cuantos por plano: ")
Lescala = tk.Label(Frame4,text="Escala del plano (A3/Esc): ")
LToleracia = tk.Label(Frame4,text="Tolerancia (Si los puntos no estan en exactos): ")
# Datos ingresables

box_X_ini= tk.Entry(Frame2)
box_X_fin= tk.Entry(Frame2)
box_X_salto= tk.Entry(Frame2)

box_Y_ini= tk.Entry(Frame2)
box_Y_fin= tk.Entry(Frame2)
box_Y_salto= tk.Entry(Frame2)

box_cuantos= tk.Entry(Frame4)
box_escala= tk.Entry(Frame4)
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
btn_grafuera.pack(side="left")
btn_graf3D.pack(side="left")
btn_cargarFrames.pack(side="left")
btn_Hist.pack(side="left")

Frame2.pack(side="top",pady=5)
btn_Xsep.pack(side="left")

Frame3.pack(side="top",pady=5)

btn_Porticos_viewX.pack(side="left")
btn_Porticos_viewY.pack(side="left")

box_X_ini.pack(side="left")
box_X_fin.pack(side="left")
box_X_salto.pack(side="left")

btn_Ysep.pack(side="left")

box_Y_ini.pack(side="left")
box_Y_fin.pack(side="left")
box_Y_salto.pack(side="left")

Frame4['borderwidth'] = 2
Frame4['relief'] = 'sunken'
Frame4.pack(side="top",pady=5)
Lcuantos.pack(side="left")
box_cuantos.pack(side="left")
Lescala.pack(side="left")
box_escala.pack(side="left")
LToleracia.pack(side="left")
box_tol.pack(side="left")

btn_exportarDXF.pack(side="bottom")
btn_exportard3.pack(side="bottom")
# MODIFICACIONES POSTERIORES
box_X_ini.insert(0,"X Inicial ...")
box_X_fin.insert(0,"X Final ...")
box_X_salto.insert(0,"X Salto ...")

box_Y_ini.insert(0,"Y Inicial ...")
box_Y_fin.insert(0,"Y Final ...")
box_Y_salto.insert(0,"Y Salto ...")
box_cuantos.insert(0,"2")
box_escala.insert(0,"4")
box_tol.insert(0,"0.01")

root.mainloop()
