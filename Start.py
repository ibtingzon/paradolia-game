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

import Game
from Game import Game

import Block
from Block import Block, Screen

import Tkinter
import tkSimpleDialog

buff_size = 6096

class Button():
    def __init__(self, text, pos, window):
        self.hovered = False
        self.window = window
        self.text = text
        self.pos = pos

    def display_text(self, font_, col):
        self.font_ = font_
        self.render_(col)

    def render_(self, col):
        pygame.font.init()
        self.rend = self.font_.render(self.text, True, self.hover_(col))
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
        window.blit(self.rend, self.rect)

    def hover_(self, col):
        if (self.hovered == True):
            return (246, 240, 120)
        else:
            return col

def send_(host, port):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((host,port))
        socketname = str(clientsocket.getsockname()[1])
        return [socketname, clientsocket]

class Start():
    
    def __init__(self, window):

        #Initialize Game
        pygame.init()
        pygame.key.set_repeat(1, 1)
        self.window = window

        #Background Setting
        self.bg_game = pygame.image.load("images/bg.png")
        self.bg = pygame.image.load("images/lobby.png")
        self.title = pygame.image.load("images/Paradolia.png")
            
    def main(self):
        screen = Screen(self.window)
        options = [Button("Start Game", (240, 270), self.window ),Button("Help", (275, 300), self.window ), Button("About", (266, 330), self.window )]

        ninja_color = ["black", "white", "red", "orange", "green"]
        conn_established = False
        wait_for_players = False
        display_high_scores = False
        high_scores_printed = False
        init_game = 0
        player_queue = []
        player_list = []
        color = "None"
        ranking = False
        display_ranks = False

        frame_count = 0
        frame_rate = 10
        start_time = 5
        clock = pygame.time.Clock()
        
        while True:
            Tkinter.Tk().withdraw()
            username = tkSimpleDialog.askstring("Name", "Enter username (max 6 char): ")
            if len(username) <= 6:
                break
        meplayer = Player(self.window, [300, 350], 0, screen, self.bg_game, color, username)

        while True:     
            e = event.poll()
            if e.type == QUIT:  
                break

            #Display Title Page: Paradolia >> Start game >> Help >> About
            if init_game == 0:
                self.window.blit(self.bg, [0,0])
                self.window.blit(self.title, [150,150])
                for opt in options:
                    opt.display_text(pygame.font.Font("V5PRC___.ttf", 20), [255,255,255])
                    if opt.rect.collidepoint(pygame.mouse.get_pos()):
                        opt.hovered = True
                        if opt == options[0] and e.type == pygame.MOUSEBUTTONUP:
                            init_game = 1  
                    else:
                        opt.hovered = False
                    opt.render_([255,255,255])
                    
            if init_game == 1:
                #Establish Connection upon starting the game
                if conn_established == False:
                    self.me, self.conn = send_('127.0.0.1', 6961)
                    conn_established = True

                total_seconds = start_time - (frame_count // frame_rate)    

                #Send data: color, ready [T/F], username
                data = json.dumps([meplayer.col, meplayer.ready, meplayer.username, total_seconds])
                self.conn.send(data)
                data = json.loads(self.conn.recv(buff_size))

                #Initialize player's colors, username
                for id_ in data.keys():
                    if(len(data[id_]) == 4 and id_ != self.me):
                        if len(data[id_]) != 0:
                            if data[id_][3] < total_seconds:
                                total_seconds = data[id_][3]
                            if(data[id_][0] != "None" and data[id_][0] in ninja_color):
                                ninja_color.remove(data[id_][0])
                                print ninja_color
                            if( data[id_][0] != "None" and data[id_][1] == True and not [data[id_][2], data[id_][0]] in player_queue):
                                player_queue.append([data[id_][2], data[id_][0]])

                #Display background
                window.blit(self.bg, (0,0))
                window.blit(pygame.image.load("images/bgbox.png"), (130,40))
                color_list = []

                fontface = "electrb.ttf"
                init_location = [240, 140]
                text_pos = init_location[1]
                fontsize = 15

                #Wait for players to connect
                max_no_players = 3
                if(wait_for_players == True):
                    wait = Button("Waiting for Players...", init_location, self.window)
                    wait.display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                    text_pos += 25
                    
                    for p in player_queue:
                        player_text = Button(p[0] + " joined", [init_location[0], text_pos + 30], self.window)
                        player_text.display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                        text_pos += 25
                        
                    if(len(player_queue) == max_no_players - 1):
                        seconds = total_seconds % 60
                        start_str = "Game starts in:"
                        start_text = Button(start_str, (250, 330), self.window)
                        start_text.display_text(pygame.font.Font(fontface, fontsize + 2), [0,0,0])
                        output_string = "{0:02}".format(seconds)
                        game_start = Button(output_string, (321, 355), self.window)
                        game_start.display_text(pygame.font.Font(fontface, fontsize + 7), [255,0,0])

                        if(total_seconds != 0):
                            frame_count += 1
                            clock.tick(frame_rate)
                        
                        if seconds == 0:
                            total_seconds =0
                            game = Game(window, self.bg_game)
                            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                            game_terminated = game.main(meplayer, screen, self.conn, self.me)
                            ninja_color = ["black", "white", "red", "orange", "green"]

                            if (game_terminated == True):
                                high_scores_printed = False
                                screen = Screen(self.window)
                                conn_established = False
                                wait_for_players = False
                                ranking = False
                                display_ranks = False
                                init_game = 0
                                player_queue = []
                                color = "[none]"
                                meplayer = Player(self.window, [300, 350], 0, screen, self.bg_game, color, username)  
                                continue
                            if (game_terminated == False):
                                print "Terminated!"
                                init_game = -1
                                wait_for_players = False
                                ranking = True
                                sleep(3)
                                player_list, meplayer = game.get_players_list()
                    
                #User chooses color   
                elif(wait_for_players == False):
                    button = Button("Choose your Warrior:", init_location, self.window)
                    if not color in ninja_color:
                        color = "[none]"
                    ninja = Button("You are " + color + " Warrior", [init_location[0], text_pos + 20], self.window)                
                    button.display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                    ninja.display_text(pygame.font.Font(fontface, fontsize-1), [0,0,0])
                    text_pos += 25
                    for col in ninja_color:
                        col_opt = Button(col, [init_location[0], text_pos + 30], self.window)
                        col_opt.display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                        color_list.append(col_opt)
                        text_pos += 25
                        
                    for col in color_list:
                        if col.text in ninja_color and col.rect.collidepoint(pygame.mouse.get_pos()):
                            if e.type == pygame.MOUSEBUTTONUP:
                                color = col.text
                            col.hovered = True
                            col.render_([0,0,0])

                    start = Button("Next >>", (300, 340), self.window)
                    start.display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                    if start.rect.collidepoint(pygame.mouse.get_pos()):
                            start.hovered = True
                            if color != "[none]" and e.type == pygame.MOUSEBUTTONUP:
                                meplayer = Player(self.window, [300, 350], 0, screen, self.bg_game, color, username)
                                meplayer.set_col(color)
                                wait_for_players = True
                                meplayer.ready = True
                                
                    start.render_([0,0,0])

            #Awards and Rankings
            if ranking == True:
                    fontface = "electrb.ttf"
                    init_location = [250, 150]
                    text_pos = init_location[1]
                    fontsize = 16
                    main_game = Button("View Awards", (300, 360), self.window)
                    main_game.display_text(pygame.font.Font(fontface, 15), [0,0,0])
                        
                    if main_game.rect.collidepoint(pygame.mouse.get_pos()):
                        main_game.hovered = True
                        main_game.render_([0,0,0])
                        if e.type == pygame.MOUSEBUTTONUP:
                            ranking = False
                            display_ranks = False
                            display_high_scores = True
                            continue
                        main_game.render_([0,0,0])

                    if(display_ranks == False):
                        display_ranks = True
                        ranks = []
                        ranks_ordered = []
                        greatest_kills = 0
                        best_killer = None
                        player_list.append(meplayer)
                        
                        for p in player_list:
                            ranks.append(p)

                        while(len(ranks) > 0):
                            greatest_kills = 0
                            for p in ranks:
                                print p.username
                                if(p.kills >= greatest_kills):
                                    greatest_kills = p.kills
                                    best_killer = p
                                    
                            ranks_ordered.append(best_killer)
                            if(best_killer in ranks):
                                ranks.remove(best_killer)
                    
                        self.window.blit(self.bg, [0,0])
                        self.window.blit(pygame.image.load("images/bgbox.png"), (130,40))
                        rank_text = Button("Ranking" , init_location, self.window)
                        rank_text.display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                        text_pos = init_location[1] 
                        for pub in ranks_ordered:
                            text_pos = text_pos + 20
                            pub_enemy_text = Button(pub.username + ": " + str(pub.kills) + " kill/s", (init_location[0], text_pos), self.window)
                            pub_enemy_text.display_text(pygame.font.Font(fontface, fontsize), [255,0,0])               
                    
                    
            if display_high_scores == True:
                fontface = "electrb.ttf"
                init_location = [250, 150]
                text_pos = init_location[1]
                fontsize = 15
                main_game = Button("Back to Menu", (300, 360), self.window)
                main_game.display_text(pygame.font.Font(fontface, 15), [0,0,0])
                    
                if main_game.rect.collidepoint(pygame.mouse.get_pos()):
                    main_game.hovered = True
                    main_game.render_([0,0,0])
                    if e.type == pygame.MOUSEBUTTONUP:
                        high_scores_printed = False
                        display_high_scores = False
                        screen = Screen(self.window)
                        conn_established = False
                        wait_for_players = False
                        init_game = 0
                        player_queue = []
                        color = "None"
                        ranking = False
                        display_ranks = False
                        meplayer = Player(self.window, [300, 350], 0, screen, self.bg_game, color, username)  
                        continue
                    main_game.render_([0,0,0])
                        
                    
                if high_scores_printed == False:
                    high_scores_printed = True
                    fontface = "electrb.ttf"
                    init_location = [250, 130]
                    text_pos = init_location[1]
                    fontsize = 14
                    self.window.blit(self.bg, [0,0])
                    self.window.blit(pygame.image.load("images/bgbox.png"), (130,40))
                    public_enemies =[]
                    survivors = []
                    suicides = []
                    bantha_fodder = []
                    greatest_kills = 0
                    least_deaths = 9999
                    most_deaths = 0
                    most_suicides = 0
                    
                    for p in player_list:
                        if(p.kills > greatest_kills):
                            greatest_kills = p.kills
                        if(p.deaths < least_deaths):
                            least_deaths = p.deaths
                        if(p.deaths > most_deaths):
                            most_deaths = p.deaths
                        if(p.suicides > most_suicides):
                            most_suicides = p.suicides
                    for p in player_list:
                        if(p.kills == greatest_kills and p.kills != 0):
                            public_enemies.append(p)
                        if(p.deaths == least_deaths):
                            survivors.append(p)
                        if(p.suicides == most_suicides and p.suicides > 0):
                            suicides.append(p)
                        if(p.deaths == most_deaths and most_deaths != least_deaths):
                            bantha_fodder.append(p)
                        
                    pub_enemy_text = Button("Public Enemy: " , init_location, self.window)
                    pub_enemy_text.display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                    text_pos = init_location[1] 
                    if(len(public_enemies) == 0):
                        text_pos = text_pos + 20
                        pub_enemy_text = Button(" No kills ", (init_location[0], text_pos), self.window).display_text(pygame.font.Font(fontface, fontsize), [255,0,0])
                    else:
                        for pub in public_enemies:
                            text_pos = text_pos + 20
                            pub_enemy_text = Button(pub.username + ": " + str(pub.kills) + " kill/s", (init_location[0], text_pos), self.window)
                            pub_enemy_text.display_text(pygame.font.Font(fontface, fontsize), [255,0,0])               
                    text_pos = text_pos + 25
                    survivor_text = Button("Survivalist: " , [init_location[0], text_pos], self.window).display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                    for pub in survivors:
                        text_pos = text_pos + 20
                        survivor_text = Button(pub.username + ": " + str(pub.deaths) + " death/s", (init_location[0], text_pos), self.window).display_text(pygame.font.Font(fontface, fontsize), [255,0,0])
                    text_pos = text_pos + 25
                    suicide_text = Button("Suicide Bomber: " , [init_location[0], text_pos], self.window).display_text(pygame.font.Font(fontface, fontsize), [0,0,0])
                    if(len(suicides) == 0):
                        text_pos = text_pos + 20
                        suicide_text = Button(" None ", (init_location[0], text_pos), self.window).display_text(pygame.font.Font(fontface, fontsize), [255,0,0])
                    else:
                        for pub in suicides:
                            text_pos = text_pos + 20
                            suicide_text = Button(pub.username + ": " + str(pub.suicides) + " idiocies", (init_location[0], text_pos), self.window).display_text(pygame.font.Font(fontface, fontsize), [255,0,0])
                    
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            pygame.display.update()
            
        pygame.quit()

if __name__ == "__main__":
    window = pygame.display.set_mode((650, 500))
    commence_game = False
    start = Start(window)
    start.main()
    
