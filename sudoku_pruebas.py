import random

# Definición del tablero de Sudoku (0 = celda vacía)
tablero_sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def imprimir_tablero(tablero):
    """Imprime el tablero con formato de Sudoku."""
    for i in range(len(tablero)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        
        for j in range(len(tablero[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(tablero[i][j])
            else:
                print(str(tablero[i][j]) + " ", end="")

def encontrar_celda_vacia(tablero):
    """Encuentra la siguiente celda vacía (representada por 0)."""
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                return fila, col  # Retorna (fila, columna)
    return None, None # Si no hay celdas vacías, retorna None

def es_valido(tablero, num, fila, col):
    """Verifica si el número 'num' es válido en la posición (fila, col)."""
    
    # 1. Comprobar la fila
    if num in tablero[fila]:
        return False

    # 2. Comprobar la columna
    for i in range(9):
        if tablero[i][col] == num:
            return False

    # 3. Comprobar el sub-cuadrante 3x3
    inicio_fila = (fila // 3) * 3
    inicio_col = (col // 3) * 3
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            if tablero[i][j] == num:
                return False
    
    return True

def resolver_sudoku(tablero):
    """
    Función principal para resolver el Sudoku usando Backtracking.
    Retorna True si encuentra solución, False en caso contrario.
    """
    fila, col = encontrar_celda_vacia(tablero)

    # Caso base: Si no hay celdas vacías, el Sudoku está resuelto.
    if fila is None:
        return True

    # Intenta números del 1 al 9
    for num in range(1, 10):
        if es_valido(tablero, num, fila, col):
            # 1. Coloca el número
            tablero[fila][col] = num

            # 2. Llama a la función recursivamente (Backtracking)
            if resolver_sudoku(tablero):
                return True
            
            # 3. Si la recursión no encontró solución,
            #    restablece la celda a 0 (backtrack)
            tablero[fila][col] = 0

    # Si probamos todos los números y ninguno funcionó
    return False

# --- Ejecución del juego ---
print("--- Tablero Inicial ---")
imprimir_tablero(tablero_sudoku)

if resolver_sudoku(tablero_sudoku):
    print("\n--- Solución Encontrada ---")
    imprimir_tablero(tablero_sudoku)
else:
    print("\nNo se pudo encontrar una solución para el Sudoku.")
