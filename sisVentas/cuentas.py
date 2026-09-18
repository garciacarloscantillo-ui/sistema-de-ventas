import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar

class CuentasBaseFrame(tk.Frame):
    def __init__(self, parent, tipo_cuenta="cobrar"):
        super().__init__(parent, bg="#F0F4F8")
        self.tabla_db = "cuentas_cobrar" if tipo_cuenta == "cobrar" else "cuentas_pagar"
        self.entidad_label = "Cliente" if tipo_cuenta == "cobrar" else "Proveedor"
        self.id_sel = None
        self.crear_interfaz()
        self.cargar_tablas()

    def crear_interfaz(self):
        # Formularios CRUD
        frame_form = tk.LabelFrame(self, text=f" Registro de Cuenta ", bg="white", padx=10, pady=10)
        frame_form.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_form, text=f"{self.entidad_label}:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.txt_entidad = ttk.Entry(frame_form)
        self.txt_entidad.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Monto:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.txt_monto = ttk.Entry(frame_form)
        self.txt_monto.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Estado:", bg="white").grid(row=0, column=4, padx=5, pady=5)
        self.cmb_estado = ttk.Combobox(frame_form, values=["Pendiente", "Saldado"], state="readonly", width=12)
        self.cmb_estado.set("Pendiente")
        self.cmb_estado.grid(row=0, column=5, padx=5, pady=5)

        btn_f = tk.Frame(self, bg="#F0F4F8")
        btn_f.pack(fill="x", padx=15, pady=5)

        tk.Button(btn_f, text="Registrar", command=self.guardar, bg="#10B981", fg="white", bd=0, padx=10, pady=4).pack(side="left", padx=5)
        tk.Button(btn_f, text="Cambiar Estado / Actualizar", command=self.actualizar, bg="#3B82F6", fg="white", bd=0, padx=10, pady=4).pack(side="left", padx=5)
        tk.Button(btn_f, text="Eliminar", command=self.eliminar, bg="#EF4444", fg="white", bd=0, padx=10, pady=4).pack(side="left", padx=5)

        # Tablas divididas (Pendientes vs Saldados)
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=15, pady=10)

        # Panel Izquierdo: Pendientes
        f_pen = tk.LabelFrame(paned, text=" ⚠️ FALTAN POR PAGAR / COBRAR ", fg="#DC2626")
        paned.add(f_pen, weight=1)

        self.tree_pen = ttk.Treeview(f_pen, columns=("ID", "Nombre", "Monto", "Estado"), show="headings")
        for col in ("ID", "Nombre", "Monto", "Estado"):
            self.tree_pen.heading(col, text=col)
            self.tree_pen.column(col, anchor="center")
        self.tree_pen.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_pen.bind("<<TreeviewSelect>>", lambda e: self.seleccionar(self.tree_pen))

        # Panel Derecho: Saldados
        f_sal = tk.LabelFrame(paned, text=" ✅ SALDADOS / COMPLETADOS ", fg="#16A34A")
        paned.add(f_sal, weight=1)

        self.tree_sal = ttk.Treeview(f_sal, columns=("ID", "Nombre", "Monto", "Estado"), show="headings")
        for col in ("ID", "Nombre", "Monto", "Estado"):
            self.tree_sal.heading(col, text=col)
            self.tree_sal.column(col, anchor="center")
        self.tree_sal.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_sal.bind("<<TreeviewSelect>>", lambda e: self.seleccionar(self.tree_sal))

    def cargar_tablas(self):
        for r in self.tree_pen.get_children(): self.tree_pen.delete(r)
        for r in self.tree_sal.get_children(): self.tree_sal.delete(r)

        conn = conectar()
        c = conn.cursor()
        
        # Evaluamos el nombre de la columna directamente en Python
        col_nombre = "cliente" if self.tabla_db == "cuentas_cobrar" else "proveedor"
        
        c.execute(f"SELECT id, {col_nombre}, monto, estado FROM {self.tabla_db}")
        
        for reg in c.fetchall():
            if reg[3] == "Pendiente":
                self.tree_pen.insert("", "end", values=reg)
            else:
                self.tree_sal.insert("", "end", values=reg)
        conn.close()

    def guardar(self):
        conn = conectar()
        c = conn.cursor()
        col = "cliente" if self.tabla_db == "cuentas_cobrar" else "proveedor"
        c.execute(f"INSERT INTO {self.tabla_db} ({col}, monto, estado) VALUES (?, ?, ?)",
                  (self.txt_entidad.get(), float(self.txt_monto.get()), self.cmb_estado.get()))
        conn.commit(); conn.close()
        self.cargar_tablas()

    def seleccionar(self, tree):
        s = tree.selection()
        if s:
            v = tree.item(s[0])['values']
            self.id_sel = v[0]
            self.txt_entidad.delete(0, tk.END); self.txt_entidad.insert(0, v[1])
            self.txt_monto.delete(0, tk.END); self.txt_monto.insert(0, v[2])
            self.cmb_estado.set(v[3])

    def actualizar(self):
        if not self.id_sel: return
        conn = conectar()
        c = conn.cursor()
        col = "cliente" if self.tabla_db == "cuentas_cobrar" else "proveedor"
        c.execute(f"UPDATE {self.tabla_db} SET {col}=?, monto=?, estado=? WHERE id=?",
                  (self.txt_entidad.get(), float(self.txt_monto.get()), self.cmb_estado.get(), self.id_sel))
        conn.commit(); conn.close()
        self.cargar_tablas()

    def eliminar(self):
        if not self.id_sel: return
        conn = conectar()
        c = conn.cursor()
        c.execute(f"DELETE FROM {self.tabla_db} WHERE id=?", (self.id_sel,))
        conn.commit(); conn.close()
        self.cargar_tablas()