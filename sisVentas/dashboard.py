import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import total_productos, total_clientes, total_proveedores, total_ventas, obtener_datos_ventas

class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F0F4F8")
        self.crear_interfaz()

    def crear_interfaz(self):
        lbl_titulo = tk.Label(self, text="DASHBOARD", font=("Helvetica", 18, "bold"), bg="#F0F4F8", fg="#1E293B")
        lbl_titulo.pack(pady=(20, 10))

        # Contenedor de Tarjetas KPI
        frame_tarjetas = tk.Frame(self, bg="#F0F4F8")
        frame_tarjetas.pack(pady=5)

        self.crear_tarjeta(frame_tarjetas, "PRODUCTOS", str(total_productos()), "#3B82F6", 0)
        self.crear_tarjeta(frame_tarjetas, "CLIENTES", str(total_clientes()), "#10B981", 1)
        self.crear_tarjeta(frame_tarjetas, "PROVEEDORES", str(total_proveedores()), "#F97316", 2)
        self.crear_tarjeta(frame_tarjetas, "VENTAS ($)", f"${total_ventas():,}", "#8B5CF6", 3)

        # Gráfica de Ventas
        self.crear_grafica_ventas()

    def crear_tarjeta(self, parent, titulo, valor, color_bg, columna):
        card = tk.Frame(parent, bg=color_bg, width=170, height=90)
        card.grid(row=0, column=columna, padx=10, pady=5)
        card.pack_propagate(False)

        lbl_tit = tk.Label(card, text=titulo, font=("Helvetica", 9, "bold"), bg=color_bg, fg="white")
        lbl_tit.pack(pady=(12, 2))

        lbl_val = tk.Label(card, text=valor, font=("Helvetica", 16, "bold"), bg=color_bg, fg="white")
        lbl_val.pack()

    def crear_grafica_ventas(self):
        datos = obtener_datos_ventas()
        meses = [row[0] for row in datos]
        totales = [row[1] / 1000000 for row in datos]  # En millones

        fig, ax = plt.subplots(figsize=(8, 3.2), dpi=100)
        fig.patch.set_facecolor('#F0F4F8')
        ax.set_facecolor('#FFFFFF')

        ax.plot(meses, totales, marker='o', color='#3B82F6', linewidth=2.5, markersize=6)
        ax.fill_between(meses, totales, color='#3B82F6', alpha=0.15)

        ax.set_title("Rendimiento Mensual de Ventas (en Millones COP)", fontsize=11, fontweight='bold', color='#1E293B', pad=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#CBD5E1')
        ax.spines['bottom'].set_color('#CBD5E1')
        ax.tick_params(colors='#475569', labelsize=8)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=15)