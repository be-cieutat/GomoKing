

import numpy as np
setval = set(i for i in range(15))
import time
import math
import random
col=('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O')

# WHITE = 'O'
# BLACK = 'X'
    
class Game:         #classe permettant d'initialiser le jeu 

    def __init__(self,val= None):
        if type(val)==np.array:    
            self.current_state = val
        else:
            self.initialize_game()
            
    

    def initialize_game(self):  #le jeu est initialisé comme une matrice 15x15,pleine de '.'
        self.current_state = np.full((15, 15),'.')
        
    
    def draw_board(self):   #affichage de notre plateau avec les colonnes (A-O) et les lignes allant de 1-15
        print('   ',end='')
        for k in col:
          print(k,' ',end='')
        print()
        for i in range(1, len(self.current_state)+1):
            if(int(i)<10):
                print(i,' ',end='')
            else:
                print(i,'',end='')
            for j in self.current_state[i-1]:
                print(j,' ',end='')
            print()
            
    def deuxieme_coup(self):#pour respecter les conditions de debut, on impose si necessaire le 2e coup
        liste = [(3,3),(11,11),(3,11),(11,3)]
        return random.choice(liste)
        
    def check_col(self, color): #verifie un gain par colonne
        neg_color = 'O' if color == 'X' else 'O'
        for i in range(15-4):
            for j in range(15):
                window = self.current_state[i:i+5, j]
                if (window== np.full((5),color)).all():
                    if 0 <= i-1 and i+5 < 15:
                        if self.current_state[i-1, j] == neg_color and self.current_state[i+5, j] == neg_color:
                            continue
                    return True
        return False

    def check_row(self, color): #verifie un gain par ligne
        neg_color = 'O' if color == 'X' else 'X'
        for i in range(15):
            for j in range(15-4):
                window = self.current_state[i, j:j+5]
                if (window== np.full((5),color)).all():
                    if 0 <= j-1 and j+5 < 15:
                        if self.current_state[i, j-1] == neg_color and self.current_state[i, j+5] == neg_color:
                            continue
                    return True
        return False

    def check_diag(self, color): #verifie un gain par diagonale
        neg_color = 'O' if color == 'X' else 'X'
        for i in range(15-4):
            for j in range(15-4):
                window = self.current_state[i:i+5, j:j+5]
                if (window.diagonal()==np.full((5),color)).all():
                    if 0 <= i-1 and i+5 < 15 and 0 < j-1 and j+5 < 15:
                        if self.current_state[i-1, j-1] == neg_color and self.current_state[i+5, j+5] == neg_color:
                            continue
                    return True
                if (np.fliplr(window).diagonal()== np.full((5),color)).all():
                    if 0 <= i-1 and i+5 < 15 and 0 < j-1 and j+5 < 15:
                        if self.current_state[i-1, j+5] == neg_color and self.current_state[i+5, j-1] == neg_color:
                            continue
                    return True
        return False

    def check_win(self, color): #verifie un gain sur le plateau pour une couleur spécifique
        if self.check_row(color):
            return True
        if self.check_col(color):
            return True
        if self.check_diag(color):
            return True
        return False
    
    def generate_moves(self,is_black): #genere les coups possibles
        color = 'O' if is_black else 'X'
        setval = set(i for i in range(15)) 
        Coups = []
        list1 = []
        list2 = []
        for i in range(0,15):
            for j in range(0,15):
                if self.current_state[i][j] != '.': # on se place a cote des cases deja occupées par des pions
                    list2.append((i, j))
                    if self.current_state[i][j] == color: #on prioritise les pions de l'adversaire
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
                    
                    
        
        Coups = list(set(list1) - set(list2)) #on garde uniquement les cases libres
                   
        return Coups
    
    def put(self, move, is_black): #place le pion au bon endroit
        color = 'X' if is_black else 'O'
        self.current_state[move] = color
        

    evaluation_count = 0



    def get_patterns(self, line, pattern_dict, is_black): #parcours le plateau en recherche des patterns de jeu
        color = 'X' if is_black else 'O'
        neg_color = 'O' if is_black else 'X'
        s = ''
        old = "."
        
        # 'p' correspond au pion de notre couleur, 'a' au pion de l'adversaire et 'v' a une case vide
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


    def get_patterns_row(self, pattern_dict, is_black): #cherche les motifs par ligne
        matrix = self.current_state
        for i in range(15):
            self.get_patterns(matrix[i], pattern_dict, is_black)


    def get_patterns_col(self, pattern_dict, is_black): #cherche les motifs par colonne
        matrix = self.current_state
        for i in range(15):
            self.get_patterns(matrix[:, i], pattern_dict, is_black)


    def get_patterns_diag(self, pattern_dict, is_black):    #cherche les motifs par diag
        matrix1 = self.current_state
        matrix2 = matrix1[::-1,:]
        for i in range(-16, 15):
            self.get_patterns(matrix1.diagonal(i), pattern_dict, is_black)
            self.get_patterns(matrix2.diagonal(i), pattern_dict, is_black)

    @classmethod
    def get_pattern_score(self, pattern_dict):       #pour chaque potif on associe un score 
        #on fait la difference entre les arrangements perdant (pion de l'adversaire de chaque coté)
        #les arrangements morts ( pion de l'adversaire d'un coté)
        #les arrangements vivants (les deux cases entourant le motif sont vides)
        
        score = 0
        for pattern in pattern_dict:
            if pattern.count('p') == 5:
                score += 1000000
                
            if pattern.count('p') == 4:
                if pattern[0] == 'a' and pattern[-1] == 'a':
                    score -= 10000 
                elif pattern[0] == 'a' or pattern[-1] == 'a':
                    score += 5000 
                else:
                    score += 10000
            if pattern.count('p') == 3:
                if pattern[0] == 'a' and pattern[-1] == 'a':
                    score -= 1000
                elif pattern[0] == 'a' or pattern[-1] == 'a':
                    score += 500
                else:
                    score += 1000
            if pattern.count('p') == 2:
                if pattern[0] == 'a' and pattern[-1] == 'a':
                   score -= 100 * pattern_dict[pattern]
                elif pattern[0] == 'a' or pattern[-1] == 'a':
                    score += 50
                else:
                    score += 100
            if pattern.count('p') == 1:
                if pattern[0] == 'a' and pattern[-1] == 'a':
                    score -= 1
                else:
                    score += 1 
        return score
    

    def get_score(self, is_black: bool, is_black_turn: bool): #on fait un score total de tous les pattern
        pattern_dict = {}
        self.get_patterns_row( pattern_dict, is_black)
        self.get_patterns_col(pattern_dict, is_black)
        self.get_patterns_diag(pattern_dict, is_black)
        return self.get_pattern_score(pattern_dict)


    def evaluate_board(self, is_black_turn: bool,is_black : bool): #on associe un score aux blancs et au noirs
        self.evaluation_count += 1
        black_score = self.get_score(True, is_black_turn)
        white_score = self.get_score(False, is_black_turn)
        #en focntion de celui qui joue on retourne une difference en particulier
        return black_score - white_score if is_black else white_score - black_score
    

    def count_occup(self, move): #compte le nbr de cases occupées autour de la case qui nous interesse
        x, y = move
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= x+i < 15 and 0 <= y+j < 15:
                    if self.current_state[x+i,y+j] != '.':
                        count += 1
        return count


    def heuristic_sort(self, all_moves): # notre heuristique : classe les coups possibles par le nombre de cases ocupées
        return sorted(all_moves, key=lambda move: self.count_occup(move), reverse=True)

    
    def MinMax_alphabeta(self, depth, alpha, beta, is_max,is_black): #l'algo minmax
        if depth == 0:
            return (self.evaluate_board( not is_max,is_black), None)

        all_possible_moves = self.generate_moves(is_black)
        all_possible_moves = self.heuristic_sort(all_possible_moves)

        if len(all_possible_moves) == 0:
            return (self.evaluate_board( not is_max,is_black), None)

        best_move = None

        if is_max:
            best_value = -math.inf
            for move in all_possible_moves:
                dumm_board = Game(np.array(self))
                dumm_board.put(move, False)
                value, temp_move = dumm_board.MinMax_alphabeta( depth-1, alpha, beta, not is_max,is_black)
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
                dumm_board = Game(np.array(self))
                dumm_board.put(move, True)
                value, temp_move = dumm_board.MinMax_alphabeta( depth-1, alpha, beta, is_max,is_black)
                if value < beta:
                    beta = value
                if value <= alpha:
                    return (value, temp_move)
                if value < best_value:
                    best_value = value
                    best_move = move
        return (best_value, best_move)

    def find_next_move(self, depth, is_black): #recherche du prochain coup
        self.evaluation_count = 0
        move = None
        alpha = -math.inf
        beta = math.inf
        value, best_move = self.MinMax_alphabeta(depth, alpha, beta, True, is_black)
        if best_move is not None:
            move = best_move
        return move

def Gomoku():

    board = Game()
    board.current_state[7,7]='X'
    board.draw_board()
    
    joueur1 = input("La machine joue en 1 ou en 2 ?")

    n = 0
    
    col=('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O')
    index_col=list(range(15)) 
    dico_col = {x:y for x,y in zip(col,index_col)}
    
    if joueur1 == "1":
        
       while n < 60:
            if n%2 == 0:
                print()
                print("Tour du joueur: veuillez placer un O")
                j = (input("Position de la colonne de votre réponse ?"))
                i = int(input("Position de la ligne de votre réponse ?"))
                j = dico_col[j]
                move = (i-1,j)
                board.put(move,False)
                board.draw_board()
                
            elif n== 1:
                print()
                print("Tour de la machine:")
                start = time.time()
                move = board.find_next_move(4, True)
                if i in set(i for i in range(4,12)) or i in set(i for i in range(j,12)):
                    move = board.deuxieme_coup()

                board.put(move,True)
                board.draw_board()
                end = time.time()
                temps = end-start
                print("temps = ",temps)
            else:
                print()
                print("Tour de la machine:")
                start = time.time()
                move = board.find_next_move(4, True)
                board.put(move,True)
                board.draw_board()
                end = time.time()
                temps = end-start
                print("temps = ",temps)
                
                
            
            n += 1
            if board.check_win("O"):
                 return( "Domination du joueur la machine s'avoue vaincu")
            if board.check_win("X"):
                 return("Domination de la machine, c'est une splendide victoire pour elle")
    else: 
        print()
        print("Tour de la machine:")

        
        while n < 60:
            if n%2 == 0:
                print()
                print("Tour de la machine:")
                start = time.time()
                move = board.find_next_move(4, False)
                board.put(move,False)
                board.draw_board()
                end = time.time()
                temps = end-start
                print("temps = ",temps)
                
            elif n == 1:
                print()
                print("Tour du joueur: veuillez placer un O")
                print("Le joueur doit jouer à l'exterieur du carré de côté 7 de centre H8")
                j = (input("Position de la colonne de votre réponse ?"))
                i = int(input("Position de la ligne de votre réponse ?"))
                
                move = (i-1,dico_col[j])
                board.put(move,True)
                board.draw_board()
            else:
                print()
                print("Tour du joueur: veuillez placer un X")
                j = (input("Position de la colonne de votre réponse ?"))
                i = int(input("Position de la ligne de votre réponse ?"))
                
                move = (i-1,dico_col[j])
                board.put(move,True)
                board.draw_board()
                
                
            
            n += 1
            if board.check_win("O"):
                 return("Domination de la machine, c'est une splendide victoire pour elle")
            if board.check_win("X"):
                return("Domination du joueur la machine s'avoue vaincu")
    
    return( "Egalité : il n'y a plus de jetons")

if __name__ == '__main__':
    Gomoku()