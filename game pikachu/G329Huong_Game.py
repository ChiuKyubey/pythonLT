from asyncio.windows_events import NULL
import os
import pygame
import numpy as np
import random
import time
clear = lambda: os.system('cls')

class Game:
    def __init__(self):
        pygame.init()

        self.screenWidth = 1000
        self.screenHeight = 650

        self.screen = pygame.display.set_mode((self.screenWidth , self.screenHeight))

        self.icon = pygame.image.load('icon.jpg')
        
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption('Game PiKaChu')
        self.background = pygame.image.load('Background.jpg')
        self.screen.blit(self.background , (0 , 0))
        

        self.running = True

        self.dangchoi = False

        # Button

        self.button = Button(self)

        #Board

        self.board = Board(self)

        #TranScript
        self.transcript = transcript(self)
        #TimeBar
        self.time_bar = Time_bar(self)

        self.befor_x = 0
        self.befor_y = 0
        self.qual_click = 0

        self.count_draw_change = 0
        self.count_draw_replay = 0
        self.is_btnchange_check_in = False
        self.is_btnreplay_check_in = False

        # time
        self.current_time = int(time.time()) + 1
        self.cout = 0 
    def re_draw(self):
        self.screen.blit(self.background , (0 , 0))
        self.board.draw()
        self.button.draw()
        self.transcript.draw()
        self.time_bar.draw()

    def draw_border_rect(self , rect):
        if rect != 0:
            color_red = (255 , 0 , 0)
            pygame.draw.line(self.screen , color_red , ( rect.x - 1 , rect.y - 3 ) , (rect.x + rect.width + 1 , rect.y - 3 ) )
            pygame.draw.line(self.screen , color_red , (rect.x + rect.width + 1 , rect.y ) , (rect.x + rect.width + 1 , rect.y + rect.height + 1) )
            pygame.draw.line(self.screen , color_red , ( rect.x - 1 , rect.y + rect.height + 1 ) , (rect.x + rect.width + 1 , rect.y + rect.height + 1) )
            pygame.draw.line(self.screen , color_red , ( rect.x - 1 , rect.y + rect.height + 1 ) , ( rect.x - 1 , rect.y - 1 ) )

    def draw_link_two_point(self , p1 , p2 , check  ):

        rect_min_y = self.board.random_Board[p1[1]][p1[0]].get_rect()
        rect_min_y.x = self.board.board_x + (self.board.rect_piece_width * (p1[0] - 1))
        rect_min_y.y = self.board.board_y + (self.board.rect_piece_height * (p1[1] - 1))

        rect_max_y = self.board.random_Board[p2[1]][p2[0]].get_rect()
        rect_max_y.x = self.board.board_x + (self.board.rect_piece_width * (p2[0] - 1))
        rect_max_y.y = self.board.board_y + (self.board.rect_piece_height * (p2[1] - 1))

        if p1[1] > p2[1]:
            rect_min_y = self.board.random_Board[p2[1]][p2[0]].get_rect()
            rect_min_y.x = self.board.board_x + (self.board.rect_piece_width * (p2[0] - 1))
            rect_min_y.y = self.board.board_y + (self.board.rect_piece_height * (p2[1] - 1))

            rect_max_y = self.board.random_Board[p1[1]][p1[0]].get_rect()
            rect_max_y.x = self.board.board_x + (self.board.rect_piece_width * (p1[0] - 1))
            rect_max_y.y = self.board.board_y + (self.board.rect_piece_height * (p1[1] - 1))

        color_red = (255 , 0 , 0)
        color_green = (0 , 255 , 0)
        color_blue = ( 0 , 0 , 255)
        if check[0] == 1 :
            pygame.draw.line(self.screen , color_red , rect_min_y.center , rect_max_y.center , 5 )
        elif check[0] == 2 :
            rect3 = pygame.Rect(rect_min_y.left , rect_min_y.top , rect_min_y.width , rect_min_y.height)
            rect3.x = self.board.board_x + (self.board.rect_piece_width * (check[1][0] - 1))
            rect3.y = self.board.board_y + (self.board.rect_piece_height * (check[1][1] - 1))
            pygame.draw.line(self.screen , color_red , rect_min_y.center , rect3.center , 5 )
            pygame.draw.line(self.screen , color_red , rect_max_y.center , rect3.center , 5 )

        elif check[0] == 3 :

            rect3 = pygame.Rect(rect_min_y.left , rect_min_y.top , rect_min_y.width , rect_min_y.height)
            rect3.x = self.board.board_x + (self.board.rect_piece_width * (check[1][0] - 1))
            rect3.y = self.board.board_y + (self.board.rect_piece_height * (check[1][1] - 1))

            rect4 = pygame.Rect(rect_min_y.left , rect_min_y.top , rect_min_y.width , rect_min_y.height)
            rect4.x = self.board.board_x + (self.board.rect_piece_width * (check[2][0] - 1))
            rect4.y = self.board.board_y + (self.board.rect_piece_height * (check[2][1] - 1))

            pygame.draw.line(self.screen , color_red , rect_min_y.center , rect3.center , 5 )
            pygame.draw.line(self.screen , color_green , rect3.center , rect4.center , 5 )
            pygame.draw.line(self.screen , color_blue , rect4.center , rect_max_y.center , 5 )


    def check_two_point(self , p1 , p2):

        min_x = p1[0]
        max_x = p2[0]
        min_y = p1[1]
        max_y = p2[1]

        if p1[0] > p2[0]:
            min_x = p2[0]
            max_x = p1[0]
        if p1[1] > p2[1]:
            min_y = p2[1]
            max_y = p1[1]
        
        if p1[1] == p2[1] :
            type = 1
            checkMoreRect_y  = self.checkMoreRect_y(p1 , p2 , type)

            if checkMoreRect_y[0] == 0:
                type = -1
                checkMoreRect_y  = self.checkMoreRect_y(p1 , p2 , type)

            check = self.checkLine_x(min_x , max_x , p1[1])

            if check[0] == 0:
                check = checkMoreRect_y
            
            return check
        elif p1[0] == p2[0] :

            #checkMoreRectX
            type = 1
            checkMoreRect_x = self.checkMoreRect_x(p1 , p2 , type)

            if checkMoreRect_x[0] == 0:
                type = -1
                checkMoreRect_x = self.checkMoreRect_x(p1 , p2 , type)

            check = self.checkLine_y(min_y , max_y , p1[0])

            if check[0] == 0:
                check = checkMoreRect_x
            
            return check
        else:
            #checkMoreRect_X
            type = 1
            checkMoreRect_x  = self.checkMoreRect_x(p1 , p2 , type)

            if checkMoreRect_x[0] == 0:
                type = -1
                checkMoreRect_x  = self.checkMoreRect_x(p1 , p2 , type)
            type = 1
            checkMoreRect_y  = self.checkMoreRect_y(p1 , p2 , type)

            if checkMoreRect_y[0] == 0:
                type = -1
                checkMoreRect_y = self.checkMoreRect_y(p1 , p2 , type)

            check = self.checkRect_x(p1 , p2)

            if check[0] == 0:
                check = self.checkRect_y(p1 , p2)
                if check[0] == 0:
                    check = checkMoreRect_x
                    if check[0] == 0:
                        check = checkMoreRect_y

            return check
        
    # type != null ktra luôn 2 đầu
    def checkLine_x(self, x1 , x2 , y , type = NULL):
        min_x = x1 
        max_x = x2

        if x1 > x2:
            min_x = x2
            max_x = x1

        if min_x  + 1  == max_x - 1  and self.board.random_Board[y][min_x+1] != -1:
            return 0 , (0 , 0)

        if type != NULL:
            for i in range(min_x , max_x + 1):
                if self.board.random_Board[y][i] != -1:
                    return 0 , (0 , 0)
            
        for i in range(min_x + 1 , max_x ):
            if self.board.random_Board[y][i] != -1:
                return 0 , (0 , 0)
        if min_x + 1 == max_x:
            return 1 , (0 , 0)
        return 1 , (0 , 0)
    
    # type != null ktra luôn 2 đầu
    def checkLine_y(self , y1 , y2 , x , type = NULL):
        min_y = y1
        max_y = y2
        
        if y1 > y2 :
            min_y = y2
            max_y = y1

        if min_y  + 1  == max_y - 1 and self.board.random_Board[min_y+1][x] != -1:
            return 0 , (0 , 0)

        if type != NULL:
            for i in range(min_y , max_y + 1):
                if self.board.random_Board[i][x] != -1:
                    return 0 , (0 , 0)
        
        for i in range(min_y + 1 , max_y ):
            if self.board.random_Board[i][x] != -1:
                return 0 , (0 , 0)

        if min_y + 1 == max_y:
            return 1 , (0 , 0)
        return 1 , (0 , 0)
    
    # có đường thì return True , ko thì False  
    def checkRect_x(self , p1 , p2):
        p_min_x = p1
        p_max_x = p2
        if p1[0] > p2[0]:
            p_min_x = p2
            p_max_x = p1
        for i in range(p_min_x[0] , p_max_x[0] + 1):
            if i == p_min_x[0]:
                if self.checkLine_y(p_min_x[1] , p_max_x[1] , i)[0] and self.checkLine_x(p_min_x[0] , p_max_x[0] , p_max_x[1])[0]:
                    if self.board.random_Board[p_max_x[1]][p_min_x[0]] == -1:
                        return 2 , (i , p_max_x[1])
            elif i == p_max_x[0]:
                if self.checkLine_x(p_min_x[0] , p_max_x[0] , p_min_x[1])[0] and self.checkLine_y(p_min_x[1] , p_max_x[1] , p_max_x[0])[0]:
                    if self.board.random_Board[p_min_x[1]][p_max_x[0]] == -1:
                        return 2 , (i , p_min_x[1])
            elif i == p_min_x[0] + 1:
                if self.checkLine_y(p_min_x[1] , p_max_x[1] , i , 1 )[0] and self.checkLine_x(i , p_max_x[0] , p_max_x[1])[0]:
                    return 3 , (i , p_min_x[1]) , (i , p_max_x[1])
            elif i == p_max_x[0] - 1:
                if self.checkLine_x(p_min_x[0] , i , p_min_x[1])[0] and self.checkLine_y(p_min_x[1] , p_max_x[1] , i , 1)[0]:
                    return 3 , (i , p_min_x[1]) , (i , p_max_x[1])
            elif self.checkLine_x(p_min_x[0] , i , p_min_x[1] )[0] and self.checkLine_y(p_min_x[1] , p_max_x[1] , i , 1)[0] and self.checkLine_x(i , p_max_x[0] , p_max_x[1])[0]:
                return 3 , (i , p_min_x[1]) , (i , p_max_x[1])
        return 0 , (0 , 0)
    
    def checkRect_y(self ,p1 , p2):
        p_min_y = p1
        p_max_y = p2
        if p1[1] > p2[1]:
            p_min_y = p2
            p_max_y = p1
        for i in range(p_min_y[1] , p_max_y[1] + 1):
            if i == p_min_y[1]:
                if self.checkLine_x(p_min_y[0] , p_max_y[0] , p_min_y[1])[0] and self.checkLine_y(p_min_y[1] , p_max_y[1] , p_max_y[0])[0]:
                    if self.board.random_Board[p_min_y[1]][p_max_y[0]] == -1:
                        return 2 , (p_max_y[0] , i)
            elif i == p_max_y[1]:
                if self.checkLine_y(p_min_y[1] , p_max_y[1] , p_min_y[0])[0] and self.checkLine_x(p_min_y[0] , p_max_y[0] , p_max_y[1])[0]:
                    if self.board.random_Board[p_max_y[1]][p_min_y[0]] == -1:
                        return 2 , (p_min_y[0] , i)
            elif i == p_min_y[1] + 1:
                if self.checkLine_x(p_min_y[0] , p_max_y[0] , i , 1)[0] and self.checkLine_y(i , p_max_y[1] , p_max_y[0])[0]:
                    return 3 , (p_min_y[0] , i ) , (p_max_y[0] , i)
            elif i == p_max_y[1] - 1:
                if self.checkLine_y(p_min_y[1] , p_max_y[1] , i )[0] and self.checkLine_x(p_min_y[0] , p_max_y[0] , i , 1)[0]:
                    return 3 , (p_min_y[0] , i ) , (p_max_y[0] , i)
            elif self.checkLine_y(p_min_y[1] , i , p_min_y[0] )[0] and self.checkLine_x(p_min_y[0] , p_max_y[0] , i , 1)[0] and self.checkLine_y(i , p_max_y[1] , p_max_y[0])[0]:
                return 3 , (p_min_y[0] , i ) , (p_max_y[0] , i)
        return 0 , (0 , 0)

# check thêm sang phải

    def checkMoreRect_x(self ,p1 , p2 , type = 1 ):
        p_min_x = p1
        p_max_x = p2
        if p1[0] > p2[0]:
            p_min_x = p2
            p_max_x = p1
        p_start = [p_max_x[0] , p_min_x[1]]
        if type == -1:
            p_start = [p_min_x[0] , p_max_x[1]]

        # check start Point
        check_start_point = self.board.random_Board[p_start[1]][p_start[0]] == -1
        
        if p1[0] == p2[0]:
            check_start_point = True
        if self.checkLine_x(p_min_x[0] , p_max_x[0] , p_start[1])[0] and check_start_point:
            if type == 1:
                for i in range(p_start[0] + 1, self.board.random_Board[p_start[1]].__len__()):
                    if i == p_start[0] + 1 :
                        if self.checkLine_y(p_min_x[1] , p_max_x[1] , i , 1)[0]:
                            return 3 , (i , p_min_x[1]) , (i , p_max_x[1])
                    elif self.checkLine_x(p_start[0] , i , p_start[1])[0] and self.checkLine_y(p_min_x[1] , p_max_x[1] , i , 1)[0] and self.checkLine_x(i , p_max_x[0] , p_max_x[1])[0]:
                        return 3 , (i , p_min_x[1]) , (i , p_max_x[1])
            elif type == -1:
                for i in range(p_start[0] - 1 , -1 , -1):
                    if i == p_start[0] -1 :
                        if self.checkLine_y(p_min_x[1] , p_max_x[1] , i , 1)[0]:
                            return 3 , (i , p_min_x[1]) , (i , p_max_x[1])
                    elif self.checkLine_x(p_min_x[0] , i , p_min_x[1])[0] and self.checkLine_y(p_min_x[1] , p_max_x[1] , i , 1)[0] and self.checkLine_x(i , p_start[0] , p_max_x[1])[0]:
                        return 3 , (i , p_min_x[1]) , (i , p_max_x[1])
        return 0 , (0 , 0)
# check thêm sang trái 

    def checkMoreRect_y(self , p1 , p2 , type = 1):
        p_min_y = p1
        p_max_y = p2
        if p1[1] > p2[1]:
            p_min_y = p2
            p_max_y = p1
        p_start = [p_max_y[0] , p_min_y[1]]
        if type == -1:
            p_start = [p_min_y[0] , p_max_y[1]]
        check_start_point = self.board.random_Board[p_start[1]][p_start[0]] == -1
        if p1[1] == p2[1]:
            check_start_point = True
        if self.checkLine_y(p_min_y[1] , p_max_y[1] , p_start[0])[0] and check_start_point:
            if type == 1:
                for i in range(p_min_y[1] - 1 , -1 , -1):
                    if i == p_min_y[1] + 1:
                        if self.checkLine_x(p_min_y[0] , p_max_y[0] , i , 1)[0]:
                            return 3 , (p_min_y[0] , i ) , (p_max_y[0] , i)
                    elif self.checkLine_y(p_min_y[1] , i , p_min_y[0])[0] and self.checkLine_x(p_min_y[0] , p_max_y[0] , i ,1)[0] and self.checkLine_y(i , p_start[1] , p_max_y[0])[0]:
                        return 3 , (p_min_y[0] , i ) , (p_max_y[0] , i)
            elif type == -1:
                for i in range(p_start[1] + 1, self.board.random_Board.__len__()):
                    if i == p_start[1] + 1:
                        if self.checkLine_x(p_min_y[0] , p_max_y[0] , i , 1)[0]:
                            return 3 , (p_min_y[0] , i ) , (p_max_y[0] , i)
                    elif self.checkLine_y(p_start[1] , i , p_min_y[0])[0] and self.checkLine_x(p_min_y[0] , p_max_y[0] , i , 1)[0] and self.checkLine_y(i , p_max_y[1] , p_max_y[0])[0]:
                        return 3 , (p_min_y[0] , i ) , (p_max_y[0] , i)
        return 0 , (0 , 0)
    
    def evenhand(self):
        for event in pygame.event.get(): 
            mouse_click_down = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click_down = pygame.mouse.get_pos()
                if self.button.btnChange_rect.collidepoint(mouse_click_down):
                    if self.transcript.quanti_change > 0:
                        self.board.mix_matran()
                        self.transcript.update_quanti_change()
                        self.re_draw()
                elif self.button.btnreplay_rect.collidepoint(mouse_click_down):
                    self.board = Board(self)
                    self.transcript = transcript(self)
                    self.time_bar = Time_bar(self)
                    self.re_draw()
                elif self.board.board_rect.collidepoint(mouse_click_down):
                    point = (mouse_click_down[0] - self.board.board_x , mouse_click_down[1] - self.board.board_y)
                    x = point[0] / self.board.rect_piece_width + 1
                    y = point[1] / self.board.rect_piece_height + 1
                    
                    x = int(x)
                    y = int(y)

                    if self.board.random_Board[y][x] != -1:
                        rect = self.board.random_Board[y][x].get_rect()
                        rect.x = self.board.board_x + (self.board.rect_piece_width * (x - 1))
                        rect.y = self.board.board_y + (self.board.rect_piece_height * (y - 1))

                        self.screen.blit(self.background , (0 , 0))
                        self.qual_click += 1
                        if self.qual_click == 2 :
                            if x != self.befor_x or y != self.befor_y:
                                p1 = [self.befor_x , self.befor_y]
                                p2 = [x , y]
                                check = self.check_two_point(p1 , p2)
                                if check[0] and self.board.random_Board[y][x] == self.board.random_Board[self.befor_y][self.befor_x]:
                                    self.board.draw()
                                    self.button.draw()
                                    
                                    self.transcript.update_point()
                                    self.transcript.draw()

                                    self.time_bar.draw()
                                    
                                    self.draw_link_two_point(p1 , p2 , check)
                                    pygame.display.flip()
                                    pygame.time.delay(200)
                                    self.board.random_Board[y][x] = -1
                                    self.board.random_Board[self.befor_y][self.befor_x] = -1
                                    
                                    rect = 0
                            self.qual_click = 0
                        self.re_draw()
                        self.draw_border_rect(rect)

                        
                        self.befor_x = x
                        self.befor_y = y
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    point = (mouse_click_down[0] - self.board.board_x , mouse_click_down[1] - self.board.board_y)
                    x = point[0] / self.board.rect_piece_width + 1
                    y = point[1] / self.board.rect_piece_height + 1
                    
                    x = int(x)
                    y = int(y)

                    self.board.random_Board[y][x] = -1
                    self.screen.blit(self.background , (0 , 0))
                    self.re_draw()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if self.button.btnChange_rect.collidepoint(mouse_pos):
                    self.is_btnchange_check_in = True
                elif self.button.btnChange_rect.collidepoint(mouse_pos) == False:
                    self.is_btnchange_check_in = False
                if self.button.btnreplay_rect.collidepoint(mouse_pos):
                    self.is_btnreplay_check_in = True
                elif self.button.btnreplay_rect.collidepoint(mouse_pos) == False:
                    self.is_btnreplay_check_in = False

                if self.is_btnchange_check_in and self.count_draw_change == 0:
                    self.button.btnChange.set_alpha(100)
                    self.re_draw()
                    self.count_draw_change = 1
                elif self.is_btnchange_check_in == False and self.count_draw_change == 1:
                    self.button.btnChange.set_alpha(255)
                    self.re_draw()
                    self.count_draw_change = 0
                elif self.is_btnreplay_check_in and self.count_draw_replay == 0:
                    self.button.btnreplay.set_alpha(100)
                    self.re_draw()
                    self.count_draw_replay = 1
                elif self.is_btnreplay_check_in == False and self.count_draw_replay == 1:
                    self.button.btnreplay.set_alpha(255)
                    self.re_draw()
                    self.count_draw_replay = 0

    def main(self):

        self.button.draw()
            
        self.board.draw()

        self.transcript.draw()

        self.time_bar.draw()
        
        while(self.running):
            if self.current_time == int(time.time()):
                self.time_bar.update()
                self.re_draw()
                self.current_time = int(time.time()) + 1

            if self.time_bar.height_time == 0:
                self.board = Board(self)
                self.transcript = transcript(self)
                self.time_bar = Time_bar(self)
                self.re_draw()

            if self.board.ktra_matran1(self.board.random_Board):
                self.transcript.current_round += 1
                self.board = Board(self)
                self.time_bar = Time_bar(self)
                self.re_draw()

            self.evenhand()
            
            pygame.display.flip()

class Board:
    def __init__(self , game):

        # width + heigh of piece
        self.rect_piece_width = 40
        self.rect_piece_height = 50

        # start position
        self.board_x = 200
        self.board_y = 80

        #quantidy of row and col
        # cột
        self.quati_col = 16
        # hàng
        self.quati_row = 9

        # width + height of board
        self.width = self.rect_piece_width * self.quati_col
        self.height = self.rect_piece_height * self.quati_row

        self.screen = game.screen
        self.board_rect = pygame.Rect(self.board_x , self.board_y , self.width , self.height)

        self.random_Board = self.random_board()
    def draw(self ):
        
        x = self.board_x
        y = self.board_y
        for i in range(1 ,  self.quati_row + 1):
            for j in range(1 ,  self.quati_col + 1):
                if (x >= self.width + self.board_x):
                    y += self.rect_piece_height
                    x = self.board_x
                if self.random_Board[i][j] != -1:
                    self.screen.blit( self.random_Board[i][j] , (x , y , self.rect_piece_width , self.rect_piece_height))
                x += self.rect_piece_width
    def update(self):
        pass
    def get_list_pikachu(self , path):
        ds_pikachu = []
        for _,_, files in os.walk(path):
            for file in files:
                img = pygame.image.load(path + file)
                
                ds_pikachu.append(img)
        return ds_pikachu
    def random_board(self ):
        self.list_pikachu = self.get_list_pikachu('./image/')
        arr = np.full((self.quati_row + 2 , self.quati_col + 2 ) , -1 ,pygame.Surface)
        while self.ktra_matran(arr):

            rand_n = random.randint( 1 , self.quati_row )
            rand_m = random.randint( 1 , self.quati_col)
            
            #
            a = self.list_pikachu[random.randint(0, self.list_pikachu.__len__() - 1)]
            mini_loop = True
            
            if (arr[rand_n][rand_m] == -1):
                arr[rand_n][rand_m] = a
                while mini_loop:
                    rand_n = random.randint( 1 , self.quati_row )
                    rand_m = random.randint( 1 , self.quati_col )
                    if (arr[rand_n][rand_m] == -1):
                        arr[rand_n][rand_m] = a
                        mini_loop = False
        return arr
    # True nếu có -1 trong ma trận , False nếu ko có -1 trong ma trận
    def ktra_matran(self , arr ):
        # hàng
        for i in range( 1 , self.quati_row + 1):
            # cột
            for j in range( 1 , self.quati_col + 1):
                if arr[i][j] == -1 :
                    return True
        return False
    # true nếu trong ma trận toàn giá trị -1  , false nếu có khác -1
    def ktra_matran1(self , arr):
        for i in range( 1 , self.quati_row + 1):
            # cột
            for j in range( 1 , self.quati_col + 1):
                if arr[i][j] != -1 :
                    return False
        return True

    def mix_matran(self):
        arr = np.full((self.quati_row  , self.quati_col ) , -1 , pygame.Surface)
        for i in range(0 , self.quati_row):
            for j in range(0 , self.quati_col):
                arr[i][j] = self.random_Board[i+1][j+1]

        for i in range(6):
            arr = np.transpose(arr)
            for j in arr:
                random.shuffle(j)

        for i in range(0 , self.quati_row):
            for j in range(0 , self.quati_col):
                self.random_Board[i+1][j+1] = arr[i][j]

class Button:
    def __init__(self , game):
        self.btnChange = pygame.image.load('btnchange.png')
        self.btnreplay = pygame.image.load('btnreplay.png')
        

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        #self.btnChange_rect = self.btnChange.get_rect()
        #self.btnreplay_rect = self.btnreplay.get_rect()

        #self.btnChange_rect = (300 , 550 )
        #self.btnreplay_rect = (300 + self.btnreplay_rect.width + 100 , 550 )

        self.btnChange_rect = pygame.Rect(300 , 550 , self.btnChange.get_width() , self.btnChange.get_height())
        
        self.btnreplay_rect = pygame.Rect(300 + self.btnChange_rect.width + 100 , 550 , self.btnreplay.get_width() , self.btnreplay.get_height())


    def draw(self):
        self.screen.blit(self.btnChange , self.btnChange_rect)
        self.screen.blit(self.btnreplay , self.btnreplay_rect)

class transcript:
    def __init__(self , game):
        self.font = pygame.font.SysFont('timesnewroman', 50)

        self.point = 0
        self.quanti_change = 10
        self.current_round = 1

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.white = ( 255 , 255 , 255)

        self.dr_point = self.font.render(str(self.point) , True , self.white)
        self.dr_quanti_change = self.font.render(str(self.quanti_change) , True , self.white)
        self.dr_current_round = self.font.render(str(self.current_round) , True , self.white)

        self.dr_point_rect = self.dr_point.get_rect()
        self.dr_point_rect.x = 65
        self.dr_point_rect.y = 450
        self.dr_quanti_change_rect = self.dr_quanti_change.get_rect()
        self.dr_quanti_change_rect.x = 64
        self.dr_quanti_change_rect.y = 300
        self.dr_current_round_rect = self.dr_current_round.get_rect()
        self.dr_current_round_rect.x = 65
        self.dr_current_round_rect.y = 150

    def draw(self ):
        self.screen.blit(self.dr_point , self.dr_point_rect)
        self.screen.blit(self.dr_quanti_change , self.dr_quanti_change_rect)
        self.screen.blit(self.dr_current_round , self.dr_current_round_rect)
    def update_point(self):
        self.point += 10
        self.dr_point = self.font.render(str(self.point) , True , self.white)
    def update_quanti_change(self):
        self.quanti_change -= 1
        self.dr_quanti_change = self.font.render(str(self.quanti_change) , True , self.white)
    def update_current_round(self):
        self.current_round += 1
        self.dr_current_round = self.font.render(str(self.current_round) , True , self.white)

class Time_bar:
    def __init__(self , game):
        self.time = 225
        self.height_time = 450
        self.width_time = 50
        self.kc = self.height_time / self.time
        self.time_bar = pygame.Surface((self.width_time , self.height_time))
        self.time_bar_rect = self.time_bar.get_rect()
        self.time_bar_rect.x = 900
        self.time_bar_rect.y = 70
        #self.time_bar_rect.bottomright = (950 , 520)

        self.screen = game.screen
    def draw(self):
        self.screen.blit(self.time_bar , self.time_bar_rect )
    def update(self):
        if self.height_time >= self.kc:
            self.height_time -= self.kc
            self.time_bar_rect.y += self.kc
            self.time_bar = pygame.Surface((50 , self.height_time))
        else:
            self.height_time = 0
            self.time_bar = pygame.Surface((50 , self.height_time))

if __name__ == '__main__':
    game = Game()
    game.main()
