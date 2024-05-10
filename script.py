from tkinter import *
import tkinter as tk

import random

class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.board = self.create_board(width, height, num_mines)
        self.game_over = False
        self.width = width
        self.height = height
        self.num_mines = num_mines

    def create_board(self, width, height, num_mines):
        # Create an empty board
        board = [[0 for _ in range(width)] for _ in range(height)] 

        # Place mines randomly
        mines_placed = 0
        while mines_placed < num_mines:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if board[y][x] != -1:  # -1 represents a mine
                board[y][x] = -1
                mines_placed += 1

        # Calculate numbers for non-mine cells
        # ... (implementation here)

        return board

    # ... other functions like reveal_cell, game logic, etc.



class MinesweeperGUI:
    def __init__(self, width, height, num_mines):
        self.game = Minesweeper(width, height, num_mines)
        self.root = tk.Tk()
        self.root.title("Tkinter Minesweeper")

        self.cell_size = 30  # Adjust cell size if needed
        self.load_images() 
        self.create_grid() 

    def load_images(self):
        self.images = {
            "mine": tk.Image.open(file="images/mine.png"),
            "flag": tk.Image(file="images/flag.png"),
            "empty": tk.PhotoImage(file="images/empty.png"),
            "one": tk.PhotoImage(file="images/one.png"),
            "two": tk.PhotoImage(file="images/two.png"),
            "three": tk.PhotoImage(file="images/three.png"),
            "four": tk.PhotoImage(file="images/four.png"),
            "five": tk.PhotoImage(file="images/five.png"),
            "six": tk.PhotoImage(file="images/six.png"),
            "seven": tk.PhotoImage(file="images/seven.png"),
            "eight": tk.PhotoImage(file="images/eight.png"),
            "unrevealed": tk.PhotoImage(file="images/unrevealed_cell.png")       
        }

    def create_grid(self):
        self.cells = {} 
        for y in range(self.game.height):
            for x in range(self.game.width):
                cell = tk.Button(self.root, 
                                 image=self.images["unrevealed"],
                                 width=self.cell_size, height=self.cell_size)
                cell.grid(row=y, column=x)
                self.cells[(x, y)] = cell  # Store buttons in a dictionary

                cell.bind("<Button-1>", lambda event, x=x, y=y: self.reveal_cell(x, y))
                cell.bind("<Button-3>", lambda event, x=x, y=y: self.flag_cell(x, y))

    def reveal_cell(self, x, y):
        cell = self.cells[(x, y)]
        if self.game.game_over:
            return

        if self.game.board[y][x] == -1:  # Mine!
            cell.config(image=self.images["mine"])
            self.game.game_over = True
            # Game over logic
        else:
            number = self.game.board[y][x]
            if number:
                cell.config(image=self.images[str(number)])
            else:
                # Recursive revealing logic (flood fill)
                self.clear_empty_cells(x, y)
            cell.config(state="disabled")  # Disable after a click

    def clear_empty_cells(self, x, y):
        # ... Implementation of recursive flood-fill
        if (0 <= x < self.game.width and  # Check boundaries
        0 <= y < self.game.height and 
        not self.cells[(x, y)]["state"] == "disabled" and  # Not visited
            self.game.board[y][x] == 0):  # Empty cell

            self.cells[(x, y)].config(image=self.images["empty"])  # Update visuals
            self.cells[(x, y)].config(state="disabled")

            # Recursive calls in four directions
            self.clear_empty_cells(x - 1, y)  # Left
            self.clear_empty_cells(x + 1, y)  # Right
            self.clear_empty_cells(x, y - 1)  # Up
            self.clear_empty_cells(x, y + 1)  # Down

    def flag_cell(self, x, y):
        cell = self.cells[(x, y)]
        if cell["image"] == self.images['unrevealed']:
            cell.config(image=self.images["flag"])
        elif cell["image"] == self.images['flag']:
            cell.config(image=self.images["unrevealed"])



if __name__ == "__main__":
    # Example: 10x10 grid with 15 mines
    game = MinesweeperGUI(10, 10, 15)  
    game.root.mainloop()
 

