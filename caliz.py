import tkinter as tk
from tkinter import ttk, messagebox

# Crear la ventana principal
root = tk.Tk()
root.title("Registro de Maquinaria")
root.geometry("1000x500")

# Definir los encabezados
columnas = [
    "FECHA", "UNIDAD", "OPERADOR", "UBICACIÓN", "CLIENTE", "FOLIO", "DIESEL",
    "HOROMETRO CARGA", "HOROMETRO INICIAL", "HOROMETRO FINAL", "REND",
    "HR. TRABAJO", "ACEITE HIDRAULICO", "ACEITE MOTOR", "ACTIVIDADES",
    "FALLAS", "REPARACION", "SERVICIOS"
]

# Diccionario para almacenar los campos de entrada
entradas = {}

# Crear un frame para los formularios
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

# Crear etiquetas y campos de entrada
for i, columna in enumerate(columnas):
    tk.Label(frame_form, text=columna).grid(row=i // 2, column=(i % 2) * 2, padx=5, pady=5, sticky="w")
    entrada = tk.Entry(frame_form, width=40)
    entrada.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=5)
    entradas[columna] = entrada

# Función para agregar datos a la tabla
def agregar_registro():
    valores = [entrada.get() for entrada in entradas.values()]
    if any(valor == "" for valor in valores):  # Verifica que no haya campos vacíos
        messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
        return
    
    tabla.insert("", "end", values=valores)  # Agrega los valores a la tabla

    # Limpiar campos después de agregar
    for entrada in entradas.values():
        entrada.delete(0, tk.END)

# Botón para agregar registro
btn_agregar = tk.Button(root, text="Agregar Registro", command=agregar_registro, bg="#4CAF50", fg="white", padx=10, pady=5)
btn_agregar.pack(pady=10)

# Crear tabla con Treeview
frame_tabla = tk.Frame(root)
frame_tabla.pack(pady=10)

tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

# Configurar encabezados
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=100)

tabla.pack()

# Iniciar la aplicación
root.mainloop()
        # 1. Obtener id de ubicación anterior (la que estaba en la BD)
        query_ubicacion_actual = """
            SELECT idubicaciones
            FROM historial_ubicacion
            WHERE idmaquina = %s
            ORDER BY fecha DESC
            LIMIT 1
        """
        resultado = ejecutar_query(query_ubicacion_actual, (id_maquina_editar,))
        id_ubicacion_anterior = resultado[0][0] if resultado else None

        # 2. Obtener el id de la ubicación nueva seleccionada en el formulario
        id_ubicacion_nueva = obtener_id("ubicaciones", "nombres", nuevos_valores["Ubicación:"])

        # 3. Comparar y registrar solo si cambió
        if id_ubicacion_nueva and id_ubicacion_nueva != id_ubicacion_anterior:
            query_historial = """
                INSERT INTO historial_ubicacion (idmaquina, idubicaciones, fecha)
                VALUES (%s, %s, %s)
            """
            ejecutar_query(query_historial, (id_maquina_editar, id_ubicacion_nueva, nuevos_valores["Fecha:"]))


        if ejecutar_query(query, valores_sql):
            messagebox.showinfo("Éxito", "Reporte actualizado correctamente")
            ventana_editar.destroy()
            # Aquí podrías agregar una función para recargar la tabla de reportes en la ventana principal