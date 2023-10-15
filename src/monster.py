import pygame as pg
from random import randint

class Monster():

    def __init__(self, game, player, x, y):
        self.game = game
        self.player = player
        self.x = x
        self.y = y
        self.hp = self.game.base_hp_monsters
        self.speed = self.game.monster_speed
        self.damage = self.game.damage_monster
        self.height = self.game.height_monster
        self.touched_count = 0
        self.base_color = "dark green"
        self.touched_color = "red"
        self.move = [0, 0, 0]

    def draw(self):
        if(self.touched_count > 0):
            pg.draw.circle(self.game.screen, self.touched_color, (self.x, self.y),  self.height)
            self.touched_count -= 1
        else:
            pg.draw.circle(self.game.screen, self.base_color, (self.x, self.y), self.height)

    def move_on_player(self):
        self.get_next_move()    
        x, y = self.x + self.move[0], self.y + self.move[1]
        if(not self.game.its_a_wall(x, y, self.height)):
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
            self.move = [factor_x*self.speed, 0, 0]
        else:
            self.move = [0, factor_y*self.speed, 0]


    def random_move(self):
        x, y = self.x + self.move[0], self.y + self.move[1]
        if(not self.game.its_a_wall(x, y, self.height)):
            self.x = x
            self.y = y
            if(self.move[2] <= 0):
                self.change_random_move()
            else:
                self.move[2] -= 1
        else:
            self.change_random_move()


    def change_random_move(self):
        self.move[0] = randint(-self.speed, self.speed)
        self.move[1] = self.speed - abs(self.move[0])
        if(randint(1, 2) == 1):
            self.move[1] *= -1
        self.move[2] = 15

    def take_damage(self, damage):
        self.touched_count = 10
        self.hp -= damage
    

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

