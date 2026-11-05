import tkinter as tk
from tkinter import ttk, messagebox
import requests
import re
from datetime import date

from frames.estudiantes import crear_estudiantes
from frames.asistencia import crear_asistencias
from frames.observaciones import crear_observaciones
from frames.docentes import crear_docentes


# ============================================================
# CONFIGURACIÓN DE LA API
# ============================================================

API_URL = "http://localhost:3000/api"

ESTUDIANTES_URL = f"{API_URL}/estudiantes"
ASISTENCIAS_URL = f"{API_URL}/asistencia"
CURSOS_URL = f"{API_URL}/cursos"


# ============================================================
# INICIO Y NAVEGACIÓN
# ============================================================

def crear_inicio(parent):

    COLOR_FONDO = "#F1F4F8"
    COLOR_AZUL = "#1E4D8F"
    COLOR_TURQUESA = "#20A4BD"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_GRIS = "#65778C"

    frame = tk.Frame(parent, bg=COLOR_FONDO)
    frame.pack(fill="both", expand=True)

    # --------------------------------------------------------
    # BARRA LATERAL
    # --------------------------------------------------------

    sidebar = tk.Frame(
        frame,
        bg=COLOR_BLANCO,
        width=235
    )

    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    logo_frame = tk.Frame(
        sidebar,
        bg=COLOR_BLANCO,
        height=85
    )

    logo_frame.pack(fill="x")
    logo_frame.pack_propagate(False)

    tk.Label(
        logo_frame,
        text="🌐",
        font=("Segoe UI Emoji", 22),
        bg=COLOR_BLANCO,
        fg=COLOR_TURQUESA
    ).pack(side="left", padx=(20, 7), pady=20)

    tk.Label(
        logo_frame,
        text="ProAConnect",
        font=("Segoe UI", 17, "bold"),
        bg=COLOR_BLANCO,
        fg=COLOR_AZUL
    ).pack(side="left", pady=20)

    tk.Frame(
        sidebar,
        bg="#DDE4EC",
        height=1
    ).pack(fill="x")

    # --------------------------------------------------------
    # CONTENIDO CENTRAL
    # --------------------------------------------------------

    contenido = tk.Frame(frame, bg=COLOR_FONDO)

    contenido.pack(
        side="left",
        fill="both",
        expand=True
    )

    botones = {}

    def mostrar_vista(nombre, funcion):

        for widget in contenido.winfo_children():
            widget.destroy()

        try:

            nueva_vista = funcion(contenido)

            if nueva_vista is not None:
                if not nueva_vista.winfo_manager():
                    nueva_vista.pack(
                        fill="both",
                        expand=True
                    )

        except Exception as error:

            messagebox.showerror(
                "Error al abrir la vista",
                f"No se pudo abrir '{nombre}'.\n\n{error}"
            )
            return

        for nombre_boton, boton in botones.items():

            seleccionado = nombre_boton == nombre

            boton.configure(
                bg=COLOR_TURQUESA if seleccionado else COLOR_BLANCO,
                fg="white" if seleccionado else COLOR_GRIS
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

        boton.pack(
            fill="x",
            padx=10,
            pady=4
        )

        botones[texto] = boton

    crear_boton("Home", "⌂", crear_home)
    crear_boton("Asistencia", "▣", crear_asistencias)
    crear_boton("Alumnos", "♟", crear_estudiantes)
    crear_boton("Docentes", "♟", crear_docentes)
    crear_boton("Observaciones", "☷", crear_observaciones)

    mostrar_vista("Home", crear_home)

    return frame


# ============================================================
# HOME
# ============================================================

def crear_home(parent):

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

    registros = []
    cursos = {}

    ciclo_actual = tk.StringVar(value="Todos")

    # ========================================================
    # FUNCIONES AUXILIARES
    # ========================================================

    def obtener_id_estudiante(alumno):
        return alumno.get("id_estudiante", alumno.get("id"))

    def obtener_nombre(alumno):

        nombre = alumno.get("nombre", "")
        apellido = alumno.get("apellido", "")

        return f"{nombre} {apellido}".strip() or "Sin nombre"

    def obtener_anio(alumno):

        anio = alumno.get("anio")

        if anio is not None:
            try:
                return int(anio)
            except (ValueError, TypeError):
                pass

        id_curso = alumno.get("id_curso")

        if id_curso is not None:

            curso = cursos.get(str(id_curso), {})

            try:
                return int(curso.get("anio", 0))
            except (ValueError, TypeError):
                pass

        texto = str(
            alumno.get("curso")
            or alumno.get("grado")
            or alumno.get("division")
            or ""
        )

        coincidencia = re.search(r"\b([1-6])\s*°?", texto)

        if coincidencia:
            return int(coincidencia.group(1))

        return 0

    def normalizar_fecha(fecha):

        if not fecha:
            return ""

        if hasattr(fecha, "isoformat"):
            return fecha.isoformat()[:10]

        return str(fecha)[:10]

    # ========================================================
    # CABECERA
    # ========================================================

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
    ).pack(side="left", pady=15)

    botones_header = tk.Frame(
        header,
        bg="#E8EDF3"
    )

    botones_header.pack(side="right", pady=15)

    for simbolo in ["+", "?", "♟", "●"]:

        tk.Label(
            botones_header,
            text=simbolo,
            font=("Segoe UI", 11, "bold"),
            bg="#E8EDF3",
            fg=COLOR_GRIS,
            width=3
        ).pack(side="left", padx=2)

    # ========================================================
    # TARJETAS DE ESTADÍSTICAS
    # ========================================================

    estadisticas = tk.Frame(
        home,
        bg=COLOR_FONDO
    )

    estadisticas.pack(
        fill="x",
        padx=25,
        pady=(5, 20)
    )

    def crear_tarjeta(
        titulo,
        color_fondo,
        color_texto,
        icono,
        color_icono
    ):

        tarjeta = tk.Frame(
            estadisticas,
            bg=color_fondo,
            height=120,
            highlightbackground="#DDE4EC",
            highlightthickness=1
        )

        tarjeta.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        tarjeta.pack_propagate(False)

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Segoe UI", 10, "bold"),
            bg=color_fondo,
            fg=color_texto
        ).pack(anchor="w", padx=18, pady=(15, 0))

        etiqueta_valor = tk.Label(
            tarjeta,
            text="0",
            font=("Segoe UI", 30, "bold"),
            bg=color_fondo,
            fg=color_texto
        )

        etiqueta_valor.pack(anchor="w", padx=18)

        tk.Label(
            tarjeta,
            text=icono,
            font=("Segoe UI", 18),
            bg=color_fondo,
            fg=color_icono
        ).place(relx=0.9, rely=0.45, anchor="center")

        barra = tk.Frame(
            tarjeta,
            bg="#E8EDF3",
            height=7
        )

        barra.pack(fill="x", padx=18, pady=(3, 0))
        barra.pack_propagate(False)

        progreso = tk.Frame(
            barra,
            bg=color_icono,
            width=0
        )

        progreso.pack(side="left", fill="y")

        return etiqueta_valor, progreso

    asistencia_valor, progreso1 = crear_tarjeta(
        "Asistencia Hoy",
        COLOR_TURQUESA,
        COLOR_BLANCO,
        "●",
        COLOR_BLANCO
    )

    faltas_valor, progreso2 = crear_tarjeta(
        "Faltas",
        COLOR_BLANCO,
        COLOR_TEXTO,
        "▲",
        COLOR_ROJO
    )

    tardanzas_valor, progreso3 = crear_tarjeta(
        "Llegadas Tarde",
        COLOR_BLANCO,
        COLOR_TEXTO,
        "▤",
        COLOR_VERDE
    )

    # ========================================================
    # PANEL DEL REGISTRO
    # ========================================================

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
    ).pack(side="left", pady=15)

    # ========================================================
    # BOTONES DE CICLO
    # ========================================================

    ciclos = tk.Frame(
        panel_header,
        bg="#E9EFF6"
    )

    ciclos.pack(side="right", pady=10)

    botones_ciclo = {}

    def seleccionar_ciclo(ciclo):

        ciclo_actual.set(ciclo)

        for nombre, boton in botones_ciclo.items():

            seleccionado = nombre == ciclo

            boton.configure(
                bg=COLOR_TURQUESA if seleccionado else "#E9EFF6",
                fg=COLOR_BLANCO if seleccionado else COLOR_TEXTO
            )

        actualizar_tabla()

    def crear_boton_ciclo(texto, ciclo):

        boton = tk.Button(
            ciclos,
            text=texto,
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_TURQUESA if ciclo == "Todos" else "#E9EFF6",
            fg=COLOR_BLANCO if ciclo == "Todos" else COLOR_TEXTO,
            activebackground=COLOR_TURQUESA,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=7,
            command=lambda: seleccionar_ciclo(ciclo)
        )

        boton.pack(side="left")
        botones_ciclo[ciclo] = boton

    crear_boton_ciclo(
        "Ciclo Básico (1° - 3°)",
        "Basico"
    )

    crear_boton_ciclo(
        "Ciclo Orientado (4° - 6°)",
        "Orientado"
    )

    crear_boton_ciclo(
        "Todos",
        "Todos"
    )

    # ========================================================
    # TABLA
    # ========================================================

    contenedor_tabla = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    contenedor_tabla.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=(0, 10)
    )

    columnas = (
        "id",
        "nombre",
        "estado",
        "observaciones"
    )

    tabla = ttk.Treeview(
        contenedor_tabla,
        columns=columnas,
        show="headings",
        height=12
    )

    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre y Año")
    tabla.heading("estado", text="Estado")
    tabla.heading("observaciones", text="Observaciones")

    tabla.column("id", width=110, anchor="center")
    tabla.column("nombre", width=250, anchor="w")
    tabla.column("estado", width=130, anchor="center")
    tabla.column("observaciones", width=280, anchor="w")

    scroll = ttk.Scrollbar(
        contenedor_tabla,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(yscrollcommand=scroll.set)

    tabla.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    tabla.tag_configure(
        "Presente",
        background="#E8F8F2",
        foreground=COLOR_VERDE
    )

    tabla.tag_configure(
        "Tardanza",
        background="#FFF3D6",
        foreground=COLOR_AMARILLO
    )

    tabla.tag_configure(
        "Falta",
        background="#FFE5E8",
        foreground=COLOR_ROJO
    )

    tabla.tag_configure(
        "Otro",
        background=COLOR_BLANCO,
        foreground=COLOR_TEXTO
    )

    # ========================================================
    # CARGAR DATOS DESDE LA API
    # ========================================================

    def cargar_datos():

        nonlocal registros, cursos

        try:

            # CURSOS

            cursos = {}

            try:

                respuesta_cursos = requests.get(
                    CURSOS_URL,
                    timeout=5
                )

                respuesta_cursos.raise_for_status()

                datos_cursos = respuesta_cursos.json()

                if isinstance(datos_cursos, dict):
                    datos_cursos = datos_cursos.get("cursos", [])

                cursos = {
                    str(curso["id_curso"]): curso
                    for curso in datos_cursos
                    if curso.get("id_curso") is not None
                }

            except requests.RequestException:
                cursos = {}

            # ALUMNOS

            respuesta_alumnos = requests.get(
                ESTUDIANTES_URL,
                timeout=5
            )

            respuesta_alumnos.raise_for_status()

            alumnos = respuesta_alumnos.json()

            if isinstance(alumnos, dict):
                alumnos = alumnos.get("estudiantes", [])

            # ASISTENCIAS

            respuesta_asistencias = requests.get(
                ASISTENCIAS_URL,
                timeout=5
            )

            respuesta_asistencias.raise_for_status()

            asistencias = respuesta_asistencias.json()

            if isinstance(asistencias, dict):
                asistencias = asistencias.get("asistencias", [])

            # RELACIONAR ASISTENCIA Y ALUMNO

            registros = []

            for asistencia in asistencias:

                id_estudiante = asistencia.get("id_estudiante")

                alumno = next(
                    (
                        a for a in alumnos
                        if str(obtener_id_estudiante(a))
                        == str(id_estudiante)
                    ),
                    None
                )

                if alumno is not None:

                    registros.append({
                        "asistencia": asistencia,
                        "alumno": alumno
                    })

            actualizar_tabla()
            actualizar_estadisticas()

        except (requests.RequestException, ValueError) as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudieron cargar los datos.\n\n"
                "Verificá que Express esté iniciado y que las "
                "rutas de estudiantes y asistencias sean correctas.\n\n"
                f"Detalle: {error}"
            )

    # ========================================================
    # FILTRAR Y ACTUALIZAR TABLA
    # ========================================================

    def actualizar_tabla():

        for elemento in tabla.get_children():
            tabla.delete(elemento)

        for registro in registros:

            asistencia = registro["asistencia"]
            alumno = registro["alumno"]

            anio = obtener_anio(alumno)

            if ciclo_actual.get() == "Basico" and anio not in (1, 2, 3):
                continue

            if ciclo_actual.get() == "Orientado" and anio not in (4, 5, 6):
                continue

            id_asistencia = asistencia.get("id_asistencia")

            if id_asistencia is None:
                continue

            nombre = obtener_nombre(alumno)

            nombre_anio = (
                f"{nombre} ({anio}° Año)"
                if anio
                else nombre
            )

            estado = asistencia.get("estado", "Sin registrar")

            observacion = (
                asistencia.get("motivo_justificacion", "")
                or ""
            )

            tag = (
                estado
                if estado in ("Presente", "Tardanza", "Falta")
                else "Otro"
            )

            tabla.insert(
                "",
                "end",
                iid=str(id_asistencia),
                values=(
                    id_asistencia,
                    nombre_anio,
                    estado,
                    observacion
                ),
                tags=(tag,)
            )

    # ========================================================
    # ACTUALIZAR ESTADÍSTICAS DEL DÍA
    # ========================================================

    def actualizar_estadisticas():

        hoy = date.today().isoformat()

        asistencias_hoy = [
            registro["asistencia"]
            for registro in registros
            if normalizar_fecha(
                registro["asistencia"].get("fecha")
            ) == hoy
        ]

        presentes = sum(
            1 for a in asistencias_hoy
            if a.get("estado") == "Presente"
        )

        faltas = sum(
            1 for a in asistencias_hoy
            if a.get("estado") in ("Falta", "Ausente")
        )

        tardanzas = sum(
            1 for a in asistencias_hoy
            if a.get("estado") == "Tardanza"
        )

        total = len(asistencias_hoy)

        porcentaje = round(presentes * 100 / total) if total else 0

        asistencia_valor.configure(text=f"{porcentaje}%")
        faltas_valor.configure(text=str(faltas))
        tardanzas_valor.configure(text=str(tardanzas))

        ancho = 250

        progreso1.configure(
            width=int(ancho * presentes / total) if total else 0
        )

        progreso2.configure(
            width=int(ancho * faltas / total) if total else 0
        )

        progreso3.configure(
            width=int(ancho * tardanzas / total) if total else 0
        )

    # ========================================================
    # EDITAR ASISTENCIA - CORREGIDO
    # ========================================================

    def editar_asistencia():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar registro",
                "Seleccioná una asistencia de la tabla."
            )

            return

        id_asistencia = seleccion[0]

        registro = next(
            (
                r for r in registros
                if str(r["asistencia"].get("id_asistencia"))
                == str(id_asistencia)
            ),
            None
        )

        if registro is None:

            messagebox.showerror(
                "Error",
                "No se encontró la asistencia seleccionada."
            )

            return

        asistencia = registro["asistencia"]

        ventana = tk.Toplevel(home)

        ventana.title("Editar asistencia")
        ventana.geometry("420x320")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_FONDO)

        ventana.transient(home.winfo_toplevel())
        ventana.grab_set()

        tk.Label(
            ventana,
            text="EDITAR ASISTENCIA",
            font=("Segoe UI", 15, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_AZUL
        ).pack(pady=(20, 15))

        # ESTADO

        tk.Label(
            ventana,
            text="Estado:",
            font=("Segoe UI", 10),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(anchor="w", padx=35)

        estado_var = tk.StringVar(
            value=asistencia.get("estado", "Presente")
        )

        ttk.Combobox(
            ventana,
            textvariable=estado_var,
            values=(
                "Presente",
                "Tardanza",
                "Falta",
                "Ausente"
            ),
            state="readonly",
            font=("Segoe UI", 10)
        ).pack(
            fill="x",
            padx=35,
            pady=(5, 15)
        )

        # MOTIVO / OBSERVACIÓN

        tk.Label(
            ventana,
            text="Motivo / observación:",
            font=("Segoe UI", 10),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(anchor="w", padx=35)

        observacion_var = tk.StringVar(
            value=asistencia.get(
                "motivo_justificacion", ""
            ) or ""
        )

        tk.Entry(
            ventana,
            textvariable=observacion_var,
            font=("Segoe UI", 10)
        ).pack(
            fill="x",
            padx=35,
            pady=(5, 15)
        )

        # GUARDAR CAMBIOS

        def guardar_cambios():

            nuevo_estado = estado_var.get().strip()
            nuevo_motivo = observacion_var.get().strip()

            if not nuevo_estado:

                messagebox.showwarning(
                    "Datos incompletos",
                    "Seleccioná un estado.",
                    parent=ventana
                )

                return

            datos = {
                "estado": nuevo_estado,
                "motivo_justificacion": nuevo_motivo
            }

            try:

                respuesta = requests.put(
                    f"{ASISTENCIAS_URL}/{id_asistencia}",
                    json=datos,
                    headers={
                        "Content-Type": "application/json"
                    },
                    timeout=10
                )

                respuesta.raise_for_status()

                messagebox.showinfo(
                    "Actualización correcta",
                    "La asistencia se modificó correctamente.",
                    parent=ventana
                )

                ventana.destroy()

                cargar_datos()

            except requests.RequestException as error:

                detalle = ""

                if error.response is not None:

                    try:
                        detalle = error.response.json()
                    except ValueError:
                        detalle = error.response.text

                messagebox.showerror(
                    "Error al editar",
                    "No se pudo actualizar la asistencia.\n\n"
                    f"Detalle: {detalle or error}",
                    parent=ventana
                )

        tk.Button(
            ventana,
            text="Guardar cambios",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_TURQUESA,
            fg=COLOR_BLANCO,
            activebackground=COLOR_AZUL,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            cursor="hand2",
            command=guardar_cambios
        ).pack(pady=10, ipadx=15, ipady=5)

    # ========================================================
    # ELIMINAR ASISTENCIA
    # ========================================================

    def eliminar_asistencia():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar registro",
                "Seleccioná una asistencia de la tabla."
            )

            return

        id_asistencia = seleccion[0]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de que querés eliminar "
            "esta asistencia?\n\n"
            "Esta acción no se puede deshacer."
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{ASISTENCIAS_URL}/{id_asistencia}",
                timeout=5
            )

            respuesta.raise_for_status()

            messagebox.showinfo(
                "Eliminación correcta",
                "La asistencia se eliminó correctamente."
            )

            cargar_datos()

        except requests.RequestException as error:

            messagebox.showerror(
                "Error al eliminar",
                "No se pudo eliminar la asistencia.\n\n"
                "Verificá que exista la ruta "
                "DELETE /api/asistencia/:id.\n\n"
                f"Detalle: {error}"
            )

    # ========================================================
    # BOTONES DE ACCIONES CRUD
    # ========================================================

    acciones = tk.Frame(
        panel,
        bg=COLOR_BLANCO
    )

    acciones.pack(
        fill="x",
        padx=18,
        pady=(0, 12)
    )

    tk.Button(
        acciones,
        text="✎ Editar asistencia",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_TURQUESA,
        fg=COLOR_BLANCO,
        activebackground=COLOR_AZUL,
        activeforeground=COLOR_BLANCO,
        relief="flat",
        cursor="hand2",
        command=editar_asistencia
    ).pack(
        side="left",
        padx=(0, 10),
        ipadx=8,
        ipady=5
    )

    tk.Button(
        acciones,
        text="▣ Eliminar asistencia",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_ROJO,
        fg=COLOR_BLANCO,
        activebackground="#C62828",
        activeforeground=COLOR_BLANCO,
        relief="flat",
        cursor="hand2",
        command=eliminar_asistencia
    ).pack(
        side="left",
        padx=5,
        ipadx=8,
        ipady=5
    )

    tk.Button(
        acciones,
        text="↻ Actualizar",
        font=("Segoe UI", 10, "bold"),
        bg="#E9EFF6",
        fg=COLOR_TEXTO,
        activebackground="#DDE4EC",
        relief="flat",
        cursor="hand2",
        command=cargar_datos
    ).pack(
        side="right",
        ipadx=8,
        ipady=5
    )

    # ========================================================
    # INICIAR HOME
    # ========================================================

    seleccionar_ciclo("Todos")
    cargar_datos()

    return home