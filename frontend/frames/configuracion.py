
import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ==========================================
# CONFIGURACION DE LA API
# ==========================================
API_URL = "http://localhost:3000/usuarios"

# Colores de la interfaz
COLOR_FONDO = "#F1F5F9"
COLOR_PANEL = "#FFFFFF"
COLOR_AZUL = "#173F78"
COLOR_CELESTE = "#18A4BD"
COLOR_TEXTO = "#24364B"
COLOR_BORDE = "#DCE5EF"
COLOR_GRIS = "#64748B"


def usuario(parent):

    # ==========================================
    # FRAME PRINCIPAL
    # ==========================================
    frame = tk.Frame(parent, bg=COLOR_FONDO)

    frame.pack(fill="both", expand=True)

    # ==========================================
    # ESTILOS
    # ==========================================
    estilo = ttk.Style()
    estilo.configure(
        "Usuarios.Treeview",
        background="white",
        foreground=COLOR_TEXTO,
        rowheight=30,
        fieldbackground="white",
        font=("Segoe UI", 10)
    )
    estilo.configure(
        "Usuarios.Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#E8EEF6",
        foreground=COLOR_AZUL
    )
    estilo.map(
        "Usuarios.Treeview",
        background=[("selected", "#D4EDF5")],
        foreground=[("selected", COLOR_TEXTO)]
    )

    # ==========================================
    # PANEL LATERAL
    # ==========================================
    lateral = tk.Frame(
        frame,
        bg=COLOR_PANEL,
        width=205
    )
    lateral.pack(side="left", fill="y")
    lateral.pack_propagate(False)

    logo = tk.Frame(lateral, bg="white")
    logo.pack(fill="x", pady=(25, 30), padx=15)

    tk.Label(
        logo,
        text="🌐 ProAConnect",
        font=("Segoe UI", 16, "bold"),
        fg=COLOR_AZUL,
        bg="white"
    ).pack(anchor="w")

    tk.Label(
        lateral,
        text="ADMINISTRACIÓN",
        font=("Segoe UI", 9, "bold"),
        fg=COLOR_GRIS,
        bg="white"
    ).pack(anchor="w", padx=20, pady=(0, 12))

    def boton_lateral(texto, comando=None, activo=False):
        btn = tk.Button(
            lateral,
            text=texto,
            command=comando,
            anchor="w",
            padx=18,
            pady=11,
            font=("Segoe UI", 10, "bold" if activo else "normal"),
            bg=COLOR_CELESTE if activo else "white",
            fg="white" if activo else COLOR_GRIS,
            activebackground=COLOR_CELESTE,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn.pack(fill="x", padx=10, pady=3)
        return btn

    boton_lateral("⌂   Home")
    boton_lateral("▣   Asistencia")
    boton_lateral("♟   Alumnos")
    boton_lateral("▤   Docentes")
    boton_lateral("⚙   Usuarios", activo=True)

    # ==========================================
    # AREA PRINCIPAL
    # ==========================================
    contenido = tk.Frame(frame, bg=COLOR_FONDO)
    contenido.pack(side="left", fill="both", expand=True)

    # Encabezado
    encabezado = tk.Frame(
        contenido,
        bg=COLOR_FONDO
    )
    encabezado.pack(fill="x", padx=25, pady=(20, 15))

    tk.Label(
        encabezado,
        text="Gestión de Usuarios",
        font=("Segoe UI", 21, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_AZUL
    ).pack(side="left")

    tk.Label(
        encabezado,
        text="Administración del sistema",
        font=("Segoe UI", 10),
        bg=COLOR_FONDO,
        fg=COLOR_GRIS
    ).pack(side="right", padx=5, pady=10)

    # Contenedor de tarjetas
    tarjetas = tk.Frame(contenido, bg=COLOR_FONDO)
    tarjetas.pack(fill="x", padx=20, pady=5)

    tarjetas.columnconfigure(0, weight=1)
    tarjetas.columnconfigure(1, weight=1)
    tarjetas.columnconfigure(2, weight=1)

    def crear_tarjeta(columna, titulo, subtitulo):
        tarjeta = tk.Frame(
            tarjetas,
            bg="white",
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        tarjeta.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=6,
            pady=4
        )

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_AZUL,
            bg="white"
        ).pack(anchor="w", padx=16, pady=(15, 3))

        tk.Label(
            tarjeta,
            text=subtitulo,
            font=("Segoe UI", 9),
            fg=COLOR_GRIS,
            bg="white",
            wraplength=210,
            justify="left"
        ).pack(anchor="w", padx=16, pady=(0, 12))

        tk.Frame(
            tarjeta,
            bg=COLOR_BORDE,
            height=1
        ).pack(fill="x", padx=15)

        cuerpo = tk.Frame(tarjeta, bg="white")
        cuerpo.pack(fill="both", expand=True, padx=15, pady=12)

        return cuerpo

    # ==========================================
    # TARJETA 1: DATOS DEL USUARIO
    # ==========================================
    tarjeta_usuario = crear_tarjeta(
        0,
        "♟  Perfil de Usuario",
        "Datos de identificación de la cuenta."
    )

    tk.Label(
        tarjeta_usuario,
        text="Nombre de usuario",
        bg="white",
        fg=COLOR_TEXTO,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 4))

    entrada_nombre = tk.Entry(
        tarjeta_usuario,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )
    entrada_nombre.pack(fill="x", ipady=7, pady=(0, 12))

    tk.Label(
        tarjeta_usuario,
        text="Rol del usuario",
        bg="white",
        fg=COLOR_TEXTO,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 4))

    entrada_rol = ttk.Combobox(
        tarjeta_usuario,
        values=["administrador", "docente", "directivo"],
        state="normal",
        font=("Segoe UI", 10)
    )
    entrada_rol.pack(fill="x", ipady=4, pady=(0, 12))

    # ==========================================
    # TARJETA 2: DATOS DE ACCESO
    # ==========================================
    tarjeta_acceso = crear_tarjeta(
        1,
        "🔐  Datos de Acceso",
        "Configuración de la contraseña."
    )

    tk.Label(
        tarjeta_acceso,
        text="Contraseña",
        bg="white",
        fg=COLOR_TEXTO,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 4))

    entrada_contrasena = tk.Entry(
        tarjeta_acceso,
        show="*",
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )
    entrada_contrasena.pack(fill="x", ipady=7, pady=(0, 8))

    tk.Label(
        tarjeta_acceso,
        text="Para editar, ingresá la nueva contraseña.",
        bg="white",
        fg=COLOR_GRIS,
        font=("Segoe UI", 9),
        wraplength=210,
        justify="left"
    ).pack(anchor="w", pady=(0, 15))

    tk.Label(
        tarjeta_acceso,
        text="ID del usuario seleccionado",
        bg="white",
        fg=COLOR_TEXTO,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 4))

    etiqueta_id = tk.Label(
        tarjeta_acceso,
        text="Nuevo usuario",
        bg="#EEF3F8",
        fg=COLOR_AZUL,
        font=("Segoe UI", 10),
        anchor="w",
        padx=10,
        pady=9
    )
    etiqueta_id.pack(fill="x")

    # ==========================================
    # TARJETA 3: DOCENTE ASOCIADO
    # ==========================================
    tarjeta_docente = crear_tarjeta(
        2,
        "▤  Docente Asociado",
        "Vinculación del usuario con un docente."
    )

    tk.Label(
        tarjeta_docente,
        text="ID del docente",
        bg="white",
        fg=COLOR_TEXTO,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 4))

    entrada_docente = tk.Entry(
        tarjeta_docente,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )
    entrada_docente.pack(fill="x", ipady=7, pady=(0, 12))

    tk.Label(
        tarjeta_docente,
        text="Este ID debe existir en la tabla docentes.",
        bg="white",
        fg=COLOR_GRIS,
        font=("Segoe UI", 9),
        wraplength=210,
        justify="left"
    ).pack(anchor="w", pady=(0, 18))

    # ==========================================
    # FUNCIONES AUXILIARES
    # ==========================================
    id_seleccionado = {"id": None}

    def limpiar():
        id_seleccionado["id"] = None

        entrada_nombre.delete(0, tk.END)
        entrada_contrasena.delete(0, tk.END)
        entrada_rol.set("")
        entrada_docente.delete(0, tk.END)

        etiqueta_id.config(text="Nuevo usuario")

        for seleccionado in tabla.selection():
            tabla.selection_remove(seleccionado)

    def obtener_datos():
        nombre = entrada_nombre.get().strip()
        contrasena = entrada_contrasena.get()
        rol = entrada_rol.get().strip()
        id_docente = entrada_docente.get().strip()

        if not nombre or not contrasena or not rol or not id_docente:
            messagebox.showwarning(
                "Campos obligatorios",
                "Completá todos los campos antes de continuar."
            )
            return None

        try:
            id_docente = int(id_docente)
            if id_docente <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "ID inválido",
                "El ID del docente debe ser un entero positivo."
            )
            return None

        return {
            "nombre_usuario": nombre,
            "contrasena": contrasena,
            "rol": rol,
            "id_docente": id_docente
        }

    # ==========================================
    # LISTAR USUARIOS
    # GET /usuarios
    # ==========================================
    def listar_usuarios():
        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            usuarios = respuesta.json()

            for fila in tabla.get_children():
                tabla.delete(fila)

            for u in usuarios:
                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        u["id_usuario"],
                        u["nombre_usuario"],
                        u.get("rol") or "",
                        u["id_docente"]
                    )
                )

        except requests.RequestException as error:
            messagebox.showerror(
                "Error de conexión",
                f"No se pudieron listar los usuarios.\n\n{error}"
            )
        except (ValueError, KeyError, TypeError) as error:
            messagebox.showerror(
                "Error de respuesta",
                f"La API devolvió datos inesperados.\n\n{error}"
            )

    # ==========================================
    # CREAR USUARIO
    # POST /usuarios
    # ==========================================
    def crear_usuario():
        datos = obtener_datos()

        if datos is None:
            return

        try:
            respuesta = requests.post(
                API_URL,
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 409:
                messagebox.showwarning(
                    "Usuario duplicado",
                    "Ese nombre de usuario ya existe."
                )
                return

            respuesta.raise_for_status()

            messagebox.showinfo(
                "Éxito",
                "Usuario creado correctamente."
            )

            limpiar()
            listar_usuarios()

        except requests.RequestException as error:
            detalle = ""

            if getattr(error, "response", None) is not None:
                detalle = error.response.text

            messagebox.showerror(
                "Error",
                f"No se pudo crear el usuario.\n{detalle or str(error)}"
            )

    # ==========================================
    # SELECCIONAR USUARIO DE LA TABLA
    # ==========================================
    def seleccionar_usuario(event=None):
        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0], "values")

        id_usuario = valores[0]

        try:
            respuesta = requests.get(
                f"{API_URL}/{id_usuario}",
                timeout=5
            )
            respuesta.raise_for_status()
            datos = respuesta.json()

            id_seleccionado["id"] = datos["id_usuario"]

            entrada_nombre.delete(0, tk.END)
            entrada_nombre.insert(0, datos["nombre_usuario"])

            entrada_rol.set(datos.get("rol") or "")

            entrada_docente.delete(0, tk.END)
            entrada_docente.insert(0, str(datos["id_docente"]))

            # La API no devuelve la contraseña.
            # Se debe ingresar una nueva para editar.
            entrada_contrasena.delete(0, tk.END)

            etiqueta_id.config(
                text=str(datos["id_usuario"])
            )

        except (requests.RequestException, ValueError, KeyError) as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los datos del usuario.\n{error}"
            )

    # ==========================================
    # EDITAR USUARIO
    # PUT /usuarios/:id
    # ==========================================
    def editar_usuario():
        id_usuario = id_seleccionado["id"]

        if id_usuario is None:
            messagebox.showwarning(
                "Seleccionar usuario",
                "Seleccioná un usuario de la tabla para editarlo."
            )
            return

        datos = obtener_datos()

        if datos is None:
            return

        try:
            respuesta = requests.put(
                f"{API_URL}/{id_usuario}",
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 409:
                messagebox.showwarning(
                    "Usuario duplicado",
                    "Ese nombre de usuario ya está registrado."
                )
                return

            respuesta.raise_for_status()

            messagebox.showinfo(
                "Éxito",
                "Usuario actualizado correctamente."
            )

            limpiar()
            listar_usuarios()

        except requests.RequestException as error:
            detalle = ""

            if getattr(error, "response", None) is not None:
                detalle = error.response.text

            messagebox.showerror(
                "Error",
                f"No se pudo editar el usuario.\n{detalle or str(error)}"
            )

    # ==========================================
    # BOTONES DE ACCIONES
    # ==========================================
    botones = tk.Frame(
        contenido,
        bg=COLOR_FONDO
    )
    botones.pack(fill="x", padx=25, pady=15)

    def crear_boton(texto, comando, color, ancho=15):
        return tk.Button(
            botones,
            text=texto,
            command=comando,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=9,
            width=ancho
        )

    crear_boton(
        "＋ Crear usuario",
        crear_usuario,
        COLOR_CELESTE
    ).pack(side="left", padx=(0, 8))

    crear_boton(
        "✎ Editar usuario",
        editar_usuario,
        COLOR_AZUL
    ).pack(side="left", padx=8)

    crear_boton(
        "Limpiar",
        limpiar,
        COLOR_GRIS,
        ancho=10
    ).pack(side="left", padx=8)

    crear_boton(
        "↻ Actualizar lista",
        listar_usuarios,
        "#32865B"
    ).pack(side="right", padx=(8, 0))

    # ==========================================
    # TABLA DE USUARIOS
    # ==========================================
    contenedor_tabla = tk.Frame(
        contenido,
        bg="white",
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    contenedor_tabla.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )

    tk.Label(
        contenedor_tabla,
        text="Usuarios registrados",
        font=("Segoe UI", 13, "bold"),
        fg=COLOR_AZUL,
        bg="white"
    ).pack(anchor="w", padx=15, pady=12)

    zona_tabla = tk.Frame(contenedor_tabla, bg="white")
    zona_tabla.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    columnas = (
        "id_usuario",
        "nombre_usuario",
        "rol",
        "id_docente"
    )

    tabla = ttk.Treeview(
        zona_tabla,
        columns=columnas,
        show="headings",
        style="Usuarios.Treeview",
        selectmode="browse"
    )

    tabla.heading("id_usuario", text="ID")
    tabla.heading("nombre_usuario", text="Nombre de usuario")
    tabla.heading("rol", text="Rol")
    tabla.heading("id_docente", text="ID docente")

    tabla.column("id_usuario", width=60, anchor="center")
    tabla.column("nombre_usuario", width=220)
    tabla.column("rol", width=150, anchor="center")
    tabla.column("id_docente", width=100, anchor="center")

    scroll_y = ttk.Scrollbar(
        zona_tabla,
        orient="vertical",
        command=tabla.yview
    )

    scroll_x = ttk.Scrollbar(
        zona_tabla,
        orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    tabla.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    zona_tabla.rowconfigure(0, weight=1)
    zona_tabla.columnconfigure(0, weight=1)

    tabla.bind("<<TreeviewSelect>>", seleccionar_usuario)

    # Cargar usuarios al abrir el módulo
    listar_usuarios()

    return frame
