# U3L4 Player
# Riya Dev
# 1/21/2021

import random

class RandomPlayer:
   def __init__(self):
      self.white = "#ffffff" # "O"
      self.black = "#000000" # "@
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = 7
      self.y_max = 6
      self.first_turn = True
      
   def best_strategy(self, board, color):
      # returns best move
      # (column num, row num), 0
      possible_moves = self.find_moves(board, color)
      x = random.choice(list(possible_moves))
      return (int(x / self.y_max), x % self.y_max), 0
     
   def find_moves(self, board, color):
      # finds all possible moves
      # returns a set, e.g., {0, 1, 2, 3, ...., 24}       
      moves_found = {}
      for i in range(len(board)): # x
         for j in reversed(range(len(board[i]))): # y
            if board[i][j] == ".":
               moves_found.update({i * self.y_max + j: 0})
               break
      return moves_found
       
class CustomPlayer:
   def __init__(self, AIPIECE):
      self.white = "#ffffff" #"O"
      self.black = "#000000" #"X"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = 7
      self.y_max = 6
      self.first_turn = True
      self.AIPIECE = AIPIECE
   
   def best_strategy(self, board, color):
      # returns best move
      # return best_move, 0
      if self.AIPIECE == "@": color = self.black
      else: color = self.white
      return self.minimax(board, color, 4) # the 4 is changeable

   def minimax(self, board, color, search_depth):
      # returns best "value"
      return self.max_value(board, color, search_depth)
      
   def max_value(self, board, color, search_depth):
      possible_moves = self.find_moves(board, color)
      best_move = (-1, -1)
      
      if len(possible_moves) == 0: return best_move, -999
      elif len(self.find_moves(board, self.opposite_color[color])) ==  0: return best_move, 999
      if search_depth == 0:
         return best_move, self.evaluate(board, self.AIPIECE, possible_moves)
         
      val = -9999
      for m in possible_moves:
         move = (m // self.y_max, m % self.y_max)
         new_board = self.make_move(board, color, move)
         m, v = self.min_value(new_board, self.opposite_color[color], search_depth - 1)
         if v > val:
            val = v
            best_move = move
      return best_move, val
   
   def min_value(self, board, color, search_depth):
      possible_moves = self.find_moves(board, color)
      best_move = (-1, -1)
      
      if len(possible_moves) == 0: return best_move, 999
      elif len(self.find_moves(board, self.opposite_color[color])) == 0: return best_move, -999
      
      if search_depth == 0:
         return best_move, self.evaluate(board, self.AIPIECE, possible_moves)
         
      val = 9999
      for m in possible_moves:  
         move = (m // self.y_max, m % self.y_max)
         new_board = self.make_move(board, color, move)         
         m, v = self.max_value(new_board, self.opposite_color[color], search_depth - 1)
         if v < val:
            val = v
            best_move = move
      return best_move, val

   def make_move(self, board, color, move):
      # returns board that has been updated
      #print(self, board, color, move)
      new_board = [x[:] for x in board] #deep copy
      new_board[move[0]][move[1]] = 'O' if color==self.white else 'X'
   
      return new_board

   def evaluate(self, board, piece, possible_moves):
      # returns the utility value
      score = 0
      WINDOW_LENGTH = 4
            
      ## Score center column
      center_array = board[3]
      center_count = center_array.count(piece)
      score += center_count * 3
   
   	## Score Horizontal
      for r in range(self.y_max):
         row_array = []
         for x in range(0, 6):
            row_array += board[x][r]
         for c in range(self.x_max-3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += self.evaluate_window(window, piece)
   
   	## Score Vertical
      for c in range(self.x_max):
         col_array = board[c]
         for r in range(self.y_max - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += self.evaluate_window(window, piece)
   
   	## Score negatively sloped diagonal
      for r in range(self.y_max - 3):
         for c in range(self.x_max - 3):
            window = [board[c+i][r+i] for i in range(WINDOW_LENGTH)]
            score += self.evaluate_window(window, piece)
      
      ## score positively sloped diagonal
      for r in range(self.y_max-3):
         for c in range(self.x_max-3):
            window = [board[c+i][r+3-i] for i in range(WINDOW_LENGTH)]
            score += self.evaluate_window(window, piece)
      return score

   def evaluate_window(self, window, piece):
      score = 0
      EMPTY = '.'
      if self.AIPIECE == "@":
        opp_piece = "O"
      else:
        opp_piece = "@"
      
      if window.count(piece) == 4:
         score += 100
      elif window.count(piece) == 3 and window.count(EMPTY) == 1:
         score += 5
      elif window.count(piece) == 2 and window.count(EMPTY) == 2:
         score += 2
      if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
         score -= 100 #higher 4
   
      return score
   
   def find_moves(self, board, color):
      moves_found = {}
      for i in range(len(board)): # x
         for j in reversed(range(len(board[i]))): # y
            if board[i][j] == ".":
               moves_found.update({i * self.y_max + j: 0})
               break
      return moves_found

# board: [['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.']]