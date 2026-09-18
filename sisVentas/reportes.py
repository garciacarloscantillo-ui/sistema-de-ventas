import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from database import conectar

class ReportesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F0F4F8")
        self.crear_interfaz()

    def crear_interfaz(self):
        lbl_tit = tk.Label(self, text="MÓDULO DE REPORTES Y AUDITORÍA", font=("Helvetica", 16, "bold"), bg="#F0F4F8", fg="#1E293B")
        lbl_tit.pack(pady=20)

        frame_cards = tk.Frame(self, bg="#F0F4F8")
        frame_cards.pack(pady=20)

        # Tarjeta Exportar a PDF
        f_pdf = tk.LabelFrame(frame_cards, text=" Reporte General PDF ", bg="white", font=("Helvetica", 11, "bold"), padx=20, pady=20)
        f_pdf.grid(row=0, column=0, padx=15)
        
        tk.Label(f_pdf, text="Genera un archivo PDF maquetado con tablas independientes\npara Clientes, Proveedores, Inventario, Ventas y Cuentas.", bg="white", justify="left").pack(pady=10)
        tk.Button(f_pdf, text="📄 Exportar PDF General", command=self.exportar_pdf, bg="#EF4444", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=15, pady=8, cursor="hand2").pack()

        # Tarjeta Exportar a Excel
        f_xls = tk.LabelFrame(frame_cards, text=" Reporte Consolidado Excel ", bg="white", font=("Helvetica", 11, "bold"), padx=20, pady=20)
        f_xls.grid(row=0, column=1, padx=15)
        
        tk.Label(f_xls, text="Genera un libro de Excel (.xlsx) creando una hoja independiente\npara cada uno de los módulos del sistema ERP.", bg="white", justify="left").pack(pady=10)
        tk.Button(f_xls, text="📊 Exportar Excel Multihoja", command=self.exportar_excel, bg="#10B981", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=15, pady=8, cursor="hand2").pack()

    def obtener_datos_completos(self):
        conn = conectar()
        
        df_clientes = pd.read_sql_query("SELECT id as ID, nombre as Nombre, documento as Documento, email as Email, telefono as Telefono FROM clientes", conn)
        df_proveedores = pd.read_sql_query("SELECT id as ID, nombre as Empresa, contacto as Contacto, telefono as Telefono, email as Email FROM proveedores", conn)
        df_productos = pd.read_sql_query("SELECT id as ID, codigo as Codigo, nombre as Producto, precio as Precio, stock as Stock FROM productos", conn)
        df_ventas = pd.read_sql_query("SELECT id as ID, cliente_id as ID_Cliente, fecha as Fecha, total as Total, metodo_pago as Pago FROM ventas_cabecera", conn)
        df_cobrar = pd.read_sql_query("SELECT id as ID, cliente as Cliente, monto as Monto, estado as Estado FROM cuentas_cobrar", conn)
        df_pagar = pd.read_sql_query("SELECT id as ID, proveedor as Proveedor, monto as Monto, estado as Estado FROM cuentas_pagar", conn)
        
        conn.close()
        return {
            "Clientes": df_clientes,
            "Proveedores": df_proveedores,
            "Inventario": df_productos,
            "Ventas": df_ventas,
            "Cuentas por Cobrar": df_cobrar,
            "Cuentas por Pagar": df_pagar
        }

    def exportar_excel(self):
        try:
            datos = self.obtener_datos_completos()
            filename = "Reporte_General_ERP.xlsx"
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for nombre_hoja, df in datos.items():
                    df.to_excel(writer, sheet_name=nombre_hoja, index=False)
                    
            messagebox.showinfo("Éxito", f"Reporte Excel generado correctamente como '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte Excel: {e}")

    def exportar_pdf(self):
        try:
            datos = self.obtener_datos_completos()
            filename = "Reporte_General_ERP.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            
            styles = getSampleStyleSheet()
            estilo_titulo = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1E293B"), spaceAfter=15)
            estilo_subtitulo = ParagraphStyle('SubTitle', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor("#2563EB"), spaceBefore=15, spaceAfter=8)

            elementos = []
            elementos.append(Paragraph("REPORTE CONSOLIDADO DEL SISTEMA ERP", estilo_titulo))
            elementos.append(Spacer(1, 10))

            estilo_tabla = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ])

            for modulo, df in datos.items():
                elementos.append(Paragraph(f"Módulo: {modulo}", estilo_subtitulo))
                
                if df.empty:
                    elementos.append(Paragraph("Sin registros disponibles.", styles['Normal']))
                else:
                    # Convertir DataFrame en lista de listas para ReportLab
                    tabla_datos = [df.columns.tolist()] + df.astype(str).values.tolist()
                    t = Table(tabla_datos, hAlign='LEFT')
                    t.setStyle(estilo_tabla)
                    elementos.append(t)
                
                elementos.append(Spacer(1, 12))

            doc.build(elementos)
            messagebox.showinfo("Éxito", f"Reporte PDF generado correctamente como '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")