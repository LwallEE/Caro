import sys
import pygame
import numpy as np
import math
from constants import *

#set up game
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('TIC TAC TOE BY HOANG VU')
screen.fill(WHITE)

class Board():
    def __init__(self,board = None):
        if board != None:
            self.squares = np.array(board.squares)
        else:
            self.squares = np.zeros((ROW,COL))
        
    def  mark_sqr(self , row , col , player):
        self.squares[row][col] = player    
    
    def empty_sqr(self,row, col):
        return self.squares[row][col] == 0
    def check_row(self, player):
        neg_pl = 1 if player == 2 else 2
        x = np.ones(5)*player
        for i in range(ROW):
            for j in range(ROW-4):
                mt = self.squares[i ,j : j+5]
                if np.equal(mt , x).all():
                    if 0 <= j-1 and j+5 < ROW:
                        if self.squares[i, j-1] == neg_pl and self.squares[i , j+5] == neg_pl:
                            continue
                    return ((i,j),(i,j+4))
        return None                
    def check_col(self, player):
        neg_col = 1 if player== 2 else 1
        x = np.ones(5)*player
        for i in range(ROW-4):
            for j in range(ROW):
                mt = self.squares[i:i+5 , j]
                if np.equal(mt , x).all():
                    if 0 <= i-1 and i+5 < ROW:
                        if self.squares[i-1 , j] == neg_col and self.squares[i , j+5] == neg_col:
                            continue
                    return ((i,j) , (i+4,j))
        return None   

    def check_dia(self, player):
        neg_col = 1 if player ==2 else 1
        x = np.ones(5)*player
        for i in range(ROW -4):
            for j in range(ROW-4):
                mt = self.squares[i: i+5 , j: j+5]
                if np.equal(mt.diagonal(),x ).all():
                    if 0 <= i-1 and i+5 < ROW and 0 <= j-1 and j+5 < ROW:
                        if self.squares[i-1][j-1] == neg_col and self.squares[i+5][j+5] == neg_col:
                            continue
                    return ((i,j),(i+4,j+4))
                if np.equal(np.fliplr(mt).diagonal() , x ).all():
                    if 0 <= i-1 and j+5 < ROW and 0 <= j-1 and i+5 < ROW:
                        if self.squares[i-1][j+5] == neg_col and self.squares[i+5][j-1] == neg_col:
                            continue
                    return ((i+4,j),(i,j+4))
        return None

    def check_win(self , player):
        if self.check_row(player) != None:
            return self.check_row(player)
        if self.check_col(player) != None:
            return self.check_col(player)
        if self.check_dia(player) != None:
            return self.check_dia(player)
        return None        

    def draw_win(self, move,player):
        dau = (move[0][1]*SQSIZE + SQSIZE//2 , move[0][0]*SQSIZE + SQSIZE//2)
        cuoi = (move[1][1]*SQSIZE + SQSIZE//2 , move[1][0]*SQSIZE + SQSIZE//2)
        color = CROSS_COLOUR if player ==1 else CIR_COLOUR
        pygame.draw.line(screen, color , dau,cuoi ,LINE_WIDTH) 

    def generate_move(self ):
        moves = []
        for i in range(ROW):
            for j in range(ROW):
                if self.squares[i][j] > 0:
                    continue
                check = 0
                for k in [-1,0,1]:
                    for h in [-1,0,1]:
                        u = i + k
                        t = j+h
                        if 0 <= u < ROW and 0 <= t < ROW:
                            if self.squares[u][t] != 0:
                                moves.append((i,j))
                                check =1 
                                break
                    if check == 1:
                        break        
        return moves

class Ai:
    @classmethod    
    def search_winning_moves(cls , board:Board):
        allpossible_move = board.generate_move()
        for move in allpossible_move:
            temp_board = Board(board = board)
            temp_board.mark_sqr(move[0],move[1],1)
            if temp_board.check_win(1):
                return (None,move)
            temp_board.mark_sqr(move[0],move[1],2)
            if temp_board.check_win(2):
                return (None,move)
        return (None,None)

    @classmethod
    def find_next_move(cls,board : Board,depth):
        value,move = cls.search_winning_moves(board)
        if move != None:
            return move
        else:
            value , move = cls.minmax_alphabeta(board, depth ,-100000000,100000000,True)
            if move != None:
                return move
            else:
                move = (ROW//2 , ROW//2)
        return move
    @classmethod
    def minmax_alphabeta(cls , board: Board , depth , alpha,beta , is_O):
        if depth == 0:
            return (cls.evaluate(board ,not is_O) , None)
        all_possible_moves = board.generate_move()
        all_possible_moves = cls.sortt(board , all_possible_moves)
        if len(all_possible_moves) == 0:
            return (cls.evaluate_board(board, not is_O), None)
        best_move = None
        if is_O:
            best_value = -math.inf
            for move in all_possible_moves:
                temp_board = Board(board= board)
                temp_board.mark_sqr(move[0],move[1],2)
                value , temp = cls.minmax_alphabeta(temp_board, depth-1,alpha,beta,not is_O)
                print((move,value))
                if value > best_value:
                    best_value = value
                    best_move = move
                if value > alpha:
                    alpha = value
                if value >= beta:
                    return (best_value ,best_move)    
        else:
            best_value = math.inf
            for move in all_possible_moves:
                temp_board = Board(board= board)
                temp_board.mark_sqr(move[0],move[1],1)
                value , temp = cls.minmax_alphabeta(temp_board, depth-1,alpha,beta,not is_O)
                if value < best_value:
                    best_value = value
                    best_move = move
                if value < beta:
                    beta = value
                if value <= alpha:
                    return (best_value, best_move)
        return (best_value ,best_move)
    
    @classmethod
    def sortt(cls , board : Board , line):
        def my_func(board, move):
            x, y = move
            count = 0
            size = ROW

            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if 0 <= x+i < size and 0 <= y+j < size:
                        if board.squares[x+i][y+j] != 0:
                            count += 1
            return count

        return sorted(line, key=lambda move: my_func(board, move), reverse=True)

    @classmethod
    def evaluate(cls,board : Board ,is_Oturn):
        X_score = cls.get_score(board , 1)
        O_score = cls.get_score(board , 2)
        return O_score - X_score

    @classmethod
    def get_score(cls, board : Board , player):
        mau = {}
        cls.mau_col( board , mau ,player)
        cls.mau_row( board, mau , player)
        cls.mau_cheo(board ,mau , player)
        return cls.get_score_consecutive(mau)
    
    @classmethod
    def mau_col(cls , board : Board , mau , player):
        board.squares
        for i in range(ROW):
            cls.get_patterns(board.squares[:, i],mau , player)
    @classmethod
    def mau_row(cls , board : Board , mau , player):
        matrix = board.squares
        for i in range(ROW):
            cls.get_patterns(matrix[i] , mau ,player)
    @classmethod
    def mau_cheo(cls, board: Board , mau, player):
        size = ROW
        matrix1 = board.squares
        matrix2 = matrix1[::-1, :]
        for i in range(-size+1, size):
            cls.get_patterns(matrix1.diagonal(i), mau, player)
            cls.get_patterns(matrix2.diagonal(i), mau, player)
    @classmethod
    def get_patterns(cls , line , mau, player):
        col = player
        neg = player%2 + 1
        s = ''
        old = 0
        for i,c in enumerate(line):
            if i == 0:
                s += 'O'
            if c == col:
                if old == neg:
                    s += 'O'
                s += 'X'
            if c != col or i == len(line)-1:
                if c == neg and len(s) > 0:
                    s += 'O'
                elif i == len(line)-1:
                    s += 'O'
                if s in mau.keys():
                    mau[s] += 1
                else:
                    mau[s] = 1
                if i+1 < len(line) and line[i+1] == col and line[i] == 0:
                    pass
                else:
                    s= ''
            old = c         
    @classmethod
    def get_score_consecutive(cls , pattern_dc):
        score = 0
        for pattern in pattern_dc:
            if pattern.count('X') == 5:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                else:
                    score += 10000000
            if pattern.count('X') == 4:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                elif pattern[0] == 'O' or pattern[-1] == 'O':
                    score += 1100 * pattern_dc[pattern]
                else:
                    score += 100000 * pattern_dc[pattern]
            if pattern.count('X') == 3:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                elif pattern[0] == 'O' or pattern[-1] == 'O':
                    score += 100 * pattern_dc[pattern]
                else:
                    score += 1000 * pattern_dc[pattern]
            if pattern.count('X') == 2:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                elif pattern[0] == 'O' or pattern[-1] == 'O':
                    score += 10 * pattern_dc[pattern]
                else:
                    score += 100 * pattern_dc[pattern]
            if pattern.count('X') == 1:
                if pattern[0] == 'O' and pattern[-1] == 'O':
                    pass
                elif pattern[0] == 'O' or pattern[-1] == 'O':
                    score += 1 * pattern_dc[pattern]
                else:
                    score += 5* pattern_dc[pattern]
        return score

class Game:
    def __init__(self):
        self.board = Board()
        self.show_lines()
        self.player = 1
        self.game_over =0

    def show_lines(self):
        #draw vertical
        for i in range (1,ROW):
            pygame.draw.line(screen, LINE_COLOUR ,(SQSIZE*i , 0),(SQSIZE*i , HEIGHT),LINE_WIDTH)
        #draw horizantal
        for i in range (1,COL):
            pygame.draw.line(screen, LINE_COLOUR ,( 0, SQSIZE*i),(WIDTH , SQSIZE*i),LINE_WIDTH)
    
    def change_player(self):
        self.player = self.player%2 + 1
    
    def draw_fig(self,row,col):
        if self.player == 1:
            pygame.draw.line(screen , CROSS_COLOUR , (col*SQSIZE+SPACE , row*SQSIZE+SPACE), ((col+1)*SQSIZE-SPACE , (row+1)*SQSIZE-SPACE),LINE_WIDTH)
            pygame.draw.line(screen , CROSS_COLOUR , (col*SQSIZE+SPACE , (row+1)*SQSIZE-SPACE), ((col+1)*SQSIZE-SPACE , row*SQSIZE+SPACE),LINE_WIDTH)
        if self.player == 2:
            center = (col*SQSIZE + SQSIZE // 2 , row*SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen , CIR_COLOUR , center , SQSIZE / 4, LINE_WIDTH)


def main():
    game = Game()
    while True:
        if game.player == 1 and game.game_over == 0:
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    col= int(pos[0] // SQSIZE)
                    row = int(pos[1] // SQSIZE)
                    if game.board.empty_sqr(row,col):
                        game.board.mark_sqr(row,col , game.player)
                        game.draw_fig(row , col)
                        move = game.board.check_win(game.player)
                        if move != None:
                            game.game_over = 1
                            game.board.draw_win(move , game.player)  
                        game.change_player() 

        elif game.player == 2 and game.game_over == 0:
            move = Ai.find_next_move(game.board ,2)   
            game.board.mark_sqr(move[0],move[1],game.player)
            game.draw_fig(move[0],move[1]) 
            game.change_player()
        else:
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
main()