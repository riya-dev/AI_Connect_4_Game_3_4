# U3L4 Runner
# Riya Dev
# 1/20/2021

import sys
import os
import time
import tkinter as tk

from dev_r_player import CustomPlayer, RandomPlayer

# constants
delay_time = 0
turn_off_printing = False
tile_size = 75
padding = 5
x_max = 7
y_max = 6
board_x = x_max*tile_size+(x_max+1)*padding-2
board_y = y_max*tile_size+(y_max+1)*padding-2
white = "#ffffff"
black = "#000000"
grey = "#505050"
green = "#00ff00"
yellow = "#ffff00"
brown = "#654321"
blue = "#0000ff"
cyan = "#00ffff"
asterisk = " "+u'\u2217'
directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
opposite_color = {black: white, white: black}

# variables
player_types = {0: "Player", 1: "Random", 2: "Minimax AI", 3: "Alpha-beta AI", 4: "Best AI"}
players = {black: None, white: None, None: None}
player_max_times = {black: 0, white: 0}
player_total_times = {black: 0, white: 0}
p1_name = ""
p2_name = ""
root = None
canvas = None
turn = white
board = []
score1_str = None
score2_str = None
score1 = 0 #2
score2 = 0 #2
possible_moves = {}
# commands

def whose_turn(my_board, prev_turn):
   global possible_moves
   
   cur_turn = opposite_color[prev_turn]
   
   possible_moves = find_moves(my_board, cur_turn)
   if len(possible_moves) > 0:
      return cur_turn
       
   possible_moves = find_moves(my_board, prev_turn)
   if len(possible_moves) > 0:
      return prev_turn
       
   return None

def find_moves(my_board, my_color):
   moves_found = {}
   # i: 7 columns
   # j: 6 rows   
   for i in range(len(my_board)): # x
      for j in reversed(range(len(my_board[i]))): # y
         if my_board[i][j] == ".":
            moves_found.update({i * y_max + j: 0})
            break
   return moves_found

def print_board(my_board):
   # return  # comment to print board each time
   print("\t", end="")
   for i in range(x_max):
      print(chr(ord("a")+i), end=" ")
   print()
   for i in range(y_max):
      print(i+1, end="\t")
      for j in range(x_max):
         print(my_board[j][i], end=" ")
      print()
   print()

def draw_rect(x_pos, y_pos, possible=False):
   coord = [x_pos*(padding+tile_size)+padding+1, y_pos*(padding+tile_size)+padding+1,
           (x_pos+1)*(padding+tile_size), (y_pos+1)*(padding+tile_size)]
   if possible:
      canvas.create_rectangle(coord, fill=cyan, activefill=yellow)
   else:
      canvas.create_rectangle(coord, fill=green)


def draw_circle(x_pos, y_pos, fill_color):
   coord = [x_pos*(padding+tile_size)+2*padding+1, y_pos*(padding+tile_size)+2*padding+1,
           (x_pos+1)*(padding+tile_size)-padding, (y_pos+1)*(padding+tile_size)-padding]
   canvas.create_oval(coord, fill=fill_color)

def make_move(x, y):
   if x*y_max+y not in possible_moves.keys():
      return False
   next_turn(x, y)
   return True

def click(event=None):
   x = int((event.x-padding)/(padding+tile_size))
   y = int((event.y-padding)/(padding+tile_size))
   if x * y_max + y not in possible_moves.keys():
      return
   next_turn(x, y)

def next_turn(x_pos, y_pos):
   global turn, possible_moves, score1, score2
   for pos in possible_moves:
      draw_rect(int(pos/y_max), pos % y_max)
   score1 = 0
   score2 = 0
   if turn == black:
      color_symbol = "@"
   else:
      color_symbol = "O"
   board[x_pos][y_pos] = color_symbol
   draw_circle(x_pos, y_pos, turn)
       
   #for pos in possible_moves[x_pos * y_max + y_pos]:
   #    board[pos[0]][pos[1]] = color_symbol
   #    draw_circle(pos[0], pos[1], turn)
  
   #for i in range(len(board)):
   #   for j in range(len(board[i])):
   #      if board[i][j] == "@":
   #         score1 += 1
   #      if board[i][j] == "O":
   #         score2 += 1
   score1_str.set(p1_name+": "+str(score1))
   score2_str.set(p2_name+": "+str(score2))
              
   turn = whose_turn(board, turn)
   
   # TERMINAL CONDITION (4 in a row)
   # vertical
   if(y_pos <= 2):
      if turn == "#ffffff": # check @
         if board[x_pos][y_pos + 1 : y_pos + 4] == ['@', '@', '@']:
            score1 += 1
            turn = None
      elif turn == "#000000": # check O
         if board[x_pos][y_pos + 1 : y_pos + 4] == ['O', 'O', 'O']:
            turn = None
            score2 += 1
            
   # horizontal
   if turn == "#ffffff": # check @
      for i in range(0, 4):
         if board[i][y_pos] == '@' and board[i + 1][y_pos] == '@' and board[i + 2][y_pos] == '@' and board[i + 3][y_pos] == '@':
            score1 += 1
            turn = None
   if turn == "#000000": # check O
      for i in range(0, 4):
         if board[i][y_pos] == 'O' and board[i + 1][y_pos] == 'O' and board[i + 2][y_pos] == 'O' and board[i + 3][y_pos] == 'O':
            score2 += 1
            turn = None

   # right diag /
   if turn == "#ffffff": # check @
      for i in range(3, 7): # x
         for j in range(0, 3):
            if board[i][j] == "@" and board[i - 1][j + 1] == "@" and board[i - 2][j + 2] == "@" and board[i - 3][j + 3] == "@":
               score1 += 1
               turn = None
   if turn == "#000000":
      for i in range(3, 7): # x
         for j in range(0, 3):
            if board[i][j] == "O" and board[i - 1][j + 1] == "O" and board[i - 2][j + 2] == "O" and board[i - 3][j + 3] == "O":
               score1 += 1
               turn = None
      
   # left diag \
   if turn == "#ffffff": # check @
      for i in range(0, 4): # x
         for j in range(0, 3):
            if board[i][j] == "@" and board[i + 1][j + 1] == "@" and board[i + 2][j + 2] == "@" and board[i + 3][j + 3] == "@":
               score1 += 1
               turn = None
   if turn == "#000000":
      for i in range(0, 4): # x
         for j in range(0, 3):
            if board[i][j] == "O" and board[i + 1][j + 1] == "O" and board[i + 2][j + 2] == "O" and board[i + 3][j + 3] == "O":
               score1 += 1
               turn = None
   
   if turn is None:
      print_board(board)
      #print("Black ("+p1_name+") Max Time", player_max_times[black])
      #print("White ("+p2_name+") Max Time", player_max_times[white])
      #print("Black ("+p1_name+") Total Time", round(player_total_times[black], 3))
      #print("White ("+p2_name+") Total Time", round(player_total_times[white], 3))
      if score1 == score2:
         score1_str.set(p1_name+": "+str(score1)+" [Tie!]")
         score2_str.set(p2_name+": "+str(score2)+" [Tie!]")
      if score1 > score2:
         score1_str.set(p1_name+": "+str(score1)+" [Winner!]")
         print("Black (", p1_name, ") won!")
      if score1 < score2:
         score2_str.set(p2_name+": "+str(score2)+" [Winner!]")
         print("White (", p2_name, ") won!")
      return
   if turn == black:
      score1_str.set(p1_name+": "+str(score1)+asterisk)
   if turn == white:
      score2_str.set(p2_name+": "+str(score2)+asterisk)
   for pos in possible_moves.keys():
      draw_rect(int(pos/y_max), pos % y_max, True)
   print_board(board)
      
   if players[turn] != "Player":
      root.update()
      time.sleep(delay_time)
      start = time.time()
      
      print(players[turn])
      
      move, idc = players[turn].best_strategy(board, turn)
      time_used = round(time.time()-start, 3)
      # print("Time Used:", time_used, end=2*"\n")
      player_max_times[turn] = max(player_max_times[turn], time_used)
      player_total_times[turn] = player_total_times[turn]+time_used
      next_turn(move[0], move[1])

def init(choice_menu, e1, e2, v1, v2):
   global turn_off_printing, turn, root, canvas, score1_str, score2_str, p1_name, p2_name, players, player_types
   if turn_off_printing:
      sys.stdout = open(os.devnull, 'w')
   p1_name = e1.get()
   p2_name = e2.get()
   players[black] = player_types[v1.get()]
   players[white] = player_types[v2.get()]
   
   #print("p1_name", type(p1_name))
   #print(type(v1.get()))
   #print("v2.get()", v2.get())
   
   #print(players[white])
   #print(type(players[white]))   
   
   p1_name = players[black]
   p2_name = players[white]
   if players[black] == "Random":
      players[black] = RandomPlayer()
   elif players[black] == "Best AI":
      players[black] = CustomPlayer("@")
   if players[white] == "Random":
      players[white] = RandomPlayer()
   elif players[white] == "Best AI":
      players[white] = CustomPlayer("O")
      
   #print(type(players[white]))   
   
   choice_menu.destroy()
   root = tk.Tk()
   root.title("U3L4 Game")
   root.resizable(width=False, height=False)
   canvas = tk.Canvas(root, width=board_x, height=board_y, bg=brown)
   score1_str = tk.StringVar()
   score2_str = tk.StringVar()
   canvas.bind("<Button-1>", click)
   canvas.grid(row=0, column=0, columnspan=2)
   score1_str.set(p1_name+": "+str(score1)+asterisk)
   score2_str.set(p2_name+": "+str(score2))
   tk.Label(textvariable=score1_str, font=("Arial", 20), bg=brown, fg=black).grid(
      row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(textvariable=score2_str, font=("Arial", 20), bg=brown, fg=white).grid(
      row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   for i in range(x_max):
      board.append([])
      for j in range(y_max):
         draw_rect(i, j)
         board[i].append(".")
   #draw_circle(x_max/2-1, y_max/2-1, white)
   #draw_circle(x_max/2, y_max/2, white)
   #draw_circle(x_max/2-1, y_max/2, black)
   #draw_circle(x_max/2, y_max/2-1, black)
   #board[int(x_max/2-1)][int(y_max/2-1)] = "O"
   #board[int(x_max/2)][int(y_max/2)] = "O"
   #board[int(x_max/2-1)][int(y_max/2)] = "@"
   #board[int(x_max/2)][int(y_max/2-1)] = "@"
   turn = whose_turn(board, turn)
   
   for pos in possible_moves.keys():
      draw_rect(int(pos/y_max), pos % y_max, True)
   print_board(board)
   if players[turn] != "Player":
      root.update()
      time.sleep(delay_time)
      move, idc = players[turn].best_strategy(board, turn)
      next_turn(move[0], move[1])
   root.mainloop()

def menu():
   global p1_name, p2_name, radio_on, radio_off
   choice_menu = tk.Tk()
   choice_menu.title("Menu")
   choice_menu.resizable(width=False, height=False)
   tk.Label(text="Black", font=("Arial", 30), bg=black, fg=grey).grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text="White", font=("Arial", 30), bg=white, fg=black).grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   v1 = tk.IntVar()
   v2 = tk.IntVar()
   v1.set(0)
   v2.set(0)
   tk.Radiobutton(text="Player", compound=tk.LEFT, font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=0).grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
   tk.Radiobutton(text="Player", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=0).grid(row=1, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
   tk.Radiobutton(text="Random", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=1).grid(row=2, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
   tk.Radiobutton(text="Random", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=1).grid(row=2, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
   #tk.Radiobutton(text="Minimax AI", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=2).grid(row=3, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
   #tk.Radiobutton(text="Minimax AI", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=2).grid(row=3, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
   #tk.Radiobutton(text="Alpha-beta AI", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=3).grid(row=4, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
   #tk.Radiobutton(text="Alpha-beta AI", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=3).grid(row=4, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
   tk.Radiobutton(text="Best AI", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=4).grid(row=5, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
   tk.Radiobutton(text="Best AI", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=4).grid(row=5, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
   e1 = tk.Entry(font=("Arial", 15), bg=black, fg=grey, width=12)
   e2 = tk.Entry(font=("Arial", 15), bg=white, fg=black, width=12)
   e1.insert(0, "Player 1 Name")
   e2.insert(0, "Player 2 Name")
   e1.grid(row=99, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   e2.grid(row=99, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
   tk.Button(text="Begin", font=("Arial", 15), bg=white, fg=black, command=lambda: init(choice_menu, e1, e2, v1, v2)).grid(row=100, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
   choice_menu.mainloop()


menu()