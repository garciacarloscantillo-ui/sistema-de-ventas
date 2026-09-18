import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_FONDO, COLOR_BLANCO
from database import conectar

class CuentasCobrarFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_interfaz()
        self.cargar_cuentas()

    def crear_interfaz(self):
        tk.Label(self, text="CUENTAS POR COBRAR", bg=COLOR_FONDO, font=("Segoe UI", 18, "bold")).pack(pady=10)

        # Formulario Registrar Cuenta
        form = tk.LabelFrame(self, text="NUEVA CUENTA POR COBRAR", bg=COLOR_BLANCO, padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="Cliente ID:", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_cliente_id = tk.Entry(form, width=15)
        self.ent_cliente_id.grid(row=1, column=0, padx=5)

        tk.Label(form, text="Monto Total:", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_monto = tk.Entry(form, width=15)
        self.ent_monto.grid(row=1, column=1, padx=5)

        tk.Label(form, text="Fecha Vencimiento (AAAA-MM-DD):", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_fecha = tk.Entry(form, width=20)
        self.ent_fecha.grid(row=1, column=2, padx=5)

        tk.Button(form, text="Registrar Cuentas", bg="#16A34A", fg="white", command=self.guardar_cuenta).grid(row=1, column=3, padx=10)

        # Tabla de Cuentas
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=10)

        columnas = ("id", "cliente", "monto", "pagado", "saldo", "estado", "vencimiento")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings")
        
        headers = ["ID", "CLIENTE", "MONTO", "PAGADO", "SALDO", "ESTADO", "VENCIMIENTO"]
        widths = [40, 180, 100, 100, 100, 100, 120]

        for col, h, w in zip(columnas, headers, widths):
            self.tree.heading(col, text=h)
            self.tree.column(col, width=w, anchor="center" if col in ("id", "estado") else "w")

        self.tree.pack(expand=True, fill="both")

    def guardar_cuenta(self):
        try:
            c_id = int(self.ent_cliente_id.get())
            monto = float(self.ent_monto.get())
            fecha = self.ent_fecha.get().strip()

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cuentas_por_cobrar (cliente_id, monto, fecha_vencimiento)
                VALUES (?, ?, ?)
            """, (c_id, monto, fecha))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cuenta por cobrar registrada.")
            self.cargar_cuentas()
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos:\n{e}")

    def cargar_cuentas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, cl.nombre, c.monto, c.monto_pagado, (c.monto - c.monto_pagado) as saldo, c.estado, c.fecha_vencimiento
            FROM cuentas_por_cobrar c
            JOIN clientes cl ON c.cliente_id = cl.id
        """)
        for fila in cursor.fetchall():
            self.tree.insert("", "end", values=fila)
        conn.close()