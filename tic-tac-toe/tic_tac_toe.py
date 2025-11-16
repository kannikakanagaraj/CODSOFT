"""
Tic-Tac-Toe AI Game with Minimax Algorithm
A simple AI that plays perfectly using the Minimax algorithm
"""

# Game Board Representation
# The board is a list of 9 positions (0-8)
# Empty positions are marked with a space ' '
# Player uses 'X' and AI uses 'O'

def create_board():
    """Create an empty tic-tac-toe board"""
    return [' ' for _ in range(9)]


def print_board(board):
    """Display the current board state in a nice format"""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")
    
    # Show position numbers for reference
    print("Position numbers:")
    print(" 0 | 1 | 2 ")
    print("---|---|---")
    print(" 3 | 4 | 5 ")
    print("---|---|---")
    print(" 6 | 7 | 8 ")
    print("\n")


def check_winner(board, player):
    """
    Check if a player has won the game
    Returns True if the player has three in a row
    """
    # All possible winning combinations
    win_patterns = [
        [0, 1, 2],  # Top row
        [3, 4, 5],  # Middle row
        [6, 7, 8],  # Bottom row
        [0, 3, 6],  # Left column
        [1, 4, 7],  # Middle column
        [2, 5, 8],  # Right column
        [0, 4, 8],  # Diagonal top-left to bottom-right
        [2, 4, 6]   # Diagonal top-right to bottom-left
    ]
    
    # Check each winning pattern
    for pattern in win_patterns:
        if (board[pattern[0]] == player and 
            board[pattern[1]] == player and 
            board[pattern[2]] == player):
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely filled"""
    return ' ' not in board


def get_available_moves(board):
    """Get a list of all empty positions on the board"""
    return [i for i in range(9) if board[i] == ' ']


def game_over(board):
    """Check if the game has ended (win or draw)"""
    return check_winner(board, 'X') or check_winner(board, 'O') or is_board_full(board)


# ===== MINIMAX ALGORITHM - THE AI BRAIN =====

def minimax(board, is_maximizing):
    """
    The Minimax Algorithm - This is the AI's decision-making logic
    
    How it works:
    1. It simulates all possible future moves
    2. Assumes both players play optimally
    3. Maximizing player (AI 'O') wants the highest score
    4. Minimizing player (Human 'X') wants the lowest score
    
    Scoring:
    - AI wins: +1 (best for AI)
    - Human wins: -1 (worst for AI)
    - Draw: 0 (neutral)
    """
    
    # Base case: Check if game is over
    if check_winner(board, 'O'):  # AI wins
        return 1
    if check_winner(board, 'X'):  # Human wins
        return -1
    if is_board_full(board):  # Draw
        return 0
    
    # Recursive case: Try all possible moves
    if is_maximizing:
        # AI's turn - wants to maximize the score
        best_score = -float('inf')  # Start with worst possible score
        
        for move in get_available_moves(board):
            board[move] = 'O'  # Try this move
            score = minimax(board, False)  # See what happens next
            board[move] = ' '  # Undo the move
            best_score = max(score, best_score)  # Keep the best score
        
        return best_score
    
    else:
        # Human's turn - wants to minimize the score
        best_score = float('inf')  # Start with worst possible score for minimizer
        
        for move in get_available_moves(board):
            board[move] = 'X'  # Try this move
            score = minimax(board, True)  # See what happens next
            board[move] = ' '  # Undo the move
            best_score = min(score, best_score)  # Keep the best score
        
        return best_score


def get_best_move(board):
    """
    Find the best move for the AI using Minimax
    Returns the position (0-8) where AI should play
    """
    best_score = -float('inf')
    best_move = None
    
    # Try each available position
    for move in get_available_moves(board):
        board[move] = 'O'  # Make the move
        score = minimax(board, False)  # Calculate the score
        board[move] = ' '  # Undo the move
        
        # If this move is better than previous ones, remember it
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move


# ===== GAME LOOP - MAIN GAMEPLAY =====

def play_game():
    """Main game function that handles the game flow"""
    print("=" * 50)
    print("Welcome to Tic-Tac-Toe with Unbeatable AI!")
    print("=" * 50)
    print("\nYou are 'X' and the AI is 'O'")
    print("The AI uses the Minimax algorithm - Good luck!\n")
    
    board = create_board()
    
    # Ask who goes first
    first = input("Do you want to go first? (y/n): ").lower()
    human_turn = first == 'y'
    
    # Main game loop
    while not game_over(board):
        print_board(board)
        
        if human_turn:
            # Human player's turn
            print("Your turn (X)")
            try:
                move = int(input("Enter position (0-8): "))
                
                # Validate the move
                if move < 0 or move > 8:
                    print("Invalid position! Choose between 0-8")
                    continue
                if board[move] != ' ':
                    print("That position is already taken!")
                    continue
                
                board[move] = 'X'
                human_turn = False
                
            except ValueError:
                print("Please enter a valid number!")
                continue
        
        else:
            # AI's turn
            print("AI is thinking...")
            move = get_best_move(board)
            board[move] = 'O'
            print(f"AI played position {move}")
            human_turn = True
    
    # Game over - show final board and result
    print_board(board)
    
    if check_winner(board, 'X'):
        print("🎉 Congratulations! You won! (This should be impossible!)")
    elif check_winner(board, 'O'):
        print("🤖 AI wins! Better luck next time!")
    else:
        print("🤝 It's a draw! Well played!")


# Start the game
if __name__ == "__main__":
    play_game()
    
    # Ask if player wants to play again
    while input("\nPlay again? (y/n): ").lower() == 'y':
        play_game()
    
    print("\nThanks for playing! Goodbye! 👋")
