import customtkinter
import gestor

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("400x230")
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
        
    def funcion_buscar(self):
        ruta = customtkinter.filedialog.askdirectory(title="Elegí una carpeta")
  
        if ruta:
           self.etiqueta_ruta.configure(text=ruta, text_color="white")
        self.directorio = ruta
    
    def FOrganizar(self):
        if self.directorio == "":
            self.etiqueta_ruta.configure(text="no se determino una ruta", text_color="red")
        else:
            self.etiqueta_estado.configure(text="Procesando", text_color="white")
            gestor.OrganizacionYReporte(self.directorio)
            self.etiqueta_estado.configure(text="Completado", text_color="white")

    def FDeshacer(self):
        if self.directorio == "":
            self.etiqueta_ruta.configure(text="no se determino una ruta", text_color="red")
        else:
            self.etiqueta_estado.configure(text="Procesando", text_color="white")
            gestor.DeshacerYReporte(self.directorio)
            self.etiqueta_estado.configure(text="Completado", text_color="white")
        
def Inicio():
    app = App()
    app.mainloop()
        
