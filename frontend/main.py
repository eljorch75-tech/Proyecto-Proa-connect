import tkinter as tk
from frames.estudiantes import crear_estudiantes
ventana = tk.Tk()
ventana.title("ProaConnect")
ventana.geometry("800x500")

def mostrar_Frame(funcion_frame):
    for widget in contenedor.winfo_children():
        widget.destroy()
    frame= funcion_frame(contenedor)
    frame.pack(fill="both", expand=True)
def mostrar_menu():
    menu = tk.Frame(ventana, bg="blue", height=60)
    menu.pack(side="top", fill="x")
    global contenedor
    contenedor = tk.Frame(ventana, bg="white")
    contenedor.pack(fill="both", expand=True)


    tk.Button(menu, text="Estudiantes", command=lambda: mostrar_Frame(crear_estudiantes)).pack(side="left", padx=10, pady=10)
mostrar_menu()
ventana.mainloop()