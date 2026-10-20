import tkinter as tk
from tkinter import ttk, messagebox
import requests

# ============================================================
# CONFIGURACIÓN DE LAS API
# ============================================================

API_URL = "http://localhost:3000/api/observaciones"
API_ESTUDIANTES_URL = "http://localhost:3000/api/estudiantes"
API_DOCENTES_URL = "http://localhost:3000/api/docentes"


def crear_observaciones(parent):
    # Limpiar solamente el contenedor recibido
    for widget in parent.winfo_children():
        widget.destroy()

    COLOR_FONDO = "#F4F7FB"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_AZUL = "#20A4BD"
    COLOR_AZUL_OSCURO = "#176B7A"
    COLOR_TEXTO = "#26364A"
    COLOR_GRIS = "#6B7A90"
    COLOR_BORDE = "#DCE3EC"
    COLOR_ROJO = "#E94B5F"

    parent.configure(bg=COLOR_FONDO)

    encabezado = tk.Frame(parent, bg=COLOR_FONDO)
    encabezado.pack(fill="x", padx=25, pady=(20, 10))

    tk.Label(
        encabezado,
        text="Observaciones - Registro Institucional",
        font=("Arial", 20, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO
    ).pack(side="left")

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

    # Buscador
    contenedor_busqueda = tk.Frame(
        parent, bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE, highlightthickness=1
    )
    contenedor_busqueda.pack(fill="x", padx=25, pady=10)

    tk.Label(
        contenedor_busqueda, text="🔎", font=("Arial", 15),
        bg=COLOR_BLANCO, fg=COLOR_GRIS
    ).pack(side="left", padx=(15, 5), pady=12)

    PLACEHOLDER = "Buscar por descripción, tipo, ID, estudiante o docente..."
    entrada_buscar = tk.Entry(
        contenedor_busqueda, font=("Arial", 11), bd=0,
        bg=COLOR_BLANCO, fg=COLOR_GRIS
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

    # Tabla
    contenedor_lista = tk.Frame(parent, bg=COLOR_FONDO)
    contenedor_lista.pack(fill="both", expand=True, padx=25, pady=(5, 10))

    estilo = ttk.Style()
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure(
        "Treeview", background=COLOR_BLANCO, foreground=COLOR_TEXTO,
        rowheight=38, fieldbackground=COLOR_BLANCO, font=("Arial", 10)
    )
    estilo.configure(
        "Treeview.Heading", background="#EEF3F8", foreground=COLOR_TEXTO,
        font=("Arial", 10, "bold"), padding=8
    )
    estilo.map("Treeview", background=[("selected", "#D9F1F5")])

    columnas = ("id", "fecha", "tipo", "descripcion", "seguimiento", "estudiante", "docente")
    tabla = ttk.Treeview(
        contenedor_lista, columns=columnas, show="headings", selectmode="browse"
    )

    encabezados = {
        "id": ("ID", 55, "center"),
        "fecha": ("Fecha", 100, "center"),
        "tipo": ("Tipo", 115, "center"),
        "descripcion": ("Descripción", 260, "w"),
        "seguimiento": ("Seguimiento", 105, "center"),
        "estudiante": ("Estudiante", 190, "w"),
        "docente": ("Docente", 190, "w"),
    }
    for columna, (titulo, ancho, ancla) in encabezados.items():
        tabla.heading(columna, text=titulo)
        tabla.column(columna, width=ancho, anchor=ancla)

    scrollbar_y = ttk.Scrollbar(contenedor_lista, orient="vertical", command=tabla.yview)
    scrollbar_x = ttk.Scrollbar(contenedor_lista, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    contenedor_lista.grid_rowconfigure(0, weight=1)
    contenedor_lista.grid_columnconfigure(0, weight=1)

    observaciones = []
    estudiantes = []
    docentes = []
    estudiantes_por_nombre = {}
    docentes_por_nombre = {}

    def nombre_completo(registro, tipo):
        nombre = str(registro.get("nombre") or "").strip()
        apellido = str(registro.get("apellido") or "").strip()
        completo = f"{apellido}, {nombre}".strip(", ")
        if not completo:
            completo = f"{tipo} sin nombre"
        identificador = registro.get("id_estudiante") if tipo == "estudiante" else registro.get("id_docente")
        return completo, identificador

    def cargar_personas():
        """Carga estudiantes y docentes para usarlos en los ComboBox."""
        nonlocal estudiantes, docentes, estudiantes_por_nombre, docentes_por_nombre

        try:
            r_estudiantes = requests.get(API_ESTUDIANTES_URL, timeout=5)
            r_estudiantes.raise_for_status()
            datos_estudiantes = r_estudiantes.json()

            r_docentes = requests.get(API_DOCENTES_URL, timeout=5)
            r_docentes.raise_for_status()
            datos_docentes = r_docentes.json()

            if not isinstance(datos_estudiantes, list) or not isinstance(datos_docentes, list):
                raise ValueError("Las rutas de estudiantes y docentes deben devolver listas JSON.")

            estudiantes = datos_estudiantes
            docentes = datos_docentes

            estudiantes_por_nombre = {}
            for estudiante in estudiantes:
                nombre, identificador = nombre_completo(estudiante, "estudiante")
                if identificador is not None:
                    # Si hay nombres repetidos, se agrega el ID para distinguirlos.
                    etiqueta = f"{nombre} (ID: {identificador})"
                    estudiantes_por_nombre[etiqueta] = identificador

            docentes_por_nombre = {}
            for docente in docentes:
                nombre, identificador = nombre_completo(docente, "docente")
                if identificador is not None:
                    etiqueta = f"{nombre} (ID: {identificador})"
                    docentes_por_nombre[etiqueta] = identificador

            return True

        except (requests.exceptions.RequestException, ValueError) as error:
            messagebox.showerror(
                "Error al cargar personas",
                "No se pudieron cargar los estudiantes y docentes.\n\n"
                "Verificá que el servidor esté activo y que existan las rutas:\n"
                f"{API_ESTUDIANTES_URL}\n{API_DOCENTES_URL}\n\n{error}",
                parent=parent
            )
            return False

    def etiqueta_por_id(mapa, identificador):
        for etiqueta, valor in mapa.items():
            if str(valor) == str(identificador):
                return etiqueta
        return ""

    def cargar_observaciones():
        nonlocal observaciones
        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            datos = respuesta.json()
            if not isinstance(datos, list):
                raise ValueError("La ruta GET de observaciones debe devolver una lista JSON.")
            observaciones = datos
            mostrar_observaciones(observaciones)
        except (requests.exceptions.RequestException, ValueError) as error:
            messagebox.showerror(
                "Error",
                "No se pudieron obtener las observaciones.\n\n" + str(error),
                parent=parent
            )

    def mostrar_observaciones(lista):
        for item in tabla.get_children():
            tabla.delete(item)

        for obs in lista:
            # Las rutas GET con JOIN devuelven los nombres. Se conserva
            # compatibilidad con la respuesta antigua que solo traía IDs.
            estudiante = (
                f"{obs.get('apellido_estudiante', '')} {obs.get('nombre_estudiante', '')}".strip()
                or str(obs.get("id_estudiante", ""))
            )
            docente = (
                f"{obs.get('apellido_docente', '')} {obs.get('nombre_docente', '')}".strip()
                or str(obs.get("id_docente", ""))
            )

            tabla.insert("", "end", values=(
                obs.get("id_observacion", ""),
                obs.get("fecha", ""),
                obs.get("tipo", ""),
                obs.get("descripcion", ""),
                obs.get("requiere_seguimiento", ""),
                estudiante,
                docente
            ))

    def buscar_observaciones(event=None):
        if placeholder:
            return

        texto = entrada_buscar.get().lower().strip()
        if not texto:
            mostrar_observaciones(observaciones)
            return

        resultados = []
        for obs in observaciones:
            campos = [
                obs.get("id_observacion", ""),
                obs.get("tipo", ""),
                obs.get("descripcion", ""),
                obs.get("id_estudiante", ""),
                obs.get("id_docente", ""),
                obs.get("nombre_estudiante", ""),
                obs.get("apellido_estudiante", ""),
                obs.get("nombre_docente", ""),
                obs.get("apellido_docente", ""),
            ]
            if any(texto in str(campo or "").lower() for campo in campos):
                resultados.append(obs)

        mostrar_observaciones(resultados)

    entrada_buscar.bind("<KeyRelease>", buscar_observaciones)

    def abrir_formulario(observacion=None):
        # Actualizar las listas antes de abrir el formulario.
        if not cargar_personas():
            return

        ventana = tk.Toplevel(parent)
        ventana.title("Editar Observación" if observacion else "Registrar Observación")
        ventana.geometry("700x650")
        ventana.minsize(650, 620)
        ventana.configure(bg=COLOR_FONDO)
        ventana.transient(parent)
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Editar Observación" if observacion else "Registrar Observación",
            font=("Arial", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO
        ).pack(pady=(20, 15))

        formulario = tk.Frame(ventana, bg=COLOR_BLANCO, padx=25, pady=18)
        formulario.pack(padx=25, fill="both", expand=True)

        formulario.grid_columnconfigure(1, weight=1)

        def crear_campo(texto, fila):
            tk.Label(
                formulario, text=texto, font=("Arial", 10, "bold"),
                bg=COLOR_BLANCO, fg=COLOR_TEXTO
            ).grid(row=fila, column=0, sticky="w", pady=9, padx=(0, 12))

        crear_campo("Fecha (AAAA-MM-DD):", 0)
        entrada_fecha = tk.Entry(formulario, font=("Arial", 10), width=40)
        entrada_fecha.grid(row=0, column=1, sticky="ew", pady=9)

        crear_campo("Tipo:", 1)
        combo_tipo = ttk.Combobox(
            formulario,
            values=["Conducta", "Académica", "Disciplinaria", "Familiar", "Salud", "Otra"],
            state="normal", width=37
        )
        combo_tipo.grid(row=1, column=1, sticky="ew", pady=9)

        crear_campo("Descripción:", 2)
        entrada_descripcion = tk.Text(
            formulario, width=40, height=5, font=("Arial", 10), relief="solid", bd=1
        )
        entrada_descripcion.grid(row=2, column=1, sticky="ew", pady=9)

        crear_campo("Requiere seguimiento:", 3)
        combo_seguimiento = ttk.Combobox(
            formulario, values=["SI", "NO"], state="readonly", width=37
        )
        combo_seguimiento.grid(row=3, column=1, sticky="ew", pady=9)

        crear_campo("Estudiante:", 4)
        combo_estudiante = ttk.Combobox(
            formulario, values=list(estudiantes_por_nombre.keys()),
            state="readonly", width=45
        )
        combo_estudiante.grid(row=4, column=1, sticky="ew", pady=9)

        crear_campo("Docente:", 5)
        combo_docente = ttk.Combobox(
            formulario, values=list(docentes_por_nombre.keys()),
            state="readonly", width=45
        )
        combo_docente.grid(row=5, column=1, sticky="ew", pady=9)

        if not estudiantes_por_nombre:
            combo_estudiante.configure(state="disabled")
        if not docentes_por_nombre:
            combo_docente.configure(state="disabled")

        if observacion:
            entrada_fecha.insert(0, str(observacion.get("fecha") or "")[:10])
            combo_tipo.set(observacion.get("tipo", ""))
            entrada_descripcion.insert("1.0", observacion.get("descripcion", ""))
            combo_seguimiento.set(str(observacion.get("requiere_seguimiento", "")).upper())

            combo_estudiante.set(etiqueta_por_id(
                estudiantes_por_nombre, observacion.get("id_estudiante")
            ))
            combo_docente.set(etiqueta_por_id(
                docentes_por_nombre, observacion.get("id_docente")
            ))

        def guardar():
            fecha = entrada_fecha.get().strip()
            tipo = combo_tipo.get().strip()
            descripcion = entrada_descripcion.get("1.0", tk.END).strip()
            seguimiento = combo_seguimiento.get().strip()
            estudiante_etiqueta = combo_estudiante.get().strip()
            docente_etiqueta = combo_docente.get().strip()

            if not fecha or not tipo or not descripcion or not seguimiento:
                messagebox.showwarning(
                    "Validación", "Completá la fecha, tipo, descripción y seguimiento.",
                    parent=ventana
                )
                return

            if not estudiante_etiqueta or estudiante_etiqueta not in estudiantes_por_nombre:
                messagebox.showwarning(
                    "Validación", "Seleccioná un estudiante de la lista.", parent=ventana
                )
                return

            if not docente_etiqueta or docente_etiqueta not in docentes_por_nombre:
                messagebox.showwarning(
                    "Validación", "Seleccioná un docente de la lista.", parent=ventana
                )
                return

            datos = {
                "fecha": fecha,
                "tipo": tipo,
                "descripcion": descripcion,
                "requiere_seguimiento": seguimiento,
                "id_estudiante": int(estudiantes_por_nombre[estudiante_etiqueta]),
                "id_docente": int(docentes_por_nombre[docente_etiqueta]),
            }

            try:
                if observacion:
                    id_observacion = observacion.get("id_observacion")
                    respuesta = requests.put(
                        f"{API_URL}/{id_observacion}", json=datos, timeout=5
                    )
                    mensaje = "Observación actualizada correctamente."
                    codigos_ok = (200,)
                else:
                    respuesta = requests.post(API_URL, json=datos, timeout=5)
                    mensaje = "Observación agregada correctamente."
                    codigos_ok = (201,)

                if respuesta.status_code in codigos_ok:
                    messagebox.showinfo("Éxito", mensaje, parent=ventana)
                    ventana.destroy()
                    cargar_observaciones()
                else:
                    try:
                        error = respuesta.json()
                        detalle = error.get("detalle") or error.get("error") or respuesta.text
                    except ValueError:
                        detalle = respuesta.text or f"HTTP {respuesta.status_code}"
                    messagebox.showerror("Error", detalle, parent=ventana)

            except requests.exceptions.RequestException as error:
                messagebox.showerror(
                    "Error de conexión", f"No se pudo conectar con el servidor.\n\n{error}",
                    parent=ventana
                )

        contenedor_botones = tk.Frame(ventana, bg=COLOR_FONDO)
        contenedor_botones.pack(pady=13)

        tk.Button(
            contenedor_botones, text="Cancelar", font=("Arial", 10, "bold"),
            bg="#E9EEF4", fg=COLOR_TEXTO, relief="flat", padx=20, pady=8,
            command=ventana.destroy, cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            contenedor_botones, text="Guardar", font=("Arial", 10, "bold"),
            bg=COLOR_AZUL, fg="white", activebackground=COLOR_AZUL_OSCURO,
            relief="flat", padx=25, pady=8, command=guardar, cursor="hand2"
        ).pack(side="left", padx=5)

    def editar_observacion():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Editar", "Seleccioná una observación.", parent=parent)
            return

        valores = tabla.item(seleccion[0], "values")
        id_observacion = valores[0]

        try:
            respuesta = requests.get(f"{API_URL}/{id_observacion}", timeout=5)
            if respuesta.status_code == 200:
                abrir_formulario(respuesta.json())
            else:
                try:
                    detalle = respuesta.json().get("error", "No se pudo obtener la observación.")
                except ValueError:
                    detalle = respuesta.text
                messagebox.showerror("Error", detalle, parent=parent)
        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error de conexión", str(error), parent=parent)

    def eliminar_observacion():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar", "Seleccioná una observación.", parent=parent)
            return

        valores = tabla.item(seleccion[0], "values")
        id_observacion = valores[0]
        descripcion = valores[3]

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar esta observación?\n\n{descripcion}",
            parent=parent
        ):
            return

        try:
            respuesta = requests.delete(f"{API_URL}/{id_observacion}", timeout=5)
            if respuesta.status_code in (200, 204):
                messagebox.showinfo(
                    "Éxito", "Observación eliminada correctamente.", parent=parent
                )
                cargar_observaciones()
            else:
                try:
                    error = respuesta.json()
                    detalle = error.get("detalle") or error.get("error") or "No se pudo eliminar."
                except ValueError:
                    detalle = respuesta.text or f"HTTP {respuesta.status_code}"
                messagebox.showerror("Error", detalle, parent=parent)
        except requests.exceptions.RequestException as error:
            messagebox.showerror(
                "Error de conexión", f"No se pudo conectar con el servidor.\n\n{error}",
                parent=parent
            )

    btn_nueva.config(command=lambda: abrir_formulario())

    contenedor_acciones = tk.Frame(parent, bg=COLOR_FONDO)
    contenedor_acciones.pack(fill="x", padx=25, pady=(0, 18))

    tk.Button(
        contenedor_acciones, text="Editar", font=("Arial", 10, "bold"),
        bg="#EAF0F6", fg=COLOR_TEXTO, relief="flat", padx=20, pady=8,
        command=editar_observacion, cursor="hand2"
    ).pack(side="right", padx=5)

    tk.Button(
        contenedor_acciones, text="Borrar", font=("Arial", 10, "bold"),
        bg="#FFF0F2", fg=COLOR_ROJO, relief="flat", padx=20, pady=8,
        command=eliminar_observacion, cursor="hand2"
    ).pack(side="right", padx=5)

    cargar_observaciones()
