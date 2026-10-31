import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Constants
WINDOW_SIZE = 400
GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
LINE_WIDTH = 5
SCORE_FILE = "scores.txt"

# Colors
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (220, 220, 220)

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Game variables
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = "X"
game_over = False
winner = None

# Score variables
scores = {"X": 0, "O": 0, "Draw": 0}

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
    
    def draw(self):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, LINE_COLOR, self.rect, 2)
        
        text_surf = small_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

def load_scores():
    """Load scores from file"""
    global scores
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r') as f:
                content = f.read().strip()
                if content:
                    parts = content.split(',')
                    scores["X"] = int(parts[0])
                    scores["O"] = int(parts[1])
                    scores["Draw"] = int(parts[2])
        except:
            pass

def save_scores():
    """Save scores to file"""
    try:
        with open(SCORE_FILE, 'w') as f:
            f.write(f"{scores['X']},{scores['O']},{scores['Draw']}")
    except:
        pass

def draw_board():
    """Draw the game board"""
    screen.fill(BACKGROUND_COLOR)
    
    # Draw grid lines
    for i in range(1, GRID_SIZE):
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, 
                        (i * CELL_SIZE, 0), 
                        (i * CELL_SIZE, WINDOW_SIZE), 
                        LINE_WIDTH)
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, 
                        (0, i * CELL_SIZE), 
                        (WINDOW_SIZE, i * CELL_SIZE), 
                        LINE_WIDTH)
    
    # Draw X and O marks
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == "X":
                # Draw X
                pygame.draw.line(screen, X_COLOR, 
                                (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                                ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20),
                                LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR,
                                ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20),
                                (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20),
                                LINE_WIDTH)
            elif board[row][col] == "O":
                # Draw O
                pygame.draw.circle(screen, O_COLOR,
                                 (col * CELL_SIZE + CELL_SIZE // 2, 
                                  row * CELL_SIZE + CELL_SIZE // 2),
                                 CELL_SIZE // 2 - 20,
                                 LINE_WIDTH)
    
    # Draw score and status
    score_text = font.render(f"X: {scores['X']}  O: {scores['O']}  Draw: {scores['Draw']}", True, TEXT_COLOR)
    screen.blit(score_text, (10, WINDOW_SIZE + 10))
    
    if game_over:
        if winner:
            status_text = font.render(f"Player {winner} wins!", True, TEXT_COLOR)
        else:
            status_text = font.render("Game ended in draw", True, TEXT_COLOR)
        screen.blit(status_text, (10, WINDOW_SIZE + 50))
    else:
        status_text = font.render(f"Player {current_player}'s turn", True, TEXT_COLOR)
        screen.blit(status_text, (10, WINDOW_SIZE + 50))

def check_winner():
    """Check if there is a winner"""
    # Check rows
    for row in range(GRID_SIZE):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    
    # Check columns
    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    # Check for draw
    if all(board[row][col] is not None for row in range(GRID_SIZE) for col in range(GRID_SIZE)):
        return "Draw"
    
    return None

def reset_game():
    """Reset the game board"""
    global board, current_player, game_over, winner
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"
    game_over = False
    winner = None

def main():
    """Main game loop"""
    global current_player, game_over, winner
    
    # Load scores
    load_scores()
    
    # Create buttons
    restart_button = Button(WINDOW_SIZE - 150, WINDOW_SIZE + 20, 130, 40, "Restart")
    quit_button = Button(WINDOW_SIZE - 150, WINDOW_SIZE + 70, 130, 40, "Quit")
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_scores()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                
                # Check if click is within board
                if 0 <= x < WINDOW_SIZE and 0 <= y < WINDOW_SIZE:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    
                    # Place mark if cell is empty
                    if board[row][col] is None:
                        board[row][col] = current_player
                        
                        # Check for winner
                        winner = check_winner()
                        if winner:
                            game_over = True
                            scores[winner] += 1
                        else:
                            # Switch player
                            current_player = "O" if current_player == "X" else "X"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check button clicks
                if restart_button.check_click(mouse_pos):
                    reset_game()
                elif quit_button.check_click(mouse_pos):
                    save_scores()
                    pygame.quit()
                    sys.exit()
        
        # Update button hover states
        restart_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        # Draw everything
        draw_board()
        restart_button.draw()
        quit_button.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()


