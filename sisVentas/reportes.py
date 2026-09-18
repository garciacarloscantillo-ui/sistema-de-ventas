import tkinter as tk
from tkinter import ttk
from config import COLOR_FONDO
from database import conectar

class ReportesAuditoriaFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_interfaz()
        self.cargar_auditoria()

    def crear_interfaz(self):
        tk.Label(self, text="REPORTES Y AUDITORÍA", bg=COLOR_FONDO, font=("Segoe UI", 18, "bold")).pack(pady=10)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=10)

        columnas = ("id", "fecha", "usuario", "accion", "detalles")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings")

        headers = ["ID", "FECHA / HORA", "USUARIO", "ACCIÓN", "DETALLES"]
        widths = [40, 150, 120, 150, 300]

        for col, h, w in zip(columnas, headers, widths):
            self.tree.heading(col, text=h)
            self.tree.column(col, width=w)

        self.tree.pack(expand=True, fill="both")

    def cargar_auditoria(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, fecha, usuario, accion, detalles FROM auditoria ORDER BY fecha DESC")
        for fila in cursor.fetchall():
            self.tree.insert("", "end", values=fila)
        conn.close()