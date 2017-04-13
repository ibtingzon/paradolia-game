import pygame
from pygame import *
import socket
import json
import time
from time import *
import threading
from threading import *
import sys

import Players
from Players import Player

import Bomb
from Bomb import Bomb

import Block
from Block import Block, Screen

import Health
from Health import Health

buff_size = 6096

class Game():            
    def __init__(self, window, bg):
        #Initialize Game
        print("Initializing game")
        pygame.init()
        pygame.key.set_repeat(1, 1)
        self.window = window
        
        #Player List
        self.players = []
        self.players_id = []

        #Background Setting
        self.bg = bg
        self.window.blit(self.bg, [0,0])
        self.killer = None

        #Bomb Settings
        self.bomb_list = []
        self.bomb_thread = Thread(None)

    def render_players(self):
            for p in self.players:
                if(p.ready == True):
                        p.render(self.window, p.direction, p.dir_index, p.sec)

    def create_bomb(self, bomb_coordinates, screen, player):
            bomb = Bomb(self.window, bomb_coordinates, screen, self.bg, player)
            self.bomb_list.append(bomb)

    def thread_bomb(self, bomb, meplayer):
            bomb.place(self.window)
            self.killer = bomb.render(self.window, self.players, meplayer, self.bg)
            
    def display_bomb(self, meplayer): 
            for bomb in self.bomb_list:
                    if bomb.activate == True:
                            self.bomb_thread = Thread(target = self.thread_bomb, args = (bomb, meplayer))
                            self.bomb_thread.start()
                            bomb.activate = False

    def clear_bomb_list(self):
            for bomb in self.bomb_list:
                    if bomb.activate == False:
                            self.bomb_list.remove(bomb)

    def get_players_list(self):
        return self.players, self.meplayer

    def print_attack(self, window, direction, location):
        for i in range(3):
            window.blit(self.meplayer.weapon[direction][i], location)
            sleep(.25)        
        
    def main(self, meplayer, screen, conn, me):
        self.meplayer = meplayer
        health = Health(self.window, meplayer)
        thread = Thread(None)
        
        bomb = None
        bomb_coordinates = [-1,-1]
        clock = pygame.time.Clock()
        
        font = pygame.font.Font("V5PRC___.ttf", 20)
        font_disc = pygame.font.SysFont(None, 20)

        frame_count = 0
        frame_rate = 20
        start_time = 45
        total_seconds = 1
        seconds = 0
        minutes = 0

        disconnect = False
        stop = False

        hitplayer = []
        wpn = []
        player_disconnect = None
        string = ""
        
        while True:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            if disconnect == False:
                if self.killer != None:
                    print self.killer.col
                    data = json.dumps([meplayer.location, meplayer.direction, meplayer.dir_index, meplayer.ready, bomb_coordinates, meplayer.col, meplayer.health, meplayer.username, frame_count, meplayer.kills, meplayer.deaths, self.killer.col, meplayer.suicides, hitplayer, wpn])
                else:
                    data = json.dumps([meplayer.location, meplayer.direction, meplayer.dir_index, meplayer.ready, bomb_coordinates, meplayer.col, meplayer.health, meplayer.username, frame_count, meplayer.kills, meplayer.deaths, None, meplayer.suicides, hitplayer, wpn])
                self.killer = None
                hitplayer = []
                wpn = []
                conn.send(data)
                data = json.loads(conn.recv(buff_size))
    
            bomb_coordinates = [-1,-1]
            self.clear_bomb_list()
            total_seconds = start_time - (frame_count // frame_rate)
        
            for id_ in data.keys():
                    if len(data[id_]) != 4 and id_ != me:
                            if id_ not in self.players_id:
                                    print str(id_), data[id_], len(data[id_])
                                    self.players_id.append(id_)
                                    if(len(data[id_]) == 0):
                                        new_char = Player(self.window, [300, 350], 0, screen, self.bg, "black", "")
                                    else:
                                        new_char = Player(self.window, data[id_][0], data[id_][2], screen, self.bg, data[id_][5], "")
                                    new_char.id = id_
                                    self.players.append(new_char)
                            elif id_ in self.players_id:
                                    if(data[id_][11] != None):
                                        if data[id_][11] == meplayer.col:
                                            meplayer.kills += 1
                                    if(len(data[id_][13]) != 0):
                                                    for player in data[id_][13]:
                                                        if player == meplayer.col:
                                                            meplayer.gotHit()
                                    if(len(data[id_][14]) != 0):
                                                    hit_thread = Thread(target = self.print_attack, args=(self.window, data[id_][14][0], data[id_][14][1]))
                                                    hit_thread.start()
                                    for p in self.players:
                                            if(p.id == id_ and len(data[id_]) != 0):
                                                if(p.ready == True):
                                                    self.window.blit(self.bg, [p.location[0] -10 , p.location[1] -50], pygame.Rect(p.location[0] -10, p.location[1] -50, 80, 100))
                                                p.location = data[id_][0]
                                                p.direction = data[id_][1]
                                                p.dir_index = data[id_][2]
                                                p.ready = data[id_][3]
                                                p.set_col(data[id_][5])
                                                p.health = data[id_][6]
                                                p.username = data[id_][7]
                                                p.suicides = data[id_][12]
                                                if(data[id_][9] > p.kills):
                                                    p.kills = data[id_][9]
                                                p.set_player_health()
                                                if data[id_][8] < frame_count:
                                                    frame_count = data[id_][8]
                                                p.deaths = data[id_][10]
                                                if(data[id_][4] != [-1,-1] ):
                                                    self.create_bomb(data[id_][4], screen, p)
            
                                                    

            if(total_seconds == 0):
                stop = True
                disconnect = True
                
            if disconnect == True:
                data = "None"
                conn.send(data)
                data = json.loads(conn.recv(buff_size))
                break                                    
           
            for p in self.players:
                if p.id not in data.keys():
                    self.window.blit(self.bg, [p.location[0] -10 , p.location[1] -50], pygame.Rect(p.location[0] -10, p.location[1] -50, 80, 100))
                    player_disconnect = p.username
                    p.ready = False

            health.update_health()                                                        
            self.window.blit(self.bg, [meplayer.location[0] , meplayer.location[1] -80], pygame.Rect(meplayer.location[0], meplayer.location[1] -80, 80, 200))
            self.window.blit(self.bg, [500 , 0], pygame.Rect(500, 0, 200, 200))
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            output_string = "TIME: {0:02}:{1:02}".format(minutes, seconds)
            text = font.render(output_string, True, [255,255,255])
            self.window.blit(text, [500, 10])
            self.window.blit(self.bg, [420, 440], pygame.Rect(420, 440, 200, 200))

            if(meplayer.ready == False):
                #sleep(1)
                meplayer.respawn()
            if(player_disconnect != None):
                string = player_disconnect + " disconnected."
            else:
                string = "Commence Game..."
            text = font_disc.render(string, True, [255,255,255])
            self.window.blit(text, [450, 440])

                
            #Read events
            e = event.poll()

            if e.type == QUIT:
                data = "None"
                conn.send(data)
                data = json.loads(conn.recv(buff_size))
                pygame.quit()

            if e.type == KEYDOWN and meplayer.ready == True:
                keystate = pygame.key.get_pressed()
                if(keystate[K_a]):
                    meplayer.direction = 'West'
                    meplayer.check_tile_exists(0,5)
                    if (not thread.isAlive() and meplayer.check_tile_exists(20,40) == False):
                        thread = Thread(target = meplayer.fall_thread, args = (self.window,))
                        thread.start()
                    else:
                            meplayer.walk(self.window, meplayer.dir_index)
                if(keystate[K_d]):
                    meplayer.direction = 'East'
                    meplayer.check_tile_exists(0,5)
                    if (not thread.isAlive() and meplayer.check_tile_exists(20,40) == False):
                        thread = Thread(target = meplayer.fall_thread, args = (self.window,))
                        thread.start()
                    else:
                            meplayer.walk(self.window, meplayer.dir_index)
                if(keystate[K_w]):
                     if (not thread.isAlive()):
                             thread = Thread(target = meplayer.jump_thread, args = (self.window, meplayer.dir_index,))
                             thread.start()
                if(keystate[K_r]):
                    hitplayer, wpn = meplayer.attack(self.window, self.players)
                    hit_thread = Thread(target = self.print_attack, args=(self.window, wpn[0], wpn[1]))
                    hit_thread.start()
                    
            elif e.type == KEYUP and meplayer.ready == True and total_seconds > 3:
                if(e.key == pygame.K_e):
                    if(meplayer.direction == 'West'):
                        bomb_coordinates = [meplayer.location[0] - 32, meplayer.location[1]]
                    else:
                        bomb_coordinates = [meplayer.location[0] + 32, meplayer.location[1]]
                    self.create_bomb(bomb_coordinates, screen, meplayer)
                if(e.key == pygame.K_p):
                    disconnect = True

            #Render Images
            meplayer.set_player_health()
            meplayer.render(self.window, meplayer.direction, meplayer.dir_index, meplayer.sec)
            screen.update_block()
            self.render_players()
            self.display_bomb(meplayer)
            health.update_health()

            frame_count += 1
            clock.tick(frame_rate)
            pygame.display.update()
                
        if(stop == True):
            return False
        return True    
