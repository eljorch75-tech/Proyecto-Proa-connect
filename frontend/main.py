import tkinter as tk
from tkinter import ttk, messagebox


# -----------------------------
# Ventana principal
# -----------------------------
ventana = tk.Tk()
ventana.title("ProAConnect - Inicio de Sesión")
ventana.geometry("1000x650")
ventana.minsize(800, 550)
ventana.configure(bg="#0d1728")


# -----------------------------
# Función para iniciar sesión
# -----------------------------
def iniciar_sesion():
    usuario = entrada_usuario.get()
    contraseña = entrada_contraseña.get()
    rol = combo_rol.get()

    if usuario == "" or contraseña == "":
        messagebox.showwarning(
            "Campos incompletos",
            "Por favor, completá el usuario y la contraseña."
        )
        return

    # Acá después podés agregar la validación real
    messagebox.showinfo(
        "Inicio de sesión",
        f"Bienvenido/a\n\nUsuario: {usuario}\nRol: {rol}"
    )


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