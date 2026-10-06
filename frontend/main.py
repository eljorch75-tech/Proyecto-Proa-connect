import tkinter as tk
from tkinter import ttk, messagebox
import requests
from frames.inicio import crear_inicio 
def mostrar_inicio():

    global contenedor

    # Eliminar el login
    login.destroy()

    # Crear un contenedor que ocupe toda la ventana
    contenedor = tk.Frame(
        ventana,
        bg="#eef1f5"
    )

    contenedor.pack(
        fill="both",
        expand=True
    )

    # Crear el frame de inicio
    frame_inicio = crear_inicio(contenedor)

    frame_inicio.pack(
        fill="both",
        expand=True
    ) 
def iniciar_sesion():

    usuario = entrada_usuario.get()
    contraseña = entrada_contraseña.get()

    if usuario == "" or contraseña == "":
        messagebox.showwarning(
            "Campos vacíos",
            "Ingrese usuario y contraseña."
        )
        return

    datos = {
        "nombre_usuario": usuario,
        "contrasena": contraseña
    }

    try:

        respuesta = requests.post(
            "http://localhost:3000/api/login",
            json=datos
        )

        if respuesta.status_code == 200:

            messagebox.showinfo(
                "Inicio de sesión",
                "¡Bienvenido!"
            )

            # Acá podrías abrir la pantalla principal
            mostrar_inicio()

        elif respuesta.status_code == 401:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos."
            )

        else:

            messagebox.showerror(
                "Error",
                "Ocurrió un error al iniciar sesión."
            )

    except requests.exceptions.RequestException:

        messagebox.showerror(
            "Error",
            "No se pudo conectar con el servidor."
        ) 


# -----------------------------
# Ventana principal
# -----------------------------
ventana = tk.Tk()
ventana.title("ProAConnect - Inicio de Sesión")
ventana.geometry("1000x650")
ventana.minsize(800, 550)
ventana.configure(bg="#0d1728")


# -----------------------------
# Contenedor principal
# -----------------------------
contenedor = tk.Frame(
    ventana,
    bg="#0d1728"
)
contenedor.pack(
    fill="both",
    expand=True
)


# -----------------------------
# Tarjeta blanca del Login
# -----------------------------
login = tk.Frame(
    contenedor,
    bg="white",
    width=480,
    height=570
)

login.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

# Evita que el contenido cambie el tamaño de la tarjeta
login.pack_propagate(False)


# -----------------------------
# Ícono superior
# -----------------------------
icono = tk.Label(
    login,
    text="🌐",
    font=("Segoe UI Emoji", 32),
    bg="#20a4bd",
    fg="white",
    width=3,
    height=1
)

icono.pack(pady=(35, 15))


# -----------------------------
# Título
# -----------------------------
titulo = tk.Label(
    login,
    text="ProAConnect",
    font=("Segoe UI", 24, "bold"),
    bg="white",
    fg="#142b45"
)

titulo.pack()


subtitulo = tk.Label(
    login,
    text="Gestión Institucional y Control de Asistencia",
    font=("Segoe UI", 11),
    bg="white",
    fg="#718096"
)

subtitulo.pack(pady=(5, 30))


# -----------------------------
# Usuario
# -----------------------------
tk.Label(
    login,
    text="Usuario / Correo Institucional",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#17304b",
    anchor="w"
).pack(
    fill="x",
    padx=40
)


entrada_usuario = tk.Entry(
    login,
    font=("Segoe UI", 11),
    bg="#f7f9fc",
    fg="#26384d",
    relief="solid",
    bd=1
)

entrada_usuario.pack(
    fill="x",
    padx=40,
    pady=(7, 18),
    ipady=9
)

entrada_usuario.insert(
    0,
    "correo@proa.edu.ar"
)


# -----------------------------
# Contraseña
# -----------------------------
tk.Label(
    login,
    text="Contraseña",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#17304b",
    anchor="w"
).pack(
    fill="x",
    padx=40
)


entrada_contraseña = tk.Entry(
    login,
    font=("Segoe UI", 11),
    bg="#f7f9fc",
    fg="#26384d",
    relief="solid",
    bd=1,
    show="•"
)

entrada_contraseña.pack(
    fill="x",
    padx=40,
    pady=(7, 18),
    ipady=9
)


# -----------------------------
# Rol
# -----------------------------
tk.Label(
    login,
    text="Rol / Cargo",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#17304b",
    anchor="w"
).pack(
    fill="x",
    padx=40
)


combo_rol = ttk.Combobox(
    login,
    font=("Segoe UI", 10),
    state="readonly",
    values=[
        "Directivo/a (Dir. Ana Martínez)",
        "Docente",
        "Preceptor/a",
        "Administrador/a",
        "Estudiante"
    ]
)

combo_rol.pack(
    fill="x",
    padx=40,
    pady=(7, 25),
    ipady=5
)

combo_rol.current(0)


# -----------------------------
# Botón Iniciar Sesión
# -----------------------------
boton_login = tk.Button(
    login,
    text="↪  Iniciar Sesión",
    command=iniciar_sesion,
    font=("Segoe UI", 11, "bold"),
    bg="#20a4bd",
    fg="white",
    activebackground="#178ca3",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    bd=0
)

boton_login.pack(
    fill="x",
    padx=40,
    ipady=10
)


# -----------------------------
# Texto inferior
# -----------------------------
separador = tk.Frame(
    login,
    bg="#e5e9ef",
    height=1
)

separador.pack(
    fill="x",
    padx=40,
    pady=(25, 15)
)


texto_inferior = tk.Label(
    login,
    text="Acceso seguro reservado para usuarios autorizados del Programa ProA.",
    font=("Segoe UI", 8),
    bg="white",
    fg="#91a0b2",
    wraplength=380
)

texto_inferior.pack(
    padx=40
)


# -----------------------------
# Enter para iniciar sesión
# -----------------------------
ventana.bind(
    "<Return>",
    lambda evento: iniciar_sesion()
)


# -----------------------------
# Ejecutar aplicación
# -----------------------------
ventana.mainloop()