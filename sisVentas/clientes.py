import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar

class ClientesFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.id_seleccionado = None
        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        frame_form = ttk.LabelFrame(self, text=" Gestión de Clientes ")
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_nombre = ttk.Entry(frame_form, width=25)
        self.txt_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Tipo Doc:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.cmb_tipo_doc = ttk.Combobox(frame_form, values=["CC", "NIT", "CE", "Pasaporte"], state="readonly", width=12)
        self.cmb_tipo_doc.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Documento:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_documento = ttk.Entry(frame_form, width=25)
        self.txt_documento.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Sexo:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.cmb_sexo = ttk.Combobox(frame_form, values=["Masculino", "Femenino", "Empresa", "Otro"], state="readonly", width=12)
        self.cmb_sexo.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.txt_email = ttk.Entry(frame_form, width=25)
        self.txt_email.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Teléfono:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.txt_telefono = ttk.Entry(frame_form, width=15)
        self.txt_telefono.grid(row=2, column=3, padx=5, pady=5)

        frame_btn = ttk.Frame(self)
        frame_btn.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_btn, text="Guardar", command=self.guardar_cliente).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Actualizar", command=self.actualizar_cliente).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Eliminar", command=self.eliminar_cliente).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Tipo Doc", "Documento", "Sexo", "Email", "Teléfono"), show="headings")
        for col in ("ID", "Nombre", "Tipo Doc", "Documento", "Sexo", "Email", "Teléfono"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_registro)

    def cargar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, tipo_documento, documento, sexo, email, telefono FROM clientes ORDER BY id DESC")
            for cliente in cursor.fetchall():
                self.tree.insert("", "end", values=cliente)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudieron cargar los clientes:\n{e}")

    def guardar_cliente(self):
        if not self.txt_nombre.get():
            messagebox.showwarning("Atención", "El nombre es obligatorio")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombre, tipo_documento, documento, sexo, email, telefono)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.txt_nombre.get(), self.cmb_tipo_doc.get(), self.txt_documento.get(), 
                  self.cmb_sexo.get(), self.txt_email.get(), self.txt_telefono.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            self.limpiar_campos()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudo guardar el cliente:\n{e}")

    def seleccionar_registro(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']
            self.id_seleccionado = valores[0]
            
            self.limpiar_campos()
            self.txt_nombre.insert(0, valores[1])
            self.cmb_tipo_doc.set(valores[2] if valores[2] else '')
            self.txt_documento.insert(0, valores[3] if valores[3] else '')
            self.cmb_sexo.set(valores[4] if valores[4] else '')
            self.txt_email.insert(0, valores[5] if valores[5] else '')
            self.txt_telefono.insert(0, valores[6] if valores[6] else '')

    def actualizar_cliente(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clientes 
                SET nombre=?, tipo_documento=?, documento=?, sexo=?, email=?, telefono=?
                WHERE id=?
            """, (self.txt_nombre.get(), self.cmb_tipo_doc.get(), self.txt_documento.get(),
                  self.cmb_sexo.get(), self.txt_email.get(), self.txt_telefono.get(), self.id_seleccionado))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            self.limpiar_campos()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudo actualizar:\n{e}")

    def eliminar_cliente(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla")
            return
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este registro?"):
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id=?", (self.id_seleccionado,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente eliminado")
                self.limpiar_campos()
                self.cargar_clientes()
            except Exception as e:
                messagebox.showerror("Error SQL", f"No se pudo eliminar:\n{e}")

    def limpiar_campos(self):
        self.id_seleccionado = None
        self.txt_nombre.delete(0, tk.END)
        self.cmb_tipo_doc.set('')
        self.txt_documento.delete(0, tk.END)
        self.cmb_sexo.set('')
        self.txt_email.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)