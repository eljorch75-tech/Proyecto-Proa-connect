import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Cambiá esta URL si tu backend utiliza otro puerto o prefijo.
# Ejemplo:
# http://localhost:3000/estudiantes
#
# Si en tu app.js tenés:
# app.use('/api/estudiantes', estudiantesRouter)
# entonces sería:
# http://localhost:3000/api/estudiantes

API_URL = "http://localhost:3000/api/estudiantes"


# ============================================================
# COLORES
# ============================================================

COLOR_FONDO = "#F3F6F9"
COLOR_AZUL_OSCURO = "#0D172B"
COLOR_AZUL = "#179DB8"
COLOR_AZUL_HOVER = "#138BA4"
COLOR_BLANCO = "#FFFFFF"
COLOR_TEXTO = "#19304A"
COLOR_GRIS = "#65758B"
COLOR_GRIS_CLARO = "#E8EEF3"
COLOR_VERDE = "#19B47A"
COLOR_ROJO = "#F04B50"
COLOR_AMARILLO = "#F2B134"


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def crear_estudiantes(parents):

    # --------------------------------------------------------
    # FRAME PRINCIPAL
    # --------------------------------------------------------

    frame = tk.Frame(
        parents,
        bg=COLOR_FONDO
    )

    frame.pack(
        fill="both",
        expand=True
    )

    # --------------------------------------------------------
    # CONFIGURACIÓN DE GRID
    # --------------------------------------------------------

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # ========================================================
    # BARRA LATERAL
    # ========================================================

    sidebar = tk.Frame(
        frame,
        bg=COLOR_BLANCO,
        width=235
    )

    sidebar.grid(
        row=0,
        column=0,
        sticky="ns"
    )

    sidebar.grid_propagate(False)

    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

    logo_frame = tk.Frame(
        sidebar,
        bg=COLOR_BLANCO
    )

    logo_frame.pack(
        fill="x",
        padx=20,
        pady=(28, 35)
    )

    tk.Label(
        logo_frame,
        text="◉",
        font=("Segoe UI", 22, "bold"),
        fg=COLOR_AZUL,
        bg=COLOR_BLANCO
    ).pack(
        side="left"
    )

    tk.Label(
        logo_frame,
        text="ProAConnect",
        font=("Segoe UI", 16, "bold"),
        fg="#17458F",
        bg=COLOR_BLANCO
    ).pack(
        side="left",
        padx=8
    )

    # --------------------------------------------------------
    # FUNCIÓN BOTÓN SIDEBAR
    # --------------------------------------------------------

    def boton_sidebar(texto, activo=False):

        color = COLOR_AZUL if activo else COLOR_BLANCO
        color_texto = COLOR_BLANCO if activo else "#50647C"

        boton = tk.Button(
            sidebar,
            text=texto,
            font=("Segoe UI", 11, "bold" if activo else "normal"),
            bg=color,
            fg=color_texto,
            activebackground=COLOR_AZUL_HOVER,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            anchor="w",
            cursor="hand2",
            padx=20,
            pady=12
        )

        boton.pack(
            fill="x",
            padx=15,
            pady=3
        )

        return boton

    boton_sidebar("⌂   Home")
    boton_sidebar("▣   Asistencia")
    boton_sidebar("♟   Alumnos", True)
    boton_sidebar("⚙   Configuración")

    # ========================================================
    # CONTENIDO PRINCIPAL
    # ========================================================

    contenido = tk.Frame(
        frame,
        bg=COLOR_FONDO
    )

    contenido.grid(
        row=0,
        column=1,
        sticky="nsew"
    )

    contenido.grid_rowconfigure(2, weight=1)
    contenido.grid_columnconfigure(0, weight=1)

    # ========================================================
    # HEADER
    # ========================================================

    header = tk.Frame(
        contenido,
        bg=COLOR_FONDO,
        height=75
    )

    header.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=25,
        pady=(20, 5)
    )

    header.grid_columnconfigure(0, weight=1)

    tk.Label(
        header,
        text="Alumnos",
        font=("Segoe UI", 24, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO
    ).grid(
        row=0,
        column=0,
        sticky="w"
    )

    # Botones superiores

    botones_header = tk.Frame(
        header,
        bg=COLOR_FONDO
    )

    botones_header.grid(
        row=0,
        column=1,
        sticky="e"
    )

    tk.Button(
        botones_header,
        text="+",
        font=("Segoe UI", 15, "bold"),
        bg="#E8EEF3",
        fg=COLOR_TEXTO,
        relief="flat",
        width=3,
        cursor="hand2"
    ).pack(side="left", padx=3)

    tk.Button(
        botones_header,
        text="?",
        font=("Segoe UI", 11, "bold"),
        bg="#E8EEF3",
        fg=COLOR_TEXTO,
        relief="flat",
        width=3,
        cursor="hand2"
    ).pack(side="left", padx=3)

    tk.Button(
        botones_header,
        text="●",
        font=("Segoe UI", 9),
        bg="#E8EEF3",
        fg=COLOR_TEXTO,
        relief="flat",
        width=3,
        cursor="hand2"
    ).pack(side="left", padx=3)

    # ========================================================
    # TARJETAS
    # ========================================================

    cards = tk.Frame(
        contenido,
        bg=COLOR_FONDO
    )

    cards.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=25,
        pady=10
    )

    cards.grid_columnconfigure(
        (0, 1, 2),
        weight=1
    )

    # --------------------------------------------------------
    # CARD TOTAL
    # --------------------------------------------------------

    card_total = tk.Frame(
        cards,
        bg=COLOR_AZUL,
        height=120
    )

    card_total.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=(0, 8)
    )

    card_total.grid_propagate(False)

    tk.Label(
        card_total,
        text="Total de alumnos",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=COLOR_AZUL
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 0)
    )

    label_total = tk.Label(
        card_total,
        text="0",
        font=("Segoe UI", 28, "bold"),
        fg="white",
        bg=COLOR_AZUL
    )

    label_total.pack(
        anchor="w",
        padx=18
    )

    # --------------------------------------------------------
    # CARD TUTORES
    # --------------------------------------------------------

    card_tutores = tk.Frame(
        cards,
        bg=COLOR_BLANCO,
        height=120
    )

    card_tutores.grid(
        row=0,
        column=1,
        sticky="ew",
        padx=8
    )

    card_tutores.grid_propagate(False)

    tk.Label(
        card_tutores,
        text="Registros cargados",
        font=("Segoe UI", 11, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_BLANCO
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 0)
    )

    label_registros = tk.Label(
        card_tutores,
        text="0",
        font=("Segoe UI", 28, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_BLANCO
    )

    label_registros.pack(
        anchor="w",
        padx=18
    )

    # --------------------------------------------------------
    # CARD ESTADO
    # --------------------------------------------------------

    card_estado = tk.Frame(
        cards,
        bg=COLOR_BLANCO,
        height=120
    )

    card_estado.grid(
        row=0,
        column=2,
        sticky="ew",
        padx=(8, 0)
    )

    card_estado.grid_propagate(False)

    tk.Label(
        card_estado,
        text="Estado del sistema",
        font=("Segoe UI", 11, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_BLANCO
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 0)
    )

    label_estado = tk.Label(
        card_estado,
        text="● Conectando...",
        font=("Segoe UI", 17, "bold"),
        fg=COLOR_AMARILLO,
        bg=COLOR_BLANCO
    )

    label_estado.pack(
        anchor="w",
        padx=18
    )

    # ========================================================
    # PANEL DE TABLA
    # ========================================================

    panel = tk.Frame(
        contenido,
        bg=COLOR_BLANCO,
        bd=0,
        highlightthickness=1,
        highlightbackground="#E2E8EE"
    )

    panel.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=25,
        pady=(10, 25)
    )

    panel.grid_rowconfigure(2, weight=1)
    panel.grid_columnconfigure(0, weight=1)

    # --------------------------------------------------------
    # TÍTULO Y BOTÓN NUEVO
    # --------------------------------------------------------

    titulo_frame = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    titulo_frame.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=18,
        pady=(18, 10)
    )

    titulo_frame.grid_columnconfigure(1, weight=1)

    tk.Label(
        titulo_frame,
        text="REGISTRO DE ALUMNOS",
        font=("Segoe UI", 12, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_BLANCO
    ).grid(
        row=0,
        column=0,
        sticky="w"
    )

    boton_nuevo = tk.Button(
        titulo_frame,
        text="+  Nuevo Alumno",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_AZUL,
        fg=COLOR_BLANCO,
        activebackground=COLOR_AZUL_HOVER,
        activeforeground=COLOR_BLANCO,
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2"
    )

    boton_nuevo.grid(
        row=0,
        column=2,
        padx=10
    )

    # --------------------------------------------------------
    # BUSCADOR
    # --------------------------------------------------------

    buscar_frame = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    buscar_frame.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=18,
        pady=(0, 10)
    )

    buscar_frame.grid_columnconfigure(0, weight=1)

    entrada_buscar = tk.Entry(
        buscar_frame,
        font=("Segoe UI", 10),
        bg="#F4F7FA",
        fg=COLOR_TEXTO,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#DDE5EC"
    )

    entrada_buscar.grid(
        row=0,
        column=0,
        sticky="ew",
        ipady=8
    )

    entrada_buscar.insert(
        0,
        "  Buscar por nombre, apellido o DNI..."
    )

    def limpiar_placeholder(event):
        if entrada_buscar.get().strip() == "Buscar por nombre, apellido o DNI...":
            entrada_buscar.delete(0, tk.END)

    entrada_buscar.bind(
        "<FocusIn>",
        limpiar_placeholder
    )

    # ========================================================
    # TABLA
    # ========================================================

    tabla_frame = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    tabla_frame.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=18,
        pady=(0, 18)
    )

    tabla_frame.grid_rowconfigure(0, weight=1)
    tabla_frame.grid_columnconfigure(0, weight=1)

    columnas = (
        "id",
        "nombre",
        "dni",
        "fecha",
        "tutor",
        "telefono",
        "email",
        "acciones"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    # --------------------------------------------------------
    # ENCABEZADOS
    # --------------------------------------------------------

    tabla.heading(
        "id",
        text="ID"
    )

    tabla.heading(
        "nombre",
        text="Nombre y Apellido"
    )

    tabla.heading(
        "dni",
        text="DNI"
    )

    tabla.heading(
        "fecha",
        text="Fecha nacimiento"
    )

    tabla.heading(
        "tutor",
        text="Tutor"
    )

    tabla.heading(
        "telefono",
        text="Teléfono"
    )

    tabla.heading(
        "email",
        text="Email"
    )

    tabla.heading(
        "acciones",
        text="Acciones (CRUD)"
    )

    # --------------------------------------------------------
    # ANCHOS
    # --------------------------------------------------------

    tabla.column(
        "id",
        width=60,
        anchor="center"
    )

    tabla.column(
        "nombre",
        width=190
    )

    tabla.column(
        "dni",
        width=100,
        anchor="center"
    )

    tabla.column(
        "fecha",
        width=130,
        anchor="center"
    )

    tabla.column(
        "tutor",
        width=170
    )

    tabla.column(
        "telefono",
        width=130
    )

    tabla.column(
        "email",
        width=190
    )

    tabla.column(
        "acciones",
        width=130,
        anchor="center"
    )

    # --------------------------------------------------------
    # SCROLLBAR
    # --------------------------------------------------------

    scrollbar = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(
        yscrollcommand=scrollbar.set
    )

    tabla.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    # ========================================================
    # ESTILO TABLA
    # ========================================================

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except:
        pass

    estilo.configure(
        "Treeview",
        background=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=45,
        fieldbackground=COLOR_BLANCO,
        font=("Segoe UI", 9)
    )

    estilo.configure(
        "Treeview.Heading",
        background="#EDF2F6",
        foreground=COLOR_TEXTO,
        font=("Segoe UI", 9, "bold"),
        relief="flat"
    )

    estilo.map(
        "Treeview",
        background=[
            ("selected", "#DDF3F7")
        ],
        foreground=[
            ("selected", COLOR_TEXTO)
        ]
    )

    # ========================================================
    # FUNCIONES CRUD
    # ========================================================

    estudiantes_data = []

    # --------------------------------------------------------
    # LIMPIAR TABLA
    # --------------------------------------------------------

    def limpiar_tabla():

        for item in tabla.get_children():
            tabla.delete(item)

    # --------------------------------------------------------
    # CARGAR ESTUDIANTES
    # --------------------------------------------------------

    def cargar_estudiantes():

        nonlocal estudiantes_data

        try:

            respuesta = requests.get(
                API_URL,
                timeout=5
            )

            if respuesta.status_code != 200:
                raise Exception(
                    f"Error HTTP {respuesta.status_code}"
                )

            estudiantes_data = respuesta.json()

            limpiar_tabla()

            for estudiante in estudiantes_data:

                nombre_completo = (
                    f"{estudiante.get('nombre', '')} "
                    f"{estudiante.get('apellido', '')}"
                )

                tabla.insert(
                    "",
                    "end",
                    iid=str(estudiante.get("id")),
                    values=(
                        estudiante.get("id", ""),
                        nombre_completo,
                        estudiante.get("dni", ""),
                        estudiante.get("fecha_nacimiento", ""),
                        estudiante.get("nombre_tutor", ""),
                        estudiante.get("telefono_tutor", ""),
                        estudiante.get("email_tutor", ""),
                        "  ✎ Editar    🗑 Eliminar"
                    )
                )

            cantidad = len(estudiantes_data)

            label_total.config(
                text=str(cantidad)
            )

            label_registros.config(
                text=str(cantidad)
            )

            label_estado.config(
                text="● Conectado",
                fg=COLOR_VERDE
            )

        except requests.exceptions.ConnectionError:

            label_estado.config(
                text="● Sin conexión",
                fg=COLOR_ROJO
            )

            limpiar_tabla()

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el backend.\n\n"
                f"Verificá que Express esté ejecutándose en:\n"
                f"{API_URL}"
            )

        except Exception as error:

            label_estado.config(
                text="● Error",
                fg=COLOR_ROJO
            )

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ========================================================
    # FORMULARIO
    # ========================================================

    def abrir_formulario(estudiante=None):

        editando = estudiante is not None

        ventana = tk.Toplevel(frame)

        ventana.title(
            "Editar estudiante"
            if editando
            else "Nuevo estudiante"
        )

        ventana.geometry(
            "620x620"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.configure(
            bg=COLOR_BLANCO
        )

        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        encabezado = tk.Frame(
            ventana,
            bg=COLOR_AZUL,
            height=80
        )

        encabezado.pack(
            fill="x"
        )

        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text=(
                "EDITAR ALUMNO"
                if editando
                else "NUEVO ALUMNO"
            ),
            font=("Segoe UI", 17, "bold"),
            fg=COLOR_BLANCO,
            bg=COLOR_AZUL
        ).pack(
            anchor="w",
            padx=25,
            pady=23
        )

        # ----------------------------------------------------
        # FORMULARIO
        # ----------------------------------------------------

        form = tk.Frame(
            ventana,
            bg=COLOR_BLANCO
        )

        form.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        campos = {}

        datos = [
            ("nombre", "Nombre"),
            ("apellido", "Apellido"),
            ("dni", "DNI"),
            ("fecha_nacimiento", "Fecha de nacimiento"),
            ("nombre_tutor", "Nombre del tutor"),
            ("telefono_tutor", "Teléfono del tutor"),
            ("email_tutor", "Email del tutor")
        ]

        for fila, (clave, etiqueta) in enumerate(datos):

            tk.Label(
                form,
                text=etiqueta,
                font=("Segoe UI", 10, "bold"),
                fg=COLOR_TEXTO,
                bg=COLOR_BLANCO
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                pady=7
            )

            entrada = tk.Entry(
                form,
                font=("Segoe UI", 10),
                bg="#F5F8FA",
                fg=COLOR_TEXTO,
                relief="flat",
                highlightthickness=1,
                highlightbackground="#D8E1E8"
            )

            entrada.grid(
                row=fila,
                column=1,
                sticky="ew",
                padx=(20, 0),
                ipady=7
            )

            campos[clave] = entrada

            if editando:

                valor = estudiante.get(
                    clave,
                    ""
                )

                if valor is None:
                    valor = ""

                # Convertimos la fecha por si MySQL la devuelve
                # como objeto/string diferente.
                valor = str(valor)

                entrada.insert(
                    0,
                    valor
                )

        form.grid_columnconfigure(
            1,
            weight=1
        )

        # ----------------------------------------------------
        # BOTONES
        # ----------------------------------------------------

        botones = tk.Frame(
            ventana,
            bg=COLOR_BLANCO
        )

        botones.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        def guardar():

            datos_enviar = {}

            for clave, entrada in campos.items():

                valor = entrada.get().strip()

                datos_enviar[clave] = valor

            # Validaciones básicas

            if not datos_enviar["nombre"]:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá el nombre del estudiante.",
                    parent=ventana
                )
                return

            if not datos_enviar["apellido"]:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá el apellido del estudiante.",
                    parent=ventana
                )
                return

            if not datos_enviar["dni"]:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá el DNI.",
                    parent=ventana
                )
                return

            try:

                if editando:

                    id_estudiante = estudiante["id"]

                    respuesta = requests.put(
                        f"{API_URL}/{id_estudiante}",
                        json=datos_enviar,
                        timeout=5
                    )

                else:

                    respuesta = requests.post(
                        API_URL,
                        json=datos_enviar,
                        timeout=5
                    )

                if respuesta.status_code in (200, 201):

                    messagebox.showinfo(
                        "Correcto",
                        (
                            "Estudiante actualizado correctamente."
                            if editando
                            else
                            "Estudiante agregado correctamente."
                        ),
                        parent=ventana
                    )

                    ventana.destroy()

                    cargar_estudiantes()

                else:

                    try:
                        error_json = respuesta.json()
                        detalle = error_json.get(
                            "detalle",
                            error_json.get(
                                "error",
                                respuesta.text
                            )
                        )
                    except:
                        detalle = respuesta.text

                    messagebox.showerror(
                        "Error",
                        detalle,
                        parent=ventana
                    )

            except requests.exceptions.ConnectionError:

                messagebox.showerror(
                    "Error de conexión",
                    "No se pudo conectar con el backend.",
                    parent=ventana
                )

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=ventana
                )

        tk.Button(
            botones,
            text="Cancelar",
            font=("Segoe UI", 10, "bold"),
            bg="#E9EEF2",
            fg=COLOR_TEXTO,
            relief="flat",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=ventana.destroy
        ).pack(
            side="right",
            padx=5
        )

        tk.Button(
            botones,
            text=(
                "Guardar cambios"
                if editando
                else "Guardar alumno"
            ),
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_AZUL,
            fg=COLOR_BLANCO,
            activebackground=COLOR_AZUL_HOVER,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=guardar
        ).pack(
            side="right",
            padx=5
        )

        ventana.grab_set()

    # ========================================================
    # EDITAR
    # ========================================================

    def editar_seleccionado():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Editar",
                "Seleccioná un estudiante."
            )

            return

        id_estudiante = seleccion[0]

        try:

            respuesta = requests.get(
                f"{API_URL}/{id_estudiante}",
                timeout=5
            )

            if respuesta.status_code != 200:

                messagebox.showerror(
                    "Error",
                    "No se pudo obtener el estudiante."
                )

                return

            estudiante = respuesta.json()

            abrir_formulario(
                estudiante
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ========================================================
    # ELIMINAR
    # ========================================================

    def eliminar_seleccionado():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Eliminar",
                "Seleccioná un estudiante."
            )

            return

        id_estudiante = seleccion[0]

        datos = tabla.item(
            seleccion[0],
            "values"
        )

        nombre = datos[1]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Querés eliminar al estudiante?\n\n"
            f"{nombre}\n\n"
            f"Esta acción no se puede deshacer."
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{API_URL}/{id_estudiante}",
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Correcto",
                    "Estudiante eliminado correctamente."
                )

                cargar_estudiantes()

            elif respuesta.status_code == 404:

                messagebox.showwarning(
                    "No encontrado",
                    "El estudiante ya no existe."
                )

                cargar_estudiantes()

            else:

                try:
                    error_json = respuesta.json()

                    detalle = error_json.get(
                        "detalle",
                        error_json.get(
                            "error",
                            respuesta.text
                        )
                    )

                except:
                    detalle = respuesta.text

                messagebox.showerror(
                    "Error",
                    detalle
                )

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el backend."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ========================================================
    # BOTÓN NUEVO
    # ========================================================

    boton_nuevo.config(
        command=lambda: abrir_formulario()
    )

    # ========================================================
    # DOBLE CLICK = EDITAR
    # ========================================================

    tabla.bind(
        "<Double-1>",
        lambda event: editar_seleccionado()
    )

    # ========================================================
    # CLICK EN TABLA PARA EDITAR / ELIMINAR
    # ========================================================

    def click_tabla(event):

        region = tabla.identify_region(
            event.x,
            event.y
        )

        if region != "cell":
            return

        columna = tabla.identify_column(
            event.x
        )

        fila = tabla.identify_row(
            event.y
        )

        if not fila:
            return

        if columna == "#8":

            # En la columna acciones se decide
            # según la posición horizontal.

            x_inicio = tabla.column(
                "#8",
                "width"
            )

            # Abrimos un menú sencillo
            menu = tk.Menu(
                frame,
                tearoff=0
            )

            menu.add_command(
                label="✎ Editar",
                command=editar_seleccionado
            )

            menu.add_command(
                label="🗑 Eliminar",
                command=eliminar_seleccionado
            )

            try:
                menu.tk_popup(
                    event.x_root,
                    event.y_root
                )
            finally:
                menu.grab_release()

    tabla.bind(
        "<Button-1>",
        click_tabla
    )

    # ========================================================
    # TECLADO
    # ========================================================

    def teclado(event):

        if event.keysym == "Delete":

            eliminar_seleccionado()

        elif event.keysym == "F2":

            editar_seleccionado()

    tabla.bind(
        "<KeyRelease>",
        teclado
    )

    # ========================================================
    # BUSCADOR
    # ========================================================

    def buscar(event=None):

        texto = entrada_buscar.get().strip().lower()

        if texto == "buscar por nombre, apellido o dni...":
            texto = ""

        limpiar_tabla()

        for estudiante in estudiantes_data:

            nombre = str(
                estudiante.get(
                    "nombre",
                    ""
                )
            )

            apellido = str(
                estudiante.get(
                    "apellido",
                    ""
                )
            )

            dni = str(
                estudiante.get(
                    "dni",
                    ""
                )
            )

            completo = (
                f"{nombre} {apellido} {dni}"
            ).lower()

            if texto in completo:

                nombre_completo = (
                    f"{nombre} {apellido}"
                )

                tabla.insert(
                    "",
                    "end",
                    iid=str(
                        estudiante.get("id")
                    ),
                    values=(
                        estudiante.get("id", ""),
                        nombre_completo,
                        estudiante.get("dni", ""),
                        estudiante.get(
                            "fecha_nacimiento",
                            ""
                        ),
                        estudiante.get(
                            "nombre_tutor",
                            ""
                        ),
                        estudiante.get(
                            "telefono_tutor",
                            ""
                        ),
                        estudiante.get(
                            "email_tutor",
                            ""
                        ),
                        "  ✎ Editar    🗑 Eliminar"
                    )
                )

    entrada_buscar.bind(
        "<KeyRelease>",
        buscar
    )

    # ========================================================
    # BOTÓN REFRESCAR
    # ========================================================

    boton_refrescar = tk.Button(
        buscar_frame,
        text="↻",
        font=("Segoe UI", 14, "bold"),
        bg="#E8EEF3",
        fg=COLOR_TEXTO,
        relief="flat",
        bd=0,
        width=4,
        cursor="hand2",
        command=cargar_estudiantes
    )

    boton_refrescar.grid(
        row=0,
        column=1,
        padx=(10, 0)
    )

    # ========================================================
    # CARGAR DATOS AL ABRIR
    # ========================================================

    cargar_estudiantes()

    return frame