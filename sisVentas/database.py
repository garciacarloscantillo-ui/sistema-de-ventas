import sqlite3

DB_NAME = "sistema_erp.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabla Clientes completa con tipo_documento, documento y sexo
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

    # Proveedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT,
            telefono TEXT,
            email TEXT
        )
    """)

    # Productos / Inventario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Cuentas por Cobrar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuentas_por_cobrar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            monto REAL NOT NULL,
            monto_pagado REAL DEFAULT 0,
            estado TEXT DEFAULT 'Pendiente',
            fecha_vencimiento DATE,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    # Cuentas por Pagar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuentas_por_pagar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proveedor_id INTEGER,
            monto REAL NOT NULL,
            monto_pagado REAL DEFAULT 0,
            estado TEXT DEFAULT 'Pendiente',
            fecha_vencimiento DATE,
            FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        )
    """)

    # Auditoría
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usuario TEXT,
            accion TEXT NOT NULL,
            detalles TEXT
        )
    """)

    conn.commit()
    conn.close()

def insertar_datos_prueba():
    crear_tablas()
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Inserción con todas las columnas correspondientes
    clientes = [
        ("Distribuidora Norte S.A.S.", "NIT", "900123456-1", "Empresa", "contacto@disnorte.com", "3001234567", "Calle 45 #23-11"),
        ("Comercializadora El Sol", "NIT", "800987654-2", "Empresa", "ventas@elsol.co", "3109876543", "Carrera 50 #70-05"),
        ("Carlos Gómez", "CC", "1015558899", "Masculino", "gomez_inv@gmail.com", "3015558899", "Avenida Calle 80 #10-15")
    ]
    cursor.executemany("""
        INSERT INTO clientes (nombre, tipo_documento, documento, sexo, email, telefono, direccion) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, clientes)

    # Proveedores
    proveedores = [
        ("Importaciones Globales Ltd", "Juan Pérez", "3154443322", "importaciones@global.com"),
        ("Suministros Industriales", "Ana Martínez", "3187776655", "ventas@sumindustriales.com")
    ]
    cursor.executemany("INSERT INTO proveedores (nombre, contacto, telefono, email) VALUES (?, ?, ?, ?)", proveedores)

    # Productos
    productos = [
        ("PROD-001", "Laptop Corp i7 16GB", 3500000.0, 15),
        ("PROD-002", "Monitor 27 Pulgadas IPS", 950000.0, 30),
        ("PROD-003", "Teclado Mecánico RGB", 220000.0, 50),
        ("PROD-004", "Mouse Inalámbrico Ergonómico", 110000.0, 40)
    ]
    cursor.executemany("INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)", productos)

    # Cuentas por Cobrar
    cuentas_cobrar = [
        (1, 3500000.0, 1000000.0, "Parcial", "2026-10-15"),
        (2, 1140000.0, 0.0, "Pendiente", "2026-09-30")
    ]
    cursor.executemany("INSERT INTO cuentas_por_cobrar (cliente_id, monto, monto_pagado, estado, fecha_vencimiento) VALUES (?, ?, ?, ?, ?)", cuentas_cobrar)

    # Cuentas por Pagar
    cuentas_pagar = [
        (1, 5000000.0, 2500000.0, "Parcial", "2026-10-01"),
        (2, 850000.0, 850000.0, "Pagado", "2026-09-10")
    ]
    cursor.executemany("INSERT INTO cuentas_por_pagar (proveedor_id, monto, monto_pagado, estado, fecha_vencimiento) VALUES (?, ?, ?, ?, ?)", cuentas_pagar)

    # Auditoría
    auditoria = [
        ("ADMIN", "INICIO_SESION", "El usuario admin ingresó al sistema."),
        ("ADMIN", "REGISTRO_CLIENTE", "Se registró el cliente Distribuidora Norte S.A.S."),
        ("SISTEMA", "CARGA_INICIAL", "Base de datos poblada con registros de prueba.")
    ]
    cursor.executemany("INSERT INTO auditoria (usuario, accion, detalles) VALUES (?, ?, ?)", auditoria)

    conn.commit()
    conn.close()

# Consultas para el Dashboard
def total_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def total_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def total_proveedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM proveedores")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def total_ventas():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM cuentas_por_cobrar")
        total = cursor.fetchone()[0]
    except:
        total = 0
    conn.close()
    return total

if __name__ == "__main__":
    insertar_datos_prueba()