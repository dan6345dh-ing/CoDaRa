import os
import sys
import comtypes.client
import numpy as np

# Initialize global variables
def VariablesIniciales():
    myHelper = None
    myEtabsObject = None
    myEtabsModel = None
    ret = 0
    program_id="CSI.ETABS.API.ETABSObject"
    program_path=r"C:\Program Files\Computers and Structures\ETABS 22\ETABS.exe" 
    return myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path

def initialize_helper(myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path):
    #Initialize the API helper object.        

    try:            
        #create API helper object        
        myHelper = comtypes.client.CreateObject('ETABSv1.Helper')
        myHelper = myHelper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    except Exception as e:
        print(f"Error: Cannot create an instance of the Helper object: {e}")

    return myHelper


def attach(myHelper,myEtabsModel,myEtabsObject,ret,program_id,program_path):
    #Attach to an active instance of the program.

    if not myHelper:
        raise RuntimeError("Helper is not initialized. Cannot attach to an instance.")

    try:
        # Get the active application object
        myEtabsObject = myHelper.GetObject(program_id)
        # Get a reference to cSapModel
        myEtabsModel = myEtabsObject.SapModel
        return myEtabsModel
    except Exception as e:
        raise RuntimeError(f"Error: Failed to attach to an active instance: {e}")

    

#-----------------------------------------------------#
#-----------------------------------------------------#
#-----------------------------------------------------#
#-----------------------------------------------------#

