import pygame, time, threading
from pygame import *
from time import *
from threading import *
import sys
from time import *
import datetime
from datetime import datetime, timedelta

import Block
from Block import Block, Screen

class Bomb():
    def __init__(self, window, location, screen, bg, player):
        self.bomb = []
        self.bomb.append(pygame.image.load("images/EXPLO0.png"))
        self.bomb.append(pygame.image.load("images/EXPLO1.png"))
        self.bomb.append(pygame.image.load("images/EXPLO2.png"))
        self.bomb.append(pygame.image.load("images/EXPLO3.png"))
        self.bomb.append(pygame.image.load("images/EXPLO4.png"))
        self.bomb.append(pygame.image.load("images/EXPLO5.png"))
        self.bomb.append(pygame.image.load("images/EXPLO6.png"))
        self.bg = bg
        self.window = window
        self.id = None
        self.location = location
        self.index = 0
        self.activate = True
        self.screen = screen
        self.thread = Thread(None)
        self.owner = player

    def check_tile_exists(self, start, end):
        exit_loop = False
        for block in self.screen.get_block_list():
            if(block.current == True):
                block.current = False
                pass
            elif(block.current == False):
                if (self.location[1] == block.location[1] - 30):
                    if(self.location[0] > block.location[0] - start  and self.location[0] < block.location[0] + end):
                        block.current = True
                        exit_loop = True
                        break
        if(self.location[1] == 350):
            return True
        return exit_loop

    def bomb_fall(self):
        while True:
            if(self.check_tile_exists(20, 40) == True):
                break
            self.window.blit(self.bg, self.location, pygame.Rect(self.location[0], self.location[1], self.bomb[1].get_width(), self.bomb[1].get_width()))
            self.location[1] = self.location[1] + 1
            sleep(.001)
            self.window.blit(self.bomb[0], self.location)

    def render(self, window, players, meplayer, bg):
        self.index = 1
        minus_health = False
        killed_players = False
        while(self.index < len(self.bomb)):
            explode_extent = 175
            rightlocation = [0,0]
            leftlocation = [0,0]
            rightlocation[0] = self.location[0]
            rightlocation[1] = self.location[1]
            leftlocation[0] = self.location[0]
            leftlocation[1] = self.location[1]
            if(minus_health == False and (meplayer.location[1] <= self.location[1] and meplayer.location[1] > self.location[1] - self.bomb[1].get_height())  and (meplayer.location[0] > rightlocation[0] - explode_extent and meplayer.location[0] < rightlocation[0] + explode_extent)):
                meplayer.health -= 1
                minus_health = True
                if(meplayer.health == 0):
                    meplayer.deaths += 1
                    meplayer.ready = False
                    if meplayer.col == self.owner.col:
                        meplayer.suicides += 1
                    else:
                        killed_players = True
            while rightlocation[0] < self.location[0] + explode_extent:
                window.blit(self.bomb[self.index], self.location)
                window.blit(self.bomb[self.index], rightlocation)
                window.blit(self.bomb[self.index], leftlocation)
                rightlocation[0] += 30
                leftlocation[0] -= 30
            self.index += 1
            sleep(.055)
            window.blit(bg, self.location, pygame.Rect(self.location[0], self.location[1], self.bomb[1].get_width() + explode_extent, self.bomb[1].get_width() ))
            window.blit(bg, [self.location[0] - explode_extent, self.location[1]], pygame.Rect(self.location[0] - explode_extent, self.location[1], self.bomb[1].get_width() + explode_extent, self.bomb[1].get_height()))
        self.activate = False
        if(killed_players == True):
            return self.owner
        else:
            return None
        
        
    def place(self, window):
        t1 = datetime.now() + timedelta(seconds=1)
        if(not self.thread.isAlive() and self.check_tile_exists(20, 40) == False):
            self.thread = Thread(target = self.bomb_fall, args = ())
            self.thread.start()
        while(datetime.now() < t1):
            window.blit(self.bomb[0], self.location)
            pass
