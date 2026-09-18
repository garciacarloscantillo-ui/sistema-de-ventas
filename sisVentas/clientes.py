import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_FONDO, COLOR_BLANCO
from database import conectar

class ClientesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.cliente_id = None
        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        titulo = tk.Label(self, text="GESTIÓN DE CLIENTES", bg=COLOR_FONDO, font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=10)

        form = tk.LabelFrame(self, text="DATOS DEL CLIENTE", bg=COLOR_BLANCO, padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        # Nombre
        tk.Label(form, text="Nombre completo", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_nombre = tk.Entry(form, width=35)
        self.ent_nombre.grid(row=1, column=0, padx=5, pady=5)

        # Tipo Documento
        tk.Label(form, text="Tipo de documento", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.cmb_tipo_documento = ttk.Combobox(form, width=28, state="readonly", values=[
            "Cédula de Ciudadanía", "Tarjeta de Identidad", "Permiso Especial Permanente"
        ])
        self.cmb_tipo_documento.grid(row=1, column=1, padx=5, pady=5)
        self.cmb_tipo_documento.current(0)

        # Documento
        tk.Label(form, text="Número de documento", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_documento = tk.Entry(form, width=25)
        self.ent_documento.grid(row=1, column=2, padx=5, pady=5)

        # Sexo
        tk.Label(form, text="Sexo", bg=COLOR_BLANCO).grid(row=0, column=3, sticky="w")
        self.cmb_sexo = ttk.Combobox(form, width=18, state="readonly", values=["Masculino", "Femenino", "Otro / LGBT+"])
        self.cmb_sexo.grid(row=1, column=3, padx=5, pady=5)
        self.cmb_sexo.current(0)

        # Teléfono
        tk.Label(form, text="Teléfono", bg=COLOR_BLANCO).grid(row=2, column=0, sticky="w")
        self.ent_telefono = tk.Entry(form, width=35)
        self.ent_telefono.grid(row=3, column=0, padx=5, pady=5)

        # Dirección
        tk.Label(form, text="Dirección", bg=COLOR_BLANCO).grid(row=2, column=1, sticky="w")
        self.ent_direccion = tk.Entry(form, width=35)
        self.ent_direccion.grid(row=3, column=1, padx=5, pady=5)

        # Email
        tk.Label(form, text="Email", bg=COLOR_BLANCO).grid(row=2, column=2, sticky="w")
        self.ent_email = tk.Entry(form, width=30)
        self.ent_email.grid(row=3, column=2, padx=5, pady=5)

        # Botones
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Button(barra, text="Guardar", bg="#16A34A", fg="white", font=("Segoe UI", 10, "bold"), command=self.guardar_cliente).pack(side="left", padx=5)
        tk.Button(barra, text="Actualizar", bg="#2563EB", fg="white", font=("Segoe UI", 10, "bold"), command=self.actualizar_cliente).pack(side="left", padx=5)
        tk.Button(barra, text="Eliminar", bg="#DC2626", fg="white", font=("Segoe UI", 10, "bold"), command=self.eliminar_cliente).pack(side="left", padx=5)
        tk.Button(barra, text="Limpiar", bg="#64748B", fg="white", font=("Segoe UI", 10, "bold"), command=self.limpiar_formulario).pack(side="left", padx=5)

    def guardar_cliente(self):
        nombre = self.ent_nombre.get().strip()
        tipo_documento = self.cmb_tipo_documento.get()
        documento = self.ent_documento.get().strip()
        sexo = self.cmb_sexo.get()
        telefono = self.ent_telefono.get().strip()
        direccion = self.ent_direccion.get().strip()
        email = self.ent_email.get().strip()

        if not nombre or not documento:
            messagebox.showwarning("Validación", "El nombre y el documento son obligatorios.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombre, tipo_documento, documento, sexo, telefono, direccion, email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nombre, tipo_documento, documento, sexo, telefono, direccion, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            self.limpiar_formulario()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el cliente:\n{e}")

    def actualizar_cliente(self):
        if self.cliente_id is None:
            messagebox.showwarning("Actualizar", "Seleccione un cliente de la tabla.")
            return

        nombre = self.ent_nombre.get().strip()
        tipo_documento = self.cmb_tipo_documento.get()
        documento = self.ent_documento.get().strip()
        sexo = self.cmb_sexo.get()
        telefono = self.ent_telefono.get().strip()
        direccion = self.ent_direccion.get().strip()
        email = self.ent_email.get().strip()

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nombre=?, tipo_documento=?, documento=?, sexo=?, telefono=?, direccion=?, email=?
                WHERE id=?
            """, (nombre, tipo_documento, documento, sexo, telefono, direccion, email, self.cliente_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.limpiar_formulario()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente:\n{e}")

    def eliminar_cliente(self):
        if self.cliente_id is None:
            messagebox.showwarning("Eliminar", "Seleccione un cliente de la tabla.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id=?", (self.cliente_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.limpiar_formulario()
                self.cargar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{e}")

    def cargar_clientes(self):
        if not hasattr(self, "tree_clientes"):
            columnas = ("id", "nombre", "tipo_documento", "documento", "sexo", "telefono", "direccion", "email")
            self.tree_clientes = ttk.Treeview(self, columns=columnas, show="headings", height=10)
            
            headers = ["ID", "NOMBRE", "TIPO DOC", "DOCUMENTO", "SEXO", "TELÉFONO", "DIRECCIÓN", "EMAIL"]
            widths = [40, 150, 130, 100, 90, 100, 130, 150]
            
            for col, h, w in zip(columnas, headers, widths):
                self.tree_clientes.heading(col, text=h)
                self.tree_clientes.column(col, width=w, anchor="center" if col == "id" else "w")

            self.tree_clientes.pack(fill="both", expand=True, padx=10, pady=10)
            self.tree_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, tipo_documento, documento, sexo, telefono, direccion, email FROM clientes ORDER BY nombre")
            for fila in cursor.fetchall():
                self.tree_clientes.insert("", "end", values=fila)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los clientes:\n{e}")

    def seleccionar_cliente(self, event):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            return
        datos = self.tree_clientes.item(seleccion[0], "values")
        self.cliente_id = datos[0]

        self.limpiar_formulario(reset_id=False)
        self.ent_nombre.insert(0, datos[1])
        self.cmb_tipo_documento.set(datos[2])
        self.ent_documento.insert(0, datos[3])
        self.cmb_sexo.set(datos[4])
        self.ent_telefono.insert(0, datos[5])
        self.ent_direccion.insert(0, datos[6])
        self.ent_email.insert(0, datos[7])

    def limpiar_formulario(self, reset_id=True):
        if reset_id:
            self.cliente_id = None
        self.ent_nombre.delete(0, tk.END)
        self.ent_documento.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.cmb_tipo_documento.current(0)
        self.cmb_sexo.current(0)
        if hasattr(self, "tree_clientes") and reset_id:
            for item in self.tree_clientes.selection():
                self.tree_clientes.selection_remove(item)