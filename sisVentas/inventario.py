import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_FONDO, COLOR_BLANCO
from database import conectar

class InventarioFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_interfaz()
        self.cargar_productos()

    def crear_interfaz(self):
        titulo = tk.Label(self, text="GESTIÓN DE INVENTARIO", bg=COLOR_FONDO, font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=10)

        form = tk.LabelFrame(self, text="DATOS DEL PRODUCTO", bg=COLOR_BLANCO, padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Código", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_codigo = tk.Entry(form, width=20)
        self.ent_codigo.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Nombre", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.ent_nombre = tk.Entry(form, width=40)
        self.ent_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Precio", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.ent_precio = tk.Entry(form, width=15)
        self.ent_precio.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(form, text="Stock", bg=COLOR_BLANCO).grid(row=0, column=3, sticky="w")
        self.ent_stock = tk.Entry(form, width=10)
        self.ent_stock.grid(row=1, column=3, padx=5, pady=5)

        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Button(barra, text="Guardar", bg="#16A34A", fg="white", command=self.agregar_producto).pack(side="left", padx=5)
        tk.Button(barra, text="Actualizar", bg="#2563EB", fg="white", command=self.actualizar_producto).pack(side="left", padx=5)
        tk.Button(barra, text="Eliminar", bg="#DC2626", fg="white", command=self.eliminar_producto).pack(side="left", padx=5)
        tk.Button(barra, text="Limpiar", bg="#EA580C", fg="white", command=self.limpiar_formulario).pack(side="left", padx=5)

        busqueda = tk.Frame(self, bg=COLOR_FONDO)
        busqueda.pack(fill="x", padx=10, pady=10)

        tk.Label(busqueda, text="Buscar:", bg=COLOR_FONDO).pack(side="left")
        self.ent_buscar = tk.Entry(busqueda)
        self.ent_buscar.pack(side="left", padx=5)
        tk.Button(busqueda, text="Buscar", command=self.buscar_producto).pack(side="left")

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=10)

        columnas = ("codigo", "nombre", "precio", "stock")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        self.tree.column("codigo", width=100)
        self.tree.column("nombre", width=300)
        self.tree.column("precio", width=120)
        self.tree.column("stock", width=100)

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    def agregar_producto(self):
        codigo = self.ent_codigo.get().strip()
        nombre = self.ent_nombre.get().strip()
        try:
            precio = float(self.ent_precio.get())
            stock = int(self.ent_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Precio o Stock inválido")
            return

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO productos VALUES (?, ?, ?, ?)", (codigo, nombre, precio, stock))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

        self.cargar_productos()
        self.limpiar_formulario()

    def actualizar_producto(self):
        codigo = self.ent_codigo.get().strip()
        try:
            precio = float(self.ent_precio.get())
            stock = int(self.ent_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos SET nombre=?, precio=?, stock=? WHERE codigo=?
        """, (self.ent_nombre.get().strip(), precio, stock, codigo))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Producto actualizado")
        self.cargar_productos()

    def eliminar_producto(self):
        item = self.tree.selection()
        if not item:
            return
        codigo = self.tree.item(item)["values"][0]

        if not messagebox.askyesno("Confirmar", "¿Eliminar producto?"):
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE codigo=?", (codigo,))
        conn.commit()
        conn.close()
        self.cargar_productos()
        self.limpiar_formulario()

    def cargar_productos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY nombre")
        for fila in cursor.fetchall():
            self.tree.insert("", tk.END, values=fila)
        conn.close()

    def buscar_producto(self):
        texto = self.ent_buscar.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ? OR codigo LIKE ?", (f"%{texto}%", f"%{texto}%"))
        for fila in cursor.fetchall():
            self.tree.insert("", tk.END, values=fila)
        conn.close()

    def seleccionar_producto(self, event):
        item = self.tree.selection()
        if not item:
            return
        datos = self.tree.item(item)["values"]
        self.ent_codigo.delete(0, tk.END)
        self.ent_codigo.insert(0, datos[0])
        self.ent_nombre.delete(0, tk.END)
        self.ent_nombre.insert(0, datos[1])
        self.ent_precio.delete(0, tk.END)
        self.ent_precio.insert(0, datos[2])
        self.ent_stock.delete(0, tk.END)
        self.ent_stock.insert(0, datos[3])

    def limpiar_formulario(self):
        self.ent_codigo.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)