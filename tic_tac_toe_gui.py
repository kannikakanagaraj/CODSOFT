"""
Tic-Tac-Toe AI Game with GUI
A graphical version with unbeatable AI using Minimax algorithm
"""

import tkinter as tk
from tkinter import messagebox
import time


class TicTacToeGUI:
    def __init__(self):
        """Initialize the GUI game"""
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe AI Game")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.configure(bg='#2C3E50')
        
        # Game state
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'
        self.current_player = self.human
        self.game_active = True
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title label
        title_label = tk.Label(
            self.window, 
            text="Tic-Tac-Toe AI", 
            font=('Arial', 20, 'bold'),
            bg='#2C3E50',
            fg='#ECF0F1'
        )
        title_label.pack(pady=15)
        
        # Info label
        self.info_label = tk.Label(
            self.window, 
            text="You are X | AI is O", 
            font=('Arial', 11),
            bg='#2C3E50',
            fg='#BDC3C7'
        )
        self.info_label.pack(pady=5)
        
        # Status label
        self.status_label = tk.Label(
            self.window, 
            text="Your turn!", 
            font=('Arial', 13, 'bold'),
            bg='#2C3E50',
            fg='#3498DB'
        )
        self.status_label.pack(pady=8)
        
        # Game board frame
        board_frame = tk.Frame(self.window, bg='#2C3E50')
        board_frame.pack(pady=10)
        
        # Create 9 buttons for the board
        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3
            
            button = tk.Button(
                board_frame,
                text=' ',
                font=('Arial', 28, 'bold'),
                width=4,
                height=1,
                bg='#34495E',
                fg='#ECF0F1',
                activebackground='#5D6D7E',
                relief='raised',
                bd=3,
                command=lambda pos=i: self.human_move(pos)
            )
            button.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(button)
        
        # Control buttons frame
        control_frame = tk.Frame(self.window, bg='#2C3E50')
        control_frame.pack(pady=15)
        
        # New Game button
        new_game_btn = tk.Button(
            control_frame,
            text="New Game",
            font=('Arial', 11, 'bold'),
            bg='#27AE60',
            fg='white',
            activebackground='#229954',
            width=10,
            height=1,
            command=self.reset_game
        )
        new_game_btn.grid(row=0, column=0, padx=8)
        
        # AI First button
        ai_first_btn = tk.Button(
            control_frame,
            text="AI Starts",
            font=('Arial', 11, 'bold'),
            bg='#E74C3C',
            fg='white',
            activebackground='#C0392B',
            width=10,
            height=1,
            command=self.ai_starts
        )
        ai_first_btn.grid(row=0, column=1, padx=8)
        
    def human_move(self, position):
        """Handle human player's move"""
        if not self.game_active:
            return
        
        if self.board[position] != ' ':
            return
        
        if self.current_player != self.human:
            return
        
        # Make the move
        self.board[position] = self.human
        self.buttons[position].config(text=self.human, fg='#3498DB', disabledforeground='#3498DB')
        self.buttons[position].config(state='disabled')
        
        # Check game state
        if self.check_game_over():
            return
        
        # AI's turn
        self.current_player = self.ai
        self.status_label.config(text="AI is thinking...", fg='#E67E22')
        self.window.update()
        
        # Small delay for better UX
        self.window.after(500, self.ai_move)
    
    def ai_move(self):
        """Handle AI's move using Minimax algorithm"""
        if not self.game_active:
            return
        
        # Get best move from AI
        move = self.get_best_move()
        
        if move is not None:
            self.board[move] = self.ai
            self.buttons[move].config(text=self.ai, fg='#E74C3C', disabledforeground='#E74C3C')
            self.buttons[move].config(state='disabled')
        
        # Check game state
        if self.check_game_over():
            return
        
        # Human's turn
        self.current_player = self.human
        self.status_label.config(text="Your turn!", fg='#3498DB')
    
    def check_game_over(self):
        """Check if game is over and handle end game"""
        if self.check_winner(self.human):
            self.game_active = False
            self.status_label.config(text="🎉 You Won! Amazing!", fg='#27AE60')
            messagebox.showinfo("Game Over", "Congratulations! You won!\n(This should be impossible!)")
            return True
        
        elif self.check_winner(self.ai):
            self.game_active = False
            self.status_label.config(text="🤖 AI Wins!", fg='#E74C3C')
            messagebox.showinfo("Game Over", "AI wins! Better luck next time!")
            return True
        
        elif self.is_board_full():
            self.game_active = False
            self.status_label.config(text="🤝 It's a Draw!", fg='#95A5A6')
            messagebox.showinfo("Game Over", "It's a draw! Well played!")
            return True
        
        return False
    
    def check_winner(self, player):
        """Check if a player has won"""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]               # Diagonals
        ]
        
        for pattern in win_patterns:
            if (self.board[pattern[0]] == player and 
                self.board[pattern[1]] == player and 
                self.board[pattern[2]] == player):
                return True
        return False
    
    def is_board_full(self):
        """Check if board is full"""
        return ' ' not in self.board
    
    def get_available_moves(self):
        """Get list of available positions"""
        return [i for i in range(9) if self.board[i] == ' ']
    
    # ===== MINIMAX ALGORITHM =====
    
    def minimax(self, board, is_maximizing):
        """
        Minimax algorithm - AI's brain
        Simulates all possible moves to find the best one
        """
        # Check terminal states
        if self.check_winner(self.ai):
            return 1
        if self.check_winner(self.human):
            return -1
        if ' ' not in board:
            return 0
        
        if is_maximizing:
            # AI's turn - maximize score
            best_score = -float('inf')
            for move in self.get_available_moves():
                board[move] = self.ai
                score = self.minimax(board, False)
                board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            # Human's turn - minimize score
            best_score = float('inf')
            for move in self.get_available_moves():
                board[move] = self.human
                score = self.minimax(board, True)
                board[move] = ' '
                best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self):
        """Find the best move for AI"""
        best_score = -float('inf')
        best_move = None
        
        for move in self.get_available_moves():
            self.board[move] = self.ai
            score = self.minimax(self.board, False)
            self.board[move] = ' '
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = [' ' for _ in range(9)]
        self.current_player = self.human
        self.game_active = True
        
        for button in self.buttons:
            button.config(text=' ', state='normal', bg='#34495E')
        
        self.status_label.config(text="Your turn!", fg='#3498DB')
    
    def ai_starts(self):
        """Start a new game with AI going first"""
        self.reset_game()
        self.current_player = self.ai
        self.status_label.config(text="AI is thinking...", fg='#E67E22')
        self.window.after(500, self.ai_move)
    
    def run(self):
        """Start the GUI application"""
        self.window.mainloop()


# Run the game
if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run()
