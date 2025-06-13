import tkinter as tk
from tkinter import Menu, Toplevel
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import mysql.connector
import tkinter.messagebox as messagebox
from tkcalendar import DateEntry
import pandas as pd
from tkinter import messagebox, filedialog
from datetime import datetime
from datetime import timedelta
import openpyxl
import os



conexion = None
cursor = None
ventana_anterior = None

def centrar_ventana(ventana, ancho, alto, offset_y=50):
    # Obtener el tamaño de la pantalla
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    # Calcular las coordenadas de la ventana centrada con desplazamiento
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2) - offset_y  # Restar offset_y para mover hacia arriba

    # Establecer la geometría de la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def conectar_bd():
    global conexion, cursor
    if conexion is None or not conexion.is_connected():
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",  # Reemplaza con tu usuario de MySQL
                password="",  # Reemplaza con tu contraseña de MySQL
                database="pruebas"
            )
            cursor = conexion.cursor()
            print("Conexión a la base de datos establecida.")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

def convertir_mayusculas(event):
    texto_actual = event.widget.get()  # Obtener el texto actual
    # Cambiar el texto a mayúsculas y actualizar la entrada
    event.widget.delete(0, tk.END)  # Borrar el texto actual
    event.widget.insert(0, texto_actual.upper()) 

# Crear la ventana principal
root = tk.Tk()
root.title("Página Inicial")
root.geometry("270x405")
centrar_ventana(root, 270, 405, offset_y=200) 

# Cargar la imagen de fondo
image = Image.open("C:/Users/PC/caliz/fondo1.jpg")
background_image = ImageTk.PhotoImage(image)

# Crear un label para la imagen de fondo
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Variable global para controlar la ventana activa
ventana_activa = None

def cambiar_ventana(nueva_ventana_func):
    """Cierra la ventana activa y abre una nueva, recordando la anterior."""
    global ventana_activa, ventana_anterior

    if ventana_activa is not None:
        ventana_anterior = ventana_activa  # Guardamos la ventana actual antes de cerrarla
        ventana_activa.destroy()

    ventana_activa = nueva_ventana_func() # Abrir la nueva ventana

def abrir_marcas():
    global ventana_activa, conexion, cursor
    root.withdraw()  # Oculta la ventana principal
    marcas = tk.Toplevel(root)  # Crea la ventana secundaria
    marcas.title("Marcas")
    marcas.geometry("300x200")  # Tamaño de la ventana
    centrar_ventana(marcas, 300, 200, offset_y=150)

    image = Image.open("C:/Users/PC/caliz/fondo_marca.jpg")
    background_image = ImageTk.PhotoImage(image)

    # Crear un label para la imagen de fondo
    background_label = tk.Label(marcas, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Cubrir toda la ventana
    marcas.background_image = background_image 

    # Label para el título
    tk.Label(marcas, text="Agregar Marca", font=("Arial", 14, "bold"), bg="blue", fg="white").pack(pady=10)

    # Label y Entry para ingresar la marca
    tk.Label(marcas, text="Marca:", bg="blue", fg="white", font=("Arial", 12)).pack(pady=5)
    marca_entry = tk.Entry(marcas, font=("Arial", 12), width=25, bd=2, relief="solid")
    marca_entry.pack(pady=10)
    marca_entry.bind("<KeyRelease>", convertir_mayusculas)

    # Función para manejar lo que se escribe en el Entry y guardar en la base de datos
    def obtener_marca():
        marca = marca_entry.get()  # Obtiene lo que el usuario escribió
        print(f"Marca ingresada: {marca}")
        
        # Verificar si la marca no está vacía
        if not marca.strip():
            messagebox.showwarning("Advertencia", "No se puede insertar una marca vacía.")
            return

        # Si la conexión no está establecida, se conecta a la base de datos
        if conexion is None or cursor is None:
            conectar_bd()  # Asegúrate de tener esta función definida en tu código

        try:
            # Ejecutar la consulta SQL para insertar la marca en la base de datos
            query = "INSERT INTO marcas (nombre) VALUES (%s)"
            cursor.execute(query, (marca,))
            conexion.commit()  # Confirmar la transacción
            messagebox.showinfo("Éxito", "Marca insertada correctamente.")  # Mostrar mensaje de éxito
            marca_entry.delete(0, tk.END)  # Borra el contenido del Entry
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar marca: {err}")  # Mostrar mensaje de error


        

    # Función para cambiar el color de fondo cuando se pasa el cursor (hover effect)
    def on_enter(button, event):
        button.config(bg="#45a049", fg="white")

    def on_leave(button, event):
        button.config(bg="#4CAF50", fg="white")

    # Botón para agregar la marca
    agregar_button = tk.Button(marcas, text="Agregar Marca", command=obtener_marca, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", width=20)
    agregar_button.pack(pady=10)
    
    # Efectos de hover para el botón
    agregar_button.bind("<Enter>", lambda event, button=agregar_button: on_enter(button, event))
    agregar_button.bind("<Leave>", lambda event, button=agregar_button: on_leave(button, event))

    def cerrar_marcas_ventana():
        marcas.destroy()  # Cierra la ventana de marcas
        cambiar_ventana(agregar_maquinaria)  # Regresa a la ventana de agregar maquinaria

    marcas.protocol("WM_DELETE_WINDOW", cerrar_marcas_ventana)  # Cierra correctamente cuando se cierra la ventana de marcas
    ventana_activa = marcas  # Guardar referencia de la ventana actual

    return marcas

def abrir_Unidad():
    global ventana_activa
    root.withdraw()  # Oculta la ventana principal
    unidad = tk.Toplevel(root)  # Crea la ventana secundaria
    unidad.title("Agregar No. Económico")
    unidad.geometry("300x200")  # Tamaño de la ventana
    centrar_ventana(unidad, 300, 200, offset_y=150)

    image = Image.open("C:/Users/PC/caliz/fondo_marca.jpg")
    background_image = ImageTk.PhotoImage(image)

    # Crear un label para la imagen de fondo
    background_label = tk.Label(unidad, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Cubrir toda la ventana
    unidad.background_image = background_image 

    # Label para el título
    tk.Label(unidad, text="Agregar No. Económico", font=("Arial", 14, "bold"), bg="blue", fg="white").pack(pady=10)

    # Label y Entry para ingresar el número económico
    tk.Label(unidad, text="No. Económico:", bg="blue", fg="white", font=("Arial", 12)).pack(pady=5)
    unidad_entry = tk.Entry(unidad, font=("Arial", 12), width=25, bd=2, relief="solid")
    unidad_entry.pack(pady=10)
    unidad_entry.bind("<KeyRelease>", convertir_mayusculas)

    # Función para manejar lo que se escribe en el Entry
    def obtener_unidad():
        no_economico = unidad_entry.get().strip().upper()  # Convierte a mayúsculas y quita espacios

        if not no_economico:
            messagebox.showwarning("Advertencia", "El No. Económico no puede estar vacío.")
            return

        try:
            conectar_bd()  # Conectar a la base de datos si no está conectado

            # Verificar si el No. Económico ya existe en la tabla
            query_verificar = "SELECT COUNT(*) FROM unidad WHERE No_Economico = %s"
            cursor.execute(query_verificar, (no_economico,))
            resultado = cursor.fetchone()

            if resultado[0] > 0:  # Si ya existe
                messagebox.showwarning("Advertencia", "El No. Económico ya existe en la base de datos.")
            else:
                # Si no existe, insertarlo
                query_insertar = "INSERT INTO unidad (No_Economico) VALUES (%s)"
                cursor.execute(query_insertar, (no_economico,))
                conexion.commit()  # Confirmar la transacción
                messagebox.showinfo("Éxito", "No. Económico insertado correctamente.")
                unidad_entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar No. Económico: {err}")

        finally:
            cursor.close()
            conexion.close()

    # Función para cambiar el color de fondo cuando se pasa el cursor (hover effect)
    def on_enter(button, event):
        button.config(bg="#45a049", fg="white")

    def on_leave(button, event):
        button.config(bg="#4CAF50", fg="white")

    # Botón para agregar el No. Económico
    agregar_button = tk.Button(unidad, text="Agregar No. Económico", command=obtener_unidad, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", width=20)
    agregar_button.pack(pady=10)
    unidad_entry.delete(0, tk.END)
    
    # Efectos de hover para el botón
    agregar_button.bind("<Enter>", lambda event, button=agregar_button: on_enter(button, event))
    agregar_button.bind("<Leave>", lambda event, button=agregar_button: on_leave(button, event))

    def cerrar_unidad_ventana():
        unidad.destroy()  # Cierra la ventana de unidad
        cambiar_ventana(agregar_maquinaria)  # Regresa a la ventana de agregar maquinaria

    unidad.protocol("WM_DELETE_WINDOW", cerrar_unidad_ventana)  # Cierra correctamente cuando se cierra la ventana de unidad
    ventana_activa = unidad  # Guardar referencia de la ventana actual

def abrir_Ubicacion():
    global ventana_activa
    root.withdraw()  # Oculta la ventana principal
    ubicacion = tk.Toplevel(root)  # Crea la ventana secundaria
    ubicacion.title("Agregar Ubicación")
    ubicacion.geometry("300x200")  # Tamaño de la ventana
    centrar_ventana(ubicacion, 300, 200, offset_y=150)

    image = Image.open("C:/Users/PC/caliz/fondo_marca.jpg")
    background_image = ImageTk.PhotoImage(image)

    # Crear un label para la imagen de fondo
    background_label = tk.Label(ubicacion, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Cubrir toda la ventana
    ubicacion.background_image = background_image 

    # Label para el título
    tk.Label(ubicacion, text="Agregar Ubicación", font=("Arial", 14, "bold"), bg="blue", fg="white").pack(pady=10)

    # Label y Entry para ingresar la ubicación
    tk.Label(ubicacion, text="Ubicación:", bg="blue", fg="white", font=("Arial", 12)).pack(pady=5)
    ubicacion_entry = tk.Entry(ubicacion, font=("Arial", 12), width=25, bd=2, relief="solid")
    ubicacion_entry.pack(pady=10)
    ubicacion_entry.bind("<KeyRelease>", convertir_mayusculas)

    # Función para manejar lo que se escribe en el Entry
    def obtener_ubicacion():
        ubicacion = ubicacion_entry.get().strip()  # Obtiene lo que el usuario escribió y elimina espacios
        if not ubicacion:
            messagebox.showwarning("Advertencia", "La ubicación no puede estar vacía.")
            return

        try:
            conectar_bd()  # Conectar a la base de datos si no está conectado

            # Ejecutar la consulta SQL para insertar la ubicación
            query = "INSERT INTO ubicaciones (nombres) VALUES (%s)"
            cursor.execute(query, (ubicacion,))
            conexion.commit()  # Confirmar la transacción
            messagebox.showinfo("Éxito", "Ubicación insertada correctamente.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar ubicación: {
                err}")
        # Función para cambiar el color de fondo cuando se pasa el cursor (hover effect)
        ubicacion_entry.delete(0, tk.END)  # Borra el contenido del Entry
    def on_enter(button, event):
        button.config(bg="#45a049", fg="white")

    def on_leave(button, event):
        button.config(bg="#4CAF50", fg="white")

    # Botón para agregar la ubicación
    agregar_button = tk.Button(ubicacion, text="Agregar Ubicacion", command=obtener_ubicacion, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", width=20)
    agregar_button.pack(pady=10)
    
    # Efectos de hover para el botón
    agregar_button.bind("<Enter>", lambda event, button=agregar_button: on_enter(button, event))
    agregar_button.bind("<Leave>", lambda event, button=agregar_button: on_leave(button, event))

    def cerrar_unidad_ventana():
        ubicacion.destroy()  # Cierra la ventana de unidad
        cambiar_ventana(agregar_maquinaria)  # Regresa a la ventana de agregar maquinaria

    ubicacion.protocol("WM_DELETE_WINDOW", cerrar_unidad_ventana)  # Cierra correctamente cuando se cierra la ventana de unidad
    ventana_activa = ubicacion  # Guardar referencia de la ventana actual

def abrir_clientes():
    global ventana_activa   
    root.withdraw()  # Oculta la ventana principal
    clientes = tk.Toplevel(root)  # Crea la ventana secundaria  
    clientes.title("Agregar Clientes")
    clientes.geometry("300x200")  # Tamaño de la ventana
    centrar_ventana(clientes, 300, 200, offset_y=150)

    image = Image.open("C:/Users/PC/caliz/fondo_marca.jpg")
    background_image = ImageTk.PhotoImage(image)
    # Crear un label para la imagen de fondo
    background_label = tk.Label(clientes, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Cubrir toda la ventana
    clientes.background_image = background_image 

    # Label para el título
    tk.Label(clientes, text="Agregar Cliente", font=("Arial", 14, "bold"), bg="blue", fg="white").pack(pady=10)

    # Label y Entry para ingresar la ubicación
    tk.Label(clientes, text="Cliente:", bg="blue", fg="white", font=("Arial", 12)).pack(pady=5)
    clientes_entry = tk.Entry(clientes, font=("Arial", 12), width=25, bd=2, relief="solid")
    clientes_entry.pack(pady=10)
    clientes_entry.bind("<KeyRelease>", convertir_mayusculas)

    # Función para manejar lo que se escribe en el Entry
    def obtener_clientes():
        ubicacion = clientes_entry.get().strip()  # Obtiene lo que el usuario escribió y elimina espacios
        if not ubicacion:
            messagebox.showwarning("Advertencia", "La ubicación no puede estar vacía.")
            return

        try:
            conectar_bd()  # Conectar a la base de datos si no está conectado

            # Ejecutar la consulta SQL para insertar la ubicación
            query = "INSERT INTO cliente (nombre) VALUES (%s)"
            cursor.execute(query, (ubicacion,))
            conexion.commit()  # Confirmar la transacción
            messagebox.showinfo("Éxito", "Ubicación insertada correctamente.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar ubicación: {
                err}")
        # Función para cambiar el color de fondo cuando se pasa el cursor (hover effect)
        clientes_entry.delete(0, tk.END)  # Borra el contenido del Entry
    def on_enter(button, event):
        button.config(bg="#45a049", fg="white")

    def on_leave(button, event):
        button.config(bg="#4CAF50", fg="white")

    # Botón para agregar la ubicación
    agregar_button = tk.Button(clientes, text="Agregar Clientes", command=obtener_clientes, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", width=20)
    agregar_button.pack(pady=10)
    
    # Efectos de hover para el botón
    agregar_button.bind("<Enter>", lambda event, button=agregar_button: on_enter(button, event))
    agregar_button.bind("<Leave>", lambda event, button=agregar_button: on_leave(button, event))

    def cerrar_unidad_ventana():
        clientes.destroy()  # Cierra la ventana de unidad
        cambiar_ventana(agregar_maquinaria)  # Regresa a la ventana de agregar maquinaria

    clientes.protocol("WM_DELETE_WINDOW", cerrar_unidad_ventana)  # Cierra correctamente cuando se cierra la ventana de unidad
    ventana_activa = clientes  # Guardar referencia de la ventana actual

def abrir_clasificacion():
    global ventana_activa
    root.withdraw()  # Oculta la ventana principal
    clasificacion = tk.Toplevel(root)  # Crea la ventana secundaria
    clasificacion.title("Agregar Clasificación")
    clasificacion.geometry("300x200")  # Tamaño de la ventana
    centrar_ventana(clasificacion, 300, 200, offset_y=150)

    image = Image.open("C:/Users/PC/caliz/fondo_marca.jpg")
    background_image = ImageTk.PhotoImage(image)
    # Crear un label para la imagen de fondo
    background_label = tk.Label(clasificacion, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Cubrir toda la ventana
    clasificacion.background_image = background_image 

    # Label para el título
    tk.Label(clasificacion, text="Agregar Clasificación", font=("Arial", 14, "bold"), bg="blue", fg="white").pack(pady=10)

    # Label y Entry para ingresar la ubicación
    tk.Label(clasificacion, text="Clasificación:", bg="blue", fg="white", font=("Arial", 12)).pack(pady=5)
    clasificacion_entry = tk.Entry(clasificacion, font=("Arial", 12), width=25, bd=2, relief="solid")
    clasificacion_entry.pack(pady=10)
    clasificacion_entry.bind("<KeyRelease>", convertir_mayusculas)

    # Función para manejar lo que se escribe en el Entry
    def obtener_clasificacion():
        ubicacion = clasificacion_entry.get().strip()  # Obtiene lo que el usuario escribió y elimina espacios
        if not ubicacion:
            messagebox.showwarning("Advertencia", "La ubicación no puede estar vacía.")
            return

        try:
            conectar_bd()  # Conectar a la base de datos si no está conectado

            # Ejecutar la consulta SQL para insertar la ubicación
            query = "INSERT INTO clasificacion (nombreClasificacion) VALUES (%s)"
            cursor.execute(query, (ubicacion,))
            conexion.commit()  # Confirmar la transacción
            messagebox.showinfo("Éxito", "Ubicación insertada correctamente.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar ubicación: {
                err}")
            
        clasificacion_entry.delete(0, tk.END)  # Borra el contenido del Entry
    def on_enter(button, event):
                button.config(bg="#45a049", fg="white")

    def on_leave(button, event):
                button.config(bg="#4CAF50", fg="white")

        # Botón para agregar la ubicación
    agregar_button = tk.Button(clasificacion, text="Agregar Clasifiacion", command=obtener_clasificacion, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", width=20)
    agregar_button.pack(pady=10)
            
        # Efectos de hover para el botón
    agregar_button.bind("<Enter>", lambda event, button=agregar_button: on_enter(button, event))
    agregar_button.bind("<Leave>", lambda event, button=agregar_button: on_leave(button, event))

    def cerrar_unidad_ventana():
        clasificacion.destroy()  # Cierra la ventana de unidad
        cambiar_ventana(agregar_maquinaria)  # Regresa a la ventana de agregar maquinaria

    clasificacion.protocol("WM_DELETE_WINDOW", cerrar_unidad_ventana)  # Cierra correctamente cuando se cierra la ventana de unidad
    ventana_activa = clasificacion  # Guardar referencia de la ventana actual

def abrir_operador():
    global ventana_activa
    root.withdraw()  # Oculta la ventana principal
    operador = tk.Toplevel(root)  # Crea la ventana secundaria
    operador.title("Agregar Operador")
    operador.geometry("300x200")  # Tamaño de la ventana
    centrar_ventana(operador, 300, 200, offset_y=150)

    image = Image.open("C:/Users/PC/caliz/fondo_marca.jpg")
    background_image = ImageTk.PhotoImage(image)
    # Crear un label para la imagen de fondo
    background_label = tk.Label(operador, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Cubrir toda la ventana
    operador.background_image = background_image 

    # Label para el título
    tk.Label(operador, text="Agregar Operador", font=("Arial", 14, "bold"), bg="blue", fg="white").pack(pady=10)

    # Label y Entry para ingresar la operador
    tk.Label(operador, text="Operador:", bg="blue", fg="white", font=("Arial", 12)).pack(pady=5)
    operador_entry = tk.Entry(operador, font=("Arial", 12), width=25, bd=2, relief="solid")
    operador_entry.pack(pady=10)
    operador_entry.bind("<KeyRelease>", convertir_mayusculas)

    # Función para manejar lo que se escribe en el Entry
    def obtener_operador():
        ubicacion = operador_entry.get().strip()  # Obtiene lo que el usuario escribió y elimina espacios
        if not ubicacion:
            messagebox.showwarning("Advertencia", "EL operador no puede estar vacía.")
            return

        try:
            conectar_bd()  # Conectar a la base de datos si no está conectado

            # Ejecutar la consulta SQL para insertar la operador
            query = "INSERT INTO operador (nombre) VALUES (%s)"
            cursor.execute(query, (ubicacion,))
            conexion.commit()  # Confirmar la transacción
            messagebox.showinfo("Éxito", "operador insertada correctamente.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar operador: {
                err}")
            
        operador_entry.delete(0, tk.END)  # Borra el contenido del Entry
    def on_enter(button, event):
                button.config(bg="#45a049", fg="white")

    def on_leave(button, event):
                button.config(bg="#4CAF50", fg="white")

        # Botón para agregar la operador
    agregar_button = tk.Button(operador, text="Agregar Operador", command=obtener_operador, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", width=20)
    agregar_button.pack(pady=10)
            
        # Efectos de hover para el botón
    agregar_button.bind("<Enter>", lambda event, button=agregar_button: on_enter(button, event))
    agregar_button.bind("<Leave>", lambda event, button=agregar_button: on_leave(button, event))

    def cerrar_unidad_ventana():
        operador.destroy()  # Cierra la ventana de unidad
        cambiar_ventana(agregar_maquinaria)  # Regresa a la ventana de agregar maquinaria

    operador.protocol("WM_DELETE_WINDOW", cerrar_unidad_ventana)  # Cierra correctamente cuando se cierra la ventana de unidad
    ventana_activa = operador  # Guardar referencia de la ventana actual

   
class PanelBase(tk.Toplevel):
    def __init__(self, master, titulo, consulta_select, consulta_update, consulta_delete):
        super().__init__(master)
        self.title(titulo)
        global ventana_activa, ventana_anterior 
        self.geometry("400x300")
        centrar_ventana(self, 400, 300, offset_y=150)
        if ventana_activa is not None:
            ventana_anterior = ventana_activa  # Guardamos la referencia de la anterior
            ventana_activa.withdraw()  # Ocultamos la ventana anterior

        ventana_activa = self  # Esta ventana se vuelve la activa

        # Configurar el comportamiento al cerrar
        self.protocol("WM_DELETE_WINDOW", self.cerrar_y_regresar)

        self.consulta_select = consulta_select
        self.consulta_update = consulta_update
        self.consulta_delete = consulta_delete

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.pack(expand=True, fill="both")

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        btn_modificar = tk.Button(frame_botones, text="Modificar", command=self.modificar_registro)
        btn_modificar.pack(side="left", padx=5)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=self.eliminar_registro)
        btn_eliminar.pack(side="left", padx=5)

        self.cargar_datos()
    def cerrar_y_regresar(self):
        """Cierra la ventana actual y regresa a la ventana anterior."""
        global ventana_activa, ventana_anterior

        self.destroy()  # Cierra la ventana actual

        if ventana_anterior is not None:
            ventana_anterior.deiconify()  # Muestra la ventana anterior
            ventana_activa = ventana_anterior  # La volvemos la ventana activa
            ventana_anterior = None  # Limpiamos la referencia a la ventana anterior
    

    def cargar_datos(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            conectar_bd()  # Llamamos a tu función de conexión
            cursor.execute(self.consulta_select)
            for registro in cursor.fetchall():
                self.tree.insert("", tk.END, values=registro)
        except mysql.connector.Error as err:
            print(f"Error al obtener los datos: {err}")

    def modificar_registro(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un registro para modificar.")
            return

        item = self.tree.item(seleccionado)
        datos = item['values']

        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.title("Modificar Registro")

        tk.Label(ventana_edicion, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_edicion)
        entry_nombre.insert(0, datos[1])
        entry_nombre.pack()

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get().strip()
            if not nuevo_nombre:
                messagebox.showwarning("Atención", "El nombre no puede estar vacío.")
                return

            try:
                conectar_bd()  # Conectamos antes de ejecutar la consulta
                cursor.execute(self.consulta_update, (nuevo_nombre, datos[0]))
                conexion.commit()

                messagebox.showinfo("Éxito", "Registro modificado correctamente.")
                self.cargar_datos()
                ventana_edicion.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al modificar el registro: {err}")

        tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios).pack()

    def eliminar_registro(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un registro para eliminar.")
            return

        item = self.tree.item(seleccionado)
        id_registro = item['values'][0]

        respuesta = messagebox.askyesno("Confirmación", "¿Seguro que deseas eliminar este registro?")
        if respuesta:
            try:
                conectar_bd()  # Aseguramos la conexión
                cursor.execute(self.consulta_delete, (id_registro,))
                conexion.commit()

                messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
                self.cargar_datos()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar el registro: {err}")
      
class PanelMarcas(PanelBase):
    def __init__(self, master):
        super().__init__(
            master, 
            "Panel de Marcas", 
            "SELECT idmarcas, nombre FROM marcas",
            "UPDATE marcas SET nombre=%s WHERE idmarcas=%s",
            "DELETE FROM marcas WHERE idmarcas=%s"
        )
class PanelClientes(PanelBase):
    def __init__(self, master):
        super().__init__(
            master, 
            "Panel de Clientes", 
            "SELECT idcliente, nombre FROM cliente",
            "UPDATE cliente SET nombre=%s WHERE idcliente=%s",
            "DELETE FROM cliente WHERE idcliente=%s"
        )
class PanelUbicaciones(PanelBase):
    def __init__(self, master):
        super().__init__(
            master, 
            "Panel de Ubicaciones", 
            "SELECT idubicaciones, nombres FROM ubicaciones",
            "UPDATE ubicaciones SET nombres=%s WHERE idubicaciones=%s",
            "DELETE FROM ubicaciones WHERE idubicaciones=%s"
        )
class PanelOperador(PanelBase):
    def __init__(self, master):
        super().__init__(
            master, 
            "Panel de Operador",
            "SELECT idoperador, nombre FROM operador", 
            "UPDATE operador SET nombre=%s WHERE idoperador=%s",
            "DELETE FROM operador WHERE idoperador=%s"
        )
class PanelUnidad(PanelBase):
    def __init__(self, master):
        super().__init__(
            master, 
            "Panel de Unidad",
            "SELECT idunidad, no_economico FROM unidad",
            "UPDATE unidad SET no_economico=%s WHERE idunidad=%s",
            "DELETE FROM unidad WHERE idunidad=%s"
        )
class PanelClasificacion(PanelBase):
    def __init__(self, master):
        super().__init__(
            master, 
            "Panel de Clasificación",
            "SELECT idclasificacion, nombreClasificacion FROM clasificacion",
            "UPDATE clasificacion SET nombreClasificacion=%s WHERE idclasificacion=%s",
            "DELETE FROM clasificacion WHERE idclasificacion=%s"
        )


def abrir_panel_clientes():
    PanelClientes(root)
def abrir_panel_ubicaciones():
    PanelUbicaciones(root)    
def abrir_panel_marcas():
    PanelMarcas(root)
def abrir_panel_operador():
    PanelOperador(root)
def abrir_panel_unidad():
    PanelUnidad(root)
def abrir_panel_clasificacion():
    PanelClasificacion(root)


def obtener_datos(tabla, columna):
    """Obtiene datos de una tabla y columna específica."""
    try:
        conectar_bd()  # Asegura que la conexión esté activa
        if conexion and conexion.is_connected():
            cursor = conexion.cursor()
            query = f"SELECT {columna} FROM {tabla}"
            cursor.execute(query)
            datos = cursor.fetchall()
            return [fila[0] for fila in datos] if datos else []
        else:
            print(f"❌ No se pudo conectar a la base de datos para obtener {columna} de {tabla}.")
            return []
    except Exception as e:
        print(f"⚠️ Error al obtener datos de {tabla}: {e}")
        return []

def llenar_combobox(combobox, datos):
    """Llena un combobox con los datos obtenidos."""
    if datos:
        combobox["values"] = [""]+ datos
        combobox.current(0)  # Seleccionar el primer valor por defecto
    else:
        combobox["values"] = ["(Sin datos)"]
        combobox.current(0)

def obtener_datos(tabla, columnas="*", condicion=None):
    """Obtiene datos de una tabla con las columnas especificadas y una condición opcional."""
    conectar_bd()
    try:
        query = f"SELECT {columnas} FROM {tabla}"
        if condicion:
            query += f" WHERE {condicion}"
        
        cursor.execute(query)
        datos = cursor.fetchall()

        # Si solo se pidió una columna, devolver una lista plana
        if "," not in columnas and columnas != "*":
            return [fila[0] for fila in datos] if datos else []
        return datos
    except Exception as e:
        print(f"⚠️ Error al obtener datos de {tabla}: {e}")
        return []

def ejecutar_query(query, valores=None):
    conectar_bd()  # Asegurar que la conexión está activa
    try:
        if valores:
            cursor.execute(query, valores)
        else:
            cursor.execute(query)
        conexion.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error al ejecutar la consulta: {err}")
        return False
    
def obtener_maquinas():
    query = """
        SELECT m.idmaquina, u.No_Economico 
        FROM maquina m
        JOIN unidad u ON m.unidad_idUnidad = u.idUnidad
    """
    conectar_bd()
    cursor.execute(query)
    maquinas = cursor.fetchall()
    return maquinas

def obtener_id(tabla, columna, valor):
    try:
        conectar_bd()
        if conexion and conexion.is_connected():
            cursor = conexion.cursor()
            query = f"SELECT id{tabla} FROM {tabla} WHERE {columna} = %s"
            cursor.execute(query, (valor,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        print(f"⚠️ Error al obtener ID de {tabla}: {e}")
        return None

def validar_anio(entrada):
    """Permite solo números de 4 dígitos en el Entry."""
    return entrada.isdigit() and len(entrada) <= 4

def cerrar_editar_y_volver_a_registro():
    ventana.destroy()
    abrir_panel_registro_maquina()

def abrir_editar_eliminar_maquina():
    global ventana, combo_maquina, entry_modelo, entry_no_serie, entry_ano, entry_placas
    global combo_marca, combo_cliente, combo_clasificacion  
    global ventana_activa

    root.withdraw()
    ventana = tk.Toplevel()
    ventana.title("Editar/Eliminar Máquina")
    ventana.geometry("420x400")
    ventana.resizable(False, False)
    centrar_ventana(ventana, 420, 400, offset_y=100)
    ventana.configure(bg="#f5f5f5")  # Fondo gris claro

    # Cargar imagen de fondo
    imagen_fondo = Image.open("C:/Users/PC/caliz/fondo_maquinaria.jpg")  # Ruta de tu imagen
    imagen_fondo = imagen_fondo.resize((420, 450))  # Ajustar tamaño a la ventana
    fondo_tk = ImageTk.PhotoImage(imagen_fondo)

    # Label para la imagen de fondo
    fondo_label = tk.Label(ventana, image=fondo_tk)
    fondo_label.place(relwidth=1, relheight=1)  # Expande la imagen en toda la ventana
    ventana.fondo_tk = fondo_tk  # Guardar la imagen para que no se borre

    # Etiqueta y ComboBox para seleccionar máquina
    tk.Label(ventana, text="Seleccionar Máquina:", font=("Arial", 10, "bold"), bg="#f5f5f5").grid(row=0, column=0, pady=10, padx=10, sticky="e")
    combo_maquina = ttk.Combobox(ventana, state="readonly", width=30)
    combo_maquina.grid(row=0, column=1, pady=10, padx=10, sticky="w")
    combo_maquina.bind("<<ComboboxSelected>>", cargar_datos)
    
    maquinas = obtener_maquinas()
    llenar_combobox(combo_maquina, [f"{m[0]} - {m[1]}" for m in maquinas])

    # Labels y campos de entrada
    labels = ["Modelo:", "No. Serie:", "Año:", "Placas:"]
    entries = []
    style = ttk.Style()
    style.configure("Custom.TCombobox", background="white", fieldbackground="white", bordercolor="#cccccc")
    style.configure("Custom.TEntry", fieldbackground="white", bordercolor="#cccccc")
    for i, label in enumerate(labels):
        tk.Label(ventana, text=label, font=("Arial", 10), bg="#f5f5f5").grid(row=i+1, column=0, pady=5, padx=10, sticky="e")
        entry = tk.Entry(ventana, width=30, font=("Arial", 10))
        entry.grid(row=i+1, column=1, pady=5, padx=10, sticky="w")
        entries.append(entry)

    entry_modelo, entry_no_serie, entry_ano, entry_placas = entries

    # Foreign keys (Combobox)
    foreign_keys = [
        ("Marca:", "marcas", "nombre"),
        ("Cliente:", "cliente", "nombre"),
        ("Clasificación:", "clasificacion", "nombreClasificacion")
    ]
    combos = []
    for i, (label, table, column) in enumerate(foreign_keys):
        tk.Label(ventana, text=label, font=("Arial", 10), bg="#f5f5f5").grid(row=i+5, column=0, pady=5, padx=10, sticky="e")
        combo = ttk.Combobox(ventana, state="readonly", width=30)
        combo.grid(row=i+5, column=1, pady=5, padx=10, sticky="w")
        llenar_combobox(combo, obtener_datos(table, column))
        combos.append(combo)

    combo_marca, combo_cliente, combo_clasificacion = combos

    # Frame para centrar los botones
    frame_botones = tk.Frame(ventana, bg="red")
    frame_botones.grid(row=8, column=0, columnspan=2, pady=15)

    # Botones con diseño mejorado
    btn_guardar = tk.Button(frame_botones, text="Guardar Cambios", width=16, bg="#4CAF50", fg="white",
                            font=("Arial", 10, "bold"), command=guardar_cambios)
    btn_guardar.pack(side=tk.LEFT, padx=10, ipadx=5)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar Máquina", width=16, bg="#D32F2F", fg="white",
                            font=("Arial", 10, "bold"), command=eliminar_maquina)
    btn_eliminar.pack(side=tk.LEFT, padx=10, ipadx=5)


    ventana.protocol("WM_DELETE_WINDOW", cerrar_editar_y_volver_a_registro)

def cargar_datos(event):
    seleccion = combo_maquina.get()
    if not seleccion:
        return
    
    id_maquina = seleccion.split(" - ")[0]  # Extraer ID de la máquina

    # Obtener datos de la máquina
    datos = obtener_datos(
        "maquina", 
        "modelo, no_serie, año, placas, marcas_idmarcas, cliente_idcliente, clasificacion_idclasificacion", 
        f"idmaquina = {id_maquina}"
    )
    
    if datos:
        datos = datos[0]  # Extraer la primera fila
        entry_modelo.delete(0, tk.END)
        entry_modelo.insert(0, datos[0])
        entry_no_serie.delete(0, tk.END)
        entry_no_serie.insert(0, datos[1])
        entry_ano.delete(0, tk.END)
        entry_ano.insert(0, datos[2])
        entry_placas.delete(0, tk.END)
        entry_placas.insert(0, datos[3])

        # Cargar valores en los combobox de Foreign Keys
        id_marca, id_cliente, id_clasificacion = datos[4], datos[5], datos[6]
        
        combo_marca.set(obtener_datos("marcas", "nombre", f"idmarcas = {id_marca}")[0])
        combo_cliente.set(obtener_datos("cliente", "nombre", f"idcliente = {id_cliente}")[0])
        combo_clasificacion.set(obtener_datos("clasificacion", "nombreClasificacion", f"idclasificacion = {id_clasificacion}")[0])
    

def guardar_cambios():
    seleccion = combo_maquina.get()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione una máquina")
        return

    id_maquina = seleccion.split(" - ")[0]
    nuevo_modelo = entry_modelo.get()
    nuevo_no_serie = entry_no_serie.get()
    nuevo_ano = entry_ano.get()
    nuevas_placas = entry_placas.get()
    nombre_marca, nombre_cliente, nombre_clasificacion = combo_marca.get(), combo_cliente.get(), combo_clasificacion.get()
    
    id_marca = obtener_id("marcas", "nombre", nombre_marca)
    id_cliente = obtener_id("cliente", "nombre", nombre_cliente)
    id_clasificacion = obtener_id("clasificacion", "nombreClasificacion", nombre_clasificacion)

    if None in [id_marca, id_cliente, id_clasificacion]:
        messagebox.showerror("Error", "Uno o más valores no son válidos.")
        return

    query = """
        UPDATE maquina
        SET modelo = %s, no_serie = %s, año = %s, placas = %s, 
            marcas_idmarcas = %s, cliente_idcliente = %s, clasificacion_idclasificacion = %s
        WHERE idmaquina = %s
    """
    
    if ejecutar_query(query, (nuevo_modelo, nuevo_no_serie, nuevo_ano, nuevas_placas, id_marca, id_cliente, id_clasificacion, id_maquina)):
        messagebox.showinfo("Éxito", "Datos actualizados correctamente")
        
    return ventana

def eliminar_maquina():
    seleccion = combo_maquina.get()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione una máquina")
        return

    id_maquina = seleccion.split(" - ")[0]
    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta máquina?"):
        if ejecutar_query("DELETE FROM maquina WHERE idmaquina = %s", (id_maquina,)):
            messagebox.showinfo("Éxito", "Máquina eliminada correctamente")
            ventana.destroy()
            abrir_panel_registro_maquina()
    

def cambiar_a_editar():
    global ventana_activa
    if ventana_activa is not None:  # Si hay una ventana abierta, cerrarla
        ventana_activa.destroy()
        ventana_activa = None  # Limpiar referencia para evitar errores

    abrir_editar_eliminar_maquina()  # Abre la nueva ventana

def conectar_bd2():
    global conexion, cursor
    if conexion is None or not conexion.is_connected():
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",  # Reemplaza con tu usuario de MySQL
                password="",  # Reemplaza con tu contraseña de MySQL
                database="pruebas"
            )
            cursor = conexion.cursor()
            print("Conexión a la base de datos establecida.")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

            
def abrir_panel_registro_maquina():
    global ventana_activa
    root.withdraw()  # Ocultar la ventana principal
    ventana = tk.Toplevel()
    ventana.title("Registro de Máquina")
    ventana.geometry("400x400")  # Tamaño de la ventana
    ventana.resizable(False, False)  # Evitar que se pueda cambiar el tamaño
    centrar_ventana(ventana, 400, 400, offset_y=150)


    image = Image.open("C:/Users/PC/caliz/fondo_maquinaria.jpg")
    background_image = ImageTk.PhotoImage(image)
    # Crear un label para la imagen de fondo
    background_label = tk.Label(ventana, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Cubrir toda la ventana
    ventana.background_image = background_image 

    # Crear menú
    menubar = tk.Menu(ventana)
    ventana.config(menu=menubar)
    
    submenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opciones", menu=submenu)
    submenu.add_command(label="Editar Máquina", command=cambiar_a_editar)
    
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=1)

    for i in range(9):
        ventana.grid_rowconfigure(i, weight=1)

    # Estilo para Combobox
    style = ttk.Style()
    style.configure("Estilo.TCombobox",
                    fieldbackground="#f0f0f0",  # Fondo de texto
                    background="white",        # Fondo desplegable
                    foreground="black",        # Color del texto
                    font=("Arial", 10))

    # Estilo de los Entry
    entry_style = {"bg": "#e6e6e6", "fg": "black", "font": ("Arial", 10), "relief": "solid", "insertbackground": "black"}
    
    # Labels y campos con diseño
    tk.Label(ventana, text="Año:", bg="#800080", fg="white").grid(row=0, column=0, pady=5, padx=20, sticky="e")
    # Validación del Entry
    vcmd = ventana.register(validar_anio)  # Registra la función para validación
    entry_anio = tk.Entry(ventana, **entry_style, validate="key", validatecommand=(vcmd, "%P"))
    entry_anio.grid(row=0, column=1, pady=5, padx=20, sticky="nsew")

    tk.Label(ventana, text="Placas:", bg="#800080", fg="white").grid(row=1, column=0, pady=5, padx=20, sticky="e")
    entry_placas = tk.Entry(ventana, **entry_style)
    entry_placas.grid(row=1, column=1, pady=5, padx=20, sticky="nsew")

    tk.Label(ventana, text="Modelo:", bg="#800080", fg="white").grid(row=2, column=0, pady=5, padx=20, sticky="e")
    entry_modelo = tk.Entry(ventana, **entry_style)
    entry_modelo.grid(row=2, column=1, pady=5, padx=20, sticky="nsew")

    tk.Label(ventana, text="No. Serie:", bg="#800080", fg="white").grid(row=3, column=0, pady=5, padx=20, sticky="e")
    entry_no_serie = tk.Entry(ventana, **entry_style)
    entry_no_serie.grid(row=3, column=1, pady=5, padx=20, sticky="nsew")

    tk.Label(ventana, text="Marca:", bg="#800080", fg="white").grid(row=4, column=0, pady=5, padx=20, sticky="e")
    combo_marca = ttk.Combobox(ventana, state="readonly", style="Estilo.TCombobox")
    combo_marca.grid(row=4, column=1, pady=10, padx=20, sticky="nsew")

    tk.Label(ventana, text="Cliente:", bg="#800080", fg="white").grid(row=5, column=0, pady=5, padx=20, sticky="e")
    combo_cliente = ttk.Combobox(ventana, state="readonly", style="Estilo.TCombobox")
    combo_cliente.grid(row=5, column=1, pady=10, padx=20, sticky="nsew")

    tk.Label(ventana, text="Numero Economico:", bg="#800080", fg="white").grid(row=6, column=0, pady=5, padx=20, sticky="e")
    combo_unidad = ttk.Combobox(ventana, state="readonly", style="Estilo.TCombobox")
    combo_unidad.grid(row=6, column=1, pady=10, padx=20, sticky="nsew")

    tk.Label(ventana, text="Clasificación:", bg="#800080", fg="white").grid(row=7, column=0, pady=5, padx=20, sticky="e")
    combo_clasificacion = ttk.Combobox(ventana, state="readonly", style="Estilo.TCombobox")
    combo_clasificacion.grid(row=7, column=1, pady=10, padx=20, sticky="nsew")

    def limpiar_campos():
        entry_anio.config(validate="none")  # Desactiva la validación
        entry_anio.delete(0, tk.END)
        entry_placas.delete(0, tk.END)
        entry_modelo.delete(0, tk.END)
        entry_no_serie.delete(0, tk.END)
        combo_marca.set("")
        combo_cliente.set("")
        combo_unidad.set("")
        combo_clasificacion.set("")
        entry_anio.config(validate="key")

    def guardar_maquina():
        año = entry_anio.get()
        placas = entry_placas.get()
        modelo = entry_modelo.get()
        no_serie = entry_no_serie.get()
        marca = combo_marca.get()
        cliente = combo_cliente.get()
        unidad = combo_unidad.get()
        clasificacion = combo_clasificacion.get()

        if not all([año, modelo, marca, cliente, unidad, clasificacion]):
            messagebox.showerror("Error", "Todos los campos obligatorios deben llenarse")
            return

        id_marca = obtener_id("marcas", "nombre", marca)
        id_cliente = obtener_id("cliente", "nombre", cliente)
        id_unidad = obtener_id("unidad", "No_Economico", unidad)
        id_clasificacion = obtener_id("clasificacion", "nombreClasificacion", clasificacion)

        query_verificar = """
            SELECT 1 FROM maquina
            WHERE unidad_idUnidad = %s
        """

        query_insertar = """
            INSERT INTO maquina (
                año, placas, modelo, no_serie,
                marcas_idmarcas, cliente_idcliente,
                unidad_idUnidad, clasificacion_idclasificacion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores_insertar = (
            año, placas, modelo, no_serie,
            id_marca, id_cliente, id_unidad, id_clasificacion
        )

        conexion = conectar_bd2()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        try:
            with conexion.cursor() as cursor:
                cursor.execute(query_verificar, (id_unidad,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Ya existe una máquina con ese número económico o placas")
                    return

                cursor.execute(query_insertar, valores_insertar)
                conexion.commit()
                messagebox.showinfo("Éxito", "Máquina registrada correctamente")
                limpiar_campos()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar la máquina: {e}")
            print(e)
        finally:
            if conexion.is_connected():
                conexion.close()
        

    # Botón de Guardar con diseño
    btn_guardar = tk.Button(ventana, text="Guardar", width=15, bg="#4CAF50", fg="white",
                            font=("Arial", 10, "bold"), command=guardar_maquina)
    btn_guardar.grid(row=8, column=0, pady=15, padx=10, sticky="e")

    # Botón de Cancelar con diseño
    btn_cancelar = tk.Button(ventana, text="Cancelar", width=15, bg="#FFC107", fg="white",
                            font=("Arial", 10, "bold"),command=limpiar_campos)  # Cierra la ventana
    btn_cancelar.grid(row=8, column=1, pady=15, padx=10, sticky="w")

    llenar_combobox(combo_marca, obtener_datos("marcas", "nombre"))
    llenar_combobox(combo_cliente, obtener_datos("cliente", "nombre"))
    llenar_combobox(combo_unidad, obtener_datos("unidad", "No_Economico"))
    llenar_combobox(combo_clasificacion, obtener_datos("clasificacion", "nombreClasificacion"))

    def cerrar_nueva_ventana():
        ventana.destroy()
        root.deiconify()  # Mostrar la ventana principal

    ventana.protocol("WM_DELETE_WINDOW", cerrar_nueva_ventana)
    ventana_activa = ventana  # Guardar referencia

    return ventana

def cambiar_foco(event, siguiente_widget):
    siguiente_widget.focus_set()

def calcular_horas_trabajadas(event, entry_inicial, entry_final, entry_horas_trabajadas):
    try:
        # Obtener los valores de los horómetros
        horometro_inicial = float(entry_inicial.get())
        horometro_final = float(entry_final.get())

        if horometro_inicial > horometro_final:
            entry_horas_trabajadas.config(state="normal")
            entry_horas_trabajadas.delete(0, tk.END)
            
            # Resaltar los campos en rojo para indicar error
            entry_inicial.config(bg="red")
            entry_final.config(bg="red")
            return  # Salir sin calcular
        
        # Restaurar colores normales si la validación pasa
        entry_inicial.config(bg="black")
        entry_final.config(bg="black")
        # Calcular horas trabajadas
        horas_trabajadas = horometro_final - horometro_inicial

        # Convertir la diferencia a horas y minutos
        horas = int(horas_trabajadas)  # Parte entera como horas completas
        minutos = (horas_trabajadas - horas) * 60  # Convertir el decimal a minutos

        # Insertar el resultado en el campo de horas trabajadas
        entry_horas_trabajadas.config(state="normal")
        entry_horas_trabajadas.delete(0, tk.END)
        entry_horas_trabajadas.insert(0, f"{horas:02}:{int(minutos):02}:00")  # Formato HH:MM:SS
        entry_horas_trabajadas.config(state="readonly")

    except ValueError:
        entry_horas_trabajadas.config(state="normal")
        entry_horas_trabajadas.delete(0, tk.END)
        entry_horas_trabajadas.insert(0, "Error")
        entry_horas_trabajadas.config(state="readonly")

def obtener_maquinas_para_combobox():
    try:
        conectar_bd()
        if conexion and conexion.is_connected():
            cursor = conexion.cursor()
            query = """
                SELECT m.idmaquina, u.No_Economico
                FROM maquina m
                JOIN unidad u ON m.unidad_idUnidad = u.idUnidad
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
    except Exception as e:
        print(f"⚠️ Error al obtener máquinas para el Combobox: {e}")
        return []
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def abrir_panel_reporte():
    global ventana_activa, root
    root.withdraw()  # Ocultar la ventana principal
    ventana = tk.Toplevel()
    ventana.title("Registro de Reporte")
    ventana.geometry("700x700")  # Aumenté la altura para más espacio
    ventana.resizable(False, False)
    centrar_ventana(ventana, 700, 700, offset_y=150)

    # Cargar imagen de fondo
    image = Image.open("C:/Users/PC/caliz/fondo reporte.jpg")
    image = image.resize((700, 700))  
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(ventana, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    ventana.background_image = background_image

    # Configuración de colores y estilos
    label_fg = "white"
    entry_bg = "#333333"
    entry_fg = "white"
    button_bg = "#4CAF50"
    button_fg = "white"

    entry_style = {"bg": entry_bg, "fg": entry_fg, "font": ("Arial", 10), "relief": "solid", "insertbackground": "white"}

    # Frame principal para organizar los elementos
    frame = tk.Frame(ventana, bg="#222222", bd=5)
    frame.place(relx=0.50, rely=0.45, anchor="center", width=660, height=570)

    # Configurar cuadrícula
    for i in range(14):  # 14 filas por los nuevos campos
        frame.grid_rowconfigure(i, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)

    # Campos del formulario
    labels = [
        "Folio:","Fecha:", "Máquina:", "Operador:", "Ubicación:", "Cliente:", "Horómetro Inicial:", "Horómetro Final:",
        "Horas Trabajadas:", "Diesel (L):", "Horómetro Carga:", "Aceite Hidráulico (L):", "Aceite Motor (L):", "Actividades:",
        "Fallas:", "Servicios:","Reparaciones:"
    ]

    entries = {}  # Diccionario para almacenar los entries
        # Crear el diccionario de mapeo: No_Economico -> idmaquina
    maquinas_data = obtener_maquinas_para_combobox()
    opciones_maquina_texto = [m[1] for m in maquinas_data] # Mostrar solo el No_Economico
    combo_maquina = ttk.Combobox(frame, state="readonly", values=opciones_maquina_texto)
    entries["Máquina:"] = combo_maquina
    maquina_a_id = {m[1]: m[0] for m in maquinas_data}
    ventana.maquina_a_id = maquina_a_id # Guardar como atributo de la ventana

    # Creación de los campos
    for i, label in enumerate(labels):
        tk.Label(frame, text=label, bg="#222222", fg=label_fg, anchor="e").grid(row=i, column=0, pady=5, padx=10, sticky="e")

        if label == "Fecha:":
            hoy = datetime.now().date()
            entry = DateEntry(frame, width=18, background="darkblue", foreground="white", borderwidth=2,
                              date_pattern="yyyy-mm-dd", year=hoy.year, month=hoy.month, day=hoy.day)
        elif label == "Máquina:":
            entry = ttk.Combobox(frame, state="readonly", values=[f"{m[1]}" for m in obtener_maquinas_para_combobox()])
        elif label == "Operador:":
            entry = ttk.Combobox(frame, state="readonly")
            llenar_combobox(entry, obtener_datos("operador", "nombre"))
        elif label == "Ubicación:":
            entry = ttk.Combobox(frame, state="readonly")
            llenar_combobox(entry, obtener_datos("ubicaciones", "nombres"))
        elif label == "Cliente:":
            entry = ttk.Combobox(frame, state="readonly")
            llenar_combobox(entry, obtener_datos("cliente", "nombre"))
        elif label == "Horas Trabajadas:":
            entry = tk.Entry(frame, fg="black")
            entry.config(state="normal")  
        elif label == "Folio:":
            entry = tk.Entry(frame, **entry_style)  # Entrada normal para ingresar el folio
        elif label == "Horómetro Carga:" or label == "Fallas:" or label == "Servicios " or label=="Reparaciones:":
            entry = tk.Entry(frame, **entry_style)
        else:
            entry = tk.Entry(frame, **entry_style)

        entry.grid(row=i, column=1, pady=5, padx=10, sticky="ew")
            
            # Guardar la entrada en el diccionario `entries` con la clave del label
        entries[label] = entry
       
        # Evitar error en el último campo
        if i < len(labels) - 1:
            # Si no es el último campo, pasamos al siguiente
            entry.bind("<Return>", lambda e, next_label=labels[i + 1]: cambiar_foco(e, entries.get(next_label)))
        else:
            # Si es el último campo, enfocamos el botón de guardar
            entry.bind("<Return>", lambda e: btn_guardar.focus_set()) 

    # Asignar función para calcular las horas trabajadas al presionar <Return> en los campos Horómetro Inicial y Horómetro Final
    entry_final = entries["Horómetro Final:"]
    entry_inicial = entries["Horómetro Inicial:"]
    entry_horas_trabajadas = entries["Horas Trabajadas:"]
    entry_final.bind("<Return>", lambda e: calcular_horas_trabajadas(e, entry_inicial, entry_final, entry_horas_trabajadas))

    # Frame para los botones
    button_frame = tk.Frame(ventana, bg="#222222")
    button_frame.place(relx=0.5, rely=0.96, anchor="center")

    def limpiar_campos_formulario():
        for entry in entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('')  # Limpiar combobox
                entries["Folio:"].focus_set()
            else:
                entry.config(state="normal")  # Asegurar que se pueda limpiar
                entry.delete(0, tk.END)       # Limpiar entrada
                if label == "Horas Trabajadas:":
                    entry.config(state="readonly")  # Volver a ponerlo como readonly si así estaba

    # Botones de acción
    btn_guardar = tk.Button(button_frame, text="Guardar", bg=button_bg, fg=button_fg, width=10,command=lambda: guardar_reporte(entries))
    btn_guardar.grid(row=0, column=0, padx=5, pady=10)

    btn_cancelar = tk.Button(button_frame, text="Limpiar", bg="red", fg="white", width=10, command=limpiar_campos_formulario)
    btn_cancelar.grid(row=0, column=1, padx=5, pady=10)

    btn_cancelar = tk.Button(button_frame, text="Editar", bg="orange", fg="white", width=10, command=abrir_editar_reportes)
    btn_cancelar.grid(row=0, column=2, padx=5, pady=10)
    
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), root.deiconify()))  # Cerrar ventana y mostrar la principal
    ventana_activa = ventana  # Guardar referencia

    return ventana

def a_float(valor):
    try:
        return float(valor.strip()) if valor.strip() else 0.0
    except ValueError:
        return 0.0
    
def obtener_datos_query(query, valores=None):
    conectar_bd()  # Asegúrate de que tienes la conexión y el cursor definidos globalmente
    try:
        if valores:
            cursor.execute(query, valores)
        else:
            cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as err:
        print(f"Error al ejecutar la consulta: {err}")
        return []

def eliminar_reporte(tree):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Aviso", "Selecciona un reporte para eliminar")
        return

    valores = tree.item(seleccion[0], "values")
    idreporte = valores[0]  # Asegúrate que esta sea la columna con el ID del reporte

    if not messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este reporte?"):
        return

    try:
        conexion = conectar_bd2()
        with conexion.cursor() as cursor:
            # Obtener el idhistorial_ubicacion relacionado ANTES de borrar el reporte
            cursor.execute("SELECT idhistorial_ubicacion FROM reporte WHERE idreporte = %s", (idreporte,))
            resultado = cursor.fetchone()

            if resultado:
                idhistorial = resultado[0]

                # Eliminar el reporte primero
                cursor.execute("DELETE FROM reporte WHERE idreporte = %s", (idreporte,))
                conexion.commit()

                # Luego eliminar el historial_ubicacion
                cursor.execute("DELETE FROM historial_ubicacion WHERE idhistorial = %s", (idhistorial,))
                conexion.commit()

                messagebox.showinfo("Éxito", "Reporte y su historial eliminados correctamente")
                tree.delete(seleccion[0])
            else:
                messagebox.showerror("Error", "No se encontró historial asociado al reporte")

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo eliminar el reporte: {e}")
        print(e)
    finally:
        if conexion.is_connected():
            conexion.close()

    
def abrir_editar_reportes():
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Reportes")
    ventana_edicion.geometry("1000x500")
    centrar_ventana(ventana_edicion, 1000, 500)

    frame_tree = tk.Frame(ventana_edicion)
    frame_tree.pack(fill=tk.BOTH, expand=True)

    columnas = (
        "idreporte", "folio", "fecha", "maquina", "operador", "ubicacion", "cliente",
        "horometro_inicial", "horometro_final", "horometro_carga", "horas_trabajadas",
        "diesel", "aceite_hidraulico", "aceite_motor", "actividades", "fallas", "servicios", "reparaciones"
    )

    tree = ttk.Treeview(frame_tree, columns=columnas, show="headings")

    # Definir el ancho deseado para cada columna (ajusta estos valores según tus necesidades)
    ancho_columnas = {
        "idreporte": 0,  # No visible
        "folio": 50,
        "fecha": 100,
        "maquina": 100,
        "operador": 120,
        "ubicacion": 120,
        "cliente": 120,
        "horometro_inicial": 120,
        "horometro_final": 120,
        "horometro_carga": 120,
        "horas_trabajadas": 120,
        "diesel": 50,
        "aceite_hidraulico": 50,
        "aceite_motor": 50,
        "actividades": 250,
        "fallas": 200,
        "servicios": 200,
        "reparaciones": 200,
    }

    # Mostrar las columnas y establecer el ancho
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=ancho_columnas[col], anchor="w")

    # Hacer que la columna 'idreporte' no sea visible (stretch=tk.NO)
    tree.column("idreporte", stretch=tk.NO)

    # Agrega Scrollbars
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # Posicionar el Treeview y los Scrollbars
    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    frame_tree.grid_rowconfigure(0, weight=1)
    frame_tree.grid_columnconfigure(0, weight=1)

    # Agrega Scrollbars
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # Posicionar el Treeview y los Scrollbars
    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    frame_tree.grid_rowconfigure(0, weight=1)
    frame_tree.grid_columnconfigure(0, weight=1)

    # Cargar los datos desde la base de datos
    query = """
        SELECT
            r.idreporte,
            r.folio,
            r.fecha_reporte,
            u.No_Economico,
            o.nombre AS nombre_operador,
            ub.nombres AS ubicacion, -- Seleccionamos el nombre de la ubicación
            c.nombre AS cliente,
            r.horometro_inicial,
            r.horometro_final,
            r.horometro_carga,
            r.horas_trabajadas,
            r.diesel,
            r.aceite_hidraulico,
            r.aceite_motor,
            r.actividades,
            r.fallas,
            r.servicios,
            r.reparacion
        FROM reporte r
        JOIN maquina m ON r.idmaquina = m.idmaquina
        JOIN unidad u ON m.unidad_idUnidad = u.idUnidad
        JOIN operador o ON r.idoperador = o.idoperador
        JOIN cliente c ON r.cliente_idcliente = c.idcliente
        JOIN historial_ubicacion hu ON r.idhistorial_ubicacion = hu.idhistorial
        JOIN ubicaciones ub ON hu.idubicaciones = ub.idubicaciones
        ORDER BY r.idreporte;
    """
    registros = obtener_datos_query(query)
    for registro in registros:
        tree.insert("", tk.END, values=registro)

    # Evento para cargar el reporte seleccionado en un nuevo formulario
    def editar_reporte_seleccionado(event):
        item = tree.selection()
        if item:
            valores = tree.item(item, "values")
            cargar_formulario_edicion(valores,tree)
    
    # Menú contextual
    menu_contextual = tk.Menu(ventana_edicion, tearoff=0)
    menu_contextual.add_command(label="Eliminar", command=lambda: eliminar_reporte(tree))

    def mostrar_menu_contextual(event):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            menu_contextual.post(event.x_root, event.y_root)

    tree.bind("<Button-3>", mostrar_menu_contextual)
    tree.bind("<Double-1>", editar_reporte_seleccionado)

def cargar_formulario_edicion(valores,tree):
    ventana_editar = tk.Toplevel()
    ventana_editar.title(f"Editar Reporte - Folio {valores[1]}")
    ventana_editar.geometry("700x700")  # Ajusta la altura si es necesario
    ventana_editar.resizable(False, False)
    centrar_ventana(ventana_editar, 700, 700, offset_y=150)

    # Configuración de colores y estilos (puedes reutilizar los de la ventana de creación)
    label_fg = "white"
    entry_bg = "#333333"
    entry_fg = "white"
    entry_style = {"bg": entry_bg, "fg": entry_fg, "font": ("Arial", 10), "relief": "solid", "insertbackground": "white"}

    contenedor = tk.Frame(ventana_editar, bg="#222222")
    contenedor.pack(fill="both", expand=True, padx=20, pady=20)

    frame = tk.Frame(contenedor, bg="#222222")
    frame.pack(fill="both", expand=True)

    # Configurar cuadrícula
    for i in range(17):  # Ajustar al número total de campos
        frame.grid_rowconfigure(i, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)

    labels = [
        "Folio:", "Fecha:", "Máquina:", "Operador:", "Ubicación:", "Cliente:",
        "Horómetro Inicial:", "Horómetro Final:", "Horómetro Carga:", "Horas Trabajadas:",
        "Diesel (L):", "Aceite Hidráulico (L):", "Aceite Motor (L):",
        "Actividades:", "Fallas:", "Servicios:", "Reparaciones:"
    ]

    entries_editar = {}  # Diccionario para almacenar los widgets de edición

    # Obtener datos para los Combobox
    maquinas_data = obtener_maquinas_para_combobox()
    opciones_operador = obtener_datos("operador", "nombre")
    opciones_ubicacion = obtener_datos("ubicaciones", "nombres")
    opciones_cliente = obtener_datos("cliente", "nombre")

    ventana_editar.maquina_a_id = {maquina[1]: maquina[0] for maquina in maquinas_data}  # Guardar como atributo de la ventana

    for i, label in enumerate(labels):
        tk.Label(frame, text=label, bg="#222222", fg=label_fg, anchor="e").grid(row=i, column=0, pady=5, padx=10, sticky="e")
        
        valor_actual = valores[i + 1]  # Obtener el valor correspondiente

        if label == "Fecha:":
            fecha_dt = datetime.strptime(valor_actual, "%Y-%m-%d").date()
            entry = DateEntry(frame, width=18, background="darkblue", foreground="white", borderwidth=2,
                              date_pattern="yyyy-mm-dd", year=fecha_dt.year, month=fecha_dt.month, day=fecha_dt.day)
        elif label == "Máquina:":
            opciones_maquina_texto = [m[1] for m in maquinas_data]
            entry = ttk.Combobox(frame, state="readonly", values=opciones_maquina_texto)
            # Buscar y seleccionar el valor actual
            for maquina in maquinas_data:
                if maquina[1] == valor_actual:
                    entry.set(valor_actual)
                    break
        elif label == "Operador:":
            entry = ttk.Combobox(frame, state="readonly", values=opciones_operador)
            entry.set(valor_actual)

        elif label == "Ubicación:":
            entry = ttk.Combobox(frame, state="readonly", values=opciones_ubicacion)
            entry.set(valor_actual)

        elif label == "Cliente:":
            entry = ttk.Combobox(frame, state="readonly", values=opciones_cliente)
            entry.set(valor_actual)

        elif label == "Horas Trabajadas:":
            entry = tk.Entry(frame, fg="black")
            entry.config(state="normal")
            entry.insert(0, valor_actual)
            entry.config(state="readonly") # Mantener como readonly en edición también
        else:
            entry = tk.Entry(frame, **entry_style)
            entry.insert(0, valor_actual)
        
        # Agregar el widget a la cuadrícula y al diccionario
        entry.grid(row=i, column=1, pady=5, padx=10, sticky="ew")
        entries_editar[label] = entry
        

    def guardar_cambios_reporte():
        id_reporte = valores[0]
        nuevos_valores = {}
        for label, entry_widget in entries_editar.items():
            nuevos_valores[label] = entry_widget.get().strip()

        def convertir_float_a_hora_string(horas_float):
            segundos = int(horas_float * 3600)
            tiempo = timedelta(seconds=segundos)
            return str(tiempo)  # Convertir a string HH:MM:SS  

        # Después de llenar los campos, calcular las horas trabajadas si los campos de horómetro tienen valores
        inicial_str_editar = entries_editar.get("Horómetro Inicial:", tk.StringVar()).get()
        final_str_editar = entries_editar.get("Horómetro Final:", tk.StringVar()).get()
        horas_trabajadas_entry_editar = entries_editar.get("Horas Trabajadas:")

        if inicial_str_editar and final_str_editar:
            try:
                inicial_editar = float(inicial_str_editar)
                final_editar = float(final_str_editar)
                horas_editar = final_editar - inicial_editar
                hora_formateada = convertir_float_a_hora_string(horas_editar)
                horas_trabajadas_entry_editar.config(state="normal")
                horas_trabajadas_entry_editar.delete(0, tk.END)
                horas_trabajadas_entry_editar.insert(0,hora_formateada)
                horas_trabajadas_entry_editar.config(state="readonly")
            except ValueError:
                hora_formateada = "00:00:00"  # Valor por defecto si falla
        else:
            hora_formateada = "00:00:00"

        nueva_fecha_reporte = nuevos_valores["Fecha:"]
        nuevo_nombre_ubicacion = nuevos_valores["Ubicación:"]
        maquina_texto = nuevos_valores["Máquina:"]

        # Obtener el idmaquina del combobox
        id_maquina_editar = ventana_editar.maquina_a_id.get(maquina_texto)
        nuevo_idubicacion = obtener_id("ubicaciones", "nombres", nuevo_nombre_ubicacion)

        # Obtener el idhistorial_ubicacion actual del reporte (asumiendo que 'valores' lo contiene)
        idhistorial_actual = valores[-1] # Ajusta el índice si es necesario

        # Obtener la idubicaciones actual
        ubicacion_actual_id = obtener_idubicacion_por_idhistorial(idhistorial_actual)

        nuevo_idhistorial = idhistorial_actual # Por defecto, mantenemos el historial actual

        if nuevo_idubicacion != ubicacion_actual_id:
            # Insertar nueva fila en historial_ubicacion solo si la ubicación cambió
            query_historial = """
                INSERT INTO historial_ubicacion (idubicaciones, fecha)
                VALUES (%s, %s)
                """
            valores_historial = (nuevo_idubicacion, nueva_fecha_reporte)

            if ejecutar_query(query_historial, valores_historial):
                conectar_bd()
                nuevo_idhistorial = cursor.lastrowid
            else:
                messagebox.showerror("Error", "No se pudo registrar la nueva ubicación")
                return # Salir de la función si falla la inserción del historial

        query = """
            UPDATE reporte SET
                folio = %s, fecha_reporte = %s, idmaquina = %s,
                idoperador = (SELECT idoperador FROM operador WHERE nombre = %s),
                cliente_idcliente = (SELECT idcliente FROM cliente WHERE nombre = %s),
                horometro_inicial = %s, horometro_final = %s, horometro_carga = %s,
                horas_trabajadas = %s, diesel = %s, aceite_hidraulico = %s,
                aceite_motor = %s, actividades = %s, fallas = %s,
                servicios = %s, reparacion = %s,
                idhistorial_ubicacion = %s
            WHERE idreporte = %s
            """

        valores_sql = (
            nuevos_valores["Folio:"], nuevos_valores["Fecha:"], id_maquina_editar,
            nuevos_valores["Operador:"], nuevos_valores["Cliente:"],
            float(nuevos_valores["Horómetro Inicial:"]), float(nuevos_valores["Horómetro Final:"]), float(nuevos_valores["Horómetro Carga:"]),
            hora_formateada, float(nuevos_valores["Diesel (L):"]), float(nuevos_valores["Aceite Hidráulico (L):"]),
            float(nuevos_valores["Aceite Motor (L):"]), nuevos_valores["Actividades:"], nuevos_valores["Fallas:"],
            nuevos_valores["Servicios:"], nuevos_valores["Reparaciones:"],
            nuevo_idhistorial, id_reporte
        )

        def recargar_tabla_reportes(tree):
            tree.delete(*tree.get_children())
            query_recargar = """
                    SELECT
                        r.idreporte,
                        r.folio,
                        r.fecha_reporte,
                        u.No_Economico,
                        o.nombre AS nombre_operador,
                        ub.nombres AS ubicacion, -- Seleccionamos el nombre de la ubicación
                        c.nombre AS cliente,
                        r.horometro_inicial,
                        r.horometro_final,
                        r.horometro_carga,
                        r.horas_trabajadas,
                        r.diesel,
                        r.aceite_hidraulico,
                        r.aceite_motor,
                        r.actividades,
                        r.fallas,
                        r.servicios,
                        r.reparacion
                    FROM reporte r
                    JOIN maquina m ON r.idmaquina = m.idmaquina
                    JOIN unidad u ON m.unidad_idUnidad = u.idUnidad
                    JOIN operador o ON r.idoperador = o.idoperador
                    JOIN cliente c ON r.cliente_idcliente = c.idcliente
                    JOIN historial_ubicacion hu ON r.idhistorial_ubicacion = hu.idhistorial
                    JOIN ubicaciones ub ON hu.idubicaciones = ub.idubicaciones
                    ORDER BY r.idreporte;
                """
            registros_actualizados = obtener_datos_query(query_recargar)
            for registro in registros_actualizados:
                tree.insert("", tk.END, values=registro)

        if ejecutar_query(query, valores_sql):
            messagebox.showinfo("Éxito", "Reporte actualizado correctamente")
            ventana_editar.destroy()
            recargar_tabla_reportes(tree)
        else:
            messagebox.showerror("Error", "No se pudo actualizar el reporte")

    def obtener_idubicacion_por_idhistorial(idhistorial):
        """Función para obtener la idubicaciones dado un idhistorial."""
        try:
            conectar_bd()
            cursor.execute("SELECT idubicaciones FROM historial_ubicacion WHERE idhistorial = %s", (idhistorial,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error al obtener idubicaciones por idhistorial: {err}")
            return None
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()  

    # Frame para botones al final
    button_frame = tk.Frame(contenedor, bg="#222222")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Guardar Cambios", bg="green", fg="white", width=15, command=guardar_cambios_reporte).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancelar", bg="red", fg="white", width=15, command=ventana_editar.destroy).pack(side="left", padx=10)

    return ventana_editar

def guardar_reporte(entries):
    # Obtener los valores de los campos del formulario
    folio = entries["Folio:"].get().strip()
    fecha_reporte = entries["Fecha:"].get().strip()
    maquina = entries["Máquina:"].get().strip()
    operador = entries["Operador:"].get().strip()
    ubicacion = entries["Ubicación:"].get().strip()
    cliente = entries["Cliente:"].get().strip()
    horometro_inicial_str = entries["Horómetro Inicial:"].get().strip()
    horometro_final_str = entries["Horómetro Final:"].get().strip()
    horas_trabajadas_str = entries["Horas Trabajadas:"].get().strip()
    diesel = a_float(entries["Diesel (L):"].get()) or 0
    horometro_carga = a_float(entries["Horómetro Carga:"].get()) or 0
    aceite_hidraulico = a_float(entries["Aceite Hidráulico (L):"].get()) or 0
    aceite_motor = a_float(entries["Aceite Motor (L):"].get()) or 0
    actividades = entries["Actividades:"].get().strip()
    fallas = entries["Fallas:"].get().strip()
    servicios = entries["Servicios:"].get().strip()
    reparaciones = entries["Reparaciones:"].get().strip()

    campos_faltantes = []
    if not folio:
        campos_faltantes.append("Folio")
    if not fecha_reporte:
        campos_faltantes.append("Fecha")
    if not maquina:
        campos_faltantes.append("Máquina")
    if not operador:
        campos_faltantes.append("Operador")
    if not ubicacion:
        campos_faltantes.append("Ubicación")
    if not cliente:
        campos_faltantes.append("Cliente")
    if not horometro_inicial_str:
        campos_faltantes.append("Horómetro Inicial")
    if not horometro_final_str:
        campos_faltantes.append("Horómetro Final")
    # Verificar horas trabajadas solo si los horómetros tienen valores
    if horometro_inicial_str and horometro_final_str and not horas_trabajadas_str:
        campos_faltantes.append("Horas Trabajadas")

    if campos_faltantes:
        mensaje_error = "Los siguientes campos obligatorios deben llenarse:\n"
        mensaje_error += "\n".join(campos_faltantes)
        messagebox.showerror("Error", mensaje_error)
        return

    # Convertir a float DESPUÉS de la validación de no vacío
    horometro_inicial = a_float(horometro_inicial_str)
    horometro_final = a_float(horometro_final_str)
    horas_trabajadas = (horas_trabajadas_str)

    # Obtener los IDs de las tablas relacionadas
    maquina_seleccionada_texto = entries["Máquina:"].get().strip()
    id_maquina = ventana_activa.maquina_a_id.get(maquina_seleccionada_texto)
    if id_maquina is None:
        messagebox.showerror("Error", f"No se encontró la máquina con el No. Económico: {maquina_seleccionada_texto}")
        return
    id_operador = obtener_id("operador", "nombre", operador)
    id_ubicacion = obtener_id("ubicaciones", "nombres", ubicacion)
    id_cliente = obtener_id("cliente", "nombre", cliente)

    # Paso 1: Insertar en historial_ubicacion y obtener idhistorial
    query_historial = """
        INSERT INTO historial_ubicacion (idubicaciones, fecha)
        VALUES (%s, %s)
    """
    valores_historial = (id_ubicacion, fecha_reporte)

    if ejecutar_query(query_historial, valores_historial):
            conectar_bd()
            idhistorial = cursor.lastrowid

            # Paso 2: Insertar el reporte con el idhistorial_ubicacion
            query = """
                INSERT INTO reporte (
                    folio, fecha_reporte, idmaquina, idoperador, cliente_idcliente,
                    horometro_inicial, horometro_final, horometro_carga, horas_trabajadas, diesel,
                    aceite_hidraulico, aceite_motor, actividades, fallas, servicios, reparacion,
                    idhistorial_ubicacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                folio, fecha_reporte, id_maquina, id_operador, id_cliente,
                horometro_inicial, horometro_final, horometro_carga, horas_trabajadas, diesel,
                aceite_hidraulico, aceite_motor, actividades, fallas, servicios, reparaciones,
                idhistorial
            )

            if ejecutar_query(query, valores):
                messagebox.showinfo("Éxito", "Reporte guardado correctamente")

                entries["Folio:"].delete(0, tk.END)
                entries["Fecha:"].delete(0, tk.END)
                entries["Diesel (L):"].delete(0, tk.END)
                entries["Horómetro Carga:"].delete(0, tk.END)
                entries["Aceite Hidráulico (L):"].delete(0, tk.END)
                entries["Aceite Motor (L):"].delete(0, tk.END)
                entries["Actividades:"].delete(0, tk.END)
                entries["Fallas:"].delete(0, tk.END)
                entries["Servicios:"].delete(0, tk.END)
                entries["Reparaciones:"].delete(0, tk.END)

                horometro_final_valor = entries["Horómetro Final:"].get().strip()
                entries["Horómetro Inicial:"].delete(0, tk.END)
                entries["Horómetro Inicial:"].insert(0, horometro_final_valor)

                entries["Horómetro Final:"].delete(0, tk.END)
                entries["Horas Trabajadas:"].delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo guardar el reporte")
    else:
        messagebox.showerror("Error", "No se pudo registrar la ubicación histórica")

def conectar_bd2():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",  # Reemplaza con tu usuario de MySQL
            password="",  # Reemplaza con tu contraseña de MySQL
            database="pruebas"
        )
        if conexion.is_connected():
            print("Conexión a la base de datos establecida.")
            return conexion
        else:
            print("No se pudo establecer la conexión.")
            return None
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def abrir_filtro_busqueda():
    ventana_busqueda = tk.Toplevel()
    ventana_busqueda.title("Buscar Reportes")
    ventana_busqueda.attributes('-fullscreen', True)  # Activar pantalla completa
    ventana_busqueda.configure(bg="#1e1e1e")
    def salir_pantalla_completa():
        ventana_busqueda.attributes('-fullscreen', False)
        ventana_busqueda.update_idletasks()
        width, height = 1200, 700
        x = (ventana_busqueda.winfo_screenwidth() // 2) - (width // 2)
        y = (ventana_busqueda.winfo_screenheight() // 2) - (height // 2)
        ventana_busqueda.geometry(f"{width}x{height}+{x}+{y}")

    top_bar = tk.Frame(ventana_busqueda, bg="#1e1e1e")
    top_bar.pack(fill="x", side="top")
    # Botón de salir en la esquina superior derecha
    btn_salir = tk.Button(top_bar, text="✕", command=salir_pantalla_completa,
                          bg="red", fg="white", font=("Arial", 10, "bold"), width=3, height=1)
    btn_salir.pack(side="right", padx=10, pady=5)

    # Encabezado de filtros
    filtro_frame = tk.Frame(ventana_busqueda, bg="#1e1e1e")
    filtro_frame.pack(padx=20, pady=10, fill="x")

    # Filtros disponibles
    tk.Label(filtro_frame, text="Desde:", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5, pady=5)
    desde_fecha = DateEntry(filtro_frame, date_pattern='yyyy-mm-dd')
    desde_fecha.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(filtro_frame, text="Hasta:", fg="white", bg="#1e1e1e").grid(row=0, column=2, padx=5, pady=5)
    hasta_fecha = DateEntry(filtro_frame, date_pattern='yyyy-mm-dd')
    hasta_fecha.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(filtro_frame, text="Cliente:", fg="white", bg="#1e1e1e").grid(row=1, column=0, padx=5, pady=5)
    combo_cliente = ttk.Combobox(filtro_frame, state="readonly")
    combo_cliente.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(filtro_frame, text="Ubicación:", fg="white", bg="#1e1e1e").grid(row=1, column=2, padx=5, pady=5)
    combo_ubicacion = ttk.Combobox(filtro_frame, state="readonly")
    combo_ubicacion.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(filtro_frame, text="Operador:", fg="white", bg="#1e1e1e").grid(row=2, column=0, padx=5, pady=5)
    combo_operador = ttk.Combobox(filtro_frame, state="readonly")
    combo_operador.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(filtro_frame, text="Máquina:", fg="white", bg="#1e1e1e").grid(row=3, column=0, padx=5, pady=5)
    combo_maquina = ttk.Combobox(filtro_frame, state="readonly")
    combo_maquina.grid(row=3, column=1, padx=5, pady=5)

    # Filtro adicional para buscar registros con fallas/servicios/reparaciones
    var_con_problemas = tk.BooleanVar()
    chk_problemas = tk.Checkbutton(
        filtro_frame, text="Solo con fallas/servicios/reparaciones",
        variable=var_con_problemas, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e",
        activebackground="#1e1e1e", activeforeground="white"
    )
    chk_problemas.grid(row=3, column=2, columnspan=2, sticky="w", padx=5, pady=5)

    # Treeview para mostrar resultados
    tree_frame = tk.Frame(ventana_busqueda)
    tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

    columnas = ("Folio", "Fecha", "Unidad", "Operador", "Ubicación", "Cliente",
                "H.Inicial", "H.Final", "H.Carga", "Horas Trab.", "Diesel", "Aceite H.", "Aceite M.",
                "Actividades", "Fallas", "Servicios", "Reparaciones")
    tree = ttk.Treeview(tree_frame, columns=columnas, show="headings")
    anchuras = {
        "Folio": 80,
        "Fecha": 90,
        "Unidad": 100,
        "Operador": 130,
        "Ubicación": 120,
        "Cliente": 130,
        "H.Inicial": 90,
        "H.Final": 90,
        "H.Carga": 90,
        "Horas Trab.": 100,
        "Diesel": 80,
        "Aceite H.": 90,
        "Aceite M.": 90,
        "Actividades": 150,
        "Fallas": 150,
        "Servicios": 150,
        "Reparaciones": 150
    }
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=anchuras.get(col, 100), minwidth=60)
    tree.pack(fill="both", expand=True)
    def limpiar_seleccion(event):
        event.widget.set('')  # El widget que recibe el evento es el Combobox

    # Asociar el evento a cada combobox
    combo_cliente.bind("<BackSpace>", limpiar_seleccion)
    combo_operador.bind("<BackSpace>", limpiar_seleccion)
    combo_ubicacion.bind("<BackSpace>", limpiar_seleccion)
    combo_maquina.bind("<BackSpace>", limpiar_seleccion)

    # Función de búsqueda
    def buscar():
        tree.delete(*tree.get_children())
        try:
            conectar_bd()
            condiciones = []
            parametros = []

            # Filtros seleccionados
            if desde_fecha.get():
                condiciones.append("r.fecha_reporte >= %s")
                parametros.append(desde_fecha.get())
            if hasta_fecha.get():
                condiciones.append("r.fecha_reporte <= %s")
                parametros.append(hasta_fecha.get())
            if combo_cliente.get():
                condiciones.append("c.nombre = %s")
                parametros.append(combo_cliente.get())
            if combo_ubicacion.get():
                condiciones.append("ub.nombres = %s")
                parametros.append(combo_ubicacion.get())
            if combo_operador.get():
                condiciones.append("o.nombre = %s")
                parametros.append(combo_operador.get())
            if combo_maquina.get():
                condiciones.append("u.No_Economico = %s")
                parametros.append(combo_maquina.get())
            if var_con_problemas.get():
                condiciones.append("(r.fallas IS NOT NULL AND r.fallas <> '') OR (r.servicios IS NOT NULL AND r.servicios <> '') OR (r.reparacion IS NOT NULL AND r.reparacion <> '')")

            query = """
                SELECT
                    r.idreporte,
                    r.folio,
                    r.fecha_reporte,
                    u.No_Economico,
                    o.nombre AS nombre_operador,
                    ub.nombres AS ubicacion,
                    c.nombre AS cliente,
                    r.horometro_inicial,
                    r.horometro_final,
                    r.horometro_carga,
                    r.horas_trabajadas,
                    r.diesel,
                    r.aceite_hidraulico,
                    r.aceite_motor,
                    r.actividades,
                    r.fallas,
                    r.servicios,
                    r.reparacion
                FROM reporte r
                JOIN maquina m ON r.idmaquina = m.idmaquina
                JOIN unidad u ON m.unidad_idUnidad = u.idUnidad
                JOIN operador o ON r.idoperador = o.idoperador
                JOIN cliente c ON r.cliente_idcliente = c.idcliente
                JOIN historial_ubicacion hu ON r.idhistorial_ubicacion = hu.idhistorial
                JOIN ubicaciones ub ON hu.idubicaciones = ub.idubicaciones
            """ + (f" WHERE {' AND '.join(condiciones)}" if condiciones else "") + """
                ORDER BY r.idreporte;
            """

            cursor.execute(query, parametros)
            resultados = cursor.fetchall()
            for row in resultados:
                tree.insert("", tk.END, values=row[1:], iid=row[0])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo ejecutar la búsqueda: {err}")
    
    def mostrar_todos_los_datos():
        tree.delete(*tree.get_children())
        try:
            conectar_bd()
            query = """
                SELECT
                    r.idreporte,
                    r.folio,
                    r.fecha_reporte,
                    u.No_Economico,
                    o.nombre AS nombre_operador,
                    ub.nombres AS ubicacion,
                    c.nombre AS cliente,
                    r.horometro_inicial,
                    r.horometro_final,
                    r.horometro_carga,
                    r.horas_trabajadas,
                    r.diesel,
                    r.aceite_hidraulico,
                    r.aceite_motor,
                    r.actividades,
                    r.fallas,
                    r.servicios,
                    r.reparacion
                FROM reporte r
                JOIN maquina m ON r.idmaquina = m.idmaquina
                JOIN unidad u ON m.unidad_idUnidad = u.idUnidad
                JOIN operador o ON r.idoperador = o.idoperador
                JOIN cliente c ON r.cliente_idcliente = c.idcliente
                JOIN historial_ubicacion hu ON r.idhistorial_ubicacion = hu.idhistorial
                JOIN ubicaciones ub ON hu.idubicaciones = ub.idubicaciones
                ORDER BY r.idreporte;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            for row in resultados:
                tree.insert("", tk.END, values=row[1:], iid=row[0])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar los datos: {err}")


    # Marco para centrar el botón de búsqueda
    boton_frame = tk.Frame(ventana_busqueda, bg="#1e1e1e")
    boton_frame.pack(pady=10)

    btn_buscar = tk.Button(boton_frame, text="Buscar", command=buscar, bg="#4CAF50", fg="white", width=20, height=2)
    btn_buscar.pack(side="left", padx=10)

    btn_mostrar_todo = tk.Button(boton_frame, text="Mostrar Todo", command=mostrar_todos_los_datos, bg="#2196F3", fg="white", width=20, height=2)
    btn_mostrar_todo.pack(side="left", padx=10)

    # Cargar datos en los Combobox (a implementar más adelante)
    combo_cliente["values"] = obtener_datos("cliente", "nombre")
    combo_ubicacion["values"] = obtener_datos("ubicaciones", "nombres")
    combo_operador["values"] = obtener_datos("operador", "nombre")
    combo_maquina["values"] = obtener_datos("unidad", "No_Economico")


def agregar_maquinaria():
    global ventana_activa
    root.withdraw()
    nueva_ventana = Toplevel(root)
    nueva_ventana.title("INSERTAR MAQUINARIAS")
    nueva_ventana.geometry("400x400")
    centrar_ventana(nueva_ventana, 400, 400, offset_y=150)

    image = Image.open("C:/Users/PC/caliz/fondo_maquinaria.jpg")
    background_image = ImageTk.PhotoImage(image)
    # Crear un label para la imagen de fondo
    background_label = tk.Label(nueva_ventana, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Cubrir toda la ventana
    nueva_ventana.background_image = background_image 
    # Crear la barra de menú principal
    menu_bar = tk.Menu(nueva_ventana)

    # Crear el submenú "Editar"
    editar_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 evita que el menú se pueda separar

    # Agregar opciones al submenú
    editar_menu.add_command(label="Editar y Eliminar Marcas", command=abrir_panel_marcas)
    editar_menu.add_command(label="Editar y Eliminar Ubicación", command=abrir_panel_ubicaciones)
    editar_menu.add_command(label="Editar y Eliminar Clientes", command=abrir_panel_clientes)
    editar_menu.add_command(label="Editar y Eliminar Unidad", command=abrir_panel_unidad)
    editar_menu.add_command(label="Editar y Eliminar Clasificacion", command=abrir_panel_clasificacion)
    editar_menu.add_command(label="Editar y Eliminar Operador", command=abrir_panel_operador)

    # Agregar el submenú "Editar" a la barra de menú principal
    menu_bar.add_cascade(label="Editar y Eliminaciones", menu=editar_menu)
        
    # Configurar la barra de menú
    nueva_ventana.config(menu=menu_bar)

    # Usamos grid para colocar todos los widgets
    tk.Label(nueva_ventana, text="Seleccione una opción", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Configuramos la cuadrícula para que las celdas se expandan y centren los elementos
    nueva_ventana.grid_rowconfigure(0, weight=1)  # Centrar la primera fila
    nueva_ventana.grid_rowconfigure(1, weight=1)  # Centrar la segunda fila
    nueva_ventana.grid_rowconfigure(2, weight=1)  # Centrar la tercera fila
    nueva_ventana.grid_rowconfigure(3, weight=1)  # Centrar la cuarta fila

    nueva_ventana.grid_columnconfigure(0, weight=1)  # Centrar columna 0
    nueva_ventana.grid_columnconfigure(1, weight=1)  # Centrar columna 1

    for i in range(4):
        nueva_ventana.grid_rowconfigure(i, weight=1)
    for j in range(2):
        nueva_ventana.grid_columnconfigure(j, weight=1)

    # Estilo de los botones
    button_style = {
        "width": 15,
        "height": 2,
        "font": ("Arial", 12, "bold"),
        "bg": "#00509E",
        "fg": "white",
        "bd": 3,
        "relief": "raised"
    }
        # Lista de botones con texto y función
    botones = [
        ("Marcas", lambda: cambiar_ventana(abrir_marcas)),
        ("Unidad", lambda: cambiar_ventana(abrir_Unidad)),
        ("Ubicación", lambda: cambiar_ventana(abrir_Ubicacion)),
        ("Clientes", lambda: cambiar_ventana(abrir_clientes)),
        ("Clasificacion", lambda: cambiar_ventana(abrir_clasificacion)),
        ("Operador", lambda: cambiar_ventana(abrir_operador)),
    ]

        # Crear y colocar los botones en la cuadrícula
    for idx, (text, command) in enumerate(botones):
        btn = tk.Button(nueva_ventana, text=text, command=command, **button_style)
        btn.grid(row=1 + idx // 2, column=idx % 2, padx=10, pady=10, sticky="nsew")

        # Agregar efecto hover (cambiar color al pasar el mouse)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#0077CC"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#00509E"))

    def cerrar_nueva_ventana():
        nueva_ventana.destroy()
        root.deiconify()  # Mostrar la ventana principal

    nueva_ventana.protocol("WM_DELETE_WINDOW", cerrar_nueva_ventana)
    ventana_activa = nueva_ventana  # Guardar referencia

    return nueva_ventana
  
def ingresar():
    print("Ingresar seleccionado")

def acerca_de():
    print("Acerca de esta aplicación")

# Crear la barra de menú
menubar = Menu(root)

# Menú desplegable principal con la primera opción modificada
menu_desplegable = Menu(menubar, tearoff=0)
menu_desplegable.add_command(label="Insertar Datos", command=lambda: cambiar_ventana(agregar_maquinaria))
menu_desplegable.add_command(label="Insertar Maquina", command=abrir_panel_registro_maquina)
menu_desplegable.add_command(label="Opción 3")
menubar.add_cascade(label="Menú", menu=menu_desplegable)

# Agregar otro menú en la barra (Ejemplo: Ayuda)
menu_ayuda = Menu(menubar, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)
menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

# Asignar la barra de menú a la ventana
root.config(menu=menubar)

# Crear los botones principales
btn_reportes = tk.Button(root, text="Reportes", command=abrir_panel_reporte, width=20, height=2, 
                         bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="raised",
                         activebackground="#45a049", activeforeground="white")
btn_reportes.pack(pady=20)

btn_ingresar = tk.Button(root, text="Busquedas", command=abrir_filtro_busqueda, width=20, height=2, 
                         bg="#008CBA", fg="white", font=("Arial", 12, "bold"), relief="raised",
                         activebackground="#007bb5", activeforeground="white")
btn_ingresar.pack(pady=20)

def cerrar_conexion():
    global conexion, cursor
    if cursor:
        cursor.close()
    if conexion:
        conexion.close()

root.protocol("WM_DELETE_WINDOW", lambda: [cerrar_conexion(), root.destroy()])

# Iniciar la aplicación
root.mainloop()

