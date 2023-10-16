import pygame as pg
from random import randint

class Boss():

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.hp_max = 1000
        self.hp = self.hp_max
        self.x, self.y = 300, 300
        self.speed = 6
        self.images = {}
        self.img_w = 300
        self.img_h = 300
        self.build_image()
        self.state = "golem"

    def draw(self):
        self.game.screen.blit(self.images[self.state], (self.x, self.y))

    def change_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

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