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

def Testcode():
    global mySapModel, ret
    
    #Initialize model
    ret = mySapModel.SetPresentUnits(14)
    # PESO PROPIO
    ret = mySapModel.LoadPatterns.Add("PP", 1, 1)
    # CARGA MUERTA
    ret = mySapModel.LoadPatterns.Add("D", 2)
    
    # CARGA VIVA
    ret = mySapModel.LoadPatterns.Add("L", 3)
    # CARGA SISMO ESTATICO X
    ret = mySapModel.LoadPatterns.Add("Ex", 5)
    ret = mySapModel.LoadPatterns.AutoSeismic.SetUserCoefficient(
        "Ex", 1, 0.05, False, 0, 0, 0.5, 1)

    # CARGA SISMO ESTATICO Y
    ret = mySapModel.LoadPatterns.Add("Ey", 5)
    ret = mySapModel.LoadPatterns.AutoSeismic.SetUserCoefficient(
        "Ey", 1, 0.05, False, 0, 0, 0.5, 1)
    
    ret = mySapObject.SapModel.LoadCases.Delete("DEAD")
    ret = mySapModel.LoadPatterns.Delete("DEAD")
    ret = mySapObject.SapModel.LoadCases.Delete("PP")
    ret = mySapModel.LoadCases.StaticLinear.SetLoads("D", 2, ["Load","Load"], ["PP","D"], [1,1])
    

    ret = mySapObject.SapModel.Func.FuncRS.SetUser(
        "SISMO NEC 15",10,[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],[1,2,3,4,5,6,7,8,9,10],0.05)
    
    ret = mySapModel.LoadCases.ResponseSpectrum.SetCase("EQx")
    ret = mySapModel.LoadCases.ResponseSpectrum.SetEccentricity("EQx", 0.05) 
    ret = mySapModel.LoadCases.ResponseSpectrum.SetLoads("EQx", 1, ["U1"], ["SISMO NEC 15"],  [1], ["Global"], [0])
    


    ret = mySapModel.LoadCases.ResponseSpectrum.SetCase("EQy")
    ret = mySapModel.LoadCases.ResponseSpectrum.SetEccentricity("EQy", 0.05)
    ret = mySapModel.LoadCases.ResponseSpectrum.SetLoads("EQy", 1, ["U2"], ["SISMO NEC 15"],  [1], ["Global"], [0])
    
def CombinaciondeCARGA():
    global mySapModel, ret
    COMBO1="1. D"
    ret = mySapModel.RespCombo.Add(COMBO1, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO1, 0, "D", 1, 1.0)

    COMBO2="2. D + L"
    ret = mySapModel.RespCombo.Add(COMBO2, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO2, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO2, 0, "L", 1, 1.0)
    
    COMBO3="3. D + 0.75L + 0.525Ex"
    ret = mySapModel.RespCombo.Add(COMBO3, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "L", 1, 0.75)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO3, 0, "Ex", 1, 0.525)

    COMBO4="4. D + 0.75L - 0.525Ex"
    ret = mySapModel.RespCombo.Add(COMBO4, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO4, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO4, 0, "L", 1, 0.75)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO4, 0, "Ex", 1, -0.525)

    COMBO5="5. D + 0.75L + 0.525Ey"
    ret = mySapModel.RespCombo.Add(COMBO5, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO5, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO5, 0, "L", 1, 0.75)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO5, 0, "Ey", 1, 0.525)
    
    COMBO6="6. D + 0.75L - 0.525Ey"
    ret = mySapModel.RespCombo.Add(COMBO6, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO6, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO6, 0, "L", 1, 0.75)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO6, 0, "Ey", 1, -0.525)
    
    COMBO7="7. D + 0.7Ex"
    ret = mySapModel.RespCombo.Add(COMBO7, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO7, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO7, 0, "Ex", 1, 0.7)
    
    COMBO8="8. D - 0.7Ex"
    ret = mySapModel.RespCombo.Add(COMBO8, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO8, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO8, 0, "Ex", 1,-0.7)
    
    COMBO9="9. D + 0.7Ey"
    ret = mySapModel.RespCombo.Add(COMBO9, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO9, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO9, 0, "Ey", 1,0.7)
    
    COMBO10="10. D - 0.7Ey"
    ret = mySapModel.RespCombo.Add(COMBO10, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO10, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO10, 0, "Ey", 1,-0.7)
    
    COMBO11="11. D + 0.75L + 0.525EQx"
    ret = mySapModel.RespCombo.Add(COMBO11, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO11, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO11, 0, "L", 1, 0.75)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO11, 0, "EQx", 1, 0.525)
    
    COMBO12="12. D + 0.75L - 0.525EQx"
    ret = mySapModel.RespCombo.Add(COMBO12, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO12, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO12, 0, "L", 1, 0.75)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO12, 0, "EQx", 1, -0.525)
    
    COMBO13="13. D + 0.75L + 0.525EQy"
    ret = mySapModel.RespCombo.Add(COMBO13, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO13, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO13, 0, "L", 1, 0.75)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO13, 0, "EQy", 1, 0.525)
    
    COMBO14="14. D + 0.75L - 0.525EQy"    
    ret = mySapModel.RespCombo.Add(COMBO14, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO14, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO14, 0, "L", 1, 0.75)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO14, 0, "EQy", 1, -0.525)

    COMBO15="15. D + 0.7EQx"
    ret = mySapModel.RespCombo.Add(COMBO15, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO15, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO15, 0, "EQx", 1,0.7)

    COMBO16="16. D - 0.7EQx"
    ret = mySapModel.RespCombo.Add(COMBO16, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO16, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO16, 0, "EQx", 1, -0.7)

    COMBO17="17. D + 0.7EQy"
    ret = mySapModel.RespCombo.Add(COMBO17, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO17, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO17, 0, "EQy", 1,0.7)

    COMBO18="18. D - 0.7EQy"
    ret = mySapModel.RespCombo.Add(COMBO18, 0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO18, 0, "D", 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(
        COMBO18, 0, "EQy", 1,-0.7)
    
    ENVOLVENTE="ENVOLVENTE"
    ret = mySapModel.RespCombo.Add(ENVOLVENTE, 1)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO1, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO2, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO3, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO4, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO5, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO6, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO7, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO8, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO9, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO10, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO11, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO12, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO13, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO14, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO15, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO16, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO17, 1, 1.0)
    ret = mySapModel.RespCombo.SetCaseList_1(ENVOLVENTE, 1, COMBO18, 1, 1.0)


    print("x")

def def_MASA():
    global mySapModel, ret
    ret = mySapModel.SourceMass.ChangeName("MSSSRC1", "MASA")
    ret = mySapModel.SourceMass.SetMassSource("MASA", False, False, True, True, 2, ["D","PP"], [1.0,1.0])

def AREAs():
    global mySapModel, ret

    ret = mySapModel.SetPresentUnits(14)
    e=[10,12,16,18,20,22,24,26,28,30,36,38,42,44,50,54,56,58,60,62,70,72,78,84,92,94,96,98]
    for i in e:
        ret= mySapObject.SapModel.PropArea.SetShell_1("M e="+str(i), 2, True, "Mam Concreto 7 MPA",0, i ,i)



#Python Running example code
initialize_helper()
attach()
#Testcode()
#CombinaciondeCARGA()
#def_MASA()

AREAs()
input("Press Enter to continue and close the model.")
# Close the program
