import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ============================================================
# CONFIGURACIÓN
# ============================================================

API_URL = "http://localhost:3000/api/docentes"


# ============================================================
# INTERFAZ DOCENTES
# Uso: crear_docentes(contenedor_principal)
# ============================================================

def crear_docentes(parent):

    # Limpiar el contenedor recibido, sin crear otra ventana ni menú
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

    parent.configure(bg=COLOR_FONDO)

    # --------------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------------

    encabezado = tk.Frame(parent, bg=COLOR_FONDO)
    encabezado.pack(fill="x", padx=25, pady=(20, 10))

    tk.Label(
        encabezado,
        text="Docentes - Registro Institucional",
        font=("Arial", 20, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO
    ).pack(side="left")

    btn_nuevo = tk.Button(
        encabezado,
        text="+ Registrar Docente",
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
    btn_nuevo.pack(side="right")

    # --------------------------------------------------------
    # BUSCADOR
    # --------------------------------------------------------

    contenedor_busqueda = tk.Frame(
        parent,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    contenedor_busqueda.pack(fill="x", padx=25, pady=10)

    tk.Label(
        contenedor_busqueda,
        text="🔎",
        font=("Arial", 15),
        bg=COLOR_BLANCO,
        fg=COLOR_GRIS
    ).pack(side="left", padx=(15, 5), pady=12)

    PLACEHOLDER = "Buscar por nombre, apellido, DNI, email o ID..."
    entrada_buscar = tk.Entry(
        contenedor_busqueda,
        font=("Arial", 11),
        bd=0,
        bg=COLOR_BLANCO,
        fg=COLOR_GRIS
    )
    entrada_buscar.pack(side="left", fill="x", expand=True, padx=5, pady=12)
    entrada_buscar.insert(0, PLACEHOLDER)
    placeholder = True

    def quitar_placeholder(event=None):
        nonlocal placeholder
        if placeholder:
            entrada_buscar.delete(0, tk.END)
            entrada_buscar.config(fg=COLOR_TEXTO)
            placeholder = False

    def poner_placeholder(event=None):
        nonlocal placeholder
        if not entrada_buscar.get().strip():
            entrada_buscar.insert(0, PLACEHOLDER)
            entrada_buscar.config(fg=COLOR_GRIS)
            placeholder = True

    entrada_buscar.bind("<FocusIn>", quitar_placeholder)
    entrada_buscar.bind("<FocusOut>", poner_placeholder)

    # --------------------------------------------------------
    # TABLA DE DOCENTES
    # --------------------------------------------------------

    contenedor_lista = tk.Frame(parent, bg=COLOR_FONDO)
    contenedor_lista.pack(fill="both", expand=True, padx=25, pady=(5, 10))

    estilo = ttk.Style()
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure(
        "Treeview",
        background=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=40,
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
        background=[("selected", "#D9F1F5")],
        foreground=[("selected", COLOR_TEXTO)]
    )

    columnas = ("id", "nombre", "apellido", "dni", "email", "telefono")
    tabla = ttk.Treeview(
        contenedor_lista,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    configuracion_columnas = {
        "id": ("ID", 60, "center"),
        "nombre": ("Nombre", 150, "w"),
        "apellido": ("Apellido", 160, "w"),
        "dni": ("DNI", 120, "center"),
        "email": ("Email", 240, "w"),
        "telefono": ("Teléfono", 150, "center")
    }

    for columna, (titulo, ancho, ancla) in configuracion_columnas.items():
        tabla.heading(columna, text=titulo)
        tabla.column(columna, width=ancho, anchor=ancla)

    scrollbar_y = ttk.Scrollbar(
        contenedor_lista, orient="vertical", command=tabla.yview
    )
    scrollbar_x = ttk.Scrollbar(
        contenedor_lista, orient="horizontal", command=tabla.xview
    )
    tabla.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    tabla.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    contenedor_lista.grid_rowconfigure(0, weight=1)
    contenedor_lista.grid_columnconfigure(0, weight=1)

    docentes = []

    # --------------------------------------------------------
    # MOSTRAR DOCENTES
    # --------------------------------------------------------

    def mostrar_docentes(lista):
        for item in tabla.get_children():
            tabla.delete(item)

        for docente in lista:
            tabla.insert(
                "",
                "end",
                values=(
                    docente.get("id_docente", ""),
                    docente.get("nombre", ""),
                    docente.get("apellido", ""),
                    docente.get("dni", ""),
                    docente.get("email") or "",
                    docente.get("telefono") or ""
                )
            )

    # --------------------------------------------------------
    # CARGAR DOCENTES DESDE LA API
    # --------------------------------------------------------

    def cargar_docentes(mostrar_error=True):
        nonlocal docentes

        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            datos = respuesta.json()

            if not isinstance(datos, list):
                raise ValueError("La API de docentes no devolvió una lista JSON.")

            docentes = datos
            aplicar_busqueda()

        except (requests.exceptions.RequestException, ValueError) as error:
            if mostrar_error:
                messagebox.showerror(
                    "Error",
                    "No se pudieron cargar los docentes.\n\n"
                    + str(error),
                    parent=parent
                )

    # --------------------------------------------------------
    # BUSCAR / FILTRAR
    # --------------------------------------------------------

    def aplicar_busqueda(event=None):
        if placeholder:
            mostrar_docentes(docentes)
            return

        texto = entrada_buscar.get().strip().lower()
        if not texto:
            mostrar_docentes(docentes)
            return

        resultados = []
        for docente in docentes:
            campos = [
                docente.get("id_docente", ""),
                docente.get("nombre", ""),
                docente.get("apellido", ""),
                docente.get("dni", ""),
                docente.get("email", ""),
                docente.get("telefono", "")
            ]

            if any(texto in str(campo or "").lower() for campo in campos):
                resultados.append(docente)

        mostrar_docentes(resultados)

    entrada_buscar.bind("<KeyRelease>", aplicar_busqueda)

    # --------------------------------------------------------
    # FORMULARIO PARA CREAR / EDITAR
    # --------------------------------------------------------

    def abrir_formulario(docente=None):
        ventana = tk.Toplevel(parent)
        ventana.title("Editar Docente" if docente else "Registrar Docente")
        ventana.geometry("570x490")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_FONDO)
        ventana.transient(parent)
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Editar Docente" if docente else "Registrar Docente",
            font=("Arial", 18, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(pady=(22, 18))

        formulario = tk.Frame(
            ventana, bg=COLOR_BLANCO, padx=28, pady=22
        )
        formulario.pack(padx=25, fill="both", expand=True)
        formulario.grid_columnconfigure(1, weight=1)

        def crear_etiqueta(texto, fila):
            tk.Label(
                formulario,
                text=texto,
                font=("Arial", 10, "bold"),
                bg=COLOR_BLANCO,
                fg=COLOR_TEXTO
            ).grid(row=fila, column=0, sticky="w", pady=10, padx=(0, 12))

        campos = {}

        definiciones = [
            ("Nombre:", "nombre"),
            ("Apellido:", "apellido"),
            ("DNI:", "dni"),
            ("Email:", "email"),
            ("Teléfono:", "telefono")
        ]

        for fila, (etiqueta, clave) in enumerate(definiciones):
            crear_etiqueta(etiqueta, fila)
            entrada = tk.Entry(
                formulario,
                font=("Arial", 10),
                relief="solid",
                bd=1
            )
            entrada.grid(row=fila, column=1, sticky="ew", pady=8, ipady=4)
            campos[clave] = entrada

        if docente:
            for clave, entrada in campos.items():
                entrada.insert(0, str(docente.get(clave) or ""))

        def guardar():
            datos = {
                clave: entrada.get().strip()
                for clave, entrada in campos.items()
            }

            if not datos["nombre"] or not datos["apellido"] or not datos["dni"]:
                messagebox.showwarning(
                    "Validación",
                    "Nombre, apellido y DNI son obligatorios.",
                    parent=ventana
                )
                return

            # Enviar cadenas vacías como null para los campos opcionales.
            datos["email"] = datos["email"] or None
            datos["telefono"] = datos["telefono"] or None

            try:
                if docente:
                    id_docente = docente.get("id_docente")
                    respuesta = requests.put(
                        f"{API_URL}/{id_docente}",
                        json=datos,
                        timeout=5
                    )
                    codigos_ok = (200,)
                    mensaje = "Docente actualizado correctamente."
                else:
                    respuesta = requests.post(
                        API_URL,
                        json=datos,
                        timeout=5
                    )
                    codigos_ok = (201,)
                    mensaje = "Docente agregado correctamente."

                if respuesta.status_code in codigos_ok:
                    messagebox.showinfo("Éxito", mensaje, parent=ventana)
                    ventana.destroy()
                    cargar_docentes()
                else:
                    try:
                        error = respuesta.json()
                        detalle = (
                            error.get("detalle")
                            or error.get("error")
                            or respuesta.text
                        )
                    except ValueError:
                        detalle = respuesta.text or f"HTTP {respuesta.status_code}"

                    messagebox.showerror("Error", detalle, parent=ventana)

            except requests.exceptions.RequestException as error:
                messagebox.showerror(
                    "Error de conexión",
                    "No se pudo conectar con el servidor.\n\n" + str(error),
                    parent=ventana
                )

        contenedor_botones_form = tk.Frame(ventana, bg=COLOR_FONDO)
        contenedor_botones_form.pack(pady=13)

        tk.Button(
            contenedor_botones_form,
            text="Cancelar",
            font=("Arial", 10, "bold"),
            bg="#E9EEF4",
            fg=COLOR_TEXTO,
            relief="flat",
            padx=20,
            pady=8,
            command=ventana.destroy,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            contenedor_botones_form,
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
        ).pack(side="left", padx=5)

    # --------------------------------------------------------
    # EDITAR DOCENTE SELECCIONADO
    # --------------------------------------------------------

    def editar_docente():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Editar", "Seleccioná un docente de la tabla.", parent=parent
            )
            return

        valores = tabla.item(seleccion[0], "values")
        id_docente = valores[0]

        try:
            respuesta = requests.get(f"{API_URL}/{id_docente}", timeout=5)
            if respuesta.status_code == 200:
                abrir_formulario(respuesta.json())
            else:
                try:
                    detalle = respuesta.json().get(
                        "error", "No se pudo obtener el docente."
                    )
                except ValueError:
                    detalle = respuesta.text
                messagebox.showerror("Error", detalle, parent=parent)

        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error de conexión", str(error), parent=parent)

    # --------------------------------------------------------
    # ELIMINAR DOCENTE SELECCIONADO
    # --------------------------------------------------------

    def eliminar_docente():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Eliminar", "Seleccioná un docente de la tabla.", parent=parent
            )
            return

        valores = tabla.item(seleccion[0], "values")
        id_docente = valores[0]
        nombre_completo = f"{valores[1]} {valores[2]}"

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar al docente {nombre_completo}?\n\n"
            "Si tiene usuarios u observaciones asociados, la base de datos "
            "puede impedir la eliminación.",
            parent=parent
        )
        if not confirmar:
            return

        try:
            respuesta = requests.delete(f"{API_URL}/{id_docente}", timeout=5)

            if respuesta.status_code in (200, 204):
                messagebox.showinfo(
                    "Éxito", "Docente eliminado correctamente.", parent=parent
                )
                cargar_docentes()
            else:
                try:
                    error = respuesta.json()
                    detalle = (
                        error.get("detalle")
                        or error.get("error")
                        or "No se pudo eliminar el docente."
                    )
                except ValueError:
                    detalle = respuesta.text or f"HTTP {respuesta.status_code}"

                messagebox.showerror("Error", detalle, parent=parent)

        except requests.exceptions.RequestException as error:
            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n" + str(error),
                parent=parent
            )

    # --------------------------------------------------------
    # BOTONES INFERIORES
    # --------------------------------------------------------

    contenedor_acciones = tk.Frame(parent, bg=COLOR_FONDO)
    contenedor_acciones.pack(fill="x", padx=25, pady=(0, 18))

    tk.Button(
        contenedor_acciones,
        text="Actualizar lista",
        font=("Arial", 10, "bold"),
        bg="#EAF0F6",
        fg=COLOR_TEXTO,
        relief="flat",
        padx=18,
        pady=8,
        command=cargar_docentes,
        cursor="hand2"
    ).pack(side="left", padx=5)

    tk.Button(
        contenedor_acciones,
        text="Borrar",
        font=("Arial", 10, "bold"),
        bg="#FFF0F2",
        fg=COLOR_ROJO,
        relief="flat",
        padx=20,
        pady=8,
        command=eliminar_docente,
        cursor="hand2"
    ).pack(side="right", padx=5)

    tk.Button(
        contenedor_acciones,
        text="Editar",
        font=("Arial", 10, "bold"),
        bg="#EAF0F6",
        fg=COLOR_TEXTO,
        relief="flat",
        padx=20,
        pady=8,
        command=editar_docente,
        cursor="hand2"
    ).pack(side="right", padx=5)

    btn_nuevo.config(command=lambda: abrir_formulario())

    # Atajos opcionales
    tabla.bind("<Double-1>", lambda event: editar_docente())
    parent.bind_all("<F2>", lambda event: editar_docente())

    # Cargar datos al abrir la vista
    cargar_docentes()
