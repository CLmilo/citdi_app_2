import os, sys
import threading
from tkinter import PhotoImage
import customtkinter as ctk
import zipfile
import tempfile
import shutil
import ctypes
from tkinter import messagebox as MessageBox
import subprocess


if not ctypes.windll.shell32.IsUserAnAdmin():
    # Si el usuario no es administrador, solicita permisos elevados y reinicia el programa con permisos de administrador
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
else:
    root = ctk.CTk()
    root.geometry("800x500")
    root.resizable(0,0)
    root.title("Installer")

    fontTITULO = ctk.CTkFont(family='FRanklin Gothic Book',size=100, weight="bold")
    fontBARRA = ('FRanklin Gothic Book',20)
    fontTEXTcoll = ctk.CTkFont(family='FRanklin Gothic Book',size=15)

    ctk.set_appearance_mode("light")

    root.grid_rowconfigure(0, weight=10)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container1 = ctk.CTkFrame(root)
    container1.grid(row=0, column=0, sticky='nsew', padx=20, pady=(20,10))
    container1.grid_rowconfigure(0, weight=1)
    container1.grid_columnconfigure(0, weight=1)
    container1.grid_columnconfigure(1, weight=1)

    def resolver_ruta(ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

    nombre_archivo_portada = resolver_ruta("CITDI_LOGO_SINFONDO.png")
    imagen = PhotoImage(file=nombre_archivo_portada)
    imagen = imagen.zoom(4, 4)
    new_imagen = imagen.subsample(15, 15)

    ctk.CTkLabel(container1, image=new_imagen, text="").grid(row=0,column=0, padx=(10), pady=(10,10))

    container3 = ctk.CTkFrame(container1)
    container3.grid(row=0, column=1, sticky='nsew', padx=10, pady=(10))
    container3.grid_rowconfigure(0, weight=1)
    container3.grid_rowconfigure(1, weight=1)
    container3.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(container3, text="Welcome to the installation wizard", font= fontBARRA).grid(row=0, column=0, padx=10, pady=10, sticky='sw')
    ctk.CTkLabel(container3, text="Click the next button to continue with the installation", font= fontTEXTcoll).grid(row=1, column=0, padx=10, pady=10, sticky='nw')

    container2 = ctk.CTkFrame(root)
    container2.grid(row=1, column=0, sticky='nsew', padx=20, pady=(0, 20))
    container2.grid_rowconfigure(0, weight=1)
    container2.grid_columnconfigure(0, weight=10)
    container2.grid_columnconfigure(1, weight=1)
    container2.grid_columnconfigure(2, weight=1)

    progressbar = ctk.CTkProgressBar(container2)
    progressbar.grid(row=0, column=0, sticky = 'nsew', padx=40, pady=25)

    confirmacion = 1

    ctk.CTkButton(container2, text="Install", command=lambda:Descomprimir_Carpeta(), width=80, height=10).grid(row=0, column=1, sticky='nsew', padx=(10, 0), pady=10)
    ctk.CTkButton(container2, text="Cancel", command=lambda:[Cancelar(), root.destroy()], width=80, height=10).grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

    ruta_carpeta_temporal = tempfile.gettempdir()
    ruta_archivo_zip = resolver_ruta("kallpa_app.zip")
    ruta_program_files = os.environ.get('ProgramFiles', 'C:\\Archivos de programa')

    def Cancelar():
        global confirmacion
        confirmacion == 0

    def Instalar():
        global progressbar, ruta_carpeta_temporal
        ruta_archivo_zip = resolver_ruta("kallpa_app.zip")
        ruta_program_files = os.environ.get('ProgramFiles', 'C:\\Archivos de programa')
        
        shutil.rmtree(ruta_program_files+"\kallpa_app")

        with zipfile.ZipFile(ruta_archivo_zip, 'r') as archivo_zip:
                archivo_zip.extractall(ruta_carpeta_temporal)
        shutil.move(ruta_carpeta_temporal+"\kallpa_app", ruta_program_files)
        script_file = resolver_ruta("script.exe")
        try:
            if confirmacion == 1:
                result = subprocess.run(script_file)
                progressbar.stop()
                MessageBox.showinfo(title="Alert", message="the installation has finished successfully")
            else:
                shutil.rmtree(ruta_program_files+"\kallpa_app")
        except Exception as e:
            progressbar.stop()
            MessageBox.showinfo(title="Alert", message=e)

    def Descomprimir_Carpeta():
        global progressbar, ruta_carpeta_temporal
        try:
            shutil.move(ruta_carpeta_temporal+"\kallpa_app", ruta_program_files)
            progressbar.start()
            threading.Thread(target=Instalar).start()

        except:
            respuesta = MessageBox.askyesno(message="Ya existe una instalación anterior, ¿desea eliminarla y sobreescribir?", title="Alerta")
            if respuesta == True:
                progressbar.start()
                threading.Thread(target=Instalar).start()
            
        print(ruta_program_files, ruta_carpeta_temporal, ruta_program_files)
    
    root.mainloop()



