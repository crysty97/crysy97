import tkinter as tk
from tkinter import messagebox
import random
import copy

class SudokuGame:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = "Fácil"
        self.score = 0
        self.mistakes = 0
        self.max_mistakes = 3
        
    def generate_board(self):
        # Generar un tablero completo válido
        self.fill_board(self.solution)
        self.board = copy.deepcopy(self.solution)
        
        # Eliminar celdas según dificultad
        if self.difficulty == "Fácil":
            cells_to_remove = 35
        elif self.difficulty == "Medio":
            cells_to_remove = 45
        else:  # Difícil
            cells_to_remove = 55
            
        removed = 0
        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1
                
    def fill_board(self, board):
        # Llenar el tablero con backtracking
        numbers = list(range(1, 10))
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.fill_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    def is_valid(self, board, row, col, num):
        # Verificar fila
        for j in range(9):
            if board[row][j] == num:
                return False
                
        # Verificar columna
        for i in range(9):
            if board[i][col] == num:
                return False
                
        # Verificar caja 3x3
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
                    
        return True
    
    def check_win(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Multiplataforma")
        self.game = SudokuGame()
        self.cells = {}
        self.selected_cell = None
        
        # Configuración de la ventana
        self.master.geometry("600x700")
        self.master.resizable(False, False)
        
        # Frame principal
        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel superior
        self.top_panel = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.top_panel.pack(fill=tk.X, pady=10)
        
        # Selector de dificultad
        tk.Label(self.top_panel, text="Dificultad:", bg="#f0f0f0", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.difficulty_var = tk.StringVar(value="Fácil")
        difficulty_menu = tk.OptionMenu(
            self.top_panel, 
            self.difficulty_var, 
            "Fácil", "Medio", "Difícil",
            command=self.change_difficulty
        )
        difficulty_menu.config(font=("Arial", 10))
        difficulty_menu.pack(side=tk.LEFT, padx=5)
        
        # Botón nuevo juego
        self.new_game_btn = tk.Button(
            self.top_panel, 
            text="Nuevo Juego", 
            command=self.new_game,
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 12),
            padx=10
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=20)
        
        # Panel de información
        self.info_panel = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.info_panel.pack(fill=tk.X, pady=5)
        
        self.score_label = tk.Label(
            self.info_panel, 
            text="Puntuación: 0", 
            bg="#f0f0f0", 
            font=("Arial", 12)
        )
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.mistakes_label = tk.Label(
            self.info_panel, 
            text="Errores: 0/3", 
            bg="#f0f0f0", 
            font=("Arial", 12)
        )
        self.mistakes_label.pack(side=tk.LEFT, padx=10)
        
        # Panel del tablero
        self.board_frame = tk.Frame(self.main_frame, bg="black")
        self.board_frame.pack(pady=20)
        
        # Crear celdas del tablero
        for i in range(9):
            for j in range(9):
                # Determinar el color de fondo según la región
                bg_color = "#ffffff"
                if (i // 3 + j // 3) % 2 == 0:
                    bg_color = "#e0e0e0"
                
                # Frame para cada celda con borde
                cell_frame = tk.Frame(
                    self.board_frame, 
                    bg="black", 
                    highlightthickness=0
                )
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                
                # Crear la celda
                cell = tk.Label(
                    cell_frame,
                    text="",
                    bg=bg_color,
                    font=("Arial", 20),
                    width=2,
                    height=1,
                    relief=tk.FLAT,
                    highlightthickness=0
                )
                cell.pack()
                
                # Eventos de ratón
                cell.bind("<Button-1>", lambda e, row=i, col=j: self.cell_clicked(row, col))
                
                self.cells[(i, j)] = cell
        
        # Panel de control numérico
        self.control_panel = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.control_panel.pack(pady=10)
        
        # Botones numéricos
        for num in range(1, 10):
            btn = tk.Button(
                self.control_panel,
                text=str(num),
                font=("Arial", 16),
                width=3,
                height=1,
                command=lambda n=num: self.number_clicked(n),
                bg="#2196F3",
                fg="white"
            )
            btn.grid(row=0, column=num-1, padx=2)
        
        # Botón borrar
        self.delete_btn = tk.Button(
            self.control_panel,
            text="Borrar",
            font=("Arial", 16),
            width=8,
            height=1,
            command=self.delete_number,
            bg="#f44336",
            fg="white"
        )
        self.delete_btn.grid(row=1, column=3, columnspan=3, pady=5)
        
        # Iniciar nuevo juego
        self.new_game()
    
    def new_game(self):
        # Reiniciar juego
        self.game = SudokuGame()
        self.game.difficulty = self.difficulty_var.get()
        self.game.generate_board()
        self.selected_cell = None
        
        # Actualizar interfaz
        self.update_board()
        self.update_info()
    
    def change_difficulty(self, difficulty):
        self.game.difficulty = difficulty
        self.new_game()
    
    def cell_clicked(self, row, col):
        # Solo permitir editar celdas vacías
        if self.game.board[row][col] == 0:
            # Resaltar celda seleccionada
            if self.selected_cell:
                prev_row, prev_col = self.selected_cell
                self.cells[(prev_row, prev_col)].config(bg="#e0e0e0" if (prev_row // 3 + prev_col // 3) % 2 == 0 else "#ffffff")
            
            self.selected_cell = (row, col)
            self.cells[(row, col)].config(bg="#bbdefb")
    
    def number_clicked(self, num):
        if self.selected_cell:
            row, col = self.selected_cell
            
            # Verificar si el número es válido
            if self.game.is_valid(self.game.board, row, col, num):
                self.game.board[row][col] = num
                self.cells[(row, col)].config(
                    text=str(num),
                    fg="#0000ff",
                    font=("Arial", 20, "bold")
                )
                
                # Actualizar puntuación
                self.game.score += 10 * ({"Fácil": 1, "Medio": 2, "Difícil": 3}[self.game.difficulty])
                self.update_info()
                
                # Verificar victoria
                if self.game.check_win():
                    self.game_over(True)
            else:
                # Incrementar errores
                self.game.mistakes += 1
                self.update_info()
                
                # Mostrar error visual
                self.cells[(row, col)].config(bg="#ffcdd2")
                self.master.after(500, lambda: self.cells[(row, col)].config(
                    bg="#e0e0e0" if (row // 3 + col // 3) % 2 == 0 else "#ffffff"
                ))
                
                # Verificar si se acabaron los intentos
                if self.game.mistakes >= self.game.max_mistakes:
                    self.game_over(False)
    
    def delete_number(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.game.board[row][col] != 0:
                self.game.board[row][col] = 0
                self.cells[(row, col)].config(text="")
    
    def update_board(self):
        for i in range(9):
            for j in range(9):
                value = self.game.board[i][j]
                if value != 0:
                    # Determinar si es un número inicial o ingresado
                    if self.game.solution[i][j] == value:
                        # Número inicial (no editable)
                        self.cells[(i, j)].config(
                            text=str(value),
                            fg="#000000",
                            font=("Arial", 20, "bold")
                        )
                    else:
                        # Número ingresado por el jugador
                        self.cells[(i, j)].config(
                            text=str(value),
                            fg="#0000ff",
                            font=("Arial", 20, "bold")
                        )
                else:
                    self.cells[(i, j)].config(text="")
    
    def update_info(self):
        self.score_label.config(text=f"Puntuación: {self.game.score}")
        self.mistakes_label.config(text=f"Errores: {self.game.mistakes}/{self.game.max_mistakes}")
    
    def game_over(self, won):
        if won:
            messagebox.showinfo(
                "¡Felicidades!", 
                f"Has completado el Sudoku {self.game.difficulty}!\n\n"
                f"Puntuación final: {self.game.score}\n"
                f"Errores cometidos: {self.game.mistakes}"
            )
        else:
            messagebox.showinfo(
                "Juego Terminado", 
                "Has cometido demasiados errores.\n\n"
                "Inténtalo de nuevo con un nuevo juego."
            )
        
        self.new_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGUI(root)
    root.mainloop()