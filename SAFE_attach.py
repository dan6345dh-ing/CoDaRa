import numpy as np
import Libreria_SAFE as SAFE

myHelper,mySafeModel,mySafeObject,ret,program_id,program_path=SAFE.VariablesIniciales()
myHelper=SAFE.initialize_helper(myHelper,mySafeModel,mySafeObject,ret,program_id,program_path)
mySafeModel=SAFE.attach(myHelper,mySafeModel,mySafeObject,ret,program_id,program_path)

Caso=2

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

#ret = mySafeModel.SetPresentUnits_2(forceUnits=3, lengthUnits=4, temperatureUnits=2)
ret = mySafeModel.SetPresentUnits(6)
if Caso==1:
    fc=float(input("f'c MPA: ")) #MPA 
    MaterialName="HA "+ str(fc) + " MPA"
    ret = mySafeModel.PropMaterial.ChangeName("Concrete", MaterialName)

    Ec=4.7*np.sqrt(fc) #fc MPA # Ec GPA
    print(fc)
    print(Ec)

    Ec=Ec*1000*1000 #GPA -> kPA 

    fc=fc*1000 #MPA -> kN/m2

    Peso=24 #kn/m3

    print(fc)

    ret = mySafeModel.PropMaterial.SetMaterial(MaterialName,2)
    ret = mySafeModel.PropMaterial.SetWeightAndMass(MaterialName, 1, Peso)
    ret = mySafeModel.PropMaterial.SetMPIsotropic(MaterialName, Ec, 0.2, 0.0000055)
    ret = mySafeModel.PropMaterial.SetOConcrete(MaterialName,
                                                  fc, False, 0, 2, 4 # Concreto Ligero (Falso), factor reduccion cortante (0), #Modelo Mander 2, #Concreto
                                                  , 0.004, 0.005)


if Caso==2: #Combinaciones de carga
    


    # PESO PROPIO


    # CARGA VIVA
    ret = mySafeModel.LoadPatterns.Add("L", 3)
    # CARGA SISMO ESTATICO X
    ret = mySafeModel.LoadPatterns.Add("Ex(1/3)", 5)

    # CARGA SISMO ESTATICO Y
    ret = mySafeModel.LoadPatterns.Add("Ey(1/3)", 5)


    Viento=0
    
    Viento=int(input("Existe Carga de Viento (Si(1)/No(0)): "))
    if Viento==1:
        # CARGA VIENTO ROOF
        ret = mySafeModel.LoadPatterns.Add("W", 6)

    Granizo=0
    Granizo=int(input("Existe Carga de Granizo (Si(1)/No(0)): "))
    if Granizo==1:
        # CARGA GRANIZO
        ret = mySafeModel.LoadPatterns.Add("S", 7)


    COMBO1="1) 1.4 D"
    ret = mySafeModel.RespCombo.Add(COMBO1, 0)
    ret = mySafeModel.RespCombo.SetCaseList_1(
        COMBO1, 0, "D", 1, 1.4)

    COMBO2="2) 1.2 D + 1.6 L "
    ret = mySafeModel.RespCombo.Add(COMBO2, 0)
    ret = mySafeModel.RespCombo.SetCaseList_1(
        COMBO2, 0, "D", 1, 1.2)
    ret = mySafeModel.RespCombo.SetCaseList_1(
        COMBO2, 0, "L", 1, 1.6)
    ret = mySafeModel.RespCombo.SetCaseList_1(
        COMBO2, 0, "Lr", 1, 0.5)

    COMBO3="3) 1.2 D + L"
    ret = mySafeModel.RespCombo.Add(COMBO3, 0)
    ret = mySafeModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "D" , 1, 1.2)
    ret = mySafeModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "Lr", 1, 1.6)
    ret = mySafeModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "L" , 1, 1.0)

    if Viento==1:
        COMBO4="4) 1.2 D + W + L"
        ret = mySafeModel.RespCombo.Add(COMBO4, 0)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO4, 0, "D" , 1, 1.2)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO4, 0, "Lr", 1, 0.5)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO4, 0, "L" , 1, 1.0)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO4, 0, "W" , 1, 1.0)
    
    SismosListas=["+ Ex","- Ex","+ Ey","- Ey","+ EQx","- EQx","+ EQy","- EQy"]
    SismosNombre=["Ex(1/3)","Ex(1/3)","Ey(1/3)","Ey(1/3)","EQx","EQx","EQy","EQy"]
    SismoFactores=[1.0,-1.0,1.0,-1.0,1.0,-1.0,1.0,-1.0]
    for E,F,N in zip(SismosListas,SismoFactores,SismosNombre):
        if Granizo==1:
            COMBO5="5) 1.2 D "+E+" + L + 0.2 S"
            ret = mySafeModel.RespCombo.Add(COMBO5, 0)
            ret = mySafeModel.RespCombo.SetCaseList_1(
                COMBO5, 0, "S", 1, 0.2)
        else:
            COMBO5="5) 1.2 D "+E+" + L"
            ret = mySafeModel.RespCombo.Add(COMBO5, 0)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO5, 0, "D", 1, 1.2)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO5, 0, N, 1, F)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO5, 0, "L", 1, 1.0)
      

    if Viento==1:
        COMBO6="6) 0.9 D + W"
        ret = mySafeModel.RespCombo.Add(COMBO6, 0)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO6, 0, "D", 1, 0.9)  
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO6, 0, "W", 1, 1.0)  

    for E,F,N in zip(SismosListas,SismoFactores,SismosNombre):
        COMBO7="7) 0.9 D "+E
        ret = mySafeModel.RespCombo.Add(COMBO7, 0)
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO7, 0, "D", 1, 0.9)  
        ret = mySafeModel.RespCombo.SetCaseList_1(
            COMBO7, 0, N, 1, F) 
