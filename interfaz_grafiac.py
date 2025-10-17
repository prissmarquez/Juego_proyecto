
import tkinter as tk
from tkinter import messagebox
import random

# ---------------- Funciones del juego ---------------- #

def generar_matriz(level):
    """Generar matriz cuadrada con True (X) o False."""
    rates = {0: 33, 1: 66, 2: 50}
    x_threshold = rates[level % 3]
    dim_matriz = 2 + ((level - 1) // 3)

    possible = [False, False]
    while False in possible:
        matriz = []
        possible = [False, False]
        for _ in range(dim_matriz):
            fila = []
            for _ in range(dim_matriz):
                prob = random.random()
                if prob * 100 >= x_threshold:
                    fila.append(True)
                    possible[1] = True
                else:
                    fila.append(False)
                    possible[0] = True
            matriz.append(fila)
    return matriz

def mostrar_matriz_x():
    """Mostrar las X al inicio para memorizar."""
    # Bloquear todos los botones durante la fase de memorización
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            botones[i][j].config(state="disabled")
            if matriz[i][j]:
                botones[i][j].config(bg="red", text="X")
            else:
                botones[i][j].config(bg="white", text="")
    root.update()

    # Calcular tiempo de memorización
    # 5 segundos base + 1 segundo extra por cada incremento de tamaño
    dim = len(matriz)
    segundos_extra = (dim - 2) * 1000  # cada vez que la matriz crece, se suma 1s
    tiempo_memorizacion = 5000 + segundos_extra

    root.after(tiempo_memorizacion, mostrar_matriz_vacia)


def mostrar_matriz_vacia():
    """Vaciar la matriz y habilitar botones para jugar."""
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            botones[i][j].config(bg="white", text="", state="normal")


# def mostrar_matriz_x():
#     """Mostrar las X al inicio para memorizar."""
#     for i in range(len(matriz)):
#         for j in range(len(matriz)):
#             if matriz[i][j]:
#                 botones[i][j].config(bg="red")
#             else:
#                 botones[i][j].config(bg="white")
#     # Después de 5 segundos, vaciar la matriz
#     root.after(5000, mostrar_matriz_vacia)

# def mostrar_matriz_vacia():
#     """Vaciar la matriz y habilitar botones para jugar."""
#     for i in range(len(matriz)):
#         for j in range(len(matriz)):
#             botones[i][j].config(bg="SystemButtonFace", state="normal")




# def boton_click(fila, columna):
#     """Acción al presionar un botón."""
#     global vidas, num_x
#     if matriz[fila][columna]:
#         botones[fila][columna].config(bg="green", text="✓", state="disabled")
#         matriz[fila][columna] = False
#         num_x -= 1
#     else:
#         botones[fila][columna].config(bg="red", text="X", state="disabled")
#         vidas -= 1
#         vida_label.config(text=f"Vidas: {vidas}")

#     if vidas == 0:
#         messagebox.showinfo("Fin del juego", "Te quedaste sin vidas. Fin del juego.")
#         root.destroy()
#     elif num_x == 0:
#         messagebox.showinfo("Nivel completado", "¡Felicidades! Pasaste el nivel.")
#         siguiente_nivel()

def boton_click(fila, columna):
    """Acción al presionar un botón."""
    global vidas, num_x
    if matriz[fila][columna]:
        botones[fila][columna].config(bg="green", text="✓", state="disabled")
        matriz[fila][columna] = False
        num_x -= 1
    else:
        botones[fila][columna].config(bg="red", text="X", state="disabled")
        vidas -= 1
        vida_label.config(text=f"Vidas: {vidas}")

    # Comprobar fin de juego
    if vidas == 0:
        messagebox.showinfo("Fin del juego", "Te quedaste sin vidas. Fin del juego.")
        root.destroy()
    # Comprobar si ya se descubrieron todas las X
    elif num_x == 0:
        messagebox.showinfo("Nivel completado", "¡Felicidades! Pasaste el nivel.")
        siguiente_nivel()  # <-- Esto hace que avance




def siguiente_nivel():
    """Avanzar al siguiente nivel."""
    global nivel, matriz, botones, num_x
    nivel += 1
    nivel_label.config(text=f"Nivel: {nivel}")
    # Destruir botones viejos
    for fila in botones:
        for b in fila:
            b.destroy()
    crear_matriz(nivel)

def crear_matriz(level):
    """Crear la matriz de botones para el nivel actual."""
    global matriz, botones, num_x, vidas
    matriz = generar_matriz(level)
    dim = len(matriz)
    botones = []

    for i in range(dim):
        fila_botones = []
        for j in range(dim):
            b = tk.Button(frame_matriz, width=4, height=2,
                        command=lambda i=i, j=j: boton_click(i, j),
                        state="disabled")  # Deshabilitados hasta mostrar X
            b.grid(row=i, column=j, padx=5, pady=5)
            fila_botones.append(b)
        botones.append(fila_botones)

    num_x = sum(sum(1 for val in row if val) for row in matriz)
    vidas = 3
    vida_label.config(text=f"Vidas: {vidas}")
    mostrar_matriz_x()  # Mostrar X al inicio

# ---------------- Interfaz gráfica ---------------- #

root = tk.Tk()
root.title("Color Search")

# Instrucciones 
instrucciones_label = tk.Label(
    root,
    text="Recuerda las casillas que contengan una X." 
        "\nTienes 5 segundos para memorizarlas antes de que desaparezcan.",
    font=("Arial", 12),
    wraplength=400,       # Ajusta el ancho 
    justify="center",
    fg="blue"
)

instrucciones_label.pack(pady=10)

nivel = 1
vidas = 3
num_x = 0
matriz = []
botones = []

# Labels
nivel_label = tk.Label(root, text=f"Nivel: {nivel}", font=("Arial", 14))
nivel_label.pack(pady=5)

vida_label = tk.Label(root, text=f"Vidas: {vidas}", font=("Arial", 14))
vida_label.pack(pady=5)

# Frame para la matriz
frame_matriz = tk.Frame(root)
frame_matriz.pack(pady=10)

# Crear primera matriz
crear_matriz(nivel)

root.mainloop()
