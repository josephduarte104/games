import json
import os
import tkinter as tk
from tkinter import messagebox

SCORE_FILE = os.path.join(os.path.expanduser("~"), "tic_tac_toe_scores.json")

BG = "#111827"
PANEL = "#1F2937"
BORDER = "#374151"
TEXT = "#F9FAFB"
SUBTEXT = "#D1D5DB"
X_COLOR = "#60A5FA"
O_COLOR = "#F472B6"
WIN_BG = "#14532D"
BUTTON_BG = "#374151"
BUTTON_HOVER = "#4B5563"
DANGER_BG = "#7F1D1D"
DANGER_HOVER = "#991B1B"


class TicTacToeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.board = [""] * 9
        self.turn = "X"
        self.first_player = "X"
        self.winning_cells = None
        self.scores = self.load_scores()

        header = tk.Label(
            self.root,
            text="TIC TAC TOE",
            bg=BG,
            fg=TEXT,
            font=("Arial", 26, "bold"),
        )
        header.grid(row=0, column=0, columnspan=3, pady=(16, 8))

        self.message = tk.Label(
            self.root,
            text=f"{self.turn} plays.",
            bg=BG,
            fg=SUBTEXT,
            font=("Arial", 14, "bold"),
        )
        self.message.grid(row=1, column=0, columnspan=3, pady=4)

        board_frame = tk.Frame(self.root, bg=BG)
        board_frame.grid(row=2, column=0, columnspan=3, pady=12)

        self.cells = []
        for i in range(9):
            row, col = divmod(i, 3)
            cell = tk.Label(
                board_frame,
                text="",
                bg=PANEL,
                fg=TEXT,
                font=("Arial", 40, "bold"),
                width=6,
                height=2,
                highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor=BORDER,
                cursor="hand2",
            )
            cell.grid(row=row, column=col, padx=5, pady=5)
            cell.bind("<Button-1>", lambda event, index=i: self.play(index))
            self.cells.append(cell)

        score_frame = tk.Frame(self.root, bg=BG)
        score_frame.grid(row=3, column=0, columnspan=3, pady=8)

        self.x_label = tk.Label(
            score_frame,
            text="X Wins: 0",
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 12, "bold"),
            width=14,
            padx=8,
            pady=6,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        self.x_label.grid(row=0, column=0, padx=4)

        self.draw_label = tk.Label(
            score_frame,
            text="Draws: 0",
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 12, "bold"),
            width=14,
            padx=8,
            pady=6,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        self.draw_label.grid(row=0, column=1, padx=4)

        self.o_label = tk.Label(
            score_frame,
            text="O Wins: 0",
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 12, "bold"),
            width=14,
            padx=8,
            pady=6,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        self.o_label.grid(row=0, column=2, padx=4)

        controls = tk.Frame(self.root, bg=BG)
        controls.grid(row=4, column=0, columnspan=3, pady=(8, 16))

        new_button = self.make_button(controls, "New Game", self.new_game, BUTTON_BG, BUTTON_HOVER)
        new_button.grid(row=0, column=0, padx=4)

        reset_button = self.make_button(controls, "Reset Scores", self.reset_scores, BUTTON_BG, BUTTON_HOVER)
        reset_button.grid(row=0, column=1, padx=4)

        quit_button = self.make_button(controls, "Quit", self.quit_app, DANGER_BG, DANGER_HOVER)
        quit_button.grid(row=0, column=2, padx=4)

        self.root.bind("<n>", lambda e: self.new_game())
        self.root.bind("<N>", lambda e: self.new_game())
        self.root.bind("<r>", lambda e: self.new_game())
        self.root.bind("<R>", lambda e: self.new_game())

        self.update_scores()
        self.center_window()
        self.root.mainloop()

    def make_button(self, parent, text, command, bg, hover_bg):
        button = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=TEXT,
            font=("Arial", 11, "bold"),
            padx=14,
            pady=10,
            cursor="hand2",
            highlightthickness=0,
        )
        button.bind("<Button-1>", lambda e: command())
        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=bg))
        return button

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_scores(self):
        defaults = {"x_wins": 0, "draws": 0, "o_wins": 0}
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                "x_wins": int(data.get("x_wins", 0)),
                "draws": int(data.get("draws", 0)),
                "o_wins": int(data.get("o_wins", 0)),
            }
        except (OSError, ValueError, json.JSONDecodeError):
            return defaults

    def save_scores(self):
        try:
            with open(SCORE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.scores, f)
        except OSError:
            pass

    def update_scores(self):
        self.x_label.config(text=f"X Wins: {self.scores['x_wins']}")
        self.draw_label.config(text=f"Draws: {self.scores['draws']}")
        self.o_label.config(text=f"O Wins: {self.scores['o_wins']}")

    def play(self, index):
        if self.is_game_over():
            self.new_game()
            return

        if self.board[index]:
            return

        self.board[index] = self.turn
        color = X_COLOR if self.turn == "X" else O_COLOR
        self.cells[index].config(text=self.turn, fg=color)

        win = self.find_win()

        if win:
            self.winning_cells = win
            self.message.config(text=f"{self.turn} wins. Click the board or New Game.")
            for i in win:
                self.cells[i].config(bg=WIN_BG)

            if self.turn == "X":
                self.scores["x_wins"] += 1
            else:
                self.scores["o_wins"] += 1

            self.first_player = "O" if self.first_player == "X" else "X"
            self.save_scores()

        elif self.is_full():
            self.message.config(text="Draw. Click the board or New Game.")
            self.scores["draws"] += 1
            self.first_player = "O" if self.first_player == "X" else "X"
            self.save_scores()

        else:
            self.turn = "O" if self.turn == "X" else "X"
            self.message.config(text=f"{self.turn} plays.")

        self.update_scores()

    def is_full(self):
        return all(cell != "" for cell in self.board)

    def is_game_over(self):
        return self.winning_cells is not None or self.is_full()

    def find_win(self):
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        for a, b, c in lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return (a, b, c)

        return None

    def new_game(self):
        in_progress = any(self.board) and not self.is_game_over()

        if in_progress:
            if not messagebox.askyesno("New Game", "Start a new game? The current game will be lost."):
                return

        for cell in self.cells:
            cell.config(text="", fg=TEXT, bg=PANEL)

        self.board = [""] * 9
        self.winning_cells = None
        self.turn = self.first_player
        self.message.config(text=f"{self.turn} plays.")

    def reset_scores(self):
        if messagebox.askyesno("Reset Scores", "Reset all scores?"):
            self.scores = {"x_wins": 0, "draws": 0, "o_wins": 0}
            self.save_scores()
            self.update_scores()

    def quit_app(self):
        self.save_scores()
        self.root.destroy()


if __name__ == "__main__":
    TicTacToeApp()
