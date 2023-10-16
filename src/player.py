import pygame as pg
from random import randint

class Player():

    def __init__(self, game):
        self.game = game
        self.height = min(self.game.width_case//2, self.game.height_case//2)
        self.hp = 100
        self.max_hp = 100
        self.speed = 6
        self.x, self.y = self.game.size[0]//2, self.game.size[1]//2
        self.color = (0, 0, 0)
        
    
    def set_pos(self, x, y):
        self.x, self.y = self.x+x, self.y+y
    
    def set_speed(self, speed):
        self.speed = speed

    def get_height(self):
        return self.height
    
    def get_speed(self):
        return self.speed
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_hp(self):
        return self.hp
    
    def get_max_hp(self):
        return self.max_hp

    def draw(self):
        pg.draw.circle(self.game.screen, self.color, (self.x, self.y), self.height)

    def spawn(self):
        while(self.game.its_a_wall(self.x, self.y, self.height)):
            self.x = randint(10, self.game.size[0]-10)
            self.y = randint(10, self.game.size[1]-10)
            

    def regen(self):
        self.hp = self.max_hp

    def take_damage(self, damage):
        self.hp -= damage
        