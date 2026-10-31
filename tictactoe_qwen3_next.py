import tkinter as tk
from tkinter import messagebox


class TicTacToeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")

        # Game state
        self.board = [""] * 9
        self.current_player = "X"
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.game_over = False

        # UI setup
        self._setup_ui()

    def _setup_ui(self):
        # Title label
        title_label = tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=("Segoe UI", 24, "bold"),
            bg="#ffffff",
            fg="#333333",
            pady=12
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="n")

        # Score frame
        score_frame = tk.Frame(self.root, bg="#ffffff")
        score_frame.grid(row=1, column=0, columnspan=3, pady=(8, 16))

        score_font = ("Segoe UI", 13, "bold")

        self.score_x = tk.Label(score_frame, text="X: 0", font=score_font, fg="#0066cc", bg="#ffffff", padx=15)
        self.score_o = tk.Label(score_frame, text="O: 0", font=score_font, fg="#cc0000", bg="#ffffff", padx=15)
        self.score_draw = tk.Label(score_frame, text="Draws: 0", font=score_font, fg="#666666", bg="#ffffff", padx=15)

        self.score_x.grid(row=0, column=0)
        self.score_o.grid(row=0, column=1)
        self.score_draw.grid(row=0, column=2)

        # Game grid
        grid_frame = tk.Frame(self.root, bg="#e0e0e0", padx=15, pady=15)
        grid_frame.grid(row=2, column=0, columnspan=3)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                grid_frame,
                text="",
                font=("Segoe UI", 36, "bold"),
                width=5,
                height=2,
                bg="#ffffff",
                fg="#333333",           # Dark neutral for unplayed cells
                activebackground="#f0f0f0",
                activeforeground="#333333",
                bd=1,
                relief="solid",
                highlightthickness=0,
                command=lambda idx=i: self._handle_click(idx)
            )
            # Add spacing between buttons for clarity
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=6)
            self.buttons.append(btn)

        # Status bar
        self.status_var = tk.StringVar(value="Player X's turn")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 14),
            bg="#ffffff",
            fg="#444444",
            pady=10
        )
        status_label.grid(row=3, column=0, columnspan=3)

        # Control buttons
        control_frame = tk.Frame(self.root, bg="#ffffff")
        control_frame.grid(row=4, column=0, columnspan=3, pady=15)

        btn_font = ("Segoe UI", 12, "bold")

        reset_button = tk.Button(
            control_frame,
            text="Restart Game",
            font=btn_font,
            bg="#0066cc",
            fg="white",
            padx=18,
            pady=7,
            bd=0,
            activebackground="#0052a3",
            activeforeground="white",
            command=self._reset_game
        )
        reset_button.grid(row=0, column=0, padx=12)

        quit_button = tk.Button(
            control_frame,
            text="Quit",
            font=btn_font,
            bg="#cc0000",
            fg="white",
            padx=22,
            pady=7,
            bd=0,
            activebackground="#990000",
            activeforeground="white",
            command=self._quit_game
        )
        quit_button.grid(row=0, column=1, padx=12)

    def _handle_click(self, index):
        if self.game_over or self.board[index]:
            return

        # Update board and UI
        self.board[index] = self.current_player
        color = "#0066cc" if self.current_player == "X" else "#cc0000"
        self.buttons[index].config(
            text=self.current_player,
            fg=color,
            bg="#f8f8f8"
        )

        # Check win/draw
        if self._check_winner():
            self._end_game(f"Player {self.current_player} wins!")
            return

        if "" not in self.board:
            self._end_game("Draw!")
            return

        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_var.set(f"Player {self.current_player}'s turn")

    def _check_winner(self):
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        return any(
            all(self.board[i] == self.current_player for i in combo)
            for combo in win_combos
        )

    def _update_score(self, result):
        if "X" in result and "wins" in result:
            self.scores["X"] += 1
        elif "O" in result and "wins" in result:
            self.scores["O"] += 1
        else:
            self.scores["Draws"] += 1
        self._update_score_labels()

    def _update_score_labels(self):
        self.score_x.config(text=f"X: {self.scores['X']}")
        self.score_o.config(text=f"O: {self.scores['O']}")
        self.score_draw.config(text=f"Draws: {self.scores['Draws']}")

    def _end_game(self, message):
        self.game_over = True
        self.status_var.set(message)
        self._update_score(message)
        self.root.after(750, lambda: messagebox.showinfo("Game Over", message))

    def _reset_game(self):
        if not self.game_over:
            if not messagebox.askyesno("Restart", "Reset the game and scores?"):
                return
        self._reset_board()
        # Clear scores if forced reset
        if not self.game_over:
            self.scores = {"X": 0, "O": 0, "Draws": 0}
            self._update_score_labels()

    def _reset_board(self):
        self.board = [""] * 9
        self.game_over = False
        self.current_player = "X"
        self.status_var.set("Player X's turn")
        for btn in self.buttons:
            btn.config(text="", fg="#333333", bg="#ffffff")

    def _quit_game(self):
        if messagebox.askyesno("Quit", "Exit Tic-Tac-Toe?"):
            self.root.destroy()


if __name__ == "__main__":
    app = TicTacToeApp()
    app.root.mainloop()

