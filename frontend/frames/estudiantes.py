import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ============================================================
# CONFIGURACIÓN
# ============================================================

API_URL = "http://localhost:3000/api/estudiantes"
CURSOS_URL = "http://localhost:3000/api/cursos"


# ============================================================
# COLORES
# ============================================================

COLOR_FONDO = "#F3F6FA"
COLOR_AZUL = "#179FB8"
COLOR_BLANCO = "#FFFFFF"
COLOR_TEXTO = "#172B4D"
COLOR_GRIS = "#65758B"
COLOR_ROJO = "#F04B50"
COLOR_VERDE = "#19B47A"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_id(estudiante):
    return estudiante.get(
        "id_estudiante",
        estudiante.get("id")
    )


def texto_curso(curso):

    nombre = curso.get("nombre_curso")

    if nombre:
        texto = str(nombre)
    else:
        texto = "Curso"

    division = curso.get("division")
    turno = curso.get("turno")

    if division:
        texto += " - " + str(division)

    if turno:
        texto += " - " + str(turno)

    return texto

def formatear_fecha(fecha):
    """
    Convierte una fecha de YYYY-MM-DD a DD/MM/YYYY
    para mostrarla en la tabla.
    """

    if not fecha:
        return ""

    fecha = str(fecha)

    try:
        # Si viene como YYYY-MM-DD
        partes = fecha[:10].split("-")

        if len(partes) == 3:
            anio, mes, dia = partes
            return f"{dia}/{mes}/{anio}"

    except Exception:
        pass

    return fecha

# ============================================================
# PANTALLA PRINCIPAL
# ============================================================

def crear_estudiantes(parent):

    frame = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )

    # ========================================================
    # VARIABLES
    # ========================================================

    estudiantes = []
    cursos = []
    cursos_diccionario = {}

    # ========================================================
    # ENCABEZADO
    # ========================================================

    encabezado = tk.Frame(
        frame,
        bg=COLOR_FONDO
    )

    encabezado.pack(
        fill="x",
        padx=25,
        pady=(20, 10)
    )

    tk.Label(
        encabezado,
        text="Gestión de alumnos",
        font=("Segoe UI", 24, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO
    ).pack(side="left")

    estado_conexion = tk.Label(
        encabezado,
        text="● Conectando...",
        font=("Segoe UI", 10),
        bg=COLOR_FONDO,
        fg=COLOR_GRIS
    )

    estado_conexion.pack(
        side="right",
        pady=10
    )

    # ========================================================
    # TARJETAS
    # ========================================================

    tarjetas = tk.Frame(
        frame,
        bg=COLOR_FONDO
    )

    tarjetas.pack(
        fill="x",
        padx=25,
        pady=5
    )

    def crear_tarjeta(titulo, valor):

        tarjeta = tk.Frame(
            tarjetas,
            bg=COLOR_BLANCO,
            highlightbackground="#DDE4EC",
            highlightthickness=1
        )

        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Segoe UI", 10),
            bg=COLOR_BLANCO,
            fg=COLOR_GRIS
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        etiqueta_valor = tk.Label(
            tarjeta,
            text=valor,
            font=("Segoe UI", 22, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        )

        etiqueta_valor.pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        return etiqueta_valor

    lbl_total = crear_tarjeta(
        "Total de alumnos",
        "0"
    )

    lbl_cargados = crear_tarjeta(
        "Registros cargados",
        "0"
    )

    lbl_cursos = crear_tarjeta(
        "Cursos disponibles",
        "0"
    )

    # ========================================================
    # PANEL
    # ========================================================

    panel = tk.Frame(
        frame,
        bg=COLOR_BLANCO,
        highlightbackground="#DDE4EC",
        highlightthickness=1
    )

    panel.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=15
    )

    # ========================================================
    # BOTONES
    # ========================================================

    zona_botones = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    zona_botones.pack(
        fill="x",
        padx=15,
        pady=(15, 10)
    )

    boton_nuevo = tk.Button(
        zona_botones,
        text="+ Nuevo alumno",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_VERDE,
        fg="white",
        activebackground=COLOR_VERDE,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=9
    )

    boton_nuevo.pack(
        side="left",
        padx=(0, 8)
    )

    boton_editar = tk.Button(
        zona_botones,
        text="✎ Editar seleccionado",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_AZUL,
        fg="white",
        activebackground=COLOR_AZUL,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=9
    )

    boton_editar.pack(
        side="left",
        padx=8
    )

    boton_eliminar = tk.Button(
        zona_botones,
        text="Eliminar seleccionado",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_ROJO,
        fg="white",
        activebackground=COLOR_ROJO,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=9
    )

    boton_eliminar.pack(
        side="left",
        padx=8
    )

    # ========================================================
    # FILTROS
    # ========================================================

    zona_filtros = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    zona_filtros.pack(
        fill="x",
        padx=15,
        pady=5
    )

    tk.Label(
        zona_filtros,
        text="Buscar:",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO
    ).pack(side="left")

    busqueda_var = tk.StringVar()

    entrada_busqueda = tk.Entry(
        zona_filtros,
        textvariable=busqueda_var,
        font=("Segoe UI", 10),
        width=30
    )

    entrada_busqueda.pack(
        side="left",
        padx=(8, 20)
    )

    tk.Label(
        zona_filtros,
        text="Curso:",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO
    ).pack(side="left")

    curso_var = tk.StringVar()

    combo_curso = ttk.Combobox(
        zona_filtros,
        textvariable=curso_var,
        state="readonly",
        width=28
    )

    combo_curso.pack(
        side="left",
        padx=8
    )

    boton_actualizar = tk.Button(
        zona_filtros,
        text="⟳ Actualizar",
        font=("Segoe UI", 9, "bold"),
        bg="#E8EEF5",
        fg=COLOR_TEXTO,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=5
    )

    boton_actualizar.pack(
        side="right"
    )

    # ========================================================
    # TABLA
    # ========================================================

    zona_tabla = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    zona_tabla.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(10, 15)
    )

    columnas = (
        "id",
        "alumno",
        "dni",
        "fecha",
        "curso",
        "tutor",
        "telefono",
        "email"
    )

    tabla = ttk.Treeview(
        zona_tabla,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    encabezados = {
        "id": "ID",
        "alumno": "Alumno",
        "dni": "DNI",
        "fecha": "Fecha nacimiento",
        "curso": "Curso",
        "tutor": "Tutor",
        "telefono": "Teléfono",
        "email": "Email"
    }

    anchos = {
        "id": 50,
        "alumno": 180,
        "dni": 100,
        "fecha": 120,
        "curso": 180,
        "tutor": 160,
        "telefono": 120,
        "email": 200
    }

    for columna in columnas:

        tabla.heading(
            columna,
            text=encabezados[columna]
        )

        tabla.column(
            columna,
            width=anchos[columna]
        )

    scroll_vertical = ttk.Scrollbar(
        zona_tabla,
        orient="vertical",
        command=tabla.yview
    )

    scroll_horizontal = ttk.Scrollbar(
        zona_tabla,
        orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        yscrollcommand=scroll_vertical.set,
        xscrollcommand=scroll_horizontal.set
    )

    tabla.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    scroll_vertical.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    scroll_horizontal.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    zona_tabla.grid_rowconfigure(
        0,
        weight=1
    )

    zona_tabla.grid_columnconfigure(
        0,
        weight=1
    )

    # ========================================================
    # MOSTRAR TABLA
    # ========================================================

    def filtrar_y_mostrar():

        texto = busqueda_var.get().strip().lower()
        curso_seleccionado = curso_var.get()

        for item in tabla.get_children():
            tabla.delete(item)

        cantidad = 0

        for alumno in estudiantes:

            nombre = str(
                alumno.get("nombre", "")
            )

            apellido = str(
                alumno.get("apellido", "")
            )

            dni = str(
                alumno.get("dni", "")
            )

            nombre_completo = (
                nombre + " " + apellido
            ).lower()

            if texto:

                if (
                    texto not in nombre_completo
                    and texto not in dni.lower()
                ):
                    continue

            # ----------------------------------------------
            # FILTRO POR CURSO
            # ----------------------------------------------

            if (
                curso_seleccionado
                and curso_seleccionado != "Todos los cursos"
            ):

                id_curso_alumno = str(
                    alumno.get("id_curso", "")
                )

                id_curso_filtro = str(
                    cursos_diccionario.get(
                        curso_seleccionado,
                        ""
                    )
                )

                if id_curso_alumno != id_curso_filtro:
                    continue

            id_estudiante = obtener_id(alumno)

            fecha = alumno.get(
                "fecha_nacimiento",
                ""
            )

            fecha = formatear_fecha(fecha)

            curso = alumno.get(
                "nombre_curso",
                "Sin curso"
            )

            if alumno.get("division"):
                curso += " - " + str(
                    alumno.get("division")
                )

            if alumno.get("turno"):
                curso += " - " + str(
                    alumno.get("turno")
                )

            nombre_completo = (
                f"{alumno.get('nombre', '')} "
                f"{alumno.get('apellido', '')}"
            ).strip()

            tabla.insert(
                "",
                "end",
                iid=str(id_estudiante),
                values=(
                    id_estudiante,
                    nombre_completo,
                    alumno.get("dni", ""),
                    fecha,
                    curso,
                    alumno.get("nombre_tutor", ""),
                    alumno.get("telefono_tutor", ""),
                    alumno.get("email_tutor", "")
                )
            )

            cantidad += 1

        lbl_cargados.config(
            text=str(cantidad)
        )

    # ========================================================
    # CARGAR CURSOS
    # ========================================================

    def cargar_cursos():

        nonlocal cursos, cursos_diccionario

        try:

            respuesta = requests.get(
                CURSOS_URL,
                timeout=8
            )

            respuesta.raise_for_status()

            cursos = respuesta.json()

            cursos_diccionario = {}

            valores = [
                "Todos los cursos"
            ]

            for curso in cursos:

                nombre = texto_curso(curso)

                id_curso = curso.get(
                    "id_curso"
                )

                cursos_diccionario[
                    nombre
                ] = id_curso

                valores.append(
                    nombre
                )

            combo_curso["values"] = valores

            curso_var.set(
                "Todos los cursos"
            )

            lbl_cursos.config(
                text=str(len(cursos))
            )

            estado_conexion.config(
                text="● Conectado",
                fg=COLOR_VERDE
            )

        except requests.RequestException as error:

            estado_conexion.config(
                text="● Error de conexión",
                fg=COLOR_ROJO
            )

            messagebox.showerror(
                "Error",
                "No se pudieron cargar los cursos.\n\n"
                + str(error),
                parent=frame
            )

    # ========================================================
    # CARGAR ESTUDIANTES
    # ========================================================

    def cargar_estudiantes(
        mostrar_mensaje=True
    ):

        nonlocal estudiantes

        try:

            respuesta = requests.get(
                API_URL,
                timeout=8
            )

            respuesta.raise_for_status()

            estudiantes = respuesta.json()

            lbl_total.config(
                text=str(len(estudiantes))
            )

            filtrar_y_mostrar()

            estado_conexion.config(
                text="● Conectado",
                fg=COLOR_VERDE
            )

        except requests.RequestException as error:

            estado_conexion.config(
                text="● Error de conexión",
                fg=COLOR_ROJO
            )

            if mostrar_mensaje:

                messagebox.showerror(
                    "Error",
                    "No se pudieron cargar los estudiantes.\n\n"
                    + str(error),
                    parent=frame
                )

    # ========================================================
    # OBTENER CURSO
    # ========================================================

    def obtener_id_curso(curso_form_var):

        nombre_curso = curso_form_var.get().strip()

        if not nombre_curso:
            return None

        return cursos_diccionario.get(
            nombre_curso
        )

    # ========================================================
    # FORMULARIO NUEVO / EDITAR
    # ========================================================

    def abrir_formulario(
        modo="nuevo",
        alumno=None
    ):

        ventana = tk.Toplevel(
            frame
        )

        ventana.transient(
            frame.winfo_toplevel()
        )

        ventana.grab_set()

        if modo == "nuevo":
            ventana.title(
                "Nuevo alumno"
            )
        else:
            ventana.title(
                "Editar alumno"
            )

        ventana.geometry(
            "650x650"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.configure(
            bg=COLOR_FONDO
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        tk.Label(
            ventana,
            text=(
                "Nuevo alumno"
                if modo == "nuevo"
                else "Editar alumno"
            ),
            font=("Segoe UI", 20, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        formulario = tk.Frame(
            ventana,
            bg=COLOR_BLANCO,
            highlightbackground="#DDE4EC",
            highlightthickness=1
        )

        formulario.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        # ====================================================
        # VARIABLES DEL FORMULARIO
        # ====================================================

        nombre_var = tk.StringVar()
        apellido_var = tk.StringVar()
        dni_var = tk.StringVar()
        fecha_var = tk.StringVar()
        tutor_var = tk.StringVar()
        telefono_var = tk.StringVar()
        email_var = tk.StringVar()

        # ESTA ES LA VARIABLE CORRECTA
        curso_form_var = tk.StringVar()

        # ====================================================
        # CAMPOS
        # ====================================================

        def crear_campo(
            fila,
            texto,
            variable
        ):

            tk.Label(
                formulario,
                text=texto,
                font=("Segoe UI", 10, "bold"),
                bg=COLOR_BLANCO,
                fg=COLOR_TEXTO
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                padx=20,
                pady=8
            )

            entrada = tk.Entry(
                formulario,
                textvariable=variable,
                font=("Segoe UI", 10),
                width=38
            )

            entrada.grid(
                row=fila,
                column=1,
                sticky="ew",
                padx=20,
                pady=8
            )

            return entrada

        formulario.grid_columnconfigure(
            1,
            weight=1
        )

        crear_campo(
            0,
            "Nombre:",
            nombre_var
        )

        crear_campo(
            1,
            "Apellido:",
            apellido_var
        )

        crear_campo(
            2,
            "DNI:",
            dni_var
        )

        crear_campo(
            3,
            "Fecha de nacimiento:",
            fecha_var
        )

        crear_campo(
            4,
            "Nombre del tutor:",
            tutor_var
        )

        crear_campo(
            5,
            "Teléfono del tutor:",
            telefono_var
        )

        crear_campo(
            6,
            "Email del tutor:",
            email_var
        )

        # ====================================================
        # CURSO
        # ====================================================

        tk.Label(
            formulario,
            text="Curso:",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).grid(
            row=7,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        combo_form_curso = ttk.Combobox(
            formulario,
            textvariable=curso_form_var,
            state="readonly",
            width=35
        )

        combo_form_curso.grid(
            row=7,
            column=1,
            sticky="ew",
            padx=20,
            pady=8
        )

        combo_form_curso["values"] = list(
            cursos_diccionario.keys()
        )

        # ====================================================
        # CARGAR DATOS PARA EDITAR
        # ====================================================

        if modo == "editar" and alumno:

            nombre_var.set(
                alumno.get("nombre", "")
            )

            apellido_var.set(
                alumno.get("apellido", "")
            )

            dni_var.set(
                alumno.get("dni", "")
            )

            fecha = alumno.get(
                "fecha_nacimiento",
                ""
            )

            fecha_var.set(
                str(fecha)
            )

            tutor_var.set(
                alumno.get(
                    "nombre_tutor",
                    ""
                )
            )

            telefono_var.set(
                alumno.get(
                    "telefono_tutor",
                    ""
                )
            )

            email_var.set(
                alumno.get(
                    "email_tutor",
                    ""
                )
            )

            id_curso_actual = alumno.get(
                "id_curso"
            )

            for nombre_curso, id_curso in cursos_diccionario.items():

                if str(id_curso) == str(
                    id_curso_actual
                ):

                    curso_form_var.set(
                        nombre_curso
                    )

                    break

        # ====================================================
        # BOTONES
        # ====================================================

        zona_botones_form = tk.Frame(
            formulario,
            bg=COLOR_BLANCO
        )

        zona_botones_form.grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="e",
            padx=20,
            pady=20
        )

        tk.Button(
            zona_botones_form,
            text="Cancelar",
            font=("Segoe UI", 10, "bold"),
            bg="#E8EEF5",
            fg=COLOR_TEXTO,
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8,
            command=ventana.destroy
        ).pack(
            side="left",
            padx=5
        )

        # ====================================================
        # GUARDAR
        # ====================================================

        def guardar():

            nombre = nombre_var.get().strip()
            apellido = apellido_var.get().strip()
            dni = dni_var.get().strip()
            fecha = fecha_var.get().strip()
            tutor = tutor_var.get().strip()
            telefono = telefono_var.get().strip()
            email = email_var.get().strip()

            # ACÁ SE USA LA VARIABLE CORRECTA
            id_curso = obtener_id_curso(
                curso_form_var
            )

            # ------------------------------------------------
            # VALIDACIONES
            # ------------------------------------------------

            if not nombre:

                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá el nombre del alumno.",
                    parent=ventana
                )

                return

            if not apellido:

                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá el apellido del alumno.",
                    parent=ventana
                )

                return

            if not dni:

                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá el DNI del alumno.",
                    parent=ventana
                )

                return

            if not id_curso:

                messagebox.showwarning(
                    "Datos incompletos",
                    "Seleccioná un curso.",
                    parent=ventana
                )

                return

            datos = {
                "nombre": nombre,
                "apellido": apellido,
                "dni": dni,
                "fecha_nacimiento": fecha,
                "nombre_tutor": tutor,
                "telefono_tutor": telefono,
                "email_tutor": email,
                "id_curso": id_curso
            }

            # =================================================
            # NUEVO ALUMNO
            # =================================================

            if modo == "nuevo":

                try:

                    respuesta = requests.post(
                        API_URL,
                        json=datos,
                        timeout=8
                    )

                    if respuesta.status_code not in (
                        200,
                        201
                    ):

                        try:

                            informacion = respuesta.json()

                            detalle = informacion.get(
                                "detalle",
                                informacion.get(
                                    "error",
                                    "Error desconocido"
                                )
                            )

                        except Exception:

                            detalle = respuesta.text

                        messagebox.showerror(
                            "Error al agregar",
                            detalle,
                            parent=ventana
                        )

                        return

                    messagebox.showinfo(
                        "Alumno agregado",
                        "El alumno fue agregado correctamente.",
                        parent=ventana
                    )

                    ventana.destroy()

                    cargar_estudiantes(
                        mostrar_mensaje=False
                    )

                except requests.RequestException as error:

                    messagebox.showerror(
                        "Error de conexión",
                        "No se pudo conectar con el servidor.\n\n"
                        + str(error),
                        parent=ventana
                    )

            # =================================================
            # EDITAR ALUMNO
            # =================================================

            else:

                id_estudiante = obtener_id(
                    alumno
                )

                try:

                    respuesta = requests.put(
                        f"{API_URL}/{id_estudiante}",
                        json=datos,
                        timeout=8
                    )

                    if respuesta.status_code not in (
                        200,
                        201
                    ):

                        try:

                            informacion = respuesta.json()

                            detalle = informacion.get(
                                "detalle",
                                informacion.get(
                                    "error",
                                    "Error desconocido"
                                )
                            )

                        except Exception:

                            detalle = respuesta.text

                        messagebox.showerror(
                            "Error al editar",
                            detalle,
                            parent=ventana
                        )

                        return

                    messagebox.showinfo(
                        "Alumno actualizado",
                        "Los datos del alumno fueron actualizados correctamente.",
                        parent=ventana
                    )

                    ventana.destroy()

                    cargar_estudiantes(
                        mostrar_mensaje=False
                    )

                except requests.RequestException as error:

                    messagebox.showerror(
                        "Error de conexión",
                        "No se pudo conectar con el servidor.\n\n"
                        + str(error),
                        parent=ventana
                    )

        tk.Button(
            zona_botones_form,
            text=(
                "Agregar alumno"
                if modo == "nuevo"
                else "Guardar cambios"
            ),
            font=("Segoe UI", 10, "bold"),
            bg=(
                COLOR_VERDE
                if modo == "nuevo"
                else COLOR_AZUL
            ),
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8,
            command=guardar
        ).pack(
            side="left",
            padx=5
        )

    # ========================================================
    # NUEVO ALUMNO
    # ========================================================

    def nuevo_alumno():

        if not cursos:

            cargar_cursos()

        if not cursos:

            messagebox.showwarning(
                "Cursos",
                "No hay cursos disponibles para seleccionar.",
                parent=frame
            )

            return

        abrir_formulario(
            modo="nuevo"
        )

    # ========================================================
    # EDITAR
    # ========================================================

    def editar_alumno():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Editar alumno",
                "Seleccioná un alumno de la tabla.",
                parent=frame
            )

            return

        id_estudiante = seleccion[0]

        alumno_encontrado = None

        for alumno in estudiantes:

            if str(
                obtener_id(alumno)
            ) == str(id_estudiante):

                alumno_encontrado = alumno
                break

        if alumno_encontrado is None:

            messagebox.showerror(
                "Error",
                "No se encontró la información del alumno.",
                parent=frame
            )

            return

        abrir_formulario(
            modo="editar",
            alumno=alumno_encontrado
        )

    # ========================================================
    # ELIMINAR
    # ========================================================

    def eliminar_alumno():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Eliminar alumno",
                "Seleccioná un alumno de la tabla.",
                parent=frame
            )

            return

        id_estudiante = seleccion[0]

        nombre = "el alumno seleccionado"

        for alumno in estudiantes:

            if str(
                obtener_id(alumno)
            ) == str(id_estudiante):

                nombre = (
                    f"{alumno.get('nombre', '')} "
                    f"{alumno.get('apellido', '')}"
                ).strip()

                break

        confirmar = messagebox.askyesno(
            "Eliminar alumno",
            f"¿Querés eliminar a {nombre}?\n\n"
            "Esta acción no se puede deshacer.",
            parent=frame
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{API_URL}/{id_estudiante}",
                timeout=8
            )

            if respuesta.status_code not in (
                200,
                204
            ):

                try:

                    informacion = respuesta.json()

                    detalle = informacion.get(
                        "detalle",
                        informacion.get(
                            "error",
                            "Error desconocido"
                        )
                    )

                except Exception:

                    detalle = respuesta.text

                messagebox.showerror(
                    "Error al eliminar",
                    detalle,
                    parent=frame
                )

                return

            messagebox.showinfo(
                "Alumno eliminado",
                "El alumno fue eliminado correctamente.",
                parent=frame
            )

            cargar_estudiantes(
                mostrar_mensaje=False
            )

        except requests.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                + str(error),
                parent=frame
            )

    # ========================================================
    # EVENTOS
    # ========================================================

    boton_nuevo.config(
        command=nuevo_alumno
    )

    boton_editar.config(
        command=editar_alumno
    )

    boton_eliminar.config(
        command=eliminar_alumno
    )

    entrada_busqueda.bind(
        "<KeyRelease>",
        lambda event: filtrar_y_mostrar()
    )

    combo_curso.bind(
        "<<ComboboxSelected>>",
        lambda event: filtrar_y_mostrar()
    )

    boton_actualizar.config(
        command=lambda: (
            cargar_cursos(),
            cargar_estudiantes(
                mostrar_mensaje=False
            )
        )
    )

    tabla.bind(
        "<Double-1>",
        lambda event: editar_alumno()
    )

    # ========================================================
    # CARGA INICIAL
    # ========================================================

    cargar_cursos()

    cargar_estudiantes(
        mostrar_mensaje=False
    )

    return frame