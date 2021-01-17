from copy import deepcopy
from os import system
from queue import Queue
from random import randint, seed

MAX_COL=4
MAX_ROW=4
SHUFFLE_MAGNITUDE= 30

class Board:
    def __init__(self):
      self.goal= [["  1", "  2", "  3", "  4"], 
                  ["  5", "  6", "  7", "  8"], 
                  ["  9", " 10", " 11", " 12"], 
                  [" 13", " 14", " 15", " __"]]
      self.board= deepcopy(self.goal)
      self.empty_loc= [MAX_ROW - 1, MAX_COL - 1]
      self.moves = {0: self.move_up, 1: self.move_right,\
         2: self.move_down, 3: self.move_left}
      

    def __repr__(self):
      #represents the board
      for i in range(MAX_ROW):
        for j in range(MAX_COL):
          print(self.board[i][j], end=" ")
        print()
      
      #repr must return something
      return ""
    
    def refresh(self):

      #Clears the screen
      system("cls")
      print("Welcome to the 15 puzzle!\n")
      print(self)

      if self.board == self.goal:
        print("\nCongratulations you Won")
        return False
      return True

    def shuffle(self):
      #Randomizes board using legal moves
      seed()
      
      for i in range(SHUFFLE_MAGNITUDE):
        m= randint(0,3)
        self.moves[m](self.board, self.empty_loc)
      
      # optionally move the empty space to the lower right corner
      for i in range(MAX_ROW):
        self.moves[2](self.board, self.empty_loc)

      for i in range(MAX_COL):
        self.moves[1](self.board, self.empty_loc)

    def move(self, board, empty_loc, x, y):
      #Makes a legal move
      #check if move is possible
      if empty_loc[0] + x < 0 or empty_loc[0]+ x > 3 or \
        empty_loc[1] + y < 0 or empty_loc[1] + y > 3:
        return board, empty_loc

      #swap
      board[empty_loc[0]][empty_loc[1]], board[empty_loc[0]+ x]\
        [empty_loc[1]+ y]= board[empty_loc[0]+ x]\
        [empty_loc[1]+ y], board[empty_loc[0]][empty_loc[1]]
      
      #update empty location
      empty_loc[0] += x
      empty_loc[1] += y

      return board, empty_loc

    def move_up(self, board, empty_loc):
      return self.move(board, empty_loc, -1, 0)

    def move_right(self, board, empty_loc):
      return self.move(board, empty_loc, 0, 1)

    def move_down(self, board, empty_loc):
      return self.move(board, empty_loc, 1, 0)

    def move_left(self, board, empty_loc):
      return self.move(board, empty_loc, 0, -1)

    def solve(self):
      """Solves the game using breadth first search algo!"""
      #self.board= deepcopy(self.goal)

      def successors(board, empty_location):
        b_lst= [deepcopy(board), deepcopy(board), deepcopy(board), deepcopy(board)]
        e_loc_lst= [list(empty_location), list(empty_location), list(empty_location)\
          , list(empty_location)]
        b_lst[0], e_loc_lst[0]= self.move_up(b_lst[0], e_loc_lst[0])
        b_lst[1], e_loc_lst[1]= self.move_right(b_lst[1], e_loc_lst[1])
        b_lst[2], e_loc_lst[2]= self.move_down(b_lst[2], e_loc_lst[2])
        b_lst[3], e_loc_lst[3]= self.move_left(b_lst[3], e_loc_lst[3])

        return [[b_lst[0], e_loc_lst[0], 0], [b_lst[1], e_loc_lst[1], 1]\
          , [b_lst[2], e_loc_lst[2], 2], [b_lst[3], e_loc_lst[3], 3]]

      searched=set()
      fringe= Queue()

      fringe.put({"board":self.board, "empty_location": self.empty_loc, "path": []})

      while True:
        #Quit if no solution is found
        if fringe.empty():
          return[]
        
        #inspect current node
        node= fringe.get()

        #quit if node contains goal
        if node["board"]==self.goal:
          return node["path"]

        #add current node to searched set: put children in fringe
        if str(node["board"]) not in searched:
          searched.add(str(node["board"]))
          for child in successors(node["board"], node["empty_location"]):
            if str(child[0]) not in searched:
              fringe.put({"board":child[0], "empty_location":child[1],\
                 "path":node["path"]+[child[2]]})
