import random
import time
from IPython.display import clear_output
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()


def generar_matriz(level):
    """
    Generar una matriz cuadrada, posteriormente llenar la matriz con valores True
    o False para representar si hay o no X.
    Cada 3 niveles el tamaño de la matriz aumenta, ej 1-3 2x2, 4-6 3x3, etc.
    """
    rates = {0: 33, 1: 66, 2: 50}  # Probabilidades para cada nivel usando su modulo
    x_threshold = rates[level % 3]
    dim_matriz = 2 + ((level - 1) // 3)

    possible = [False, False]  # Verificar que haya False y True en la Matriz
    while False in possible:
        matriz = []  # Declarar matriz vacía
        for dim in range(dim_matriz):
            matriz.append([])
        possible = [False, False]
        for row in matriz:
            for _ in range(dim_matriz):
                prob = random.random()
                if prob * 100 >= x_threshold:
                    row.append(True)
                    possible[1] = True
                else:
                    row.append(False)
                    possible[0] = True
    return matriz

def print_matriz(matriz):
    """
    Dada una matriz cuadrada de T y F, imprimirla, representando T con x, y
    F como un punto vacío.
    """
    for row in matriz:
        for column in row:
            print("[x]" if column else "[ ]", end=" ")
        print("")

def get_x(matriz):
    """
    Ver cuantos espacios de una matriz tienen x
    """
    suma = 0
    for row in matriz:
        for column in row:
            suma += 1 if column else 0
    return suma

def matriz_vacia(matriz):
    # Vaciar la terminal
    # Imprimir una matriz cuadrada, con [ ] por cada espacio de la matriz
    # Devolver una matriz cuadrada con [ ] en todos los espacios.
    mat = []
    for fila in matriz:
        mat.append([])

    for fila in mat:
        for columna in range(len(mat)):
            fila.append("\033[36m[ ]\033[39m")
    clear_screen()


    time.sleep(0.1)
    for row in matriz:
        for column in row:
            print("\033[36m[ ]\033[39m", end=" ")
        print("")
    return mat

def pregame(nivel):
    mat = generar_matriz(nivel)
    print_matriz(mat)
    minas = get_x(mat)
    time.sleep(5)
    mat_vacia = matriz_vacia(mat)
    return mat, minas, mat_vacia

def get_fila_columna(tamaño: int, inputs_usados: list) -> tuple:
    fila, columna = -1, -1
    while True:
        while not 0 <= fila < tamaño:
            try:
                fila = int(input(f"Escriba la fila (1 a {tamaño}): ")) - 1
            except:
                print("Ingrese un número válido")
        while not 0 <= columna < tamaño:
            try:
                columna = int(input(f"Escriba la columna (1 a {tamaño}): ")) - 1
            except:
                print("Ingrese un número válido")
        inputs = (fila, columna)
        if inputs in inputs_usados:
            print("Celda ya usada, ingrese otra celda.")
            fila, columna = -1, -1
        else:
            inputs_usados.append(inputs)
            break
    return inputs

def matriz_inputs(mat_vacia: list, fila, columna, result: bool):
    if result:
        mat_vacia[fila][columna] = "\033[32m[✓]\033[39m"
    else:
        mat_vacia[fila][columna] = "\033[31m[X]\033[39m"
    clear_screen()


    for row in mat_vacia:
        for column in row:
            print(column, end=" ")
        print("")

def game(matriz, vidas, num_x, mat_vacia):
    inputs_usados = []
    while num_x > 0:
        fila, columna = get_fila_columna(len(matriz), inputs_usados)
        if matriz[fila][columna]:
            matriz[fila][columna] = False
            num_x -= 1
            matriz_inputs(mat_vacia, fila, columna, True)
        else:
            vidas -= 1
            matriz_inputs(mat_vacia, fila, columna, False)
            if vidas == 0:
                return False, 0
            else:
                print("Incorrecto, le quedan 2 vidas." if vidas == 2 else "Incorrecto, le queda 1 vida.")
    return True, vidas

def postgame(nivel):
    print(f"Felicidades, paso el nivel {nivel - 1}")
    time.sleep(0.1)
    print("Presione Enter para iniciar el siguiente nivel.")
    print("")
    input(">")

def main():
    vidas = 3
    nivel = 1
    print("Recuerde las casillas que contengan una x.")
    print("Presione Enter para comenzar.")
    input(">")
    while vidas > 0:
        nivel += 1  # Empezar en el nivel 2, para que las partes iniciales sean un poco menos tediosas
        matriz, num_x, mat_vacia = pregame(nivel)
        continuar, vidas = game(matriz, vidas, num_x, mat_vacia)
        if not continuar:
            print("Fin del juego.")
            print(f"Su puntuación es: {nivel*1000 + random.randint(1,750)}." if nivel > 2
                else "Su puntuación es: 0")
            break
        else:
            print()
            postgame(nivel)

main()
