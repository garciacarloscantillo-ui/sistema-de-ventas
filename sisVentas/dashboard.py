import tkinter as tk
from config import COLOR_FONDO
from database import total_productos, total_clientes, total_proveedores, total_ventas

class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_dashboard()

    def crear_tarjeta(self, parent, titulo, valor, color):
        card = tk.Frame(parent, bg=color, width=200, height=110)
        card.pack_propagate(False)

        tk.Label(card, text=titulo, bg=color, fg="white", font=("Segoe UI", 11, "bold")).pack(pady=(20, 5))
        tk.Label(card, text=str(valor), bg=color, fg="white", font=("Segoe UI", 22, "bold")).pack()
        return card

    def crear_dashboard(self):
        titulo = tk.Label(self, text="DASHBOARD", bg=COLOR_FONDO, font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=20)

        tarjetas = tk.Frame(self, bg=COLOR_FONDO)
        tarjetas.pack(pady=15)

        self.crear_tarjeta(tarjetas, "PRODUCTOS", total_productos(), "#2563EB").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "CLIENTES", total_clientes(), "#16A34A").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "PROVEEDORES", total_proveedores(), "#EA580C").pack(side="left", padx=10)
        self.crear_tarjeta(tarjetas, "VENTAS", total_ventas(), "#7C3AED").pack(side="left", padx=10)

        tk.Label(self, text="Bienvenido al ERP Empresarial", bg=COLOR_FONDO, font=("Segoe UI", 12)).pack(pady=30)