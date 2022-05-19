# -*- coding: utf-8 -*-
"""
Created on Sat May 14 23:17:25 2022

@author: sophi
"""

import numpy as np
setval = set(i for i in range(15))
import time
import math

class Player:
    WHITE = 'O'
    BLACK = 'X'
    
class Game:

    def __init__(self,val= None):
        if type(val)==np.array:    
            self.current_state = val
        else:
            self.initialize_game()
            
    

    def initialize_game(self):
        self.current_state = np.full((15, 15),'.')
    
    def draw_board(self):
        for i in range(0, 15):
            for j in range(0, 15):
                print('{}|'.format(self.current_state[i,j]), end=" ")
            print()
        print()
            
    
    def __check_col(self, color):
        for i in range(0, 11):
            for j in range(0,15):
                if (self.current_state[i,j] == color and
                    self.current_state[i,j] == self.current_state[i+1,j] and
                    self.current_state[i+1,j] == self.current_state[i+2,j] and
                    self.current_state[i+2,j] == self.current_state[i+3,j] and
                    self.current_state[i+3,j] == self.current_state[i+4,j]):
                    return True
        return False

    def __check_row(self, color):
        for i in range(0, 15):
            for j in range (0,11):
                if (all(self.current_state[i,j:j+5] == [color]*5)):
                    return True
        return False

    def __check_diagonal_right(self, color):
        for i in range(0,11):
            for j in range(0,11):
                if (self.current_state[j,i] == color and
                    self.current_state[j,i] == self.current_state[j+1,i+1] and
                    self.current_state[j+1,i+1] == self.current_state[j+2,i+2] and
                    self.current_state[j+2,i+2] == self.current_state[j+3,i+3] and
                    self.current_state[j+3,i+3] == self.current_state[j+4,i+4]):
                    return True
        return False
    
    def __check_diagonal_left(self, color):
        for i in range(4,15):
            for j in range(4,15):
                if (self.current_state[j,i] == color and
                    self.current_state[j,i] == self.current_state[j-1,i-1] and
                    self.current_state[j-1,i+1] == self.current_state[j-2,i+2] and
                    self.current_state[j-2,i+2] == self.current_state[j-3,i+3] and
                    self.current_state[j-3,i+3] == self.current_state[j-4,i+4]):
                    return True
        return False

    def check_win(self, color):
        if self.__check_row(color):
            return True
        if self.__check_col(color):
            return True
        if self.__check_diagonal_right(color):
            return True
        if self.__check_diagonal_left(color):
            return True
        return False
    
    def generate_moves(self,is_black):
        color = 'O' if is_black else 'X'
        setval = set(i for i in range(15)) 
        Coups = []
        list1 = []
        list2 = []
        for i in range(0,15):
            for j in range(0,15):
                if self.current_state[i][j] != '.':
                    list2.append((i, j))
                    if self.current_state[i][j] == color: 
                        if i-1 in setval and j-1 in setval:
                            list1.append((i-1, j-1))
                            
                        if i-1 in setval and j in setval:
                            list1.append((i-1, j))
                            
                        if i-1 in setval and j+1 in setval:
                            list1.append((i-1, j+1))
                            
                        if i in setval and j+1 in setval:
                            list1.append( (i, j+1) )
                            
                        if i+1 in setval and j+1 in setval:
                            list1.append( (i+1, j+1) )
                            
                        if i+1 in setval and j in setval:
                            list1.append( (i+1, j) )
                            
                        if i+1 in setval and j-1 in setval:
                            list1.append( (i+1, j-1) )
                            
                        if i in setval and j-1 in setval:
                            list1.append( (i, j-1) )
                    
                    
        
        Coups = list(set(list1) - set(list2))
                   
        return Coups
    
    def draw(self, move, is_black):
        color = 'X' if is_black else 'O'
        self.current_state[move] = color
        
    def swap(self):
        board = self.current_state
        for i in range(15):
            for j in range(15):
                if board[i][j] == 'X':
                    board[i][j] = 'O'
                elif board[i][j] == 'O':
                    board[i][j] = 'X'
        return board

    
class Playthrough:
    evaluation_count = 0
    calculation_time = 0

    @classmethod
    def __get_patterns(cls, line, pattern_dict, is_black):
        color = 'X' if is_black else 'O'
        neg_color = 'O' if is_black else 'X'
        s = ''
        old = "."

        for i, c in enumerate(line):
            if i == '.':
                s += 'v'
            if c == color:
                if old == neg_color:
                    s += 'a'
                s += 'p'
            if c != color or i == len(line)-1:
                if c == neg_color and len(s) > 0:
                    s += 'a'
                elif i == len(line)-1:
                    s += 'p'
                if s in pattern_dict.keys():
                    pattern_dict[s] += 1
                else:
                    pattern_dict[s] = 1
                s = ''
            old = c

    @classmethod
    def __get_patterns_row(cls, board: Game, pattern_dict, is_black):
        size = 15
        matrix = board.current_state
        for i in range(size):
            cls.__get_patterns(matrix[i], pattern_dict, is_black)

    @classmethod
    def __get_patterns_col(cls, board: Game, pattern_dict, is_black):
        size = 15
        matrix = board.current_state
        for i in range(size):
            cls.__get_patterns(matrix[:, i], pattern_dict, is_black)

    @classmethod
    def __get_patterns_diagonal(cls, board: Game, pattern_dict, is_black):
        size = 15
        matrix1 = board.current_state
        matrix2 = matrix1[::-1,:]
        for i in range(-size+1, size):
            cls.__get_patterns(matrix1.diagonal(i), pattern_dict, is_black)
            cls.__get_patterns(matrix2.diagonal(i), pattern_dict, is_black)

    @classmethod
    def evaluate_board(cls, board: Game, is_black_turn: bool):
        cls.evaluation_count += 1
        black_score = cls.get_score(board, True, is_black_turn)
        white_score = cls.get_score(board, False, is_black_turn)
        if black_score == 0: black_score = 1.0
        return white_score - black_score

    @classmethod
    def get_score(cls, board: Game, is_black: bool, is_black_turn: bool):
        pattern_dict = {}
        cls.__get_patterns_row(board, pattern_dict, is_black)
        cls.__get_patterns_col(board, pattern_dict, is_black)
        cls.__get_patterns_diagonal(board, pattern_dict, is_black)
        return cls.get_consecutive_score(pattern_dict)

    @classmethod
    def get_consecutive_score(cls, pattern_dict):
        score = 0
        for pattern in pattern_dict:
            if pattern.count('p') == 5:
                if pattern[0] == 'v' and pattern[-1] == 'v':
                    pass
                if pattern[0] == 'a' and pattern[-1] == 'a':
                    pass
                else:
                    score += 100000
            if pattern.count('p') == 4:
                if pattern[0] == 'a' and pattern[-1] == 'a':
                    score -= 10000 * pattern_dict[pattern]
                elif pattern[0] == 'a' or pattern[-1] == 'a':
                    score += 5000 * pattern_dict[pattern]
                else:
                    score += 10000 * pattern_dict[pattern]
            if pattern.count('p') == 3:
                if pattern[0] == 'a' and pattern[-1] == 'a':
                    score -= 1000 * pattern_dict[pattern]
                elif pattern[0] == 'a' or pattern[-1] == 'a':
                    score += 500 * pattern_dict[pattern]
                else:
                    score += 1000 * pattern_dict[pattern]
            if pattern.count('p') == 2:
                if pattern[0] == 'a' and pattern[-1] == 'a':
                   score -= 100 * pattern_dict[pattern]
                elif pattern[0] == 'a' or pattern[-1] == 'a':
                    score += 50 * pattern_dict[pattern]
                else:
                    score += 100 * pattern_dict[pattern]
            if pattern.count('p') == 1:
                if pattern[0] == 'a' and pattern[-1] == 'a':
                    score -= 1 * pattern_dict[pattern]
                else:
                    score += 1 * pattern_dict[pattern]
        return score

    @classmethod
    def find_next_move(cls, board: Game, depth, is_black):
        cls.evaluation_count = 0
        cls.calculation_time = 0
        

        start = time.time()
        value, best_move = cls.__search_winning_move(board,is_black)
        if best_move is not None:
            move = best_move
        else:
            value, best_move = cls.minimax_alphabeta(board, depth, -1.0, 100000000, True, is_black)
            if best_move is None:
                move = None
            else:
                move = best_move
        end = time.time()
        cls.calculation_time = end-start
        if move is None:
            move = (15//2, 15//2)
        return move

    @classmethod
    def heuristic_sort(cls, board, all_moves):
        def my_func(board, move):
            x, y = move
            count = 0
            size = 15
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if 0 <= x+i < size and 0 <= y+j < size:
                        if board.current_state[x+i,y+j] != '.':
                            count += 1
            return count

        return sorted(all_moves, key=lambda move: my_func(board, move), reverse=True)

    @classmethod
    def minimax_alphabeta(cls, board: Game, depth, alpha, beta, is_max,is_black):
        if depth == 0:
            return (cls.evaluate_board(board, not is_max), None)

        all_possible_moves = board.generate_moves(is_black)
        all_possible_moves = cls.heuristic_sort(board, all_possible_moves)

        if len(all_possible_moves) == 0:
            return (cls.evaluate_board(board, not is_max), None)

        best_move = None

        if is_max:
            best_value = -math.inf
            for move in all_possible_moves:
                dumm_board = Game(np.array(board))
                dumm_board.draw(move, False)
                value, temp_move = cls.minimax_alphabeta(dumm_board, depth-1, alpha, beta, not is_max,is_black)
                if value > alpha:
                    alpha = value
                if value >= beta:
                    return (value, temp_move)
                if value > best_value:
                    best_value = value
                    best_move = move
        else:
            best_value = math.inf
            for move in all_possible_moves:
                dumm_board = Game(np.array(board))
                dumm_board.draw(move, True)
                value, temp_move = cls.minimax_alphabeta(dumm_board, depth-1, alpha, beta, not is_max,is_black)
                if value < beta:
                    beta = value
                if value <= alpha:
                    return (value, temp_move)
                if value < best_value:
                    best_value = value
                    best_move = move
        return (best_value, best_move)

    @classmethod
    def __search_winning_move(cls, board: Game,is_black):
        all_possible_moves = board.generate_moves(is_black)

        for move in all_possible_moves:
            dumm_board = Game(board.current_state)
            dumm_board.draw(move, False)
            if dumm_board.check_win('O'):
                return (None, move)
            dumm_board = Game(board.current_state)
            dumm_board.draw(move, True)
            if dumm_board.check_win('X'):
                return (None, move)
        return (None, None)


def Gomoku():

    board = Game()
    board.current_state[7,7]='X'
    board.draw_board()
    
    joueur1 = int(input("La machine joue en 1 ou en 2 ?"))

    n = 0
    if joueur1 == 1:
        print()
        print("Tour du joueur: veuillez placer un O")
        print("Le joueur doit jouer à l'exterieur du carré de côté 7 de centre H8")
        i = int(input("Position de la ligne de votre réponse ?"))
        j = int(input("Position de la colonne de votre réponse ?"))
        move = (i,j)
        board.draw(move,False)
        board.draw_board()
        n += 1
        
        while n < 119:
            if n%2 == 0:
                print()
                print("Tour du joueur: veuillez placer un O")
                i = int(input("Position de la ligne de votre réponse ?"))
                j = int(input("Position de la colonne de votre réponse ?"))
                move = (i,j)
                board.draw(move,False)
                board.draw_board()
                
                
            else:
                print()
                print("Tour de la machine:")
                move = Playthrough.find_next_move(board, 4, True)
                board.draw(move,True)
                board.draw_board()
                
                
            
            n += 1
            if board.check_win("O"):
                return( "Domination du joueur la machine s'avoue vaincu")
            if board.check_win("X"):
                return("Domination de la machine, c'est une splendide victoire pour elle")
    else: 
        print()
        print("Tour de la machine:")
        print("L'ordinateur doit jouer à l'exterieur du carré de côté 7 de centre H8")
        i = int(input("Position de la ligne de la réponse de l'ordinateur ?"))
        j = int(input("Position de la colonne de la réponse de l'ordinateur ?"))
        move = (i,j)
        board.draw(move,False)
        board.draw_board()
        n += 1
        
        while n < 119:
            if n%2 == 0:
                print()
                print("Tour de la machine:")
                move = Playthrough.find_next_move(board, 4, False)
                board.draw(move,False)
                board.draw_board()
                
            else:
                print()
                print("Tour du joueur: veuillez placer un X")
                i = int(input("Position de la ligne de votre réponse ?"))
                j = int(input("Position de la colonne de votre réponse ?"))
                move = (i,j)
                board.draw(move,True)
                board.draw_board()
                
                
            
            n += 1
            if board.check_win("O"):
                return("Domination de la machine, c'est une splendide victoire pour elle")
            if board.check_win("X"):
                return("Domination du joueur la machine s'avoue vaincu")
    
    return( "Egalité : il n'y a plus de jetons")

if __name__ == '__main__':
    Gomoku()