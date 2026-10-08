import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ============================================================
# CONFIGURACIÓN
# ============================================================

API_URL = "http://localhost:3000/observaciones"


# ============================================================
# INTERFAZ OBSERVACIONES
# ============================================================

def crear_observaciones(parent):

    # --------------------------------------------------------
    # LIMPIAR EL CONTENEDOR
    # --------------------------------------------------------

    for widget in parent.winfo_children():
        widget.destroy()


    # --------------------------------------------------------
    # COLORES
    # --------------------------------------------------------

    COLOR_FONDO = "#F4F7FB"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_AZUL = "#20A4BD"
    COLOR_AZUL_OSCURO = "#176B7A"
    COLOR_TEXTO = "#26364A"
    COLOR_GRIS = "#6B7A90"
    COLOR_BORDE = "#DCE3EC"
    COLOR_ROJO = "#E94B5F"
    COLOR_VERDE = "#18B77A"
    COLOR_NARANJA = "#F5A623"


    # --------------------------------------------------------
    # CONFIGURAR PARENT
    # --------------------------------------------------------

    parent.configure(bg=COLOR_FONDO)


    # --------------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------------

    encabezado = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )

    encabezado.pack(
        fill="x",
        padx=25,
        pady=(20, 10)
    )


    titulo = tk.Label(
        encabezado,
        text="Observaciones - Registro Institucional",
        font=("Arial", 20, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO
    )

    titulo.pack(side="left")


    # --------------------------------------------------------
    # BOTÓN NUEVA OBSERVACIÓN
    # --------------------------------------------------------

    btn_nueva = tk.Button(
        encabezado,
        text="+ Registrar Observación",
        font=("Arial", 10, "bold"),
        bg=COLOR_AZUL,
        fg="white",
        activebackground=COLOR_AZUL_OSCURO,
        activeforeground="white",
        relief="flat",
        padx=18,
        pady=10,
        cursor="hand2"
    )

    btn_nueva.pack(side="right")


    # --------------------------------------------------------
    # BUSCADOR
    # --------------------------------------------------------

    contenedor_busqueda = tk.Frame(
        parent,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )

    contenedor_busqueda.pack(
        fill="x",
        padx=25,
        pady=10
    )


    tk.Label(
        contenedor_busqueda,
        text="🔎",
        font=("Arial", 15),
        bg=COLOR_BLANCO,
        fg=COLOR_GRIS
    ).pack(
        side="left",
        padx=(15, 5),
        pady=12
    )


    entrada_buscar = tk.Entry(
        contenedor_busqueda,
        font=("Arial", 11),
        bd=0,
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO
    )

    entrada_buscar.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5,
        pady=12
    )


    entrada_buscar.insert(
        0,
        "Buscar por descripción, tipo o ID..."
    )

    # Variable para controlar placeholder
    placeholder = True


    def quitar_placeholder(event=None):

        nonlocal placeholder

        if placeholder:

            entrada_buscar.delete(0, tk.END)
            entrada_buscar.config(fg=COLOR_TEXTO)

            placeholder = False


    def poner_placeholder(event=None):

        nonlocal placeholder

        if entrada_buscar.get().strip() == "":

            entrada_buscar.insert(
                0,
                "Buscar por descripción, tipo o ID..."
            )

            entrada_buscar.config(
                fg=COLOR_GRIS
            )

            placeholder = True


    entrada_buscar.config(
        fg=COLOR_GRIS
    )

    entrada_buscar.bind(
        "<FocusIn>",
        quitar_placeholder
    )

    entrada_buscar.bind(
        "<FocusOut>",
        poner_placeholder
    )


    # --------------------------------------------------------
    # CONTENEDOR DEL LISTADO
    # --------------------------------------------------------

    contenedor_lista = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )

    contenedor_lista.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(5, 20)
    )


    # --------------------------------------------------------
    # TABLA
    # --------------------------------------------------------

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except:
        pass


    estilo.configure(
        "Treeview",
        background=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=42,
        fieldbackground=COLOR_BLANCO,
        font=("Arial", 10)
    )

    estilo.configure(
        "Treeview.Heading",
        background="#EEF3F8",
        foreground=COLOR_TEXTO,
        font=("Arial", 10, "bold"),
        padding=8
    )

    estilo.map(
        "Treeview",
        background=[
            ("selected", "#D9F1F5")
        ],
        foreground=[
            ("selected", COLOR_TEXTO)
        ]
    )


    columnas = (
        "id",
        "fecha",
        "tipo",
        "descripcion",
        "seguimiento",
        "estudiante",
        "docente"
    )


    tabla = ttk.Treeview(
        contenedor_lista,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )


    tabla.heading(
        "id",
        text="ID"
    )

    tabla.heading(
        "fecha",
        text="Fecha"
    )

    tabla.heading(
        "tipo",
        text="Tipo"
    )

    tabla.heading(
        "descripcion",
        text="Descripción"
    )

    tabla.heading(
        "seguimiento",
        text="Seguimiento"
    )

    tabla.heading(
        "estudiante",
        text="ID Estudiante"
    )

    tabla.heading(
        "docente",
        text="ID Docente"
    )


    tabla.column(
        "id",
        width=60,
        anchor="center"
    )

    tabla.column(
        "fecha",
        width=110,
        anchor="center"
    )

    tabla.column(
        "tipo",
        width=120,
        anchor="center"
    )

    tabla.column(
        "descripcion",
        width=350,
        anchor="w"
    )

    tabla.column(
        "seguimiento",
        width=120,
        anchor="center"
    )

    tabla.column(
        "estudiante",
        width=110,
        anchor="center"
    )

    tabla.column(
        "docente",
        width=110,
        anchor="center"
    )


    scrollbar = ttk.Scrollbar(
        contenedor_lista,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(
        yscrollcommand=scrollbar.set
    )


    tabla.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # --------------------------------------------------------
    # FUNCIONES
    # --------------------------------------------------------

    observaciones = []


    def cargar_observaciones():

        nonlocal observaciones

        try:

            respuesta = requests.get(
                API_URL,
                timeout=5
            )

            if respuesta.status_code == 200:

                observaciones = respuesta.json()

                mostrar_observaciones(
                    observaciones
                )

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudieron obtener las observaciones."
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                + str(error)
            )


    def mostrar_observaciones(lista):

        # Limpiar tabla

        for item in tabla.get_children():
            tabla.delete(item)


        # Cargar registros

        for observacion in lista:

            tabla.insert(
                "",
                "end",
                values=(
                    observacion.get(
                        "id_observacion",
                        ""
                    ),
                    observacion.get(
                        "fecha",
                        ""
                    ),
                    observacion.get(
                        "tipo",
                        ""
                    ),
                    observacion.get(
                        "descripcion",
                        ""
                    ),
                    observacion.get(
                        "requiere_seguimiento",
                        ""
                    ),
                    observacion.get(
                        "id_estudiante",
                        ""
                    ),
                    observacion.get(
                        "id_docente",
                        ""
                    )
                )
            )


    # --------------------------------------------------------
    # BUSCAR
    # --------------------------------------------------------

    def buscar_observaciones(event=None):

        if placeholder:
            return

        texto = entrada_buscar.get().lower().strip()

        if texto == "":

            mostrar_observaciones(
                observaciones
            )

            return


        resultados = []

        for observacion in observaciones:

            id_observacion = str(
                observacion.get(
                    "id_observacion",
                    ""
                )
            ).lower()

            tipo = str(
                observacion.get(
                    "tipo",
                    ""
                )
            ).lower()

            descripcion = str(
                observacion.get(
                    "descripcion",
                    ""
                )
            ).lower()

            id_estudiante = str(
                observacion.get(
                    "id_estudiante",
                    ""
                )
            ).lower()

            if (
                texto in id_observacion
                or texto in tipo
                or texto in descripcion
                or texto in id_estudiante
            ):

                resultados.append(
                    observacion
                )


        mostrar_observaciones(
            resultados
        )


    entrada_buscar.bind(
        "<KeyRelease>",
        buscar_observaciones
    )


    # --------------------------------------------------------
    # VENTANA PARA CREAR / EDITAR
    # --------------------------------------------------------

    def abrir_formulario(observacion=None):

        ventana = tk.Toplevel(parent)

        ventana.title(
            "Editar Observación"
            if observacion
            else "Registrar Observación"
        )

        ventana.geometry(
            "600x600"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.configure(
            bg=COLOR_FONDO
        )

        ventana.transient(
            parent
        )

        ventana.grab_set()


        # -----------------------------------------------
        # TÍTULO
        # -----------------------------------------------

        tk.Label(
            ventana,
            text=(
                "Editar Observación"
                if observacion
                else "Registrar Observación"
            ),
            font=("Arial", 18, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(
            pady=(25, 20)
        )


        formulario = tk.Frame(
            ventana,
            bg=COLOR_BLANCO,
            padx=30,
            pady=25
        )

        formulario.pack(
            padx=25,
            fill="both",
            expand=True
        )


        # -----------------------------------------------
        # FUNCIÓN PARA CREAR CAMPOS
        # -----------------------------------------------

        def crear_campo(
            texto,
            fila
        ):

            tk.Label(
                formulario,
                text=texto,
                font=("Arial", 10, "bold"),
                bg=COLOR_BLANCO,
                fg=COLOR_TEXTO
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                pady=8
            )


        # -----------------------------------------------
        # FECHA
        # -----------------------------------------------

        crear_campo(
            "Fecha:",
            0
        )

        entrada_fecha = tk.Entry(
            formulario,
            font=("Arial", 10),
            width=40
        )

        entrada_fecha.grid(
            row=0,
            column=1,
            padx=15,
            pady=8
        )


        # -----------------------------------------------
        # TIPO
        # -----------------------------------------------

        crear_campo(
            "Tipo:",
            1
        )

        combo_tipo = ttk.Combobox(
            formulario,
            values=[
                "Conducta",
                "Académica",
                "Disciplinaria",
                "Familiar",
                "Salud",
                "Otra"
            ],
            state="normal",
            width=37
        )

        combo_tipo.grid(
            row=1,
            column=1,
            padx=15,
            pady=8
        )


        # -----------------------------------------------
        # DESCRIPCIÓN
        # -----------------------------------------------

        crear_campo(
            "Descripción:",
            2
        )

        entrada_descripcion = tk.Text(
            formulario,
            width=40,
            height=6,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        entrada_descripcion.grid(
            row=2,
            column=1,
            padx=15,
            pady=8
        )


        # -----------------------------------------------
        # SEGUIMIENTO
        # -----------------------------------------------

        crear_campo(
            "Requiere seguimiento:",
            3
        )

        combo_seguimiento = ttk.Combobox(
            formulario,
            values=[
                "SI",
                "NO"
            ],
            state="readonly",
            width=37
        )

        combo_seguimiento.grid(
            row=3,
            column=1,
            padx=15,
            pady=8
        )


        # -----------------------------------------------
        # ID ESTUDIANTE
        # -----------------------------------------------

        crear_campo(
            "ID Estudiante:",
            4
        )

        entrada_estudiante = tk.Entry(
            formulario,
            font=("Arial", 10),
            width=40
        )

        entrada_estudiante.grid(
            row=4,
            column=1,
            padx=15,
            pady=8
        )


        # -----------------------------------------------
        # ID DOCENTE
        # -----------------------------------------------

        crear_campo(
            "ID Docente:",
            5
        )

        entrada_docente = tk.Entry(
            formulario,
            font=("Arial", 10),
            width=40
        )

        entrada_docente.grid(
            row=5,
            column=1,
            padx=15,
            pady=8
        )


        # -----------------------------------------------
        # CARGAR DATOS SI ES EDICIÓN
        # -----------------------------------------------

        if observacion:

            entrada_fecha.insert(
                0,
                observacion.get(
                    "fecha",
                    ""
                )
            )

            combo_tipo.set(
                observacion.get(
                    "tipo",
                    ""
                )
            )

            entrada_descripcion.insert(
                "1.0",
                observacion.get(
                    "descripcion",
                    ""
                )
            )

            combo_seguimiento.set(
                observacion.get(
                    "requiere_seguimiento",
                    ""
                )
            )

            entrada_estudiante.insert(
                0,
                observacion.get(
                    "id_estudiante",
                    ""
                )
            )

            entrada_docente.insert(
                0,
                observacion.get(
                    "id_docente",
                    ""
                )
            )


        # -----------------------------------------------
        # GUARDAR
        # -----------------------------------------------

        def guardar():

            fecha = entrada_fecha.get().strip()
            tipo = combo_tipo.get().strip()
            descripcion = entrada_descripcion.get(
                "1.0",
                tk.END
            ).strip()

            requiere_seguimiento = combo_seguimiento.get().strip()

            id_estudiante = entrada_estudiante.get().strip()
            id_docente = entrada_docente.get().strip()


            # -------------------------------------------
            # VALIDACIONES
            # -------------------------------------------

            if not fecha:
                messagebox.showwarning(
                    "Validación",
                    "Ingrese la fecha.",
                    parent=ventana
                )
                return


            if not tipo:
                messagebox.showwarning(
                    "Validación",
                    "Ingrese el tipo de observación.",
                    parent=ventana
                )
                return


            if not descripcion:
                messagebox.showwarning(
                    "Validación",
                    "Ingrese una descripción.",
                    parent=ventana
                )
                return


            if not requiere_seguimiento:
                messagebox.showwarning(
                    "Validación",
                    "Seleccione si requiere seguimiento.",
                    parent=ventana
                )
                return


            if not id_estudiante:
                messagebox.showwarning(
                    "Validación",
                    "Ingrese el ID del estudiante.",
                    parent=ventana
                )
                return


            if not id_docente:
                messagebox.showwarning(
                    "Validación",
                    "Ingrese el ID del docente.",
                    parent=ventana
                )
                return


            # -------------------------------------------
            # DATOS
            # -------------------------------------------

            datos = {

                "fecha": fecha,

                "tipo": tipo,

                "descripcion": descripcion,

                "requiere_seguimiento":
                    requiere_seguimiento,

                "id_estudiante":
                    int(id_estudiante),

                "id_docente":
                    int(id_docente)
            }


            try:

                # ---------------------------------------
                # EDITAR
                # ---------------------------------------

                if observacion:

                    id_observacion = observacion.get(
                        "id_observacion"
                    )

                    respuesta = requests.put(
                        f"{API_URL}/{id_observacion}",
                        json=datos,
                        timeout=5
                    )


                    if respuesta.status_code == 200:

                        messagebox.showinfo(
                            "Éxito",
                            "Observación actualizada correctamente.",
                            parent=ventana
                        )

                        ventana.destroy()

                        cargar_observaciones()


                    else:

                        try:

                            error = respuesta.json()

                            detalle = error.get(
                                "detalle",
                                error.get(
                                    "error",
                                    "Error desconocido"
                                )
                            )

                        except:

                            detalle = respuesta.text


                        messagebox.showerror(
                            "Error",
                            detalle,
                            parent=ventana
                        )


                # ---------------------------------------
                # CREAR
                # ---------------------------------------

                else:

                    respuesta = requests.post(
                        API_URL,
                        json=datos,
                        timeout=5
                    )


                    if respuesta.status_code == 201:

                        messagebox.showinfo(
                            "Éxito",
                            "Observación agregada correctamente.",
                            parent=ventana
                        )

                        ventana.destroy()

                        cargar_observaciones()


                    else:

                        try:

                            error = respuesta.json()

                            detalle = error.get(
                                "detalle",
                                error.get(
                                    "error",
                                    "Error desconocido"
                                )
                            )

                        except:

                            detalle = respuesta.text


                        messagebox.showerror(
                            "Error",
                            detalle,
                            parent=ventana
                        )


            except ValueError:

                messagebox.showwarning(
                    "Validación",
                    "Los ID de estudiante y docente deben ser números.",
                    parent=ventana
                )


            except requests.exceptions.RequestException as error:

                messagebox.showerror(
                    "Error de conexión",
                    "No se pudo conectar con el servidor.\n\n"
                    + str(error),
                    parent=ventana
                )


        # -----------------------------------------------
        # BOTONES
        # -----------------------------------------------

        contenedor_botones = tk.Frame(
            ventana,
            bg=COLOR_FONDO
        )

        contenedor_botones.pack(
            pady=15
        )


        tk.Button(
            contenedor_botones,
            text="Cancelar",
            font=("Arial", 10, "bold"),
            bg="#E9EEF4",
            fg=COLOR_TEXTO,
            relief="flat",
            padx=20,
            pady=8,
            command=ventana.destroy,
            cursor="hand2"
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            contenedor_botones,
            text="Guardar",
            font=("Arial", 10, "bold"),
            bg=COLOR_AZUL,
            fg="white",
            activebackground=COLOR_AZUL_OSCURO,
            relief="flat",
            padx=25,
            pady=8,
            command=guardar,
            cursor="hand2"
        ).pack(
            side="left",
            padx=5
        )


    # --------------------------------------------------------
    # EDITAR
    # --------------------------------------------------------

    def editar_observacion():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Editar",
                "Seleccione una observación."
            )

            return


        valores = tabla.item(
            seleccion[0],
            "values"
        )

        id_observacion = valores[0]


        try:

            respuesta = requests.get(
                f"{API_URL}/{id_observacion}",
                timeout=5
            )


            if respuesta.status_code == 200:

                observacion = respuesta.json()

                abrir_formulario(
                    observacion
                )

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo obtener la observación."
                )


        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                str(error)
            )


    # --------------------------------------------------------
    # ELIMINAR
    # --------------------------------------------------------

    def eliminar_observacion():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Eliminar",
                "Seleccione una observación."
            )

            return


        valores = tabla.item(
            seleccion[0],
            "values"
        )

        id_observacion = valores[0]

        descripcion = valores[3]


        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de eliminar esta observación?\n\n"
            + descripcion
        )


        if not confirmar:
            return


        try:

            respuesta = requests.delete(
                f"{API_URL}/{id_observacion}",
                timeout=5
            )


            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Éxito",
                    "Observación eliminada correctamente."
                )

                cargar_observaciones()


            else:

                try:

                    error = respuesta.json()

                    detalle = error.get(
                        "detalle",
                        error.get(
                            "error",
                            "No se pudo eliminar."
                        )
                    )

                except:

                    detalle = respuesta.text


                messagebox.showerror(
                    "Error",
                    detalle
                )


        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                + str(error)
            )


    # --------------------------------------------------------
    # BOTONES INFERIORES
    # --------------------------------------------------------

    contenedor_acciones = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )

    contenedor_acciones.pack(
        fill="x",
        padx=25,
        pady=(0, 20)
    )


    tk.Button(
        contenedor_acciones,
        text="Editar",
        font=("Arial", 10, "bold"),
        bg="#EAF0F6",
        fg=COLOR_TEXTO,
        relief="flat",
        padx=20,
        pady=8,
        command=editar_observacion,
        cursor="hand2"
    ).pack(
        side="right",
        padx=5
    )


    tk.Button(
        contenedor_acciones,
        text="Borrar",
        font=("Arial", 10, "bold"),
        bg="#FFF0F2",
        fg=COLOR_ROJO,
        relief="flat",
        padx=20,
        pady=8,
        command=eliminar_observacion,
        cursor="hand2"
    ).pack(
        side="right",
        padx=5
    )


    # --------------------------------------------------------
    # BOTÓN NUEVA OBSERVACIÓN
    # --------------------------------------------------------

    btn_nueva.config(
        command=lambda: abrir_formulario()
    )


    # --------------------------------------------------------
    # CARGAR DATOS AL ABRIR
    # --------------------------------------------------------

    cargar_observaciones()