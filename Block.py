import pygame
from pygame import *
import socket
import json
import time
from time import *
import threading
from threading import *
import sys

tiles = [pygame.Rect(0,0,49,47), pygame.Rect(49,0,49,47), pygame.Rect(49*2,0,49,47), pygame.Rect(49,50,49,47) ]
blocks = []

class Block():
    def __init__(self, window, location):
        self.window = window
        self.location = location
        self.img = pygame.image.load("images/tiles.png")
        self.current = False

    def get_location(self):
        return self.location

    def display_tile(self, tile_index):
        self.window.blit(self.img, self.location, tiles[tile_index])

class Screen():
    def __init__(self, window):
        self.window = window
        self.create_tiles()

    def create_tiles(self):
        block1 = Block(self.window, [300, 280])
        blocks.append(block1)
        block2 = Block(self.window, [200, 280])
        blocks.append(block2)
        block4 = Block(self.window, [150, 280])
        blocks.append(block4)
        block14 = Block(self.window, [400, 280])
        blocks.append(block14)
        block15 = Block(self.window, [450, 280])
        blocks.append(block15)
        block16 = Block(self.window, [500, 280])
        blocks.append(block16)
        block3 = Block(self.window, [250, 205])
        blocks.append(block3)
        block5 = Block(self.window, [100, 205])
        blocks.append(block5)
        block6 = Block(self.window, [50, 205])
        blocks.append(block6)
        block7 = Block(self.window, [00, 205])
        blocks.append(block7)
        block17 = Block(self.window, [600, 205])
        blocks.append(block17)
        block39 = Block(self.window, [400, 205])
        blocks.append(block39)
        block40 = Block(self.window, [450, 205])
        blocks.append(block40)
        block41 = Block(self.window, [350, 205])
        blocks.append(block41)
        block27 = Block(self.window, [550, 205])
        blocks.append(block27)
        block8 = Block(self.window, [200, 115])
        blocks.append(block8)
        block9 = Block(self.window, [250, 115])
        blocks.append(block9)
        block10 = Block(self.window, [300, 115])
        blocks.append(block10)
        block11 = Block(self.window, [400, 115])
        blocks.append(block11)
        block12 = Block(self.window, [450, 115])
        blocks.append(block12)
        block13 = Block(self.window, [500, 115])
        blocks.append(block13)

    def update_block(self):
        i = 0
        for block in blocks:
            self.window.blit(block.img, block.location, tiles[i])
            i += 1
            if (i == len(tiles)):
                i = 0
        #i = 0
        #ground = [i, 400]
        #while i < 650:
         #   self.window.blit(block.img, ground, tiles[0])
          #  i += 45
          #  ground = [i, 400]
            
    def get_block_list(self):
        return blocks
        
    
    

    
    

