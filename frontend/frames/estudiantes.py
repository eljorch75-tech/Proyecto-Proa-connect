import tkinter as tk
from tkinter import ttk, messagebox
import requests

# ============================================================
# CONFIGURACIÓN DE API
# ============================================================
API_URL = "http://localhost:3000/api/estudiantes"
API_CURSOS_URL = "http://localhost:3000/api/cursos"
# Si tu backend registra la ruta como /api/curso (singular),
# cambia API_CURSOS_URL por "http://localhost:3000/api/curso".

# ============================================================
# COLORES
# ============================================================
COLOR_FONDO = "#F3F6F9"
COLOR_AZUL = "#179DB8"
COLOR_AZUL_HOVER = "#138BA4"
COLOR_BLANCO = "#FFFFFF"
COLOR_TEXTO = "#19304A"
COLOR_GRIS = "#65758B"
COLOR_VERDE = "#19B47A"
COLOR_ROJO = "#F04B50"
COLOR_AMARILLO = "#F2B134"


def crear_estudiantes(parent):
    """
    Vista CRUD de estudiantes integrada dentro del Frame recibido.
    Requiere:
      GET/POST     API_URL
      GET/PUT/DELETE API_URL/:id
      GET          API_CURSOS_URL
    """

    frame = tk.Frame(parent, bg=COLOR_FONDO)
    # No empaquetar aquí: el menú principal debe colocar esta vista
    # dentro de su contenedor de contenido para no duplicar el menú lateral.

    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # ========================================================
    # CABECERA
    # ========================================================
    header = tk.Frame(frame, bg=COLOR_FONDO)
    header.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 8))
    header.grid_columnconfigure(0, weight=1)

    tk.Label(
        header, text="Alumnos", font=("Segoe UI", 24, "bold"),
        fg=COLOR_TEXTO, bg=COLOR_FONDO
    ).grid(row=0, column=0, sticky="w")

    label_estado = tk.Label(
        header, text="● Conectando...", font=("Segoe UI", 10, "bold"),
        fg=COLOR_AMARILLO, bg=COLOR_FONDO
    )
    label_estado.grid(row=0, column=1, sticky="e", padx=8)

    # ========================================================
    # TARJETAS RESUMEN
    # ========================================================
    cards = tk.Frame(frame, bg=COLOR_FONDO)
    cards.grid(row=1, column=0, sticky="ew", padx=25, pady=8)
    for col in range(3):
        cards.grid_columnconfigure(col, weight=1)

    def crear_tarjeta(col, titulo, color=COLOR_BLANCO, color_texto=COLOR_TEXTO):
        tarjeta = tk.Frame(cards, bg=color, height=100)
        tarjeta.grid(row=0, column=col, sticky="ew", padx=5)
        tarjeta.grid_propagate(False)
        tk.Label(
            tarjeta, text=titulo, font=("Segoe UI", 10, "bold"),
            fg=color_texto, bg=color
        ).pack(anchor="w", padx=16, pady=(13, 0))
        valor = tk.Label(
            tarjeta, text="0", font=("Segoe UI", 25, "bold"),
            fg=color_texto, bg=color
        )
        valor.pack(anchor="w", padx=16)
        return valor

    label_total = crear_tarjeta(0, "Total de alumnos", COLOR_AZUL, COLOR_BLANCO)
    label_registros = crear_tarjeta(1, "Registros cargados")
    label_cursos = crear_tarjeta(2, "Cursos disponibles")

    # ========================================================
    # PANEL PRINCIPAL
    # ========================================================
    panel = tk.Frame(
        frame, bg=COLOR_BLANCO, highlightthickness=1,
        highlightbackground="#E2E8EE"
    )
    panel.grid(row=2, column=0, sticky="nsew", padx=25, pady=(8, 22))
    panel.grid_columnconfigure(0, weight=1)
    panel.grid_rowconfigure(2, weight=1)

    barra = tk.Frame(panel, bg=COLOR_BLANCO)
    barra.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 10))
    barra.grid_columnconfigure(0, weight=1)

    tk.Label(
        barra, text="REGISTRO DE ALUMNOS", font=("Segoe UI", 12, "bold"),
        fg=COLOR_TEXTO, bg=COLOR_BLANCO
    ).grid(row=0, column=0, sticky="w")

    boton_nuevo = tk.Button(
        barra, text="+ Nuevo alumno", font=("Segoe UI", 10, "bold"),
        bg=COLOR_AZUL, fg=COLOR_BLANCO, activebackground=COLOR_AZUL_HOVER,
        activeforeground=COLOR_BLANCO, relief="flat", bd=0,
        padx=15, pady=8, cursor="hand2"
    )
    boton_nuevo.grid(row=0, column=1, padx=(8, 0))

    boton_editar = tk.Button(
        barra, text="Editar seleccionado", font=("Segoe UI", 10, "bold"),
        bg="#E8EEF3", fg=COLOR_TEXTO, activebackground="#D9E4EC",
        relief="flat", bd=0, padx=12, pady=8, cursor="hand2"
    )
    boton_editar.grid(row=0, column=2, padx=(8, 0))

    boton_eliminar = tk.Button(
        barra, text="Eliminar seleccionado", font=("Segoe UI", 10, "bold"),
        bg="#FDEBEC", fg=COLOR_ROJO, activebackground="#FAD5D7",
        relief="flat", bd=0, padx=12, pady=8, cursor="hand2"
    )
    boton_eliminar.grid(row=0, column=3, padx=(8, 0))

    # ========================================================
    # BUSCADOR Y FILTRO POR CURSO
    # ========================================================
    filtros = tk.Frame(panel, bg=COLOR_BLANCO)
    filtros.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
    filtros.grid_columnconfigure(0, weight=2)
    filtros.grid_columnconfigure(1, weight=1)

    entrada_buscar = tk.Entry(
        filtros, font=("Segoe UI", 10), bg="#F4F7FA",
        fg=COLOR_TEXTO, relief="flat", highlightthickness=1,
        highlightbackground="#DDE5EC"
    )
    entrada_buscar.grid(row=0, column=0, sticky="ew", ipady=8, padx=(0, 10))
    entrada_buscar.insert(0, "Buscar por nombre, apellido o DNI...")

    def limpiar_placeholder(event=None):
        if entrada_buscar.get() == "Buscar por nombre, apellido o DNI...":
            entrada_buscar.delete(0, tk.END)

    def restaurar_placeholder(event=None):
        if not entrada_buscar.get().strip():
            entrada_buscar.insert(0, "Buscar por nombre, apellido o DNI...")

    entrada_buscar.bind("<FocusIn>", limpiar_placeholder)
    entrada_buscar.bind("<FocusOut>", restaurar_placeholder)

    filtro_curso = ttk.Combobox(filtros, state="readonly", font=("Segoe UI", 10))
    filtro_curso.grid(row=0, column=1, sticky="ew", ipady=4)
    filtro_curso.set("Todos los cursos")

    boton_refrescar = tk.Button(
        filtros, text="↻", font=("Segoe UI", 13, "bold"),
        bg="#E8EEF3", fg=COLOR_TEXTO, relief="flat", bd=0,
        width=3, cursor="hand2"
    )
    boton_refrescar.grid(row=0, column=2, padx=(10, 0))

    # ========================================================
    # TABLA
    # ========================================================
    tabla_frame = tk.Frame(panel, bg=COLOR_BLANCO)
    tabla_frame.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
    tabla_frame.grid_rowconfigure(0, weight=1)
    tabla_frame.grid_columnconfigure(0, weight=1)

    columnas = (
        "id", "nombre", "dni", "fecha", "curso",
        "tutor", "telefono", "email"
    )
    tabla = ttk.Treeview(
        tabla_frame, columns=columnas, show="headings", selectmode="browse"
    )

    encabezados = {
        "id": ("ID", 55, "center"),
        "nombre": ("Nombre y apellido", 175, "w"),
        "dni": ("DNI", 90, "center"),
        "fecha": ("Nacimiento", 105, "center"),
        "curso": ("Curso", 180, "w"),
        "tutor": ("Tutor", 150, "w"),
        "telefono": ("Teléfono", 115, "w"),
        "email": ("Email", 175, "w"),
    }
    for clave, (titulo, ancho, ancla) in encabezados.items():
        tabla.heading(clave, text=titulo)
        tabla.column(clave, width=ancho, anchor=ancla)

    scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    scrollbar_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    estilo = ttk.Style()
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass
    estilo.configure(
        "Treeview", background=COLOR_BLANCO, foreground=COLOR_TEXTO,
        rowheight=35, fieldbackground=COLOR_BLANCO, font=("Segoe UI", 9)
    )
    estilo.configure(
        "Treeview.Heading", background="#EDF2F6", foreground=COLOR_TEXTO,
        font=("Segoe UI", 9, "bold"), relief="flat"
    )
    estilo.map("Treeview", background=[("selected", "#DDF3F7")])

    # ========================================================
    # DATOS EN MEMORIA
    # ========================================================
    estudiantes_data = []
    cursos_data = []
    curso_por_texto = {}
    curso_por_id = {}

    def texto_curso(curso):
        nombre = str(curso.get("nombre_curso") or "Curso")
        anio = curso.get("anio")
        division = curso.get("division")
        turno = curso.get("turno")
        ciclo = curso.get("ciclo_lectivo")

        partes = [nombre]
        if anio not in (None, "") and str(anio) != nombre:
            partes.append(f"Año {anio}")
        if division:
            partes.append(f"Div. {division}")
        if turno:
            partes.append(str(turno))
        if ciclo:
            partes.append(str(ciclo))
        return " - ".join(partes)

    def cargar_cursos(mostrar_error=True):
        nonlocal cursos_data, curso_por_texto, curso_por_id
        try:
            respuesta = requests.get(API_CURSOS_URL, timeout=5)
            respuesta.raise_for_status()
            datos = respuesta.json()
            if not isinstance(datos, list):
                raise ValueError("La ruta de cursos debe devolver una lista JSON.")

            cursos_data = datos
            curso_por_texto = {}
            curso_por_id = {}

            opciones = ["Todos los cursos"]
            for curso in cursos_data:
                id_curso = curso.get("id_curso")
                if id_curso is None:
                    continue
                etiqueta = texto_curso(curso)
                # Evita etiquetas duplicadas si hay cursos con igual descripción.
                if etiqueta in curso_por_texto:
                    etiqueta = f"{etiqueta} (ID {id_curso})"
                curso_por_texto[etiqueta] = curso
                curso_por_id[str(id_curso)] = curso
                opciones.append(etiqueta)

            filtro_curso["values"] = opciones
            if filtro_curso.get() not in opciones:
                filtro_curso.set("Todos los cursos")
            label_cursos.config(text=str(len(cursos_data)))
            return True
        except Exception as error:
            label_cursos.config(text="—")
            if mostrar_error:
                messagebox.showerror(
                    "Error al cargar cursos",
                    f"No se pudieron cargar los cursos desde:\n{API_CURSOS_URL}\n\n{error}",
                    parent=frame
                )
            return False

    def nombre_curso_estudiante(estudiante):
        id_curso = estudiante.get("id_curso")
        curso = curso_por_id.get(str(id_curso)) if id_curso is not None else None
        if curso:
            return texto_curso(curso)
        # El backend de estudiantes incluye nombre_curso mediante LEFT JOIN.
        return estudiante.get("nombre_curso") or (
            f"ID curso: {id_curso}" if id_curso else "Sin curso"
        )

    def limpiar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

    def filtrar_y_mostrar(event=None):
        texto = entrada_buscar.get().strip().lower()
        if texto == "buscar por nombre, apellido o dni...":
            texto = ""
        curso_seleccionado = filtro_curso.get()
        curso_filtrado = curso_por_texto.get(curso_seleccionado)
        id_curso_filtro = str(curso_filtrado.get("id_curso")) if curso_filtrado else None

        limpiar_tabla()
        for estudiante in estudiantes_data:
            nombre = str(estudiante.get("nombre") or "")
            apellido = str(estudiante.get("apellido") or "")
            dni = str(estudiante.get("dni") or "")
            completo = f"{nombre} {apellido} {dni}".lower()

            if texto and texto not in completo:
                continue
            if id_curso_filtro and str(estudiante.get("id_curso")) != id_curso_filtro:
                continue

            id_estudiante = estudiante.get("id_estudiante")
            if id_estudiante is None:
                # Compatibilidad temporal con APIs que devuelvan "id".
                id_estudiante = estudiante.get("id")
            if id_estudiante is None:
                continue

            tabla.insert(
                "", "end", iid=str(id_estudiante),
                values=(
                    id_estudiante,
                    f"{nombre} {apellido}".strip(),
                    dni,
                    str(estudiante.get("fecha_nacimiento") or "")[:10],
                    nombre_curso_estudiante(estudiante),
                    estudiante.get("nombre_tutor") or "",
                    estudiante.get("telefono_tutor") or "",
                    estudiante.get("email_tutor") or "",
                )
            )

    def cargar_estudiantes(mostrar_error=True):
        nonlocal estudiantes_data
        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            datos = respuesta.json()
            if not isinstance(datos, list):
                raise ValueError("La ruta de estudiantes debe devolver una lista JSON.")
            estudiantes_data = datos
            cantidad = len(estudiantes_data)
            label_total.config(text=str(cantidad))
            label_registros.config(text=str(cantidad))
            label_estado.config(text="● Conectado", fg=COLOR_VERDE)
            filtrar_y_mostrar()
        except Exception as error:
            label_estado.config(text="● Sin conexión / error", fg=COLOR_ROJO)
            limpiar_tabla()
            if mostrar_error:
                messagebox.showerror(
                    "Error al cargar estudiantes",
                    f"No se pudieron cargar los estudiantes desde:\n{API_URL}\n\n{error}",
                    parent=frame
                )

    # ========================================================
    # FORMULARIO ALTA / EDICIÓN
    # ========================================================
    def abrir_formulario(estudiante=None):
        editando = estudiante is not None

        if not cursos_data and not cargar_cursos(mostrar_error=False):
            messagebox.showwarning(
                "Cursos no disponibles",
                "No se pudo cargar la lista de cursos.\n"
                "Verificá que exista la ruta GET de cursos y que haya cursos registrados.",
                parent=frame
            )
            return

        ventana = tk.Toplevel(frame)
        ventana.title("Editar estudiante" if editando else "Nuevo estudiante")
        ventana.geometry("640x690")
        ventana.minsize(600, 650)
        ventana.configure(bg=COLOR_BLANCO)
        ventana.transient(frame.winfo_toplevel())

        encabezado = tk.Frame(ventana, bg=COLOR_AZUL, height=75)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)
        tk.Label(
            encabezado,
            text="EDITAR ALUMNO" if editando else "NUEVO ALUMNO",
            font=("Segoe UI", 17, "bold"), fg=COLOR_BLANCO, bg=COLOR_AZUL
        ).pack(anchor="w", padx=25, pady=20)

        form = tk.Frame(ventana, bg=COLOR_BLANCO)
        form.pack(fill="both", expand=True, padx=30, pady=18)
        form.grid_columnconfigure(1, weight=1)

        campos = {}
        datos_campos = [
            ("nombre", "Nombre"),
            ("apellido", "Apellido"),
            ("dni", "DNI"),
            ("fecha_nacimiento", "Fecha de nacimiento (AAAA-MM-DD)"),
            ("nombre_tutor", "Nombre del tutor"),
            ("telefono_tutor", "Teléfono del tutor"),
            ("email_tutor", "Email del tutor"),
        ]

        for fila, (clave, etiqueta) in enumerate(datos_campos):
            tk.Label(
                form, text=etiqueta, font=("Segoe UI", 10, "bold"),
                fg=COLOR_TEXTO, bg=COLOR_BLANCO
            ).grid(row=fila, column=0, sticky="w", pady=7)

            entrada = tk.Entry(
                form, font=("Segoe UI", 10), bg="#F5F8FA",
                fg=COLOR_TEXTO, relief="flat", highlightthickness=1,
                highlightbackground="#D8E1E8"
            )
            entrada.grid(row=fila, column=1, sticky="ew", padx=(18, 0), ipady=7)
            campos[clave] = entrada

            if editando:
                valor = estudiante.get(clave, "")
                if valor is not None:
                    entrada.insert(0, str(valor)[:10] if clave == "fecha_nacimiento" else str(valor))

        fila_curso = len(datos_campos)
        tk.Label(
            form, text="Curso", font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXTO, bg=COLOR_BLANCO
        ).grid(row=fila_curso, column=0, sticky="w", pady=7)

        combo_curso = ttk.Combobox(form, state="readonly", font=("Segoe UI", 10))
        combo_curso.grid(row=fila_curso, column=1, sticky="ew", padx=(18, 0), ipady=5)

        opciones_cursos = list(curso_por_texto.keys())
        combo_curso["values"] = opciones_cursos

        curso_actual_id = estudiante.get("id_curso") if editando else None
        curso_actual = curso_por_id.get(str(curso_actual_id)) if curso_actual_id is not None else None
        if curso_actual:
            combo_curso.set(texto_curso(curso_actual))
        elif opciones_cursos:
            combo_curso.current(0)

        tk.Label(
            form,
            text="Seleccioná el curso al que pertenece el estudiante.",
            font=("Segoe UI", 9), fg=COLOR_GRIS, bg=COLOR_BLANCO
        ).grid(row=fila_curso + 1, column=1, sticky="w", padx=(18, 0), pady=(0, 8))

        botones = tk.Frame(ventana, bg=COLOR_BLANCO)
        botones.pack(fill="x", padx=30, pady=(0, 22))

        def guardar():
            datos_enviar = {
                clave: entrada.get().strip()
                for clave, entrada in campos.items()
            }

            if not datos_enviar["nombre"]:
                messagebox.showwarning("Datos incompletos", "Ingresá el nombre del estudiante.", parent=ventana)
                return
            if not datos_enviar["apellido"]:
                messagebox.showwarning("Datos incompletos", "Ingresá el apellido del estudiante.", parent=ventana)
                return
            if not datos_enviar["dni"]:
                messagebox.showwarning("Datos incompletos", "Ingresá el DNI.", parent=ventana)
                return
            if not datos_enviar["fecha_nacimiento"]:
                messagebox.showwarning("Datos incompletos", "Ingresá la fecha de nacimiento.", parent=ventana)
                return
            if not combo_curso.get():
                messagebox.showwarning("Curso obligatorio", "Seleccioná un curso.", parent=ventana)
                return

            curso_elegido = curso_por_texto.get(combo_curso.get())
            if not curso_elegido:
                messagebox.showwarning("Curso inválido", "Seleccioná un curso válido de la lista.", parent=ventana)
                return

            datos_enviar["id_curso"] = int(curso_elegido["id_curso"])

            try:
                if editando:
                    id_estudiante = estudiante.get("id_estudiante", estudiante.get("id"))
                    respuesta = requests.put(
                        f"{API_URL}/{id_estudiante}", json=datos_enviar, timeout=8
                    )
                else:
                    respuesta = requests.post(API_URL, json=datos_enviar, timeout=8)

                if respuesta.status_code in (200, 201):
                    messagebox.showinfo(
                        "Correcto",
                        "Estudiante actualizado correctamente." if editando
                        else "Estudiante agregado correctamente.",
                        parent=ventana
                    )
                    ventana.destroy()
                    cargar_estudiantes()
                else:
                    try:
                        error_json = respuesta.json()
                        detalle = error_json.get("detalle") or error_json.get("error") or respuesta.text
                    except ValueError:
                        detalle = respuesta.text
                    messagebox.showerror("Error", detalle, parent=ventana)

            except requests.RequestException as error:
                messagebox.showerror("Error de conexión", f"No se pudo conectar con el backend.\n{error}", parent=ventana)

        tk.Button(
            botones, text="Cancelar", font=("Segoe UI", 10, "bold"),
            bg="#E9EEF2", fg=COLOR_TEXTO, relief="flat", bd=0,
            padx=22, pady=10, cursor="hand2", command=ventana.destroy
        ).pack(side="right", padx=5)

        tk.Button(
            botones, text="Guardar cambios" if editando else "Guardar alumno",
            font=("Segoe UI", 10, "bold"), bg=COLOR_AZUL, fg=COLOR_BLANCO,
            activebackground=COLOR_AZUL_HOVER, activeforeground=COLOR_BLANCO,
            relief="flat", bd=0, padx=22, pady=10, cursor="hand2",
            command=guardar
        ).pack(side="right", padx=5)

        ventana.grab_set()

    # ========================================================
    # ACCIONES DE EDICIÓN Y ELIMINACIÓN
    # ========================================================
    def estudiante_seleccionado():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar estudiante", "Seleccioná un estudiante de la tabla.", parent=frame)
            return None
        id_seleccionado = str(seleccion[0])
        for estudiante in estudiantes_data:
            id_est = estudiante.get("id_estudiante", estudiante.get("id"))
            if str(id_est) == id_seleccionado:
                return estudiante
        return None

    def editar_seleccionado(event=None):
        estudiante = estudiante_seleccionado()
        if estudiante is None:
            return
        # Consultar el registro actualizado para obtener id_curso y demás campos.
        id_est = estudiante.get("id_estudiante", estudiante.get("id"))
        try:
            respuesta = requests.get(f"{API_URL}/{id_est}", timeout=8)
            respuesta.raise_for_status()
            abrir_formulario(respuesta.json())
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo obtener el estudiante.\n{error}", parent=frame)

    def eliminar_seleccionado(event=None):
        estudiante = estudiante_seleccionado()
        if estudiante is None:
            return
        id_est = estudiante.get("id_estudiante", estudiante.get("id"))
        nombre = f"{estudiante.get('nombre', '')} {estudiante.get('apellido', '')}".strip()

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Querés eliminar al estudiante?\n\n{nombre}\n\nEsta acción no se puede deshacer.",
            parent=frame
        ):
            return

        try:
            respuesta = requests.delete(f"{API_URL}/{id_est}", timeout=8)
            if respuesta.status_code in (200, 204):
                messagebox.showinfo("Correcto", "Estudiante eliminado correctamente.", parent=frame)
                cargar_estudiantes()
            else:
                try:
                    body = respuesta.json()
                    detalle = body.get("detalle") or body.get("error") or respuesta.text
                except ValueError:
                    detalle = respuesta.text
                messagebox.showerror("Error", detalle, parent=frame)
        except requests.RequestException as error:
            messagebox.showerror("Error de conexión", str(error), parent=frame)

    boton_nuevo.config(command=abrir_formulario)
    boton_editar.config(command=editar_seleccionado)
    boton_eliminar.config(command=eliminar_seleccionado)
    boton_refrescar.config(command=lambda: (cargar_cursos(), cargar_estudiantes()))
    tabla.bind("<Double-1>", editar_seleccionado)
    tabla.bind("<Delete>", eliminar_seleccionado)
    tabla.bind("<F2>", editar_seleccionado)
    entrada_buscar.bind("<KeyRelease>", filtrar_y_mostrar)
    filtro_curso.bind("<<ComboboxSelected>>", filtrar_y_mostrar)

    # Cargar cursos primero para poder mostrar nombres en la tabla.
    cargar_cursos(mostrar_error=False)
    cargar_estudiantes(mostrar_error=True)

    return frame
