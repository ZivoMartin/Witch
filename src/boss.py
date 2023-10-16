import pygame as pg
from random import randint

class Boss():

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.hp_max = 150
        self.hp = self.hp_max
        self.x, self.y = int(self.game.size[0]*0.4), int(self.game.size[0]*0.03)
        self.speed = 6
        self.images = {}
        self.img_w = int(self.game.size[0]*0.23)
        self.img_h = self.img_w
        self.next_move = [0, 0]
        self.build_image()
        self.damage = 20
        self.state = "golem"
        
    def move(self):
        if(self.state != "dead_golem"):
            self.get_next_move()    
            x, y = self.x + self.next_move[0], self.y + self.next_move[1]
            self.x, self.y = x, y
            if(self.player.get_x()<x+20 and self.player.get_x()>x-20 and self.player.get_y()<y+20 and self.player.get_y()>y-20):
                self.player.take_damage(self.damage)


    def get_next_move(self):
        x_p, y_p = self.player.get_x(), self.player.get_y()
        factor_x, factor_y = -1, -1
        if(self.x-x_p < 0):
            factor_x = 1
        if(self.y-y_p < 0):
            factor_y = 1
        if(randint(0, abs(self.x-x_p)+abs(self.y-y_p)) < abs(self.x-x_p)):
            self.next_move = [factor_x*self.speed, 0]
        else:
            self.next_move = [0, factor_y*self.speed, 0]

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def draw(self):
        self.game.screen.blit(self.images[self.state], (self.x, self.y))

    def change_state(self, state):
        self.state = state

    def get_state(self):
        return self.state
    
    def take_damage(self, damage):
        self.hp -= damage
        
    def get_hp(self):
        return self.hp

    def get_img_size(self):
        return self.img_w, self.img_h

    def build_image(self):
        img = pg.image.load(self.game.img_path + "/golem/golem.png")  
        self.images["golem"] = pg.transform.scale(img, (self.img_w, self.img_h))
        img = pg.image.load(self.game.img_path + "/golem/golem_spe_1.png")  
        self.images["golem_spe_1"] = pg.transform.scale(img, (self.img_w, self.img_h))
        img = pg.image.load(self.game.img_path + "/golem/golem_spe_2.png")  
        self.images["golem_spe_2"] = pg.transform.scale(img, (self.img_w, self.img_h))
        img = pg.image.load(self.game.img_path + "/golem/hot_golem.png")  
        self.images["hot_golem"] = pg.transform.scale(img, (self.img_w, self.img_h))
        img = pg.image.load(self.game.img_path + "/golem/dead_golem.png")  
        self.images["dead_golem"] = pg.transform.scale(img, (self.img_w, self.img_h))