import tkinter as tk
from tkinter import filedialog, messagebox
import oficina as of
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import uuid

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
    global archivo_rut, archivo
    seleccion = lista.curselection()  # devuelve una tupla con los índices seleccionados
    if seleccion:
        archivo_rut = lista.get(seleccion[0])  # obtener el texto (ruta) del primer índice
        messagebox.showinfo("Archivo seleccionado", f"Ruta:\n{archivo_rut}")
    else:
        messagebox.showwarning("Atención", "No has seleccionado ningún archivo.")

    archivo=of.Leer_Puntos(archivo_rut)
    archivo.set_index("Joint")
    
    

def graficar_excel():
    print(archivo)
    ax.scatter(archivo["XorR"],archivo["Y"])
    ax.set_xlabel("XorR")
    ax.set_ylabel("Y")
    Zunicos=archivo["Z"].unique()
    print("Z unicos diferenciados: ",Zunicos)
    canvas.draw()
    
def Union_Lineas():
    n=boxN.get()
    Z=boxZ.get()
    n=int(n)
    Z=float(Z)
    Lineas=[]
    archivoexp=archivo.set_index("Joint")
    dfpZ0=archivoexp[archivoexp["Z"]<=Z]
    dfpZ1=archivoexp[archivoexp["Z"]>=Z]

    dfpZ0.sort_values(by=["XorR","Y","Z"],inplace=True)
    dfpZ1.sort_values(by=["XorR","Y","Z"],inplace=True)
    
    
    for i,j in zip(dfpZ0.index,dfpZ1.index):
        Lineas.append({"ID": n, "PI": i,"PF":j})
        n=n+1


    borrar=pd.DataFrame(Lineas)
    borrar["isC"]=borrar.apply(lambda x: "No",axis=1)
    borrar["GUID"]=borrar.apply(lambda x: uuid.uuid4(),axis=1)

    borrar.to_csv("Archivos_Salida\Frames_Verticales.csv",sep="\t",index=False)



# Ventana principal
root = tk.Tk()

root.title("Frames Verticales")
root.geometry("1000x700")

fig, ax = plt.subplots()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=1, row=1,sticky="nsew")



root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=4)
root.grid_columnconfigure(2, weight=1)

# Botones
btn_archivos = tk.Button(root, text="Seleccionar Excel", command=seleccionar_archivos)
btn_archivos.grid(column=0 ,row=0)

btn_graficar = tk.Button(root, text="Graficar", command=graficar_excel)

btn_graficar.grid(column=0 ,row=1)

btn_get = tk.Button(root, text="Obtener archivo seleccionado", command=obtener_seleccion)
btn_get.grid(column=2, row=0)

btn_crear_csv = tk.Button(root, text= "ExportarCsV", command=Union_Lineas)
btn_crear_csv.grid(column=2, row=1)


# Datos

boxZ= tk.Entry(root)
boxN= tk.Entry(root)

boxZ.grid(column=0, row=2)
boxN.grid(column=1, row=2)
boxZ.insert(0,"Z diferencial ...")
boxN.insert(0,"N inicial ...")

lista = tk.Listbox(root)

lista.grid(column=1 ,row=0,sticky="nsew")

root.mainloop()
