# programa generador de inputs
# a partir de coordenadas xyz de un scan

# importar librerias necesarias
import os
import sys
import re # expresiones regulares
import tkinter as tk # ventanas
from pathlib import Path # manejo de directorios
from tkinter import filedialog



def sel_files():  # Seleccionar archivos xyz usando una ventana
    root=tk.Tk() # crear ventana
    root.title("Seleccionar archivos") # titulo de la ventana
    root.withdraw() # cerrar ventana tkinter
    filepath=filedialog.askopenfilenames( # abrir multiples files
        multiple=(True),
        filetypes=[("ORCA xyz files", ".xyz")] # lista que contenga una tupla
        )
    if filepath: # corroborar que se selecciono algo
        print("Archivos seleccionados:")
        print(*[item for item in filepath],sep='\n')
        return(filepath) # devolver archivos seleccionados
    else:
        tk.messagebox.showinfo(title="Error",message="Ningun archivo seleccionado")
        root.destroy()
        exit()
    root.mainloop() # necesario para mantener la ventana abierta

def write_new_method():
    root=tk.Tk()
    root.withdraw()
    ventana = tk.Toplevel(root)
    ventana.title("Introduce el nuevo método de cálculo")
    ventana.grab_set() 
    ventana.geometry()
    # Instrucción
    etiqueta = tk.Label(ventana, text=("Puede contener saltos de línea, espacios y tabulaciones:"))
    etiqueta.pack(pady=10)
    # Campo de texto multilinea
    cuadro_texto = tk.Text(ventana, wrap="word", height=10)
    cuadro_texto.pack(expand=True, fill="both", padx=10)

    resultado = {"texto": None}
    def confirmar():
        resultado["texto"] = cuadro_texto.get("1.0", tk.END).rstrip()  # Eliminar salto de línea final
        ventana.destroy()
    # Botón aceptar
    boton_aceptar = tk.Button(ventana, text="Aceptar", command=confirmar)
    boton_aceptar.pack(pady=10)
    root.wait_window(ventana)
    return resultado["texto"]

def gen_inp(files):
# Seccion 1 de la funcion: busqueda de las coordenadas xyz 
    n=len(files) # cantidad de files seleccionados
    for i in range(n): # iterar sobre la cantidad de files
        with open(files[i],"r+") as xyz: # abrir cada file y leer
            data=xyz.readlines() # leer el file numero i
            # print(data)
            pattern=re.compile(r"\s+[A-Za-z]{1,2}\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\n?") # expresion regular para los atomos
            print("Coordenadas extraidas del archivo xyz",files[0],"(conteo en formato ORCA):",'\n')
            coord=[] # inicializacion de lista con coordenadas xyz de todos los atomos
            for n, data in enumerate(data): # extraer cada linea de xyz mediante iteracion sobre el contenido
                if pattern.fullmatch(data): # probar si la expresion regular esta
                    xyz=data.strip()# almacenar en variable xyz
                    n= n - 2 # coordenadas en formato ORCA. Comienzan desde 0
                    print(n,'\t',xyz) # imprimir coordenadas
                    xyz=xyz+'\n' # añadir nueva linea para adjuntar
                    coord.append(xyz) # adjuntar xyz a las coordenadas nuevas
                    
# Seccion 2: pedirle al usuario crear un nuevo file
            root = tk.Tk() # raiz de tkinter
            root.withdraw()  # Oculta la ventana principal
            dir = os.path.dirname(files[i])    # directorio de trabajo
            nom=os.path.basename(files[i])
            title="Generando nuevo archivo a partir de "+ nom
            body="Introduce el nombre del nuevo archivo en "+ dir +" (con extension):" 
            newFile = tk.simpledialog.askstring(title, body )
            # Comprobar si se introdujo algo
            if newFile :
                print(f"Nombre introducido: {newFile}")
            else:
               tk.messagebox.showinfo(title="Error",message="No se introdujo un nombre")
               break
            newDir = os.path.join(dir, f"{newFile}") # crear el nuevo path del archivo
            with open(newDir, "w+") as newF: # crear una archivo editable nuevo con el nombre que le dimos
                newMeth=write_new_method() # llamar a la funcion que crea el nuevo metodo
                newF.writelines(newMeth) # insertar el metodo de calculo introducido
                newF.writelines("\n")
                newF.writelines("\n")
                newF.writelines("*xyz 0 1\n") # insertar tipo de coord, carga y multiplicidad
                newF.writelines([item for item in coord]) # insertar todas las xyz
                newF.writelines("*") # insertar fin de coordenadas orca
                msg="Archivo generado en "+newDir
            tk.messagebox.showinfo(title="Fin del programa",message=(msg))

files=sel_files() # crear una lista con los files
gen_inp(files) # abrir cada file, extraer xyz y crear un nuevo input
