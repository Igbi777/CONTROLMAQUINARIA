import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk

def cambiar_foco(event, siguiente_widget):
    siguiente_widget.focus_set()

def calcular_horas_trabajadas(event, entry_inicial, entry_final, entry_horas_trabajadas):
    try:
        horometro_inicial = float(entry_inicial.get())
        horometro_final = float(entry_final.get())
        horas_trabajadas = (horometro_final - horometro_inicial) / 24
        entry_horas_trabajadas.delete(0, tk.END)  # Limpiar el campo de horas trabajadas
        entry_horas_trabajadas.insert(0, str(horas_trabajadas))  # Insertar el valor calculado
    except ValueError:
        entry_horas_trabajadas.delete(0, tk.END)  # Limpiar el campo si los valores no son válidos
        entry_horas_trabajadas.insert(0, "Error")

def abrir_panel_reporte():
    global ventana_activa, root
    root.withdraw()  # Ocultar la ventana principal
    ventana = tk.Toplevel()
    ventana.title("Registro de Reporte")
    ventana.geometry("650x550")  # Aumenté la altura para más espacio
    ventana.resizable(False, False)
    centrar_ventana(ventana, 650, 550, offset_y=150)

    # Cargar imagen de fondo
    image = Image.open("C:/Users/PC/caliz/fondo reporte.jpg")
    image = image.resize((650, 550))  
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
    frame.place(relx=0.5, rely=0.45, anchor="center", width=600, height=400)

    # Configurar cuadrícula
    for i in range(14):  # 14 filas por los nuevos campos
        frame.grid_rowconfigure(i, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)

    # Campos del formulario
    labels = [
        "Fecha:", "Máquina:", "Operador:", "Horómetro Inicial:", "Horómetro Final:",
        "Horas Trabajadas:", "Diesel (L):", "Aceite Hidráulico (L):", "Aceite Motor (L):", "Actividades:",
        "Ubicación:", "Horómetro Carga:", "Fallas:", "Servicios y Reparaciones:"
    ]

    entries = {}  # Diccionario para almacenar los entries
    # Creación de los campos
    for i, label in enumerate(labels):
        tk.Label(frame, text=label, bg="#222222", fg=label_fg, anchor="e").grid(row=i, column=0, pady=5, padx=10, sticky="e")

        if label == "Fecha:":
            entry = DateEntry(frame, width=18, background="darkblue", foreground="white", borderwidth=2,
                              date_pattern="yyyy-mm-dd", year=2024)
        elif label == "Máquina:":
            entry = ttk.Combobox(frame, state="readonly")
            entry['values'] = [m[1] for m in obtener_maquinas()]
        elif label == "Operador:":
            entry = ttk.Combobox(frame, state="readonly")
            llenar_combobox(entry, obtener_datos("operador", "nombre"))
        elif label == "Ubicación:":
            entry = ttk.Combobox(frame, state="readonly")
            llenar_combobox(entry, obtener_datos("ubicaciones", "nombres"))
        elif label == "Horas Trabajadas:":
            entry = tk.Entry(frame, **entry_style)
            entry.config(state="readonly")  # No editable, calculado automáticamente
        elif label == "Horómetro Carga:" or label == "Fallas:" or label == "Servicios y Reparaciones:":
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
    entry_horas_trabajadas = entries["Horas Trabajadas"]
    entry_final.bind("<Return>", lambda e: calcular_horas_trabajadas(e, entry_inicial, entry_final, entry_horas_trabajadas))

    # Frame para los botones
    button_frame = tk.Frame(ventana, bg="#222222")
    button_frame.place(relx=0.5, rely=0.90, anchor="center")

    # Función para cerrar ventana y volver a la principal
    def cerrar_nueva_ventana():
        ventana.destroy()
        root.deiconify()  # Mostrar la ventana principal

    # Botones de acción
    btn_guardar = tk.Button(button_frame, text="Guardar", bg=button_bg, fg=button_fg, width=10)
    btn_guardar.grid(row=0, column=0, padx=5, pady=10)

    btn_cancelar = tk.Button(button_frame, text="Cancelar", bg="red", fg="white", width=10, command=cerrar_nueva_ventana)
    btn_cancelar.grid(row=0, column=1, padx=5, pady=10)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_nueva_ventana)
    ventana_activa = ventana  # Guardar referencia

    return ventana
