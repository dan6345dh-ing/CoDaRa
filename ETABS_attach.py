import numpy as np
import Libreria_ETABS as ETB

myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path=ETB.VariablesIniciales()
myHelper=ETB.initialize_helper(myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path)
myEtabsModel=ETB.attach(myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path)

Caso=4

# FUERZA
#lb(1),kip(2),N(3),kN(4),kgf(5),tonf(6)
# LONGITUD
#inch(1),ft(2),micron(3),mm(4),cm(5),m(6)
# TEMPERATURA
#Farenheid(1),Celsius(2)
# MAT TIPO
#ACERO(1),CONCRETO(2),REBAR(6),MASONRY(8)

#MPA -> N/mm2
# PA -> N/m2


# KPA -> kN/m2

#ret = myEtabsModel.SetPresentUnits_2(forceUnits=3, lengthUnits=4, temperatureUnits=2)
ret = myEtabsModel.SetPresentUnits(6)
if Caso==1:
    fc=float(input("f'c MPA: ")) #MPA 
    MaterialName="HA "+ str(fc) + " MPA"
    ret = myEtabsModel.PropMaterial.ChangeName("Concrete", MaterialName)

    Ec=4.7*np.sqrt(fc) #fc MPA # Ec GPA
    print(fc)
    print(Ec)

    Ec=Ec*1000*1000 #GPA -> kPA 

    fc=fc*1000 #MPA -> kN/m2

    Peso=24 #kn/m3

    print(fc)

    ret = myEtabsModel.PropMaterial.SetMaterial(MaterialName,2)
    ret = myEtabsModel.PropMaterial.SetWeightAndMass(MaterialName, 1, Peso)
    ret = myEtabsModel.PropMaterial.SetMPIsotropic(MaterialName, Ec, 0.2, 0.0000055)
    ret = myEtabsModel.PropMaterial.SetOConcrete(MaterialName,
                                                  fc, False, 0, 2, 4 # Concreto Ligero (Falso), factor reduccion cortante (0), #Modelo Mander 2, #Concreto
                                                  , 0.004, 0.005)


if Caso==2:
    
    input("Agrege Manualmente el Response Espectrum de NEC 15: \nSISMO NEC 15")


    # PESO PROPIO

    ret = myEtabsModel.LoadPatterns.ChangeName("DEAD", "PP")
    ret = myEtabsModel.LoadPatterns.ChangeName("Live", "L")
    ret = myEtabsModel.LoadCases.ChangeName("Live", "L")
    # CARGA MUERTA
    ret = myEtabsModel.LoadPatterns.Add("D", 2)

    # CARGA VIVA
    ret = myEtabsModel.LoadPatterns.Add("L", 3)
    # CARGA SISMO ESTATICO X
    ret = myEtabsModel.LoadPatterns.Add("Ex", 5)
    #ret = myEtabsModel.LoadCases.StaticLinear.SetCase("EQx")
    # CARGA SISMO ESTATICO Y
    ret = myEtabsModel.LoadPatterns.Add("Ey", 5)
    #ret = myEtabsModel.LoadCases.StaticLinear.SetCase("EQy")
    # CARGA LIVE ROOF
    ret = myEtabsModel.LoadPatterns.Add("Lr", 11)
    ret = myEtabsModel.LoadCases.ResponseSpectrum.SetCase("EQx")
    ret = myEtabsModel.LoadCases.ResponseSpectrum.SetLoads("EQx",1,["U1"],["SISMO NEC 15"],[9.81],["Global"],[0])
    ret = myEtabsModel.LoadCases.ResponseSpectrum.SetCase("EQy")
    ret = myEtabsModel.LoadCases.ResponseSpectrum.SetLoads("EQy",1,["U2"],["SISMO NEC 15"],[9.81],["Global"],[0])
    Viento=0
    Viento=int(input("Existe Carga de Viento (Si(1)/No(0)): "))
    if Viento==1:
        # CARGA VIENTO ROOF
        ret = myEtabsModel.LoadPatterns.Add("W", 6)

    Granizo=0
    Granizo=int(input("Existe Carga de Granizo (Si(1)/No(0)): "))
    if Granizo==1:
        # CARGA GRANIZO
        ret = myEtabsModel.LoadPatterns.Add("S", 7)


    ret = myEtabsModel.LoadCases.Delete("Dead")
    ret = myEtabsModel.LoadCases.StaticLinear.SetLoads("D", 2, ["Load","Load"], ["PP","D"], [1,1])

    COMBO1="1) 1.4 D"
    ret = myEtabsModel.RespCombo.Add(COMBO1, 0)
    ret = myEtabsModel.RespCombo.SetCaseList_1(
        COMBO1, 0, "D", 1, 1.4)

    COMBO2="2) 1.2 D + 1.6 L + 0.5 Lr"
    ret = myEtabsModel.RespCombo.Add(COMBO2, 0)
    ret = myEtabsModel.RespCombo.SetCaseList_1(
        COMBO2, 0, "D", 1, 1.2)
    ret = myEtabsModel.RespCombo.SetCaseList_1(
        COMBO2, 0, "L", 1, 1.6)
    ret = myEtabsModel.RespCombo.SetCaseList_1(
        COMBO2, 0, "Lr", 1, 0.5)

    COMBO3="3) 1.2 D + 1.6 Lr + L"
    ret = myEtabsModel.RespCombo.Add(COMBO3, 0)
    ret = myEtabsModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "D" , 1, 1.2)
    ret = myEtabsModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "Lr", 1, 1.6)
    ret = myEtabsModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "L" , 1, 1.0)

    if Viento==1:
        COMBO4="4) 1.2 D + W + L + 0.5 Lr"
        ret = myEtabsModel.RespCombo.Add(COMBO4, 0)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO4, 0, "D" , 1, 1.2)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO4, 0, "Lr", 1, 0.5)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO4, 0, "L" , 1, 1.0)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO4, 0, "W" , 1, 1.0)
    
    SismosListas=["+ Ex","- Ex","+ Ey","- Ey","+ EQx","- EQx","+ EQy","- EQy"]
    SismosNombre=["Ex","Ex","Ey","Ey","EQx","EQx","EQy","EQy"]
    SismoFactores=[1.0,-1.0,1.0,-1.0,1.0,-1.0,1.0,-1.0]
    for E,F,N in zip(SismosListas,SismoFactores,SismosNombre):
        if Granizo==1:
            COMBO5="5) 1.2 D "+E+" + L + 0.2 S"
            ret = myEtabsModel.RespCombo.Add(COMBO5, 0)
            ret = myEtabsModel.RespCombo.SetCaseList_1(
                COMBO5, 0, "S", 1, 0.2)
        else:
            COMBO5="5) 1.2 D "+E+" + L"
            ret = myEtabsModel.RespCombo.Add(COMBO5, 0)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO5, 0, "D", 1, 1.2)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO5, 0, N, 1, F)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO5, 0, "L", 1, 1.0)
      

    if Viento==1:
        COMBO6="6) 0.9 D + W"
        ret = myEtabsModel.RespCombo.Add(COMBO6, 0)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO6, 0, "D", 1, 0.9)  
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO6, 0, "W", 1, 1.0)  

    for E,F,N in zip(SismosListas,SismoFactores,SismosNombre):
        COMBO7="7) 0.9 D "+E
        ret = myEtabsModel.RespCombo.Add(COMBO7, 0)
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO7, 0, "D", 1, 0.9)  
        ret = myEtabsModel.RespCombo.SetCaseList_1(
            COMBO7, 0, N, 1, F) 

if Caso==3: #Agregar Elementos de Dimensiones Comunes (HA)
    import itertools
    ret = myEtabsModel.PropMaterial.AddMaterial("FY 4200", 6, "United States", "ASTM A706", "Grade 60","FY 4200")

    fc=float(input("f'c MPA: ")) #MPA 
    MaterialName="HA "+ str(fc) + " MPA"
    #0.8 col 0.5 vig
    #          AXIAL COR2 COR3 TOR  M2  M3    MASS  w
    ReduccionCol=[1,    1,  1,  1,  0.8,0.8,    1,  1]
    ReduccionVig=[1,    1,  1,  1,  1,  0.5,    1,  1]
    

    ColumnasDimension=   [0.30,0.35,0.40]
    VigasDimension=   [0.25,0.30,0.35,0.40,0.45]
    for Base,Altura in itertools.combinations_with_replacement(ColumnasDimension,2):
        
        NombreCol="COL H.A "+str(Base)+"x"+str(Altura)
        ret = myEtabsModel.PropFrame.SetRectangle(NombreCol, MaterialName, Base, Altura)
        #0.8 col 0.5 vig
        #          AXIAL COR2 COR3 TOR  M2  M3    MASS  2

        ret = myEtabsModel.PropFrame.SetModifiers(NombreCol,ReduccionCol)

    for Base,Altura in itertools.combinations_with_replacement(VigasDimension,2):
        NombreVig="Vig H.A "+str(Base)+"x"+str(Altura)
        ret = myEtabsModel.PropFrame.SetRectangle(NombreVig, MaterialName, Altura, Base)

        ret = myEtabsModel.PropFrame.SetModifiers(NombreVig,ReduccionVig)
        aux=[]
        
        print(Base, "  -   ",Altura)

        recubrimiento = 4.5 #cm
        bw=Base*1000 #mm
        d=(Altura*1000-recubrimiento*10)
        AsMin=np.max([1.4/420*bw*d,
                     ((fc)**0.5)/(4*420)*bw*d])
        
        recubrimiento=recubrimiento/100
        AsMin=AsMin/(1000**2)
        ret = myEtabsModel.PropFrame.SetRebarBeam(NombreVig, "FY 4200", "FY 4200", recubrimiento, recubrimiento, AsMin, AsMin, AsMin, AsMin)

if Caso==4: #Crear Areas
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.spatial import cKDTree
    import itertools
        
    
    
    i=''
    X=0
    Y=0
    Coord=[]
    i=input("\nSeleccion (1 Terminar)")
    while i=='':
        X=0
        Puntos,_,_=ETB.obtenerseleccion(myEtabsModel, myEtabsObject, ret)
        for j in Puntos:
            Coord.append([X,Y,0,int(j)])
            X=X+1

        Y=Y+1
        i=input("\nSeleccion (1 Terminar)")

 
    df=pd.DataFrame(Coord,columns=["XorR","Y","Z","Joint"])
    df.sort_values(by=["Y","XorR"],inplace=True)
    df.reset_index(drop=True, inplace=True)  
    print(df)

    ids = df['Joint'].astype(str)  # ID de cada punto
    X = df['XorR'].values
    Y = df['Y'].values

    Nx=len(np.unique(df['XorR'].values))
    Ny=len(np.unique(df['Y'].values))

    elementos=[]
    for j in range(Ny-1):  # filas
        for i in range(Nx-1):  # columnas
            n1 = j * Nx + i + 1
            n2 = j * Nx + i + 2
            n3 = (j + 1) * Nx + i + 2
            n4 = (j + 1) * Nx + i + 1

            print(n1,n2,n3,n4)
            elementos.append([ids[n1-1], ids[n2-1], ids[n3-1], ids[n4-1]])
            print([ids[n1-1], ids[n2-1], ids[n3-1], ids[n4-1]])
    
            
    plt.show()
    for idx, elem in enumerate(elementos, start=1):
        #print(f"Elemento {idx}: {elem}")
        print("-------------")
        Nombre="Techo_"+str(idx+1)
        ID=[]
        for i in elem:
            ID.append(str(int(float(i))))
        print("-------------")
        print(ID)
        ret = myEtabsModel.AreaObj.AddByPoint(int(len(elem)),ID ,Nombre)
       
    ret = myEtabsModel.View.RefreshView(0, False)
    

    Mallas=pd.DataFrame(elementos,columns=["P1","P2","P3","P4"])
    print(Mallas)
    
