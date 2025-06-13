import tkinter as tk
from tkinter import Menu, Toplevel
from PIL import Image, ImageTk
import mysql.connector

# Variables globales
conexion = None
cursor = None
ventana_activa = None

# Conexión a la base de datos
def conectar_bd():
    global conexion, cursor
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="maquinaria"
        )
        cursor = conexion.cursor()
        print("Conexión a la base de datos establecida.")
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")

# Función genérica para abrir ventanas
def abrir_ventana(titulo, tamano, funcion_destino=None):
    global ventana_activa
    root.withdraw()
    nueva_ventana = Toplevel(root)
    nueva_ventana.title(titulo)
    nueva_ventana.geometry(tamano)
    
    if funcion_destino:
        nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(nueva_ventana, funcion_destino))
    
    ventana_activa = nueva_ventana
    return nueva_ventana

# Función para cerrar ventanas
def cerrar_ventana(ventana, ventana_destino=None):
    ventana.destroy()
    if ventana_destino:
        ventana_destino()

# Función para abrir la ventana de marcas
def abrir_marcas():
    marcas = abrir_ventana("Marcas", "300x200", agregar_maquinaria)
    tk.Label(marcas, text="Agregar marca", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(marcas, text="Marca:").pack(pady=5)
    marca_entry = tk.Entry(marcas, font=("Arial", 12))
    marca_entry.pack(pady=5)

    def obtener_marca():
        marca = marca_entry.get()
        if marca.strip():
            insertar_marca(marca)
            marca_entry.delete(0, tk.END)

    tk.Button(marcas, text="Agregar Marca", command=obtener_marca, bg="#4CAF50", fg="white").pack(pady=10)

# Función para insertar marcas en la base de datos
def insertar_marca(marca):
    global conexion, cursor
    try:
        if conexion is None or cursor is None:
            conectar_bd()
        query = "INSERT INTO marcas (nombre) VALUES (%s)"
        cursor.execute(query, (marca,))
        conexion.commit()
        print("Marca insertada correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar marca: {err}")

# Función para la ventana de agregar maquinaria
def agregar_maquinaria():
    nueva_ventana = abrir_ventana("INSERTAR MAQUINARIAS", "400x400")
    tk.Label(nueva_ventana, text="Seleccione una opción", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Button(nueva_ventana, text="Abrir Marcas", width=15, height=2, command=abrir_marcas).pack(pady=5)
    tk.Button(nueva_ventana, text="Botón 2", width=15, height=2).pack(pady=5)
    tk.Button(nueva_ventana, text="Botón 3", width=15, height=2).pack(pady=5)
    tk.Button(nueva_ventana, text="Botón 4", width=15, height=2).pack(pady=5)

# Ventana principal
root = tk.Tk()
root.title("Página Inicial")
root.geometry("270x405")

# Fondo
image = Image.open("C:/Users/PC/caliz/fondo1.jpg")
background_image = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Menú
menubar = Menu(root)
menu_desplegable = Menu(menubar, tearoff=0)
menu_desplegable.add_command(label="Insertar Maquinaria", command=agregar_maquinaria)
menubar.add_cascade(label="Menú", menu=menu_desplegable)
root.config(menu=menubar)

# Botones principales
tk.Button(root, text="Reportes", width=20, height=2, bg="#4CAF50", fg="white").pack(pady=20)
tk.Button(root, text="Ingresar", width=20, height=2, bg="#008CBA", fg="white").pack(pady=20)

# Cerrar conexión al cerrar la app
def cerrar_conexion():
    global conexion, cursor
    if cursor:
        cursor.close()
    if conexion:
        conexion.close()
    print("Conexión cerrada.")

root.protocol("WM_DELETE_WINDOW", lambda: [cerrar_conexion(), root.destroy()])

# Iniciar la app
root.mainloop()
