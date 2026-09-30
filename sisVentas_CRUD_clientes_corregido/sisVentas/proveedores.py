import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar

class ProveedoresFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F0F4F8")
        self.id_sel = None
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        lbl_tit = tk.Label(self, text="GESTIÓN DE PROVEEDORES", font=("Helvetica", 16, "bold"), bg="#F0F4F8", fg="#1E293B")
        lbl_tit.pack(pady=10)

        frame = tk.LabelFrame(self, text=" Datos Proveedor ", bg="white", padx=10, pady=10)
        frame.pack(fill="x", padx=15, pady=5)

        tk.Label(frame, text="Nombre Empresa:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.txt_nom = ttk.Entry(frame)
        self.txt_nom.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Contacto:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.txt_con = ttk.Entry(frame)
        self.txt_con.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame, text="Teléfono:", bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.txt_tel = ttk.Entry(frame)
        self.txt_tel.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Email:", bg="white").grid(row=1, column=2, padx=5, pady=5)
        self.txt_eml = ttk.Entry(frame)
        self.txt_eml.grid(row=1, column=3, padx=5, pady=5)

        f_btn = tk.Frame(self, bg="#F0F4F8")
        f_btn.pack(fill="x", padx=15, pady=5)

        tk.Button(f_btn, text="Guardar", command=self.guardar, bg="#10B981", fg="white", bd=0, padx=10, pady=4).pack(side="left", padx=5)
        tk.Button(f_btn, text="Actualizar", command=self.actualizar, bg="#3B82F6", fg="white", bd=0, padx=10, pady=4).pack(side="left", padx=5)
        tk.Button(f_btn, text="Eliminar", command=self.eliminar, bg="#EF4444", fg="white", bd=0, padx=10, pady=4).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Empresa", "Contacto", "Teléfono", "Email"), show="headings")
        for col in ("ID", "Empresa", "Contacto", "Teléfono", "Email"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar_tabla(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT id, nombre, contacto, telefono, email FROM proveedores")
        for p in c.fetchall(): self.tree.insert("", "end", values=p)
        conn.close()

    def guardar(self):
        conn = conectar()
        c = conn.cursor()
        c.execute("INSERT INTO proveedores (nombre, contacto, telefono, email) VALUES (?, ?, ?, ?)",
                  (self.txt_nom.get(), self.txt_con.get(), self.txt_tel.get(), self.txt_eml.get()))
        conn.commit(); conn.close()
        self.cargar_tabla()

    def seleccionar(self, event):
        s = self.tree.selection()
        if s:
            v = self.tree.item(s[0])['values']
            self.id_sel = v[0]
            self.txt_nom.delete(0, tk.END); self.txt_nom.insert(0, v[1])
            self.txt_con.delete(0, tk.END); self.txt_con.insert(0, v[2])
            self.txt_tel.delete(0, tk.END); self.txt_tel.insert(0, v[3])
            self.txt_eml.delete(0, tk.END); self.txt_eml.insert(0, v[4])

    def actualizar(self):
        if not self.id_sel: return
        conn = conectar()
        c = conn.cursor()
        c.execute("UPDATE proveedores SET nombre=?, contacto=?, telefono=?, email=? WHERE id=?",
                  (self.txt_nom.get(), self.txt_con.get(), self.txt_tel.get(), self.txt_eml.get(), self.id_sel))
        conn.commit(); conn.close()
        self.cargar_tabla()

    def eliminar(self):
        if not self.id_sel: return
        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM proveedores WHERE id=?", (self.id_sel,))
        conn.commit(); conn.close()
        self.cargar_tabla()