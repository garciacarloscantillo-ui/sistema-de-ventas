import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_FONDO, COLOR_BLANCO
from database import conectar

class VentasFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.carrito = []
        self.total_venta = 0.0
        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        titulo = tk.Label(self, text="MÓDULO DE VENTAS", bg=COLOR_FONDO, font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=10)

        # Selección de Cliente
        f_cliente = tk.LabelFrame(self, text="CLIENTE", bg=COLOR_BLANCO, padx=10, pady=5)
        f_cliente.pack(fill="x", padx=10, pady=5)

        tk.Label(f_cliente, text="Seleccionar Cliente:", bg=COLOR_BLANCO).pack(side="left", padx=5)
        self.cmb_clientes = ttk.Combobox(f_cliente, width=40, state="readonly")
        self.cmb_clientes.pack(side="left", padx=5)

        # Búsqueda y Selección de Producto
        f_producto = tk.LabelFrame(self, text="AGREGAR PRODUCTO", bg=COLOR_BLANCO, padx=10, pady=5)
        f_producto.pack(fill="x", padx=10, pady=5)

        tk.Label(f_producto, text="Código:", bg=COLOR_BLANCO).grid(row=0, column=0, sticky="w")
        self.ent_codigo = tk.Entry(f_producto, width=15)
        self.ent_codigo.grid(row=1, column=0, padx=5)
        self.ent_codigo.bind("<Return>", self.buscar_producto_por_codigo)

        tk.Label(f_producto, text="Producto:", bg=COLOR_BLANCO).grid(row=0, column=1, sticky="w")
        self.lbl_nombre_prod = tk.Label(f_producto, text="-", bg=COLOR_BLANCO, font=("Segoe UI", 10, "bold"))
        self.lbl_nombre_prod.grid(row=1, column=1, padx=5, sticky="w")

        tk.Label(f_producto, text="Precio:", bg=COLOR_BLANCO).grid(row=0, column=2, sticky="w")
        self.lbl_precio_prod = tk.Label(f_producto, text="0.00", bg=COLOR_BLANCO, font=("Segoe UI", 10, "bold"))
        self.lbl_precio_prod.grid(row=1, column=2, padx=5, sticky="w")

        tk.Label(f_producto, text="Cantidad:", bg=COLOR_BLANCO).grid(row=0, column=3, sticky="w")
        self.ent_cantidad = tk.Entry(f_producto, width=10)
        self.ent_cantidad.grid(row=1, column=3, padx=5)
        self.ent_cantidad.insert(0, "1")

        tk.Button(f_producto, text="Agregar al Carrito", bg="#2563EB", fg="white", command=self.agregar_al_carrito).grid(row=1, column=4, padx=10)

        # Tabla del Carrito
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=5)

        columnas = ("codigo", "nombre", "precio", "cantidad", "subtotal")
        self.tree_carrito = ttk.Treeview(frame_tree, columns=columnas, show="headings", height=8)

        self.tree_carrito.heading("codigo", text="Código")
        self.tree_carrito.heading("nombre", text="Producto")
        self.tree_carrito.heading("precio", text="Precio U.")
        self.tree_carrito.heading("cantidad", text="Cant.")
        self.tree_carrito.heading("subtotal", text="Subtotal")

        self.tree_carrito.pack(expand=True, fill="both")

        # Total y Procesamiento
        f_pago = tk.Frame(self, bg=COLOR_FONDO)
        f_pago.pack(fill="x", padx=10, pady=10)

        self.lbl_total = tk.Label(f_pago, text="TOTAL: $0.00", bg=COLOR_FONDO, font=("Segoe UI", 16, "bold"), fg="#1E293B")
        self.lbl_total.pack(side="left", padx=10)

        tk.Button(f_pago, text="PROCESAR VENTA", bg="#16A34A", fg="white", font=("Segoe UI", 12, "bold"), command=self.procesar_venta).pack(side="right", padx=10)

        self.producto_actual = None

    def cargar_clientes(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, documento FROM clientes ORDER BY nombre")
        self.clientes_dict = {}
        lista_clientes = []
        for row in cursor.fetchall():
            text = f"{row[1]} - ({row[2]})"
            self.clientes_dict[text] = row[0]
            lista_clientes.append(text)
        self.cmb_clientes["values"] = lista_clientes
        if lista_clientes:
            self.cmb_clientes.current(0)
        conn.close()

    def buscar_producto_por_codigo(self, event=None):
        codigo = self.ent_codigo.get().strip()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nombre, precio, stock FROM productos WHERE codigo=?", (codigo,))
        prod = cursor.fetchone()
        conn.close()

        if prod:
            self.producto_actual = prod
            self.lbl_nombre_prod.config(text=prod[1])
            self.lbl_precio_prod.config(text=f"{prod[2]:.2f}")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")
            self.producto_actual = None
            self.lbl_nombre_prod.config(text="-")
            self.lbl_precio_prod.config(text="0.00")

    def agregar_al_carrito(self):
        if not self.producto_actual:
            messagebox.showwarning("Atención", "Busque y seleccione un producto válido primero.")
            return

        try:
            cant = int(self.ent_cantidad.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad entera positiva.")
            return

        if cant > self.producto_actual[3]:
            messagebox.showwarning("Stock Insuficiente", f"Solo hay {self.producto_actual[3]} unidades disponibles.")
            return

        subtotal = cant * self.producto_actual[2]
        self.carrito.append({
            "codigo": self.producto_actual[0],
            "nombre": self.producto_actual[1],
            "precio": self.producto_actual[2],
            "cantidad": cant,
            "subtotal": subtotal
        })

        self.actualizar_tabla_carrito()

    def actualizar_tabla_carrito(self):
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)

        self.total_venta = 0.0
        for item in self.carrito:
            self.tree_carrito.insert("", "end", values=(
                item["codigo"], item["nombre"], f"${item['precio']:.2f}", item["cantidad"], f"${item['subtotal']:.2f}"
            ))
            self.total_venta += item["subtotal"]

        self.lbl_total.config(text=f"TOTAL: ${self.total_venta:.2f}")

    def procesar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Atención", "El carrito está vacío.")
            return

        cliente_sel = self.cmb_clientes.get()
        if not cliente_sel:
            messagebox.showwarning("Atención", "Seleccione un cliente.")
            return

        cliente_id = self.clientes_dict[cliente_sel]

        try:
            conn = conectar()
            cursor = conn.cursor()

            # Insertar Cabecera de la Venta
            cursor.execute("INSERT INTO ventas (cliente_id, total) VALUES (?, ?)", (cliente_id, self.total_venta))
            venta_id = cursor.lastrowid

            # Insertar Detalles y Actualizar Stock
            for item in self.carrito:
                cursor.execute("""
                    INSERT INTO detalle_ventas (venta_id, producto_codigo, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (venta_id, item["codigo"], item["cantidad"], item["precio"], item["subtotal"]))

                cursor.execute("""
                    UPDATE productos SET stock = stock - ? WHERE codigo = ?
                """, (item["cantidad"], item["codigo"]))

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Venta registrada con éxito.")
            self.carrito = []
            self.actualizar_tabla_carrito()
            self.ent_codigo.delete(0, tk.END)
            self.lbl_nombre_prod.config(text="-")
            self.lbl_precio_prod.config(text="0.00")
            self.producto_actual = None

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la venta:\n{e}")