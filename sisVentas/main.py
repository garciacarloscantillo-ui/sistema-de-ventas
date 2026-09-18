import tkinter as tk
from database import crear_tablas, insertar_datos_prueba
from dashboard import DashboardFrame
from clientes import ClientesFrame
from inventario import InventarioFrame
from proveedores import ProveedoresFrame
from ventas import VentasFrame
from cuentas import CuentasBaseFrame
from reportes import ReportesFrame

class ERPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ERP EMPRESARIAL")
        self.geometry("1150x700")
        
        crear_tablas()
        insertar_datos_prueba()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_sidebar()

        self.area_principal = tk.Frame(self, bg="#F0F4F8")
        self.area_principal.grid(row=0, column=1, sticky="nsew")

        self.vista_actual = None
        self.mostrar_dashboard()

    def crear_sidebar(self):
        sidebar = tk.Frame(self, bg="#1E293B", width=220)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.pack_propagate(False)

        lbl_logo = tk.Label(sidebar, text="📊 ERP EMPRESARIAL", font=("Helvetica", 13, "bold"), bg="#1E293B", fg="white")
        lbl_logo.pack(pady=(20, 15))

        opciones = [
            ("Dashboard", self.mostrar_dashboard),
            ("Ventas", lambda: self.cargar_frame(VentasFrame)),
            ("Inventario", lambda: self.cargar_frame(InventarioFrame)),
            ("Clientes", lambda: self.cargar_frame(ClientesFrame)),
            ("Proveedores", lambda: self.cargar_frame(ProveedoresFrame)),
            ("Cuentas por Cobrar", lambda: self.cargar_cuentas("cobrar")),
            ("Cuentas por Pagar", lambda: self.cargar_cuentas("pagar")),
            ("Reportes / Auditoría", lambda: self.cargar_frame(ReportesFrame)),
            ("Cerrar Sesión", self.destroy)
        ]

        for texto, comando in opciones:
            btn = tk.Button(
                sidebar, text=texto, command=comando,
                font=("Helvetica", 9, "bold"), bg="#1E293B", fg="#E2E8F0",
                activebackground="#334155", activeforeground="white",
                bd=0, anchor="w", padx=20, cursor="hand2"
            )
            btn.pack(fill="x", pady=3)

    def limpiar_area(self):
        if self.vista_actual is not None:
            self.vista_actual.destroy()

    def mostrar_dashboard(self):
        self.limpiar_area()
        self.vista_actual = DashboardFrame(self.area_principal)
        self.vista_actual.pack(fill="both", expand=True)

    def cargar_frame(self, ClaseFrame):
        self.limpiar_area()
        self.vista_actual = ClaseFrame(self.area_principal)
        self.vista_actual.pack(fill="both", expand=True)

    def cargar_cuentas(self, tipo):
        self.limpiar_area()
        self.vista_actual = CuentasBaseFrame(self.area_principal, tipo_cuenta=tipo)
        self.vista_actual.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = ERPApp()
    app.mainloop()