import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests


# ============================================================
# CONFIGURACIÓN
# ============================================================

API_URL = "http://localhost:3000"

ESTUDIANTES_URL = f"{API_URL}/estudiantes"
ASISTENCIAS_URL = f"{API_URL}/asistencias"

                                                                                                                                                                                                                                                                                                                                                                                                                                                    
# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def crear_asistencias(parent):

    # ========================================================
    # VARIABLES
    # ========================================================

    alumnos = []
    asistencias_existentes = {}

    filas = []

    fecha_var = tk.StringVar(
        value=datetime.now().strftime("%d/%m/%Y")
    )

    anio_var = tk.StringVar(
        value="Todos los Años"
    )

    # ========================================================
    # FRAME PRINCIPAL
    # ========================================================

    contenedor = tk.Frame(
        parent,
        bg="#F3F6FA"
    )

    contenedor.pack(
        fill="both",
        expand=True
    )

    # ========================================================
    # TÍTULO
    # ========================================================

    titulo = tk.Label(
        contenedor,
        text="Asistencia - Toma Diaria",
        font=("Segoe UI", 22, "bold"),
        bg="#F3F6FA",
        fg="#172B4D"
    )

    titulo.pack(
        anchor="w",
        padx=25,
        pady=(20, 15)
    )

    # ========================================================
    # PANEL SUPERIOR
    # ========================================================

    panel_filtros = tk.Frame(
        contenedor,
        bg="white",
        bd=0,
        highlightthickness=1,
        highlightbackground="#DDE4EC"
    )

    panel_filtros.pack(
        fill="x",
        padx=25,
        pady=(0, 20)
    )

    # --------------------------------------------------------
    # FECHA
    # --------------------------------------------------------

    lbl_fecha = tk.Label(
        panel_filtros,
        text="Fecha de Toma",
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#40526B"
    )

    lbl_fecha.grid(
        row=0,
        column=0,
        padx=(20, 5),
        pady=(15, 5),
        sticky="w"
    )

    entry_fecha = tk.Entry(
        panel_filtros,
        textvariable=fecha_var,
        font=("Segoe UI", 11),
        width=15,
        relief="solid",
        bd=1
    )

    entry_fecha.grid(
        row=1,
        column=0,
        padx=(20, 20),
        pady=(0, 15)
    )

    # --------------------------------------------------------
    # FILTRO AÑO
    # --------------------------------------------------------

    lbl_anio = tk.Label(
        panel_filtros,
        text="Filtrar Año",
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#40526B"
    )

    lbl_anio.grid(
        row=0,
        column=1,
        padx=5,
        pady=(15, 5),
        sticky="w"
    )

    combo_anio = ttk.Combobox(
        panel_filtros,
        textvariable=anio_var,
        state="readonly",
        width=18,
        font=("Segoe UI", 10)
    )

    combo_anio["values"] = (
        "Todos los Años",
        "1° Año",
        "2° Año",
        "3° Año",
        "4° Año",
        "5° Año",
        "6° Año"
    )

    combo_anio.grid(
        row=1,
        column=1,
        padx=5,
        pady=(0, 15)
    )

    # --------------------------------------------------------
    # BOTÓN MARCAR TODOS
    # --------------------------------------------------------

    btn_todos = tk.Button(
        panel_filtros,
        text="✓ Marcar Todos\nPresentes",
        font=("Segoe UI", 10, "bold"),
        bg="#E5FFF4",
        fg="#008F68",
        activebackground="#D3F9E8",
        activeforeground="#008F68",
        relief="flat",
        cursor="hand2",
        width=18,
        height=2
    )

    btn_todos.grid(
        row=1,
        column=2,
        padx=10,
        pady=(0, 15)
    )

    # --------------------------------------------------------
    # BOTÓN GUARDAR
    # --------------------------------------------------------

    btn_guardar = tk.Button(
        panel_filtros,
        text="▣ Guardar\nPlanilla",
        font=("Segoe UI", 10, "bold"),
        bg="#159BB5",
        fg="white",
        activebackground="#11869D",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=17,
        height=2
    )

    btn_guardar.grid(
        row=1,
        column=3,
        padx=(5, 20),
        pady=(0, 15)
    )

    # ========================================================
    # CONTENEDOR DE PLANILLA
    # ========================================================

    panel_planilla = tk.Frame(
        contenedor,
        bg="white",
        bd=0,
        highlightthickness=1,
        highlightbackground="#DDE4EC"
    )

    panel_planilla.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )

    # ========================================================
    # TÍTULO PLANILLA
    # ========================================================

    titulo_planilla = tk.Label(
        panel_planilla,
        text="PLANILLA DIARIA DE TOMA DE ASISTENCIA",
        font=("Segoe UI", 12, "bold"),
        bg="white",
        fg="#20354F"
    )

    titulo_planilla.pack(
        anchor="w",
        padx=20,
        pady=(18, 10)
    )

    # ========================================================
    # ENCABEZADO
    # ========================================================

    encabezado = tk.Frame(
        panel_planilla,
        bg="#EEF3F8"
    )

    encabezado.pack(
        fill="x",
        padx=20
    )

    encabezado.columnconfigure(0, weight=4)
    encabezado.columnconfigure(1, weight=1)
    encabezado.columnconfigure(2, weight=1)
    encabezado.columnconfigure(3, weight=1)
    encabezado.columnconfigure(4, weight=3)

    tk.Label(
        encabezado,
        text="Alumno / Curso",
        font=("Segoe UI", 10, "bold"),
        bg="#EEF3F8",
        fg="#40526B"
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=12,
        pady=10
    )

    tk.Label(
        encabezado,
        text="Presente",
        font=("Segoe UI", 10, "bold"),
        bg="#EEF3F8",
        fg="#40526B"
    ).grid(
        row=0,
        column=1,
        pady=10
    )

    tk.Label(
        encabezado,
        text="Tardanza",
        font=("Segoe UI", 10, "bold"),
        bg="#EEF3F8",
        fg="#40526B"
    ).grid(
        row=0,
        column=2,
        pady=10
    )

    tk.Label(
        encabezado,
        text="Falta",
        font=("Segoe UI", 10, "bold"),
        bg="#EEF3F8",
        fg="#40526B"
    ).grid(
        row=0,
        column=3,
        pady=10
    )

    tk.Label(
        encabezado,
        text="Observación Rápida",
        font=("Segoe UI", 10, "bold"),
        bg="#EEF3F8",
        fg="#40526B"
    ).grid(
        row=0,
        column=4,
        sticky="w",
        padx=10,
        pady=10
    )

    # ========================================================
    # ZONA SCROLL
    # ========================================================

    zona_scroll = tk.Frame(
        panel_planilla,
        bg="white"
    )

    zona_scroll.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    canvas = tk.Canvas(
        zona_scroll,
        bg="white",
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        zona_scroll,
        orient="vertical",
        command=canvas.yview
    )

    frame_filas = tk.Frame(
        canvas,
        bg="white"
    )

    frame_filas.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=frame_filas,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ========================================================
    # FUNCIONES AUXILIARES
    # ========================================================

    def convertir_fecha_api():

        try:
            fecha = datetime.strptime(
                fecha_var.get(),
                "%d/%m/%Y"
            )

            return fecha.strftime("%Y-%m-%d")

        except ValueError:

            messagebox.showerror(
                "Fecha incorrecta",
                "La fecha debe tener el formato DD/MM/YYYY.\n\n"
                "Ejemplo: 30/09/2026"
            )

            return None

    # --------------------------------------------------------

    def obtener_nombre(alumno):

        nombre = alumno.get("nombre", "")
        apellido = alumno.get("apellido", "")

        return f"{nombre} {apellido}".strip()

    # --------------------------------------------------------

    def obtener_id(alumno):

        return (
            alumno.get("id_estudiante")
            or alumno.get("id")
        )

    # --------------------------------------------------------

    def obtener_curso(alumno):

        # Intentamos varios nombres posibles
        curso = (
            alumno.get("curso")
            or alumno.get("Curso")
            or alumno.get("division")
            or alumno.get("grado")
        )

        if curso:
            return str(curso)

        return "Sin curso"

    # --------------------------------------------------------

    def obtener_anio(curso):

        texto = str(curso).lower()

        if "1" in texto:
            return "1° Año"

        if "2" in texto:
            return "2° Año"

        if "3" in texto:
            return "3° Año"

        if "4" in texto:
            return "4° Año"

        if "5" in texto:
            return "5° Año"

        if "6" in texto:
            return "6° Año"

        return "Sin año"

    # ========================================================
    # CARGAR ESTUDIANTES
    # ========================================================

    def cargar_estudiantes():

        nonlocal alumnos

        try:

            respuesta = requests.get(
                ESTUDIANTES_URL,
                timeout=5
            )

            if respuesta.status_code != 200:

                messagebox.showerror(
                    "Error",
                    "No se pudieron obtener los estudiantes."
                )

                return

            alumnos = respuesta.json()

            actualizar_filtro_anios()

            cargar_asistencias()

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                "Verificá que Node.js / Express esté ejecutándose."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Ocurrió un error:\n{error}"
            )

    # ========================================================
    # ACTUALIZAR FILTRO DE AÑOS
    # ========================================================

    def actualizar_filtro_anios():

        anios = set()

        for alumno in alumnos:

            curso = obtener_curso(alumno)
            anio = obtener_anio(curso)

            if anio != "Sin año":
                anios.add(anio)

        valores = ["Todos los Años"]

        for i in range(1, 7):

            anio = f"{i}° Año"

            if anio in anios:
                valores.append(anio)

        combo_anio["values"] = valores

    # ========================================================
    # CARGAR ASISTENCIAS
    # ========================================================

    def cargar_asistencias():

        nonlocal asistencias_existentes

        fecha = convertir_fecha_api()

        if not fecha:
            return

        try:

            respuesta = requests.get(
                ASISTENCIAS_URL,
                timeout=5
            )

            if respuesta.status_code != 200:

                messagebox.showerror(
                    "Error",
                    "No se pudieron obtener las asistencias."
                )

                return

            todas = respuesta.json()

            asistencias_existentes = {}

            for asistencia in todas:

                if str(asistencia.get("fecha", ""))[:10] == fecha:

                    id_estudiante = asistencia.get(
                        "id_estudiante"
                    )

                    if id_estudiante is not None:

                        asistencias_existentes[
                            int(id_estudiante)
                        ] = asistencia

            mostrar_filas()

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error",
                "No se pudo conectar con el servidor."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las asistencias:\n{error}"
            )

    # ========================================================
    # MOSTRAR FILAS
    # ========================================================

    def mostrar_filas():

        # Limpiar filas anteriores
        for widget in frame_filas.winfo_children():
            widget.destroy()

        filas.clear()

        filtro = anio_var.get()

        alumnos_filtrados = []

        for alumno in alumnos:

            curso = obtener_curso(alumno)
            anio = obtener_anio(curso)

            if (
                filtro == "Todos los Años"
                or anio == filtro
            ):
                alumnos_filtrados.append(alumno)

        for indice, alumno in enumerate(alumnos_filtrados):

            crear_fila(
                alumno,
                indice
            )

    # ========================================================
    # CREAR FILA DE ALUMNO
    # ========================================================

    def crear_fila(alumno, indice):

        id_estudiante = obtener_id(alumno)

        if id_estudiante is None:
            return

        curso = obtener_curso(alumno)
        nombre = obtener_nombre(alumno)

        fila = tk.Frame(
            frame_filas,
            bg="white"
        )

        fila.pack(
            fill="x"
        )

        fila.columnconfigure(0, weight=4)
        fila.columnconfigure(1, weight=1)
        fila.columnconfigure(2, weight=1)
        fila.columnconfigure(3, weight=1)
        fila.columnconfigure(4, weight=3)

        # ----------------------------------------------------
        # DATOS DEL ALUMNO
        # ----------------------------------------------------

        info = tk.Frame(
            fila,
            bg="white"
        )

        info.grid(
            row=0,
            column=0,
            sticky="w",
            padx=12,
            pady=9
        )

        tk.Label(
            info,
            text=nombre,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#172B4D"
        ).pack(
            anchor="w"
        )

        tk.Label(
            info,
            text=f"{curso}  -  {obtener_anio(curso)}",
            font=("Segoe UI", 8),
            bg="white",
            fg="#8A9BB2"
        ).pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        estado_var = tk.StringVar()

        # Valores por defecto
        estado_var.set("Presente")

        # Si existe una asistencia guardada
        asistencia = asistencias_existentes.get(
            int(id_estudiante)
        )

        observacion_inicial = ""

        if asistencia:

            estado_guardado = asistencia.get(
                "estado",
                "Presente"
            )

            estado_var.set(
                estado_guardado
            )

            observacion_inicial = (
                asistencia.get(
                    "motivo_justificacion"
                )
                or ""
            )

        # ----------------------------------------------------
        # RADIO PRESENTE
        # ----------------------------------------------------

        rb_presente = tk.Radiobutton(
            fila,
            variable=estado_var,
            value="Presente",
            bg="white",
            activebackground="white",
            selectcolor="white",
            cursor="hand2"
        )

        rb_presente.grid(
            row=0,
            column=1
        )

        # ----------------------------------------------------
        # RADIO TARDANZA
        # ----------------------------------------------------

        rb_tardanza = tk.Radiobutton(
            fila,
            variable=estado_var,
            value="Tardanza",
            bg="white",
            activebackground="white",
            selectcolor="white",
            cursor="hand2"
        )

        rb_tardanza.grid(
            row=0,
            column=2
        )

        # ----------------------------------------------------
        # RADIO FALTA
        # ----------------------------------------------------

        rb_falta = tk.Radiobutton(
            fila,
            variable=estado_var,
            value="Falta",
            bg="white",
            activebackground="white",
            selectcolor="white",
            cursor="hand2"
        )

        rb_falta.grid(
            row=0,
            column=3
        )

        # ----------------------------------------------------
        # OBSERVACIÓN
        # ----------------------------------------------------

        observacion_var = tk.StringVar(
            value=observacion_inicial
        )

        entry_observacion = tk.Entry(
            fila,
            textvariable=observacion_var,
            font=("Segoe UI", 9),
            relief="solid",
            bd=1,
            fg="#40526B"
        )

        entry_observacion.grid(
            row=0,
            column=4,
            sticky="ew",
            padx=10,
            pady=8
        )

        # ----------------------------------------------------
        # SEPARADOR
        # ----------------------------------------------------

        separador = tk.Frame(
            fila,
            bg="#EDF1F5",
            height=1
        )

        separador.grid(
            row=1,
            column=0,
            columnspan=5,
            sticky="ew"
        )

        # ----------------------------------------------------
        # GUARDAR REFERENCIAS
        # ----------------------------------------------------

        filas.append({
            "id_estudiante": id_estudiante,
            "curso": curso,
            "estado": estado_var,
            "observacion": observacion_var
        })

    # ========================================================
    # MARCAR TODOS PRESENTES
    # ========================================================

    def marcar_todos_presentes():

        for fila in filas:

            fila["estado"].set(
                "Presente"
            )

    # ========================================================
    # GUARDAR PLANILLA
    # ========================================================

    def guardar_planilla():

        fecha = convertir_fecha_api()

        if not fecha:
            return

        if len(filas) == 0:

            messagebox.showwarning(
                "Sin alumnos",
                "No hay alumnos para guardar."
            )

            return

        guardados = 0
        errores = []

        for fila in filas:

            id_estudiante = fila["id_estudiante"]
            curso = fila["curso"]
            estado = fila["estado"].get()
            observacion = fila["observacion"].get().strip()

            datos = {
                "curso": curso,
                "fecha": fecha,
                "estado": estado,
                "motivo_justificacion": observacion,
                "id_estudiante": id_estudiante
            }

            try:

                # =================================================
                # SI YA EXISTE -> PUT
                # SI NO EXISTE -> POST
                # =================================================

                asistencia_existente = (
                    asistencias_existentes.get(
                        int(id_estudiante)
                    )
                )

                if asistencia_existente:

                    id_asistencia = (
                        asistencia_existente
                        .get("id_asistencia")
                    )

                    respuesta = requests.put(
                        f"{ASISTENCIAS_URL}/{id_asistencia}",
                        json=datos,
                        timeout=5
                    )

                else:

                    respuesta = requests.post(
                        ASISTENCIAS_URL,
                        json=datos,
                        timeout=5
                    )

                if respuesta.status_code in (200, 201):

                    guardados += 1

                else:

                    errores.append(
                        f"Alumno ID {id_estudiante}: "
                        f"{respuesta.text}"
                    )

            except Exception as error:

                errores.append(
                    f"Alumno ID {id_estudiante}: {error}"
                )

        # =====================================================
        # RESULTADO
        # =====================================================

        if errores:

            messagebox.showwarning(
                "Planilla guardada con errores",
                f"Se guardaron {guardados} registros.\n\n"
                f"Errores: {len(errores)}"
            )

        else:

            messagebox.showinfo(
                "Asistencia",
                f"Planilla guardada correctamente.\n\n"
                f"Registros procesados: {guardados}"
            )

        # Volver a cargar para actualizar los IDs
        cargar_asistencias()

    # ========================================================
    # EVENTOS
    # ========================================================

    btn_todos.config(
        command=marcar_todos_presentes
    )

    btn_guardar.config(
        command=guardar_planilla
    )

    combo_anio.bind(
        "<<ComboboxSelected>>",
        lambda event: mostrar_filas()
    )

    entry_fecha.bind(
        "<Return>",
        lambda event: cargar_asistencias()
    )

    # ========================================================
    # CARGAR DATOS INICIALES
    # ========================================================

    cargar_estudiantes()

    return contenedor