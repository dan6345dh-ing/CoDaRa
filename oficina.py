import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def Deriva(Pisos,Desplazamientos,Dibujo):
    
    for i in range(int(Pisos.size)):
        if i == 0:
            deriva=np.array([0])
        else:
            Valor=(Desplazamientos[i]-Desplazamientos[int(i-1)])/Pisos[i]
            deriva=np.append(deriva,Valor*100)

    fig, ax= plt.subplots()
    ax.plot(deriva,Pisos)
    fig.show()
    return deriva

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)
    

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

import numpy as np

def unit_vector(v):
    return v / np.linalg.norm(v)

def angle_between_2pi(v1, v2):
    """
    Retorna el ángulo entre v1 y v2 en radianes, entre 0 y 2π.
    El ángulo es medido desde v1 hacia v2 (antihorario).
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)

    # Producto cruzado (z componente en 2D)
    cross = v1_u[0]*v2_u[1] - v1_u[1]*v2_u[0]
    dot = np.dot(v1_u, v2_u)

    # Ángulo con signo entre -π y π
    angle_rad = np.arctan2(cross, dot)

    # Ajustar para que esté entre 0 y 2π
    if angle_rad < 0:
        angle_rad += 2 * np.pi

    return angle_rad


def p_s_l(Punto1,Punto2,Dist):
    dX=Punto2[0]-Punto1[0]
    dY=Punto2[1]-Punto1[1]
    D=np.sqrt((dX)**2+(dY)**2)
    E=Dist/D
    dXL=dX*E
    dYL=dY*E
    XL=dXL+Punto1[0]
    YL=dYL+Punto1[1]
    return np.array([XL,YL]), D


def arco(R,Pi,Pf,JoinINI,ArcoRegular,Dibujo):
    SaltoZ=0.1
    Vec2=Pf-Pi
    Vec2=np.append(Vec2,0)
    
    Dist=0.1
    Pp,L=p_s_l(Pi,Pf,Dist)
    Diam=R*2

    if Diam==L or ArcoRegular==1:
        ArcoRegular=L/2
        Y_i=np.linspace(0,R,int(R/SaltoZ+1))
        X_i=(R**2-Y_i**2)**0.5
        X_i_inv=X_i[::-1]

        XT=np.append(-X_i[0:-1],X_i_inv)
        YT=np.append(Y_i[0:-1],Y_i[::-1])
        VECTOR=np.array([XT,YT])
    elif Diam>L:
        Xini=(Diam-L)/2
        Xini=R-Xini
        Yi=(R**2-(Xini)**2)**0.5
        Y_i=np.arange(Yi,R,0.1)
        X_i=(R**2-Y_i**2)**0.5
        X_i_inv=X_i[::-1]
        XT=np.append(-X_i[0::],X_i_inv)
        YT=np.append(Y_i[0::],Y_i[::-1])

   
    XT=XT-XT[0]
    YT=YT-YT[0]
    XTr=XT.copy()
    YTr=YT.copy()
    ZTr=XT.copy()
    ZT=XT.copy()
   

    #XT=XT+Pi[0]
    #YT=YT+Pi[1]
    
    Angulo=angle_between(np.array([1,0,0]),Vec2)
    Rot=np.array([[np.cos(Angulo),-np.sin(Angulo),0],[np.sin(Angulo),np.cos(Angulo),0],[0,0,1]])
    for i in range(XT.size):
        VECaux=np.array([XT[i],0,YT[i]])
        VECaux=np.dot(Rot,VECaux)
        XTr[i]=VECaux[0]
        YTr[i]=VECaux[1]
        ZTr[i]=VECaux[2]

    JOINT=np.arange(JoinINI,JoinINI+XT.size,1)
    TX=np.full(int(XT.size),np.empty)
    CORDSYS=np.full(int(XT.size),'GLOBAL')
    CORDTYPE=np.full(int(XT.size),'Cartesian')
    SPE=np.full(int(XT.size),'No')

    XTr=XTr+Pi[0]
    YTr=YTr+Pi[1]       

    if Dibujo==1:
        ax = plt.figure().add_subplot(projection='3d')
        ax.plot(XT,0,YT,marker="o")
        ax.plot(XTr,YTr,ZTr,marker="*")

        plt.axis('equal')
        plt.xlabel('X (m)')
        plt.ylabel('Y (m)')
        plt.show()
   

    return XTr,YTr,ZTr,JOINT,CORDSYS,CORDTYPE,SPE,TX

def Puntos_Lineales(Punto1,Punto2,Dist,h):
    acumn=0
    Px=[0]
    for i in range(Dist.size):
        acumn=acumn+Dist[i]

        A,D=p_s_l(Punto1,Punto2,acumn)  
    
        if i==0:
            Px=np.array([A])
        elif i==1:
            Px=np.append(Px,np.array([A]),axis=0)
        else:
            Px=np.append(Px,np.array([A]),axis=0)

    Px=np.insert(Px,2,h,axis=1)
    return Px

def recta_dospuntos(Punto1,Punto2):
    # Punto (X,Y,Z) SE CONSIDERA Z1=Z0
    # Formula Ax+By+C=0
    A=Punto1[1]-Punto2[1]
    B=Punto2[0]-Punto1[0]
    C=Punto1[0]*Punto2[1]-Punto2[0]*Punto1[1]
    return A,B,C

def distancia_puntoarecta(Punto1,Punto2,PuntoX):
    A,B,C = recta_dospuntos(Punto1,Punto2)
    d=np.abs((A*PuntoX[0]+B*PuntoX[1]+C)/np.sqrt(A*A+B*B))
    x0=PuntoX[0]
    y0=PuntoX[1]
    Px_xy=np.array([x0-d*(A/np.sqrt(A*A+B*B)),y0-d*(B/np.sqrt(A*A+B*B))])
    return d,Px_xy


def Traslacion_de_Eje_vs2(Punto1,Punto2,Puntos_rotables,SobreEje,VectorXY=["XorR","Y"],ContenerX="No",VectorSentido=[1,0,0]):
    # VECTOR XY: da datos "X, como XorR, Y como "Y"
    # Translacion de eje respecto al centro de coordenadas X,Y, =0,0
    # Incluye rotacion translacion los puntos generan una recta que sera la nueva X
    # Punto 1 y Punto 2  Forman la nueva recta --> 
    # PUNTOS A ROTAR DEBE SER UN PANDAS DATAFRAME

    XorTxt=VectorXY[0]
    YorTxY=VectorXY[1]

    Puntos_a_rotar=Puntos_rotables.copy()
    
    PuntosList=[]
    
    deltaX=Punto1[0]
    deltaY=Punto1[1]

    Punto2=Punto2-np.array([deltaX,deltaY])
    Punto1=Punto1-Punto1

    A,B,C=recta_dospuntos(Punto1,Punto2)

    Puntos_a_rotar["Xtras"]=Puntos_a_rotar[XorTxt].apply(lambda x: x-deltaX)
    Puntos_a_rotar["Ytras"]=Puntos_a_rotar[YorTxY].apply(lambda x: x-deltaY)

    #print(Puntos_a_rotar)

    Vec2=Punto2-Punto1
    Vec2=np.append(Vec2,0)

    if SobreEje=="Y":
        angulo=angle_between(np.array([0,1,0]),Vec2)
        MatrixRotacion=np.array([[np.cos(angulo),np.sin(angulo)],[-np.sin(angulo),np.cos(angulo)]])
    elif SobreEje=="X":
        angulo=angle_between(np.array([1,0,0]),Vec2)
        MatrixRotacion=np.array([[np.cos(angulo),np.sin(angulo)],[-np.sin(angulo),np.cos(angulo)]])
    elif SobreEje=="Especial":
        angulo=angle_between_2pi(np.array(VectorSentido),Vec2)

        MatrixRotacion=np.array([[np.cos(-angulo),-np.sin(-angulo)],
                                 [np.sin(-angulo),np.cos(-angulo)]])
    #MatrixRotacion=np.array([[np.cos(angulo),np.sin(angulo)],[-np.sin(angulo),np.cos(angulo)]])
    

    for i in Puntos_a_rotar.index:
        # Separa Puntos
        Puntos=Puntos_a_rotar.loc[i,["Xtras","Ytras"]].to_numpy()
        Puntos=np.transpose(Puntos)
        P_rot=np.dot(MatrixRotacion,Puntos)
        
        #Rotacion de puntos

        Punto = {"Pi": i ,"Xrot": P_rot[0], "Yrot": P_rot[1]}
        PuntosList.append(Punto)
        # Lista de Puntos ROTADOS
    
        
    del Puntos_a_rotar['Xtras']
    del Puntos_a_rotar['Ytras']

    PuntosRotados=pd.DataFrame(PuntosList)
    PuntosRotados.set_index("Pi",inplace=True)
    if ContenerX=="Si":
        
        PuntosRotados["Xrot"]=PuntosRotados.apply(lambda x: x["Xrot"]+deltaX,axis=1)
        PuntosRotados["Yrot"]=PuntosRotados.apply(lambda x: x["Yrot"]+deltaY,axis=1)
        


    return PuntosRotados

def Traslacion_de_Eje(Punto1,Punto2,Puntos_rotables,SobreEje,VectorXY=["XorR","Y"]):
    # VECTOR XY: da datos "X, como XorR, Y como "Y"
    # Translacion de eje respecto al centro de coordenadas X,Y, =0,0
    # Incluye rotacion translacion los puntos generan una recta que sera la nueva X
    # Punto 1 y Punto 2  Forman la nueva recta --> 
    # PUNTOS A ROTAR DEBE SER UN PANDAS DATAFRAME

    XorTxt=VectorXY[0]
    YorTxY=VectorXY[1]
    Puntos_a_rotar=Puntos_rotables.copy()
    
    PuntosList=[]
    
    deltaX=Punto1[0]
    deltaY=Punto1[1]

    Punto2=Punto2-np.array([deltaX,deltaY])
    Punto1=Punto1-Punto1
    A,B,C=recta_dospuntos(Punto1,Punto2)

    Puntos_a_rotar["Xtras"]=Puntos_a_rotar[XorTxt].apply(lambda x: x-deltaX)
    Puntos_a_rotar["Ytras"]=Puntos_a_rotar[YorTxY].apply(lambda x: x-deltaY)

    #print(Puntos_a_rotar)

    Vec2=Punto2-Punto1
    Vec2=np.append(Vec2,0)
    if SobreEje=="Y":
        angulo=angle_between(np.array([0,1,0]),Vec2)
        MatrixRotacion=np.array([[np.cos(angulo),np.sin(angulo)],[-np.sin(angulo),np.cos(angulo)]])
    elif SobreEje=="X":
        angulo=angle_between(np.array([1,0,0]),Vec2)
        MatrixRotacion=np.array([[np.cos(angulo),np.sin(angulo)],[-np.sin(angulo),np.cos(angulo)]])
    elif SobreEje=="Especial":
        angulo=angle_between_2pi(np.array([1,0,0]),Vec2)
        MatrixRotacion=np.array([[np.cos(angulo),-np.sin(angulo)],
                                 [np.sin(angulo),np.cos(angulo)]])
    #MatrixRotacion=np.array([[np.cos(angulo),np.sin(angulo)],[-np.sin(angulo),np.cos(angulo)]])
    

    for i in range(len(Puntos_a_rotar)):
        # Separa Puntos
        Puntos=Puntos_a_rotar.iloc[i][["Xtras","Ytras"]].to_numpy()
        Puntos=np.transpose(Puntos)
        P_rot=np.dot(MatrixRotacion,Puntos)
        #Rotacion de puntos

        Punto = {"Xrot": P_rot[0], "Yrot": P_rot[1]}
        PuntosList.append(Punto)
        # Lista de Puntos ROTADOS

    del Puntos_a_rotar['Xtras']
    del Puntos_a_rotar['Ytras']

    PuntosRotados=pd.DataFrame(PuntosList)
    
    return PuntosRotados

def Interseccion_Plano_Recta(P1,P2,P3,PL1,PL2):
    # Vectores en el plano
    v1 = P2 - P1
    v2 = P3 - P1

    # Vector normal al plano (producto cruzado)
    normal = np.cross(v1, v2)
    A, B, C = normal
    # Constante D
    D = -np.dot(normal, P1)

    

    vector_direccion=PL2-PL1

    Plano=np.array([A,B,C])
    Numerador= -(np.dot(Plano,PL1)+D)
    Denominador= np.dot(Plano, vector_direccion)
    t=Numerador/Denominador

    PuntoInterseccion=PL1+t*vector_direccion
    return PuntoInterseccion       


def relleno_para_sap(Join_ini,PuntosXYZ):
    X=PuntosXYZ[:,0]
    Y=PuntosXYZ[:,1]
    Z=PuntosXYZ[:,2]
    Total=X.size
    JOINT=np.arange(Join_ini,Join_ini+Total,1)
    TX=np.full(int(Total),'BORRAR')
    CORDSYS=np.full(int(Total),'GLOBAL')
    CORDTYPE=np.full(int(Total),'Cartesian')
    SPE=np.full(int(Total),'No')
    
    Arreglo=np.transpose(np.array([JOINT,CORDSYS,CORDTYPE,X,Y,TX,Z,SPE]))


    return Arreglo

def Leer_Puntos(Excel1):
    Puntos=pd.read_excel(Excel1,sheet_name="Joint Coordinates",usecols=[0,3,4,5],skiprows=[0,2])
    return Puntos

def Leer_Frames(Excel1):
    Puntos_Lista=[]
    Findex=[]
    Frames=pd.read_excel(Excel1,sheet_name="Connectivity - Frame",usecols=[0,1,2],skiprows=[0,2])
    Frames.set_index("Frame",inplace=True)
    #print(Frames)
    Puntos=pd.read_excel(Excel1,sheet_name="Joint Coordinates",usecols=[0,3,4,5],skiprows=[0,2])
    Puntos.set_index("Joint",inplace=True)

    for i in Frames.index:
        PI_PF={"Px1": Puntos.loc[Frames.loc[i,["JointI"]].values,["XorR"]].values[0][0],\
               "Py1": Puntos.loc[Frames.loc[i,["JointI"]].values,["Y"]].values[0][0],\
               "Pz1": Puntos.loc[Frames.loc[i,["JointI"]].values,["Z"]].values[0][0],\
               "P1" : Frames.loc[i,["JointI"]].values[0],\
               "Px2": Puntos.loc[Frames.loc[i,["JointJ"]].values,["XorR"]].values[0][0],\
               "Py2": Puntos.loc[Frames.loc[i,["JointJ"]].values,["Y"]].values[0][0],\
               "Pz2": Puntos.loc[Frames.loc[i,["JointJ"]].values,["Z"]].values[0][0],\
               "P2" : Frames.loc[i,["JointJ"]].values[0]}
        Puntos_Lista.append(PI_PF)
        Findex.append(i)

    Puntos_SAP=pd.DataFrame(Puntos_Lista)

    return Puntos_SAP,Frames,Findex

def Leer_Frames_vs2(Excel1):

    Frames=pd.read_excel(Excel1,sheet_name="Connectivity - Frame",usecols=[0,1,2],skiprows=[0,2])
    Frames.set_index("Frame",inplace=True)
    #print(Frames)
    Puntos=pd.read_excel(Excel1,sheet_name="Joint Coordinates",usecols=[0,3,4,5],skiprows=[0,2])
    Puntos.set_index("Joint",inplace=True)
    FramesDF=pd.DataFrame()
    FramesDF.index=Frames.index

    FramesDF["P1"]=Frames["JointI"]

    FramesDF["Px1"]=FramesDF.apply(lambda x: Puntos.loc[x["P1"],["XorR"]],axis=1)
    FramesDF["Py1"]=FramesDF.apply(lambda x: Puntos.loc[x["P1"],["Y"]],axis=1)
    FramesDF["Pz1"]=FramesDF.apply(lambda x: Puntos.loc[x["P1"],["Z"]],axis=1)

    FramesDF["P2"]=Frames["JointJ"]
    FramesDF["Px2"]=FramesDF.apply(lambda x: Puntos.loc[x["P2"],["XorR"]],axis=1)
    FramesDF["Py2"]=FramesDF.apply(lambda x: Puntos.loc[x["P2"],["Y"]],axis=1)
    FramesDF["Pz2"]=FramesDF.apply(lambda x: Puntos.loc[x["P2"],["Z"]],axis=1)

    return FramesDF,Frames,Puntos
        
def Leer_Area(Excel1):
    Puntos_Lista=[]
    
    Areas=pd.read_excel(Excel1,sheet_name="Connectivity - Area",usecols=[0,2,3,4,5],skiprows=[0,2])
    Areas.set_index("Area",inplace=True)

    Puntos=pd.read_excel(Excel1,sheet_name="Joint Coordinates",usecols=[0,3,4,5],skiprows=[0,2])
    Puntos.set_index("Joint",inplace=True)

    for i in Areas.index:
        PI_PF={"P1x": Puntos.loc[Areas.loc[i,["Joint1"]].values,["XorR"]].values[0][0],\
               "P1y": Puntos.loc[Areas.loc[i,["Joint1"]].values,["Y"]].values[0][0],\
               "P1z": Puntos.loc[Areas.loc[i,["Joint1"]].values,["Z"]].values[0][0],\
               "P1" : Areas.loc[i,["Joint1"]].values[0],\
               "P2x": Puntos.loc[Areas.loc[i,["Joint2"]].values,["XorR"]].values[0][0],\
               "P2y": Puntos.loc[Areas.loc[i,["Joint2"]].values,["Y"]].values[0][0],\
               "P2z": Puntos.loc[Areas.loc[i,["Joint2"]].values,["Z"]].values[0][0],\
               "P2" : Areas.loc[i,["Joint2"]].values[0],\
               "P3x": Puntos.loc[Areas.loc[i,["Joint3"]].values,["XorR"]].values[0][0],\
               "P3y": Puntos.loc[Areas.loc[i,["Joint3"]].values,["Y"]].values[0][0],\
               "P3z": Puntos.loc[Areas.loc[i,["Joint3"]].values,["Z"]].values[0][0],\
               "P3" : Areas.loc[i,["Joint3"]].values[0],\
               "P4x": Puntos.loc[Areas.loc[i,["Joint4"]].values,["XorR"]].values[0][0],\
               "P4y": Puntos.loc[Areas.loc[i,["Joint4"]].values,["Y"]].values[0][0],\
               "P4z": Puntos.loc[Areas.loc[i,["Joint4"]].values,["Z"]].values[0][0],\
               "P4" : Areas.loc[i,["Joint4"]].values[0],\
               "ID" : i}
        Puntos_Lista.append(PI_PF)
        


    Puntos_SAP=pd.DataFrame(Puntos_Lista)

    return Puntos_SAP

def DibujarDerivas(AlturasdePiso, desplazamientos, R, Deriva="X"):
    
    # Alturas de niveles (en metros)
    alturas = AlturasdePiso.copy()
    #u1,u2

    pisoanterior=[0,0]
    drifts=[0]
    drifts2=[0]
    hn=0
    for h,u in zip(alturas,desplazamientos):
        hi=h-hn
        hn=h
        unx=pisoanterior[0]
        uny=pisoanterior[1]
        drifts.append((u[0]-unx)/hi)
        drifts2.append((u[1]-uny)/hi)
        pisoanterior=[u[0],u[1]]
        print(hi)
    
    drifts=np.array(drifts)
    drifts2=np.array(drifts2)
    
    alturas =np.insert(alturas,0,0)
        
    niveles_etiquetas = [f"N+{h:.2f}" for h in alturas]

    # Buscar el máximo
    if Deriva =="X":
        max_drift = np.max(drifts)
        idx_max = np.argmax(drifts)
        altura_max = alturas[idx_max]
        nivel_max = niveles_etiquetas[idx_max]
        min_drift = np.min(drifts)
        idx_min = np.argmin(drifts)
        nivel_min = niveles_etiquetas[idx_min]
    else:
        max_drift = np.max(drifts2)
        idx_max = np.argmax(drifts2)
        altura_max = alturas[idx_max]
        nivel_max = niveles_etiquetas[idx_max]
        min_drift = np.min(drifts2)
        idx_min = np.argmin(drifts2)
        nivel_min = niveles_etiquetas[idx_min]

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(6, 8))
    fig.patch.set_facecolor('#d3d3d3')    # Fondo gris claro (fuera del gráfico)
    ax.set_facecolor('white')             # Fondo blanco (área del gráfico)
    # Graficar línea roja + puntos azules
    SentidoYY, =ax.plot(drifts2, alturas, color='blue', linewidth=1.5, label="Sentido Y")
    ax.plot(drifts2, alturas, 'bs', markersize=5)

    SentidoXX, =ax.plot(drifts, alturas, color='red', linewidth=1.5, label="Sentido X")
    ax.plot(drifts, alturas, 'rs', markersize=5)

    # Etiquetas y estilo
    ax.set_title('Maximum Story Drifts', fontsize=14, fontweight='bold', fontstyle='italic')
    ax.set_xlabel('Drift, Unitless',fontweight='bold')
    ax.set_yticks(alturas)  # Para que las líneas estén alineadas

    ax.set_yticklabels(niveles_etiquetas)

    ax.grid(True, which='both', linestyle='-', linewidth=0.5)

    # Invertir eje Y para que N+1 esté abajo
    ax.invert_xaxis()

    # Resaltar máximo con un cuadro de texto
    texto = f"Max: {max_drift:.6f}, {nivel_max}"
    ax.annotate(
       texto,
       xy=(max_drift, altura_max),
       xytext=(max_drift * 1.1, altura_max),
       bbox=dict(boxstyle="round,pad=0.3", edgecolor='red', facecolor='white'),
       fontsize=9,
       color='black',
       arrowprops=dict(arrowstyle='->', color='red', lw=1)
    )

    #Opcional: estilo visual tipo ETABS

    ax.set_xlim(left=-max_drift * 1.5, right=max_drift * 1.5)
    texto_info = f"Max: {max_drift:.6f}, {nivel_max}   Min: {min_drift:.6f}, {nivel_min}                                                                       "
    fig.text(
        0.01, -0.02,
        texto_info,
        fontsize=9,
        color='black',
        bbox=dict(facecolor='#e6e6e6', edgecolor='gray', boxstyle='round,pad=1.4')
    )
    print("Deriva: ",round(max_drift*R*0.75*100,2),"%")
    ax.legend([SentidoXX, SentidoYY],['Sentido X','Sentido Y'])
    plt.tight_layout()
    plt.show()
    
    