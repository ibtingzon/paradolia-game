import pygame
from pygame import *
import socket
import json
import time
from time import *
import threading
from threading import *
import sys

health = []

class Health():
    def __init__(self, window, player):
        self.window = window
        self.player = player
        self.init_health()

    def init_health(self):
        fullhealth = pygame.image.load("images/fullhealth.png")
        health.append(fullhealth)
        modhealth = pygame.image.load("images/modhealth.png")
        health.append(modhealth)
        criticalhealth = pygame.image.load("images/criticalhealth.png")
        health.append(criticalhealth)
        dead = pygame.image.load("images/dead.png")
        health.append(dead)

    def update_health(self):
        if self.player.health == 3:
            self.window.blit(health[0], [0,0])
        elif self.player.health == 2:
            self.window.blit(health[1], [0,0])
        elif self.player.health == 1:
            self.window.blit(health[2], [0,0])
        elif self.player.health == 0:
            self.window.blit(health[3], [0,0])
        # render text
        myfont = pygame.font.Font("V5PRC___.ttf", 20)
        label = myfont.render(self.player.username, 1, (255,255,255))
        self.window.blit(label, (50, 1))
