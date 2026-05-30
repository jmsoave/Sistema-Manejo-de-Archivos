import customtkinter
import gestor
import threading

class MyScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title, height=80)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1, minsize=0)
        self.values = values
        self.labels = []

        for i, value in enumerate(self.values):
            etiquetaReporte = customtkinter.CTkLabel(self, text=value)
            etiquetaReporte.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w", columnspan=2)
            self.labels.append(etiquetaReporte)

            

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("400x500")
        self.title("Organizador de Archivos")
        self.resizable(False, False)     
        customtkinter.set_appearance_mode("Dark")
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.directorio = ""
        
        self.botonOrganizar = customtkinter.CTkButton(self, text="Organizar", command=self.FOrganizar)
        self.botonOrganizar.grid(row=0, column=0, padx=20, pady=(30,10), columnspan=2, sticky="w")
        
        self.botonDeshacer = customtkinter.CTkButton(self, text="Deshacer", command=self.FDeshacer)
        self.botonDeshacer.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky="w")

        self.botonCerrar = customtkinter.CTkButton(self, text="Cerrar", fg_color="#FF3C00", hover_color="#ffffff", command=self.destroy)
        self.botonCerrar.grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky="w")
        
        self.etiqueta_ruta = customtkinter.CTkLabel(self, text="Ninguna ruta elegida", text_color="gray",fg_color="#333333", corner_radius=8, padx=10, pady=0)
        self.etiqueta_ruta.grid(row=2, column=2, pady=10)
        self.boton_buscar = customtkinter.CTkButton(self, text="Buscar Carpeta", command= self.funcion_buscar)
        self.boton_buscar.grid(row=0, column=2, padx=30, pady=(30,10), rowspan=2, sticky="ns")
        
        self.etiqueta_estado = customtkinter.CTkLabel(self, text="Estado Pendiente", text_color="gray",fg_color="#333333", corner_radius=8, padx=10, pady=0)
        self.etiqueta_estado.grid(row=3, column=2, pady=5)
        
    def AnadirErrores(self, lista_error):
        if hasattr(self, 'scrollable_frame'):
            self.scrollable_frame.destroy()
        self.scrollable_frame = MyScrollableFrame(self, title="Errores", values=lista_error)
        self.scrollable_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")
        
    def funcion_buscar(self):
        ruta = customtkinter.filedialog.askdirectory(title="Elegí una carpeta")
  
        if ruta:
           self.etiqueta_ruta.configure(text=ruta, text_color="white")
           self.directorio = ruta
    
    def FOrganizar(self):
        self.botonOrganizar.configure(state="disabled")
        self.botonDeshacer.configure(state="disabled")
        if self.directorio == "":
            self.etiqueta_ruta.configure(text="no se determino una ruta", text_color="red")
            self.botonOrganizar.configure(state="normal")
            self.botonDeshacer.configure(state="normal")
        else:
            self.etiqueta_estado.configure(text="Procesando...", text_color="white")
            hilo = threading.Thread(target=self.OrganizarHilo, daemon=True)
            hilo.start()
        
    def OrganizarHilo(self):
        lista_error = gestor.OrganizacionYReporte(self.directorio)
        self.after(0, lambda err=lista_error: self._finalizar(err))

    def FDeshacer(self):
        self.botonOrganizar.configure(state="disabled")
        self.botonDeshacer.configure(state="disabled")
        if self.directorio == "":
            self.etiqueta_ruta.configure(text="no se determino una ruta", text_color="red") 
            self.botonOrganizar.configure(state="normal")
            self.botonDeshacer.configure(state="normal")
        else:
            self.etiqueta_estado.configure(text="Procesando...", text_color="white")
            hilo = threading.Thread(target=self.DeshacerHilo, daemon=True)
            hilo.start()
            
    def DeshacerHilo(self):
        lista_error = gestor.DeshacerYReporte(self.directorio)
        self.after(0, lambda err=lista_error: self._finalizar(err))

    def _finalizar(self, lista_error):
        self.AnadirErrores(lista_error)
        self.etiqueta_estado.configure(text="Completado", text_color="white")
        self.botonOrganizar.configure(state="normal")
        self.botonDeshacer.configure(state="normal")
        
        
        
def Inicio():
    app = App()
    app.mainloop()
        
