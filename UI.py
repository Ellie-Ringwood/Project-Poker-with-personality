import pygame
import sys
from pygame.locals import *

class UI():
    def __init__(self, table):
        self.table = table
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((960,540))
        self.DISPLAYSURF.fill((255, 255, 255))
        pygame.display.set_caption("Poker")
        self.font = pygame.font.SysFont("Verdana", 20)
    
    def update(self):
        self.input()
        turn = self.font.render(str("Round "+str(self.table.currentRound)+": "+self.table.currentPlayerBetting.name+"'s turn"), True, (0,0,0))
        pot = self.font.render(str("Pot: 8"), True, (0,0,0))
        funds = self.font.render(str("Funds: 5"), True, (0,0,0))
        #funds_so_far = font.render(str("Funds bet so far: "), True, (0,0,0))
        card = self.font.render(str("Card: Queen"), True, (0,0,0))

        call = self.font.render(str("CALL"), True, (0,0,0))
        check = self.font.render(str("CHECK"), True, (0,0,0))
        action_raise = self.font.render(str("RAISE"), True, (0,0,0))
        fold = self.font.render(str("FOLD"), True, (0,0,0))

        confirm_action = self.font.render(str("Confirm action"), True, (0,0,0))
        confirm_next = self.font.render(str("See next player's turn"), True, (255,255,255))
    
        self.DISPLAYSURF.blit(turn, (10,10))
        self.DISPLAYSURF.blit(pot, (10,110))
        self.DISPLAYSURF.blit(funds, (300,110))
        #self.DISPLAYSURF.blit(funds_so_far, (10,160))
        self.DISPLAYSURF.blit(card, (180,210))

       # pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (rect_x, rect_y, rect_width, rect_height))

        self.DISPLAYSURF.blit(call, (50,350))
        self.DISPLAYSURF.blit(check, (150,350))
        self.DISPLAYSURF.blit(action_raise, (280,350))
        self.DISPLAYSURF.blit(fold, (400,350))

        self.DISPLAYSURF.blit(confirm_action, (180,450))
    
        pygame.display.update()
        
    def input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                #if (rect_x <= mouse_x <= rect_x + rect_width and rect_y <= mouse_y <= rect_y + rect_height):
                #    running = False


