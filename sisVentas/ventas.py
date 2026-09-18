import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import conectar

class VentasFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F0F4F8")
        self.carrito = []
        self.total_venta = 0.0
        self.crear_interfaz()
        self.cargar_combos()

    def crear_interfaz(self):
        lbl_tit = tk.Label(self, text="MÓDULO DE VENTAS", font=("Helvetica", 16, "bold"), bg="#F0F4F8", fg="#1E293B")
        lbl_tit.pack(pady=10)

        # Selección de Cliente y Producto
        frame_top = tk.LabelFrame(self, text=" Datos de Venta ", bg="white", padx=10, pady=10)
        frame_top.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_top, text="Cliente:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.cmb_cliente = ttk.Combobox(frame_top, state="readonly", width=30)
        self.cmb_cliente.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_top, text="Producto:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.cmb_producto = ttk.Combobox(frame_top, state="readonly", width=30)
        self.cmb_producto.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_top, text="Cantidad:", bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.txt_cant = ttk.Entry(frame_top, width=10)
        self.txt_cant.insert(0, "1")
        self.txt_cant.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Button(frame_top, text="➕ Agregar al Carrito", command=self.agregar_producto, bg="#3B82F6", fg="white", bd=0, padx=10, pady=4).grid(row=1, column=3, padx=5, pady=5)

        # Tabla de Items en Carrito
        self.tree = ttk.Treeview(self, columns=("ID", "Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=8)
        for col in ("ID", "Producto", "Precio", "Cantidad", "Subtotal"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=5)

        # Pie de Venta y Procesamiento
        frame_bot = tk.Frame(self, bg="#F0F4F8")
        frame_bot.pack(fill="x", padx=15, pady=10)

        self.lbl_total = tk.Label(frame_bot, text="Total: $0", font=("Helvetica", 14, "bold"), bg="#F0F4F8", fg="#1E293B")
        self.lbl_total.pack(side="left")

        tk.Button(frame_bot, text="💳 Registrar Venta", command=self.finalizar_venta, bg="#10B981", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=15, pady=8).pack(side="right")

    def cargar_combos(self):
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT id, nombre FROM clientes")
        self.dict_clientes = {f"{r[1]} (ID: {r[0]})": r[0] for r in c.fetchall()}
        self.cmb_cliente['values'] = list(self.dict_clientes.keys())

        c.execute("SELECT id, nombre, precio, stock FROM productos")
        self.prods_db = {f"{r[1]} - ${r[2]} (Stock: {r[3]})": (r[0], r[1], r[2], r[3]) for r in c.fetchall()}
        self.cmb_producto['values'] = list(self.prods_db.keys())
        conn.close()

    def agregar_producto(self):
        prod_sel = self.cmb_producto.get()
        cant_str = self.txt_cant.get()
        if not prod_sel or not cant_str.isdigit():
            messagebox.showwarning("Atención", "Selecciona un producto y cantidad válida")
            return

        p_id, p_nom, p_precio, p_stock = self.prods_db[prod_sel]
        cant = int(cant_str)

        if cant > p_stock:
            messagebox.showerror("Stock Insuficiente", f"Solo quedan {p_stock} unidades disponibles")
            return

        subtotal = p_precio * cant
        self.carrito.append((p_id, p_nom, p_precio, cant, subtotal))
        self.tree.insert("", "end", values=(p_id, p_nom, f"${p_precio:,}", cant, f"${subtotal:,}"))
        
        self.total_venta += subtotal
        self.lbl_total.config(text=f"Total: ${self.total_venta:,.0f}")

    def finalizar_venta(self):
        if not self.carrito or not self.cmb_cliente.get():
            messagebox.showwarning("Atención", "Selecciona un cliente y agrega productos al carrito")
            return

        try:
            conn = conectar()
            c = conn.cursor()
            cli_id = self.dict_clientes[self.cmb_cliente.get()]

            c.execute("INSERT INTO ventas_cabecera (cliente_id, total, metodo_pago) VALUES (?, ?, ?)", (cli_id, self.total_venta, "Efectivo"))
            
            for item in self.carrito:
                p_id, _, _, cant, _ = item
                c.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cant, p_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Venta realizada correctamente")
            self.carrito.clear()
            self.total_venta = 0
            self.lbl_total.config(text="Total: $0")
            for r in self.tree.get_children(): self.tree.delete(r)
            self.cargar_combos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la venta: {e}")