#importing Packages from tkinter
from tkinter import *
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tic Tac Toe")
        self.root.resizable(0,0)
        
        # Game variables
        self.Player1 = 'X'
        self.Player2 = 'O'
        self.current_player = self.Player1
        self.stop_game = False
        self.scores = {'X': 0, 'O': 0, 'Ties': 0}
        self.game_count = 0
        
        # Create GUI
        self.create_widgets()
        self.reset_game()
        
    def create_widgets(self):
        # Score display
        self.score_frame = Frame(self.root)
        self.score_frame.pack(pady=10)
        
        self.score_label = Label(self.score_frame, text="Score: X: 0  O: 0  Ties: 0", font=("Helvetica", 12))
        self.score_label.pack()
        
        # Game board
        self.board_frame = Frame(self.root)
        self.board_frame.pack()
        
        # Create 3x3 grid of buttons with larger clickable areas
        self.b = [[0 for _ in range(3)] for _ in range(3)]
        self.states = [[0 for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                # Create button with larger height and width
                self.b[i][j] = Button(
                    self.board_frame,
                    height=6,  # Increased height
                    width=12,  # Increased width
                    font=("Helvetica", 24),  # Larger font
                    command=lambda r=i, c=j: self.clicked(r, c),
                    # Add padding to increase clickable area
                    padx=20,
                    pady=20
                )
                self.b[i][j].grid(row=i, column=j, padx=2, pady=2)
        
        # Game status
        self.status_label = Label(self.root, text="Player X's turn", font=("Helvetica", 12))
        self.status_label.pack(pady=5)
        
        # Control buttons
        self.control_frame = Frame(self.root)
        self.control_frame.pack(pady=10)
        
        self.restart_button = Button(self.control_frame, text="Restart Game", command=self.reset_game, font=("Helvetica", 10))
        self.restart_button.pack(side=LEFT, padx=5)
        
        self.quit_button = Button(self.control_frame, text="Quit", command=self.root.quit, font=("Helvetica", 10))
        self.quit_button.pack(side=LEFT, padx=5)
        
    def clicked(self, r, c):
        if self.states[r][c] == 0 and not self.stop_game:
            self.b[r][c].configure(text=self.current_player)
            self.states[r][c] = self.current_player
            
            if self.check_winner():
                self.stop_game = True
                self.scores[self.current_player] += 1
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.update_score()
                self.game_count += 1
                self.root.after(1000, self.reset_game)
            elif self.is_board_full():
                self.stop_game = True
                self.scores['Ties'] += 1
                messagebox.showinfo("Game Over", "Game ends in a tie!")
                self.update_score()
                self.game_count += 1
                self.root.after(1000, self.reset_game)
            else:
                # Switch player
                self.current_player = self.Player2 if self.current_player == self.Player1 else self.Player1
                self.update_status()
                
    def check_winner(self):
        # Check rows
        for i in range(3):
            if self.states[i][0] == self.states[i][1] == self.states[i][2] != 0:
                return True
                
        # Check columns
        for j in range(3):
            if self.states[0][j] == self.states[1][j] == self.states[2][j] != 0:
                return True
                
        # Check diagonals
        if self.states[0][0] == self.states[1][1] == self.states[2][2] != 0:
            return True
            
        if self.states[0][2] == self.states[1][1] == self.states[2][0] != 0:
            return True
            
        return False
        
    def is_board_full(self):
        for i in range(3):
            for j in range(3):
                if self.states[i][j] == 0:
                    return False
        return True
        
    def update_status(self):
        self.status_label.config(text=f"Player {self.current_player}'s turn")
        
    def update_score(self):
        self.score_label.config(text=f"Score: X: {self.scores['X']}  O: {self.scores['O']}  Ties: {self.scores['Ties']}")
        
    def reset_game(self):
        # Clear board
        for i in range(3):
            for j in range(3):
                self.b[i][j].configure(text="")
                self.states[i][j] = 0
                
        # Reset game state
        self.current_player = self.Player1
        self.stop_game = False
        self.update_status()
        
    def run(self):
        self.root.mainloop()

# Run the game
if __name__ == "__main__":
    game = TicTacToe()
    game.run()
