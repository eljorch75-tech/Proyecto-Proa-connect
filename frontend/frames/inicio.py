import tkinter as tk
from tkinter import messagebox

from frames.estudiantes import crear_estudiantes
from frames.asistencia import crear_asistencias
from frames.observaciones import crear_observaciones
from frames.docentes import crear_docentes


def crear_inicio(parent):
    # Colores generales
    COLOR_FONDO = "#F1F4F8"
    COLOR_AZUL = "#1E4D8F"
    COLOR_TURQUESA = "#20A4BD"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_GRIS = "#65778C"

    # Contenedor principal
    frame = tk.Frame(parent, bg=COLOR_FONDO)
    frame.pack(fill="both", expand=True)

    # Barra lateral
    sidebar = tk.Frame(frame, bg=COLOR_BLANCO, width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    logo_frame = tk.Frame(sidebar, bg=COLOR_BLANCO, height=85)
    logo_frame.pack(fill="x")
    logo_frame.pack_propagate(False)

    tk.Label(
        logo_frame, text="🌐", font=("Segoe UI Emoji", 22),
        bg=COLOR_BLANCO, fg=COLOR_TURQUESA
    ).pack(side="left", padx=(20, 7), pady=20)

    tk.Label(
        logo_frame, text="ProAConnect", font=("Segoe UI", 17, "bold"),
        bg=COLOR_BLANCO, fg=COLOR_AZUL
    ).pack(side="left", pady=20)

    tk.Frame(sidebar, bg="#DDE4EC", height=1).pack(fill="x")

    # Área donde se reemplazan las vistas
    contenido = tk.Frame(frame, bg=COLOR_FONDO)
    contenido.pack(side="left", fill="both", expand=True)

    botones = {}

    def mostrar_vista(nombre, funcion):
        # Limpiar únicamente el contenido central
        for widget in contenido.winfo_children():
            widget.destroy()

        # Cargar la vista seleccionada
        try:
            nueva_vista = funcion(contenido)
            if nueva_vista is not None:
                # Si la función devuelve un Frame que ya está empaquetado,
                # se evita empaquetarlo una segunda vez.
                if not nueva_vista.winfo_manager():
                    nueva_vista.pack(fill="both", expand=True)
        except Exception as error:
            messagebox.showerror(
                "Error al abrir la vista",
                f"No se pudo abrir '{nombre}'.\n\nDetalle: {error}"
            )
            return

        # Actualizar el estilo de los botones
        for nombre_boton, boton in botones.items():
            seleccionado = nombre_boton == nombre
            boton.configure(
                bg=COLOR_TURQUESA if seleccionado else COLOR_BLANCO,
                fg="white" if seleccionado else COLOR_GRIS,
                activebackground=COLOR_TURQUESA,
                activeforeground="white"
            )

    def crear_boton(texto, icono, funcion):
        boton = tk.Button(
            sidebar,
            text=f"{icono}   {texto}",
            font=("Segoe UI", 11),
            bg=COLOR_BLANCO,
            fg=COLOR_GRIS,
            activebackground=COLOR_TURQUESA,
            activeforeground="white",
            anchor="w",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=12,
            command=lambda: mostrar_vista(texto, funcion)
        )
        boton.pack(fill="x", padx=10, pady=4)
        botones[texto] = boton
        return boton

    # Botones conectados a sus respectivas vistas
    crear_boton("Home", "⌂", crear_home)
    crear_boton("Asistencia", "▣", crear_asistencias)
    crear_boton("Alumnos", "♟", crear_estudiantes)
    crear_boton("Docentes", "♟", crear_docentes)
    crear_boton("Observaciones", "☷", crear_observaciones)
    

    # Vista inicial
    mostrar_vista("Home", crear_home)

    return frame


def crear_home(parent):
    # Colores usados en la pantalla Home
    COLOR_FONDO = "#F1F4F8"
    COLOR_AZUL = "#1E4D8F"
    COLOR_TURQUESA = "#20A4BD"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_TEXTO = "#19324D"
    COLOR_GRIS = "#65778C"
    COLOR_VERDE = "#12B981"
    COLOR_ROJO = "#F0444F"
    COLOR_AMARILLO = "#F5A623"

    home = tk.Frame(parent, bg=COLOR_FONDO)

    # =========================================================
    # CABECERA
    # =========================================================
    header = tk.Frame(
        home,
        bg=COLOR_FONDO,
        height=75
    )

    header.pack(
        fill="x",
        padx=25,
        pady=(10, 0)
    )

    header.pack_propagate(False)

    tk.Label(
        header,
        text="Home",
        font=("Segoe UI", 23, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO
    ).pack(
        side="left",
        pady=15
    )

    # Botones visuales solamente
    botones_header = tk.Frame(
        header,
        bg="#E8EDF3"
    )

    botones_header.pack(
        side="right",
        pady=15
    )

    for simbolo in ["+", "?", "♟", "●"]:
        tk.Label(
            botones_header,
            text=simbolo,
            font=("Segoe UI", 11, "bold"),
            bg="#E8EDF3",
            fg=COLOR_GRIS,
            width=3
        ).pack(
            side="left",
            padx=2
        )

    # =========================================================
    # TARJETAS DE ESTADÍSTICAS
    # =========================================================
    estadisticas = tk.Frame(
        home,
        bg=COLOR_FONDO
    )

    estadisticas.pack(
        fill="x",
        padx=25,
        pady=(5, 20)
    )

    # ---------------------------------------------------------
    # Tarjeta 1 - Asistencia
    # ---------------------------------------------------------
    tarjeta1 = tk.Frame(
        estadisticas,
        bg=COLOR_TURQUESA,
        height=120
    )

    tarjeta1.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 8)
    )

    tarjeta1.pack_propagate(False)

    tk.Label(
        tarjeta1,
        text="Asistencia Hoy",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_TURQUESA,
        fg="white"
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 0)
    )

    tk.Label(
        tarjeta1,
        text="50%",
        font=("Segoe UI", 30, "bold"),
        bg=COLOR_TURQUESA,
        fg="white"
    ).pack(
        anchor="w",
        padx=18
    )

    barra1 = tk.Frame(
        tarjeta1,
        bg="#66C9D8",
        height=7
    )

    barra1.pack(
        fill="x",
        padx=18,
        pady=(3, 0)
    )

    barra1.pack_propagate(False)

    tk.Frame(
        barra1,
        bg="white",
        width=135
    ).pack(
        side="left",
        fill="y"
    )

    # ---------------------------------------------------------
    # Tarjeta 2 - Faltas
    # ---------------------------------------------------------
    tarjeta2 = tk.Frame(
        estadisticas,
        bg=COLOR_BLANCO,
        height=120,
        highlightbackground="#DDE4EC",
        highlightthickness=1
    )

    tarjeta2.pack(
        side="left",
        fill="x",
        expand=True,
        padx=8
    )

    tarjeta2.pack_propagate(False)

    tk.Label(
        tarjeta2,
        text="Faltas",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 0)
    )

    tk.Label(
        tarjeta2,
        text="2",
        font=("Segoe UI", 30, "bold"),
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO
    ).pack(
        anchor="w",
        padx=18
    )

    tk.Label(
        tarjeta2,
        text="▲",
        font=("Segoe UI", 18),
        bg=COLOR_BLANCO,
        fg=COLOR_ROJO
    ).place(
        relx=0.9,
        rely=0.45,
        anchor="center"
    )

    barra2 = tk.Frame(
        tarjeta2,
        bg="#E8EDF3",
        height=7
    )

    barra2.pack(
        fill="x",
        padx=18,
        pady=(3, 0)
    )

    barra2.pack_propagate(False)

    tk.Frame(
        barra2,
        bg=COLOR_ROJO,
        width=100
    ).pack(
        side="left",
        fill="y"
    )

    # ---------------------------------------------------------
    # Tarjeta 3 - Llegadas tarde
    # ---------------------------------------------------------
    tarjeta3 = tk.Frame(
        estadisticas,
        bg=COLOR_BLANCO,
        height=120,
        highlightbackground="#DDE4EC",
        highlightthickness=1
    )

    tarjeta3.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(8, 0)
    )

    tarjeta3.pack_propagate(False)

    tk.Label(
        tarjeta3,
        text="Llegadas Tarde",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 0)
    )

    tk.Label(
        tarjeta3,
        text="3",
        font=("Segoe UI", 30, "bold"),
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO
    ).pack(
        anchor="w",
        padx=18
    )

    tk.Label(
        tarjeta3,
        text="▤",
        font=("Segoe UI", 18),
        bg=COLOR_BLANCO,
        fg=COLOR_VERDE
    ).place(
        relx=0.9,
        rely=0.45,
        anchor="center"
    )

    barra3 = tk.Frame(
        tarjeta3,
        bg="#E8EDF3",
        height=7
    )

    barra3.pack(
        fill="x",
        padx=18,
        pady=(3, 0)
    )

    barra3.pack_propagate(False)

    tk.Frame(
        barra3,
        bg=COLOR_VERDE,
        width=70
    ).pack(
        side="left",
        fill="y"
    )

    # =========================================================
    # PANEL REGISTRO DE ASISTENCIA
    # =========================================================
    panel = tk.Frame(
        home,
        bg=COLOR_BLANCO,
        highlightbackground="#DDE4EC",
        highlightthickness=1
    )

    panel.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )

    # ---------------------------------------------------------
    # Encabezado del panel
    # ---------------------------------------------------------
    panel_header = tk.Frame(
        panel,
        bg=COLOR_BLANCO,
        height=65
    )

    panel_header.pack(
        fill="x",
        padx=18,
        pady=(8, 0)
    )

    panel_header.pack_propagate(False)

    tk.Label(
        panel_header,
        text="REGISTRO DE ASISTENCIA",
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO
    ).pack(
        side="left",
        pady=15
    )

    # Botón visual
    tk.Label(
        panel_header,
        text="+  Nuevo Alumno",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_TURQUESA,
        fg="white",
        padx=12,
        pady=6
    ).pack(
        side="left",
        padx=20
    )

    # Ciclos
    ciclos = tk.Frame(
        panel_header,
        bg="#E9EFF6"
    )

    ciclos.pack(
        side="right",
        pady=10
    )

    tk.Label(
        ciclos,
        text="Ciclo Básico (1° - 3°)",
        font=("Segoe UI", 9, "bold"),
        bg=COLOR_TURQUESA,
        fg="white",
        padx=10,
        pady=7
    ).pack(
        side="left"
    )

    tk.Label(
        ciclos,
        text="Ciclo Orientado (4° - 6°)",
        font=("Segoe UI", 9),
        bg="#E9EFF6",
        fg=COLOR_TEXTO,
        padx=10,
        pady=7
    ).pack(
        side="left"
    )

    # =========================================================
    # TABLA
    # =========================================================
    tabla = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    tabla.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=(0, 18)
    )

    # Encabezados
    encabezados = [
        "ID",
        "Nombre y Año",
        "Estado",
        "Observaciones",
        "Acciones (CRUD)"
    ]

    anchos = [12, 28, 18, 30, 18]

    encabezado = tk.Frame(
        tabla,
        bg="#EDF2F7",
        height=40
    )

    encabezado.pack(
        fill="x"
    )

    encabezado.pack_propagate(False)

    for texto, ancho in zip(encabezados, anchos):

        tk.Label(
            encabezado,
            text=texto,
            font=("Segoe UI", 9, "bold"),
            bg="#EDF2F7",
            fg=COLOR_TEXTO,
            width=ancho
        ).pack(
            side="left",
            fill="both",
            expand=True
        )

    # =========================================================
    # DATOS ESTÁTICOS - SOLO VISUALES
    # =========================================================
    alumnos = [
        ("PROA-401", "Facundo González (4° Año)",
         "Presente", "Taller de Robótica", COLOR_VERDE),

        ("PROA-402", "Martina Rodríguez (4° Año)",
         "Tardanza", "Ingreso 8:20 AM", COLOR_AMARILLO),

        ("PROA-501", "Mateo Benítez (5° Año)",
         "Falta", "Certificado presentado", COLOR_ROJO),

        ("PROA-502", "Sofía Romero (5° Año)",
         "Presente", "Proyecto Biotecnología", COLOR_VERDE),

        ("PROA-601", "Lucas Herrera (6° Año)",
         "Presente", "Entrega de Práctica", COLOR_VERDE)
    ]

    for i, (id_alumno, nombre, estado, observacion, color) in enumerate(alumnos):

        fila = tk.Frame(
            tabla,
            bg=COLOR_BLANCO,
            height=55
        )

        fila.pack(
            fill="x"
        )

        fila.pack_propagate(False)

        # ID
        tk.Label(
            fila,
            text=id_alumno,
            font=("Segoe UI", 9),
            bg=COLOR_BLANCO,
            fg=COLOR_AZUL,
            width=12
        ).pack(
            side="left",
            fill="both",
            expand=True
        )

        # Nombre
        tk.Label(
            fila,
            text=nombre,
            font=("Segoe UI", 9),
            bg=COLOR_BLANCO,
            fg="#142B45",
            anchor="w",
            width=28
        ).pack(
            side="left",
            fill="both",
            expand=True
        )

        # Estado
        estado_label = tk.Label(
            fila,
            text=estado,
            font=("Segoe UI", 9, "bold"),
            bg="#E8F8F2" if color == COLOR_VERDE
               else "#FFF3D6" if color == COLOR_AMARILLO
               else "#FFE5E8",
            fg=color,
            padx=8,
            pady=3
        )

        estado_label.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        # Observación
        tk.Label(
            fila,
            text=observacion,
            font=("Segoe UI", 9),
            bg=COLOR_BLANCO,
            fg=COLOR_GRIS,
            anchor="w",
            width=30
        ).pack(
            side="left",
            fill="both",
            expand=True
        )

        # Acciones
        acciones = tk.Frame(
            fila,
            bg=COLOR_BLANCO
        )

        acciones.pack(
            side="left",
            fill="both",
            expand=True
        )

        tk.Label(
            acciones,
            text="✎",
            font=("Segoe UI", 12),
            bg="#EEF3F8",
            fg=COLOR_TEXTO,
            width=3
        ).pack(
            side="left",
            padx=3,
            pady=10
        )

        tk.Label(
            acciones,
            text="▣",
            font=("Segoe UI", 11),
            bg="#EEF3F8",
            fg=COLOR_TEXTO,
            width=3
        ).pack(
            side="left",
            padx=3,
            pady=10
        )

        # Separador
        tk.Frame(
            fila,
            bg="#E8EDF3",
            height=1
        ).pack(
            side="bottom",
            fill="x"
        )

    return home


