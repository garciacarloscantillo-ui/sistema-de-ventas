import tkinter as tk
from tkinter import messagebox
from config import COLOR_BARRA_LATERAL, COLOR_BOTON_MENU, COLOR_FONDO
from database import crear_tablas

from dashboard import DashboardFrame
from ventas import VentasFrame
from inventario import InventarioFrame
from clientes import ClientesFrame
from proveedores import ProveedoresFrame
from cuentas_cobrar import CuentasCobrarFrame
from cuentas_pagar import CuentasPagarFrame
from reportes import ReportesAuditoriaFrame

class SistemaERP(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema ERP de Gestión")
        self.geometry("1150x680")
        self.config(bg=COLOR_FONDO)

        crear_tablas()

        self.barra_lateral = tk.Frame(self, bg=COLOR_BARRA_LATERAL, width=220)
        self.barra_lateral.pack(side="left", fill="y")

        self.contenedor_principal = tk.Frame(self, bg=COLOR_FONDO)
        self.contenedor_principal.pack(side="right", expand=True, fill="both")

        self.frames = {}
        self.inicializar_frames()
        self.crear_menu()
        self.mostrar_frame("DashboardFrame")

    def inicializar_frames(self):
        paginas = (
            DashboardFrame, VentasFrame, InventarioFrame, ClientesFrame,
            ProveedoresFrame, CuentasCobrarFrame, CuentasPagarFrame, ReportesAuditoriaFrame
        )
        for F in paginas:
            nombre = F.__name__
            frame = F(parent=self.contenedor_principal)
            self.frames[nombre] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.contenedor_principal.grid_rowconfigure(0, weight=1)
        self.contenedor_principal.grid_columnconfigure(0, weight=1)

    def crear_menu(self):
        # Lista exacta del menú desplegado en la captura
        opciones = [
            ("Dashboard", "DashboardFrame"),
            ("Ventas", "VentasFrame"),
            ("Inventario", "InventarioFrame"),
            ("Clientes", "ClientesFrame"),
            ("Proveedores", "ProveedoresFrame"),
            ("Cuentas por Cobrar", "CuentasCobrarFrame"),
            ("Cuentas por Pagar", "CuentasPagarFrame"),
            ("ReportesAuditoria", "ReportesAuditoriaFrame"),
        ]

        for text, frame_name in opciones:
            btn = tk.Button(
                self.barra_lateral,
                text=text,
                bg=COLOR_BARRA_LATERAL,
                fg="white",
                font=("Segoe UI", 11),
                bd=0,
                anchor="w",
                padx=20,
                pady=8,
                command=lambda f=frame_name: self.mostrar_frame(f)
            )
            btn.pack(fill="x")

        # Botón Cerrar Sesión
        btn_cerrar = tk.Button(
            self.barra_lateral,
            text="Cerrar Sesión",
            bg=COLOR_BARRA_LATERAL,
            fg="#EF4444",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            anchor="w",
            padx=20,
            pady=8,
            command=self.cerrar_sesion
        )
        btn_cerrar.pack(fill="x", side="bottom", pady=20)

    def mostrar_frame(self, nombre_frame):
        frame = self.frames[nombre_frame]
        
        # Ejecutar refresco de datos según el módulo
        for metodo in ["cargar_clientes", "cargar_productos", "cargar_proveedores", "cargar_cuentas", "cargar_auditoria", "crear_dashboard"]:
            if hasattr(frame, metodo):
                getattr(frame, metodo)()

        frame.tkraise()

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea salir?"):
            self.destroy()

if __name__ == "__main__":
    app = SistemaERP()
    app.mainloop()