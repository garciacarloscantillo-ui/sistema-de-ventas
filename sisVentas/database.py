import sqlite3

DB_NAME = "sistema_erp.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_documento TEXT,
            documento TEXT,
            sexo TEXT,
            email TEXT,
            telefono TEXT,
            direccion TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT,
            telefono TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas_cabecera (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            metodo_pago TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuentas_cobrar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            monto REAL NOT NULL,
            estado TEXT DEFAULT 'Pendiente',
            fecha DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuentas_pagar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proveedor TEXT NOT NULL,
            monto REAL NOT NULL,
            estado TEXT DEFAULT 'Pendiente',
            fecha DATE
        )
    """)

    conn.commit()
    conn.close()

def insertar_datos_prueba():
    crear_tablas()
    conn = conectar()
    cursor = conn.cursor()

    # 1. Clientes
    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        clientes = [
            ("Distribuidora Norte S.A.S.", "NIT", "900123456-1", "Empresa", "contacto@disnorte.com", "3001234567", "Calle 45 #23-11"),
            ("Comercializadora El Sol", "NIT", "800987654-2", "Empresa", "ventas@elsol.co", "3109876543", "Carrera 50 #70-05"),
            ("Carlos Gómez", "CC", "1015558899", "Masculino", "gomez@gmail.com", "3015558899", "Calle 80 #10-15")
        ]
        cursor.executemany("INSERT INTO clientes (nombre, tipo_documento, documento, sexo, email, telefono, direccion) VALUES (?, ?, ?, ?, ?, ?, ?)", clientes)

    # 2. Proveedores
    cursor.execute("SELECT COUNT(*) FROM proveedores")
    if cursor.fetchone()[0] == 0:
        proveedores = [
            ("Tech Supplies Co", "Juan Pérez", "3154443322", "ventas@techsupplies.com"),
            ("Global Logistics", "Ana Martínez", "3187776655", "contacto@globallogistics.com"),
            ("Insumos Industriales", "Roberto Silva", "3201112233", "rsilva@insumos.com")
        ]
        cursor.executemany("INSERT INTO proveedores (nombre, contacto, telefono, email) VALUES (?, ?, ?, ?)", proveedores)

    # 3. Productos
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        prods = [
            ("P001", "Teclado Mecánico RGB", 150000, 25),
            ("P002", "Mouse Inalámbrico", 80000, 40),
            ("P003", "Monitor 24 IPS", 650000, 12),
            ("P004", "Diadema Gamer USB", 120000, 18)
        ]
        cursor.executemany("INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)", prods)

    # 4. Ventas
    cursor.execute("SELECT COUNT(*) FROM ventas_cabecera")
    if cursor.fetchone()[0] == 0:
        ventas = [
            (1, 230000, "Efectivo"),
            (2, 650000, "Transferencia"),
            (3, 150000, "Tarjeta")
        ]
        cursor.executemany("INSERT INTO ventas_cabecera (cliente_id, total, metodo_pago) VALUES (?, ?, ?)", ventas)

    # 5. Cuentas por Cobrar
    cursor.execute("SELECT COUNT(*) FROM cuentas_cobrar")
    if cursor.fetchone()[0] == 0:
        c_cobrar = [
            ("Distribuidora Norte S.A.S.", 450000, "Pendiente"),
            ("Carlos Gómez", 150000, "Saldado"),
            ("Comercializadora El Sol", 820000, "Pendiente")
        ]
        cursor.executemany("INSERT INTO cuentas_cobrar (cliente, monto, estado) VALUES (?, ?, ?)", c_cobrar)

    # 6. Cuentas por Pagar
    cursor.execute("SELECT COUNT(*) FROM cuentas_pagar")
    if cursor.fetchone()[0] == 0:
        c_pagar = [
            ("Tech Supplies Co", 1200000, "Pendiente"),
            ("Global Logistics", 350000, "Saldado")
        ]
        cursor.executemany("INSERT INTO cuentas_pagar (proveedor, monto, estado) VALUES (?, ?, ?)", c_pagar)

    conn.commit()
    conn.close()

# Funciones del Dashboard
def total_productos():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM productos")
    res = c.fetchone()[0]
    conn.close()
    return res if res else 0

def total_clientes():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM clientes")
    res = c.fetchone()[0]
    conn.close()
    return res if res else 0

def total_proveedores():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM proveedores")
    res = c.fetchone()[0]
    conn.close()
    return res if res else 0

def total_ventas():
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute("SELECT SUM(total) FROM ventas_cabecera")
        res = c.fetchone()[0]
    except Exception:
        res = 0
    conn.close()
    return int(res) if res else 0

def obtener_datos_ventas():
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute("SELECT strftime('%m', fecha) as mes, SUM(total) FROM ventas_cabecera GROUP BY mes")
        datos = c.fetchall()
    except Exception:
        datos = []
    
    if not datos:
        datos = [("Ene", 100000), ("Feb", 250000), ("Mar", 400000)]
    conn.close()
    return datos