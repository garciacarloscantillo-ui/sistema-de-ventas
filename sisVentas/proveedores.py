import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_FONDO, COLOR_BLANCO
from database import conectar

class ProveedoresFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.proveedor_id = None
        self.crear_interfaz()
        self.cargar_proveedores()

    def crear_interfaz(self):
        titulo = tk.Label(self, text="GESTIÓN DE PROVEEDORES", bg=COLOR_FONDO, font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=10)

        form = tk.LabelFrame(self, text="DATOS DEL PROVEEDOR", bg=COLOR_BLANCO, padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="NIT", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_nit = tk.Entry(form, width=20)
        self.ent_nit.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Nombre / Razón Social", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_nombre = tk.Entry(form, width=35)
        self.ent_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Contacto", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_contacto = tk.Entry(form, width=25)
        self.ent_contacto.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(form, text="Teléfono", bg=COLOR_BLANCO).grid(row=2, column=0, sticky="w")
        self.ent_telefono = tk.Entry(form, width=20)
        self.ent_telefono.grid(row=3, column=0, padx=5, pady=5)

        tk.Label(form, text="Email", bg=COLOR_BLANCO).grid(row=2, column=1, sticky="w")
        self.ent_email = tk.Entry(form, width=35)
        self.ent_email.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form, text="Dirección", bg=COLOR_BLANCO).grid(row=2, column=2, sticky="w")
        self.ent_direccion = tk.Entry(form, width=25)
        self.ent_direccion.grid(row=3, column=2, padx=5, pady=5)

        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Button(barra, text="Guardar", bg="#16A34A", fg="white", font=("Segoe UI", 10, "bold"), command=self.guardar_proveedor).pack(side="left", padx=5)
        tk.Button(barra, text="Actualizar", bg="#2563EB", fg="white", font=("Segoe UI", 10, "bold"), command=self.actualizar_proveedor).pack(side="left", padx=5)
        tk.Button(barra, text="Eliminar", bg="#DC2626", fg="white", font=("Segoe UI", 10, "bold"), command=self.eliminar_proveedor).pack(side="left", padx=5)
        tk.Button(barra, text="Limpiar", bg="#64748B", fg="white", font=("Segoe UI", 10, "bold"), command=self.limpiar_formulario).pack(side="left", padx=5)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=10)

        columnas = ("id", "nit", "nombre", "contacto", "telefono", "email", "direccion")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings")

        headers = ["ID", "NIT", "NOMBRE", "CONTACTO", "TELÉFONO", "EMAIL", "DIRECCIÓN"]
        widths = [40, 100, 180, 120, 100, 150, 150]

        for col, h, w in zip(columnas, headers, widths):
            self.tree.heading(col, text=h)
            self.tree.column(col, width=w, anchor="center" if col == "id" else "w")

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    def guardar_proveedor(self):
        nit = self.ent_nit.get().strip()
        nombre = self.ent_nombre.get().strip()
        if not nit or not nombre:
            messagebox.showwarning("Validación", "El NIT y el Nombre son obligatorios.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO proveedores (nit, nombre, contacto, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nit, nombre, self.ent_contacto.get().strip(), self.ent_telefono.get().strip(), self.ent_email.get().strip(), self.ent_direccion.get().strip()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            self.limpiar_formulario()
            self.cargar_proveedores()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el proveedor:\n{e}")

    def actualizar_proveedor(self):
        if self.proveedor_id is None:
            messagebox.showwarning("Actualizar", "Seleccione un proveedor de la tabla.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE proveedores SET nit=?, nombre=?, contacto=?, telefono=?, email=?, direccion=? WHERE id=?
            """, (self.ent_nit.get().strip(), self.ent_nombre.get().strip(), self.ent_contacto.get().strip(), self.ent_telefono.get().strip(), self.ent_email.get().strip(), self.ent_direccion.get().strip(), self.proveedor_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor actualizado.")
            self.limpiar_formulario()
            self.cargar_proveedores()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")

    def eliminar_proveedor(self):
        if self.proveedor_id is None:
            messagebox.showwarning("Eliminar", "Seleccione un proveedor.")
            return

        if messagebox.askyesno("Confirmar", "¿Desea eliminar el proveedor seleccionado?"):
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM proveedores WHERE id=?", (self.proveedor_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Proveedor eliminado.")
                self.limpiar_formulario()
                self.cargar_proveedores()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    def cargar_proveedores(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proveedores ORDER BY nombre")
        for fila in cursor.fetchall():
            self.tree.insert("", "end", values=fila)
        conn.close()

    def seleccionar_proveedor(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        datos = self.tree.item(seleccion[0], "values")
        self.proveedor_id = datos[0]

        self.limpiar_formulario(reset_id=False)
        self.ent_nit.insert(0, datos[1])
        self.ent_nombre.insert(0, datos[2])
        self.ent_contacto.insert(0, datos[3])
        self.ent_telefono.insert(0, datos[4])
        self.ent_email.insert(0, datos[5])
        self.ent_direccion.insert(0, datos[6])

    def limpiar_formulario(self, reset_id=True):
        if reset_id:
            self.proveedor_id = None
        self.ent_nit.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_contacto.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)
        for item in self.tree.selection():
            self.tree.selection_remove(item)