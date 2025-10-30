import numpy as np
import Libreria_SAFE as SAFE

myHelper,mySafeModel,mySafeObject,ret,program_id,program_path=SAFE.VariablesIniciales()
myHelper=SAFE.initialize_helper(myHelper,mySafeModel,mySafeObject,ret,program_id,program_path)
mySafeModel=SAFE.attach(myHelper,mySafeModel,mySafeObject,ret,program_id,program_path)

Caso=1

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
