import pygame as pg
import math

class Bullet():

    def __init__(self, game, player, click_x, click_y):
        self.game = game
        self.player = player
        self.click_x = click_x
        self.click_y = click_y
        self.x = self.player.x
        self.y = self.player.y
        self.angle_rotate = 15
        self.color = (228, 91, 0)
        self.speed = 8
        self.height = self.player.get_height()//2
        self.image_bullet = pg.image.load(self.game.img_path + "/kunai/kunai1.png")  
        self.image_bullet = pg.transform.scale(self.image_bullet, (30, 30))
        self.image_explosion = pg.image.load(self.game.img_path + "/explosion.jpg")  
        self.image_explosion = pg.transform.scale(self.image_explosion, (10, 10))
        self.alive = True
        self.count_before_disapear = 10
        self.m, self.d, self.b, self.f = self.get_param(self.x, self.y, self.click_x, self.click_y)
        self.d -= self.speed


    def move(self):
        if(self.alive):
            self.d -= self.speed
            self.x = self.click_x - int(self.f*(self.d/math.sqrt(self.m**2 + 1)))
            self.y = int(self.x*self.m + self.b)
        else:
            self.count_before_disapear -= 1


    def get_height(self):
        return self.height
    
    def get_speed(self):
        return self.speed
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_count(self):
        return self.count_before_disapear

    def is_alive(self):
        return self.alive
    
    def kill(self):
        self.alive = False
    
    def draw(self):
        if(self.alive):
            # pg.draw.circle(self.game.screen, self.color, (self.x, self.y), self.height)
            self.game.screen.blit(self.image_bullet, (self.x, self.y))
            # self.image_bullet = pg.transform.rotate(self.image_bullet, self.angle_rotate)
        else:
            pass
            # self.game.screen.blit(self.image_explosion, (self.x, self.y))
    
    def get_param(self, x1, y1, x2, y2):
        m = (y1-y2)/(x1-x2)
        factor = 1
        if(x1>x2):
            m = (y2-y1)/(x2-x1)
            factor = -1
        dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        b = y1 - m*x1
        return m, dist, b, factor

