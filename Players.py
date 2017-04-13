import pygame
from pygame import *
import json
import time
from time import *
import threading
from threading import *
import sys
import datetime
from datetime import datetime, timedelta
import Block
from Block import Block, Screen

left = [pygame.Rect(0,32,32,32), pygame.Rect(32,32,32,32), pygame.Rect(32*2,32,32,32)]
right = [pygame.Rect(0,32*2,32,32), pygame.Rect(32,32*2,32,32), pygame.Rect(32*2,32*2,32,32)]
colors = [pygame.image.load("images/black.png"), pygame.image.load("images/white.png"), pygame.image.load("images/red.png"), pygame.image.load("images/orange.png"), pygame.image.load("images/green.png")]

class Player():
    def __init__(self, window, location, dir_index, screen, bg, col, username):
        self.id = None
        self.image = colors[0]
        self.window = window
        self.ready = False
        self.direction = 'East'
        self.location = location
        self.dir_index = dir_index
        self.state = left[dir_index]
        self.health = 3
        self.sec =.0050
        self.bg = bg
        self.screen = screen
        self.col = col
        self.set_col(self.col)
        self.username = username
        self.no_deaths = 0
        myfont = pygame.font.SysFont("electrb.ttf", 15)
        self.username_font = myfont.render(self.username, 1, (255,255,255))
        self.kills = 0
        self.deaths = 0
        self.suicides = 0
        self.hit = 0
        self.weapon = [[pygame.image.load("images/hammer1.png"),pygame.image.load("images/hammer2.png"),pygame.image.load("images/hammer3.png")]]
        self.weapon.append([pygame.transform.flip(self.weapon[0][0],1,0),pygame.transform.flip(self.weapon[0][1],1,0),pygame.transform.flip(self.weapon[0][2],1,0)])

    def respawn(self):
        self.health = 3
        self.no_deaths += 1
        #sleep(3)
        self.ready = True
                                 
    def set_col(self, col):
        self.col = col
        if self.col == "black":
            self.image = colors[0]
        elif self.col == "white":
            self.image = colors[1]
        elif self.col == "red":
            self.image = colors[2]
        elif self.col == "orange":
            self.image = colors[3]
        elif self.col == "green":
            self.image = colors[4]

    def check_tile_exists(self, start, end):
        exit_loop = False
        for block in self.screen.get_block_list():
            if(block.current == True):
                block.current = False
                pass
            elif(block.current == False):
                if self.location[1] == block.location[1]- 30:
                    if(self.location[0] > block.location[0] - start  and self.location[0] < block.location[0] + end):
                        block.current = True
                        exit_loop = True
                        break
        if(self.location[1] == 350):
            return True
        return exit_loop

    def jump_thread(self, window, index):
        max_height = self.location[1] - 120
        reach_max = False
        #self.window.blit(self.bg, [self.location[0], self.location[1] - 20], pygame.Rect(self.location[0], self.location[1]-10, self.health_img.get_width()+10, self.health_img.get_height() + 10))
        while True:
            #print self.location
            if(reach_max == False and self.location[1] == max_height):
                reach_max = True
            elif(reach_max == False):
                self.location[1] = self.location[1] - 1
                self.render(window, self.location, self.state, sec = .002)
            if(reach_max == True):
                if self.check_tile_exists(20, 40) == True:
                    break
            if(reach_max == True and self.location[1] == 350):
                break
            elif(reach_max == True):
                self.location[1] = self.location[1] + 1
                self.render(window, self.location, self.state, sec =.0025)

    def fall_thread(self, window):
        while True:
            if(self.check_tile_exists(20, 40) == True):
                break
            self.location[1] = self.location[1] + 1
            self.render(window, self.location, self.state, sec = .0025)
        
    def walk(self, window, index):
        window.blit(self.bg, self.location, pygame.Rect(self.location[0], self.location[1], 32, 32))
        if(self.direction == 'West'):
            self.location[0] = self.location[0] - 5
            if(self.dir_index < 2):
                self.dir_index += 1  
            else:
                self.dir_index = 0
            self.state = left[self.dir_index]
        if(self.direction == 'East'):
            self.location[0] = self.location[0] + 5
            if(self.dir_index < 2):
                self.dir_index += 1  
            else:
                self.dir_index = 0
            self.state = right[self.dir_index]
            
        if self.location[0] < 0:
            window.blit(self.bg, [self.location[0] + 5, self.location[1] - 20], pygame.Rect(self.location[0] + 3, self.location[1] -20, 32, 20))
            self.location[0] = window.get_size()[0]
        if self.location[0] > window.get_size()[0]:
            self.location[0] = 0
        self.render(window, self.direction, self.dir_index, self.sec)

    def set_player_health(self):
        myfont = pygame.font.SysFont(None, 13)
        self.username_font = myfont.render(self.username, 1, (255,255,255))
        health_list = [pygame.image.load("images/hbfull.png"), pygame.image.load("images/hbhalf.png"), pygame.image.load("images/hbcritical.png"), pygame.image.load("images/hbdead.png")]
        health_img = None
        if(self.health == 3):
            self.health_img = health_list[0]
        elif(self.health == 2):
            self.health_img = health_list[1]
        elif(self.health == 1):
            self.health_img = health_list[2]
        else:
            self.health_img = health_list[3]
        return self.health_img

    def render_player_health(self, window):
         if(self.health_img != None):
            #window.blit(self.username_font, [self.location[0]+5, self.location[1] - 20])
            window.blit(self.health_img, [self.location[0]+5, self.location[1] - 10])

    def display_username(self, window):
        window.blit(self.username_font, [self.location[0]+5, self.location[1] - 20]) 
        
    def render(self, window, direction, index, sec):
        self.window.blit(self.bg, [self.location[0], self.location[1] - 10], pygame.Rect(self.location[0], self.location[1]-10, self.health_img.get_width()+10, self.health_img.get_height()))
        self.render_player_health(self.window)
        
        if(direction == 'West'):
            self.state = left[index]
        elif(direction == 'East'):
            self.state = right[index]

        self.display_username(self.window)    
        window.blit(self.image, self.location, self.state)
        
        t1 = datetime.now() + timedelta(seconds=sec)
        while(datetime.now() < t1):
            pass
        
    def attack(self, window, players):
        hit = 15
        if(self.direction == 'West' ):
            loc = (self.location[0]-23, self.location[1])
            wpn = [1,loc]
        else:
            loc = (self.location[0]+hit, self.location[1])
            wpn = [0,loc]
        attackrange = 32
        hitplayer = []
        for player in players:
            if(self.location[1] == player.location[1]):
                print "enter if"
                print self.direction,' ', player.location, ' ', self.location
                if (self.direction == 'East' and (player.location[0] <= self.location[0]+attackrange and player.location[0] >= self.location[0])):
                    print self.username," hit ",player.username
                    hitplayer.append(player.col)
                    if(player.health - 1 <= 0):
                        self.kills += 1
                elif(self.direction == 'West' and (player.location[0] <= self.location[0] and player.location[0] >= self.location[0]-attackrange)):
                    print self.username," hit ",player.username
                    hitplayer.append(player.col)
                    if(player.health - 1 <= 0):
                        self.kills += 1
        return hitplayer, wpn
	
    def gotHit(self):
        self.hit += 1
        if(self.hit == 3):
            self.hit = 0
            self.health -= 1
            if(self.health == 0):
                self.deaths += 1
                self.ready = False
