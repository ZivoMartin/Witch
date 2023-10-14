import pygame as pg
from random import randint
import math

class Game():
    
    
    def __init__(self, img_path):
        self.img_path = img_path
        pg.init()
        pg.font.init()
        screen_info = pg.display.Info()
        self.menu_bar_height =30
        self.size = (screen_info.current_w, screen_info.current_h-self.menu_bar_height)
        self.screen = pg.display.set_mode(self.size, pg.FULLSCREEN)
        self.init_const()
        self.build_img()
        self.map_tab = self.generate_random_map()
        self.spawn_player()
        self.generate_ennemys()
        self.life_time_explosions = 20
        self.bullets_speed = 10
        clock = pg.time.Clock()
        
        while self.running:
            self.iter += 1
            self.screen.fill(self.bg_color)
            self.event_gestion()
            if(not self.current_hp_player<=0):
                if(len(self.monsters) == 0):
                    self.out_open = True
                else:
                    self.out_open = False
                self.display_map()
                self.display_room_number()
                pg.draw.rect(self.screen, self.health_bar_color, (0, self.size[1]-8, self.current_hp_player*self.size[0]/self.max_hp_player, self.menu_bar_height+8))
                self.display_bullets()
                self.display_explosions()
                self.move_player()
                self.display_monsters()
                self.move_monsters()
                pg.draw.circle(self.screen, "black", self.player_pos, 20)
            else:
                self.screen.blit(self.game_over_txt, (int(self.size[0]*0.35), int(self.size[1]*0.4)))
            pg.display.flip()
            clock.tick(60)
        pg.quit()
        
        


    def event_gestion(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if(self.current_hp_player > 0):
                if(event.type == pg.KEYDOWN):
                    if(event.unicode in self.moves_dico):
                        self.moves[self.moves_dico[event.unicode]][0] = True
                elif(event.type == pg.KEYUP and event.unicode in self.moves_dico):
                    self.moves[self.moves_dico[event.unicode]][0] = False
                elif(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                    x1, y1, x2, y2 = self.player_pos[0], self.player_pos[1], event.pos[0], event.pos[1]
                    if(x1 != x2):
                        m, d, b, f = get_param(x1, y1, x2, y2)
                        self.bullets.append({"x": x1, "y": y1, "m": m, "dist": d-self.bullets_speed, "b": b, "f": f, "x2": x2, "y2": y2})
        
    def display_bullets(self):
        for i in range(len(self.bullets)):
            if(i>=len(self.bullets)):
                break
            pg.draw.circle(self.screen, self.bullets_color, (self.bullets[i]["x"], self.bullets[i]["y"]), 10)
            self.bullets[i]["dist"] -= self.bullets_speed
            self.bullets[i]["x"] = self.bullets[i]["x2"] - int(self.bullets[i]["f"]*(self.bullets[i]["dist"]/math.sqrt(self.bullets[i]["m"]**2 + 1)))
            self.bullets[i]["y"] = int(self.bullets[i]["x"]*self.bullets[i]["m"] + self.bullets[i]["b"])
            if(self.its_a_wall(self.bullets[i]["x"], self.bullets[i]["y"]) or self.monster_touched_by_bullet(i)):
                self.explosions.append([self.bullets[i]["x"], self.bullets[i]["y"], 10])
                self.bullets.pop(i)
                
                    
    def move_player(self):
        for i in range(4):
            if(self.moves[i][0] and not self.its_a_wall(self.player_pos[0]+self.moves[i][1][0], self.player_pos[1]+self.moves[i][1][1])):
                self.player_pos[0] += self.moves[i][1][0]
                self.player_pos[1] += self.moves[i][1][1]
                self.try_to_switch_map()  
                
    def move_monsters(self):
        nb_monster = len(self.monsters)
        for i in range(nb_monster):
            if(self.wall_between_monster_player(i)):
                x, y = self.monsters[i]["x"] + self.monsters[i]["move"][0], self.monsters[i]["y"] + self.monsters[i]["move"][1]
                if(not self.its_a_wall(x, y)):
                    self.monsters[i]["x"] = x
                    self.monsters[i]["y"] = y
                    if(self.monsters[i]["move"][2] <= 0):
                        self.change_random_move(i)
                    else:
                        self.monsters[i]["move"][2] -= 1
                else:
                    self.change_random_move(i)
            else:
                self.get_next_move(i)    
                x, y = self.monsters[i]["x"] + self.monsters[i]["move"][0], self.monsters[i]["y"] + self.monsters[i]["move"][1]
                self.monsters[i]["x"], self.monsters[i]["y"] = x, y
                if(self.player_pos[0]<x+30 and self.player_pos[0]>x-30 and self.player_pos[1]<y+30 and self.player_pos[1]>y-30):
                    self.current_hp_player -= self.damage_monster
    
    def wall_between_monster_player(self, i):
        x_p, y_p, x_m, y_m = self.player_pos[0], self.player_pos[1], self.monsters[i]["x"], self.monsters[i]["y"]
        factor_x, factor_y = -1, -1
        if(x_m-x_p < 0):
            factor_x = 1
        if(y_m-y_p < 0):
            factor_y = 1
        x, y = self.convert(x_m, y_m)
        while(self.coord_valid(x, y) and not (x_m <= x_p+self.width_case and x_m>=x_p-self.width_case and y_m <= y_p+self.height_case and y_m>=y_p-self.height_case)):
            if(randint(0, abs(x_m-x_p)+abs(y_m-y_p)) < abs(x_m-x_p)):
                x_m += factor_x*self.monster_speed
            else:
                y_m += factor_y*self.monster_speed
            x, y = self.convert(x_m, y_m)
            if(self.coord_valid(x, y) and self.map_tab[x][y] == 1):
                return True
        return False

    
    def change_random_move(self, i):
        self.monsters[i]["move"][0] = randint(-self.monster_speed, self.monster_speed)
        self.monsters[i]["move"][1] = self.monster_speed - abs(self.monsters[i]["move"][0])
        if(randint(1, 2) == 1):
            self.monsters[i]["move"][1] *= -1
        self.monsters[i]["move"][2] = 15

    def get_next_move(self, i):
        x_p, y_p, x_m, y_m = self.player_pos[0], self.player_pos[1], self.monsters[i]["x"], self.monsters[i]["y"]
        factor_x, factor_y = -1, -1
        if(x_m-x_p < 0):
            factor_x = 1
        if(y_m-y_p < 0):
            factor_y = 1
        if(randint(0, abs(x_m-x_p)+abs(y_m-y_p)) < abs(x_m-x_p)):
            self.monsters[i]["move"][0] = factor_x*self.monster_speed
            self.monsters[i]["move"][1] = 0
        else:
            self.monsters[i]["move"][0] = 0
            self.monsters[i]["move"][1] = factor_y*self.monster_speed
            
        

    def display_map(self):
        for i in range(self.nb_case_horizontal):
            for j in range(self.nb_case_vertical):
                if(self.map_tab[i][j] == 0):
                    self.screen.blit(self.floor_img, (i*self.width_case, j*self.height_case))
                elif(self.map_tab[i][j] == 1):
                    self.screen.blit(self.wall_img, (i*self.width_case, j*self.height_case))
                elif(self.map_tab[i][j] == 2):
                    if(self.out_open):
                        pg.draw.rect(self.screen, self.next_room_color, (i*self.width_case, j*self.height_case, self.width_case, self.height_case)) 
                    else:
                        self.screen.blit(self.floor_img, (i*self.width_case, j*self.height_case))

    def display_monsters(self):
        nb_ghost = len(self.monsters)
        for i in range(nb_ghost):
            if(self.monsters[i]["red"] > 0):
                pg.draw.circle(self.screen, "red", (self.monsters[i]["x"], self.monsters[i]["y"]), self.width_monster)
                self.monsters[i]["red"] -= 1
            else:
                pg.draw.circle(self.screen, "dark green", (self.monsters[i]["x"], self.monsters[i]["y"]), self.width_monster)


    def generate_ennemys(self):
        self.monsters = []
        for i in range(self.nb_monster_per_room):
            x, y = randint(0, self.size[0]-1), randint(0, self.size[1]-1)
            x_case, y_case = self.convert(x, y)
            while(not self.coord_valid(x_case, y_case) or self.map_tab[x_case][y_case] == 1):
                x, y = randint(0, self.size[0]-1), randint(10, self.size[1]-10)
                x_case, y_case = self.convert(x, y)
            self.monsters.append({"x": x, "y": y, "hp": self.base_hp_monsters, "red": 0, "move": [0, 0, -1]})
            
    def monster_touched_by_bullet(self, indice_bullet):
        x, y = self.bullets[indice_bullet]["x"], self.bullets[indice_bullet]["y"]
        nb_monster = len(self.monsters)
        for i in range(nb_monster):
            x_m, y_m = self.monsters[i]["x"], self.monsters[i]["y"]
            if(x < x_m+self.width_monster and x>x_m-self.width_monster and y < y_m+self.height_monster and y>y_m-self.height_monster):
                self.monsters[i]["red"] = 10
                self.monsters[i]["hp"] -= self.bullet_damage
                if(self.monsters[i]["hp"] <= 0):
                    self.monsters.pop(i)
                
                return True
        return False
        
    def display_explosions(self):
        for i in range(len(self.explosions)):
            if(i>=len(self.explosions)):
                break
            self.screen.blit(self.explosion_img, (self.explosions[i][0], self.explosions[i][1]))
            self.explosions[i][2] += 1
            if(self.explosions[i][2] == self.life_time_explosions):
                self.explosions.pop(i)
    
    def its_a_wall(self, i, j):
        i_l, i_r, j_t, j_b = i-self.width_monster, i+self.width_monster, j-self.heigh_monster, j+self.heigh_monster
        x_t = [i_l, i_r]
        y_t = [j_t, j_b]
        result = []
        for k in range(2):
            for l in range(2)
                x, y = self.convert(x_t[k], y_t[l])
                result.append(self.coord_valid(x, y) or self.map_tab[x][y] == 1)
        return True in result
    def its_change_room_case(self, i, j):
        i, j = self.convert(i, j)
        return self.coord_valid(i, j) and self.map_tab[i][j] == 2
    
    def convert(self, i, j):
        x, y = int(i/self.width_case), int(j/self.height_case)
        if(i<0):
            x = -1
        if(y<0):
            y = -1
        return x, y
        
    def generate_random_coord(self):
        return [randint(0, self.size[0]), randint(0, self.size[1])]

    def generate_random_map(self):
        map_tab = [None]*self.nb_case_horizontal
        
        for i in range(self.nb_case_horizontal):
            map_tab[i] = [0]*self.nb_case_vertical
              
        for i in range(self.nb_case_horizontal):
            for j in range(self.nb_case_vertical):
                if(self.there_is_a_wall_near(map_tab, i, j) and randint(1, 3) == 1):
                    map_tab[i][j] = 1
                elif(randint(1, 14) == 1):
                    map_tab[i][j] = 1
        i = randint(0, self.nb_case_horizontal-1)
        j = randint(0, self.nb_case_vertical-1)
        while(map_tab[i][j] == 1):
            i = randint(0, self.nb_case_horizontal-1)
            j = randint(0, self.nb_case_vertical-1)
        map_tab[i][j] = 2      
        return map_tab
    
    def coord_valid(self, i, j):
        return i>=0 and j>=0 and i<(self.nb_case_horizontal) and j<(self.nb_case_vertical)
        
    def there_is_a_wall_near(self, map_tab, i, j):  
        return (i-1>=0 and map_tab[i-1][j] == 1) or (i+1<self.nb_case_horizontal and map_tab[i+1][j] == 1) or (j+1<self.nb_case_vertical and map_tab[i][j+1] == 1) or (j-1>=0 and map_tab[i][j-1] == 1)
    
    def spawn_player(self):
        i, j = self.convert(self.player_pos[0], self.player_pos[1])
        while(self.map_tab[i][j]):
            self.player_pos[0] = randint(10, self.size[0]-10)
            self.player_pos[1] = randint(10, self.size[1]-10)
            i, j = self.convert(self.player_pos[0], self.player_pos[1])
            
    def try_to_switch_map(self):
        if(self.out_open and self.its_change_room_case(self.player_pos[0], self.player_pos[1])):
            self.monster_speed += 2
            self.current_room += 1
            self.map_tab = self.generate_random_map()
            self.spawn_player()
            self.generate_ennemys()
    
    
    def display_room_number(self):
        nb_room_txt = self.font_nb_room.render('Room '+str(self.current_room), False, (0, 0, 200))
        self.screen.blit(nb_room_txt, (self.size[0]-150, 30))

    
    def init_const(self):    
        self.bullets = []
        self.explosions = []
        self.monsters = []
        self.width_monster = 20
        self.height_monster = 20
        self.base_hp_monsters = 10
        self.nb_monster_per_room = 6
        self.bg_color = (0, 0, 0)
        self.current_hp_player = 100
        self.max_hp_player = 100
        self.health_bar_color = (150, 0, 0)
        self.next_room_color = (255, 246, 159)
        self.bullets_color = (228, 91, 0)
        self.iter = 0
        self.current_room = 1
        self.bullet_damage = 2
        self.damage_monster = 1
        self.running = True
        self.out_open = False
        self.nb_case_vertical = 40
        self.nb_case_horizontal = 60
        self.width_case = int(self.size[0]/self.nb_case_horizontal)
        self.height_case = int(self.size[1]/self.nb_case_vertical)
        self.speed = 6
        self.monster_speed = 5
        self.moves = [[False, (self.speed, 0)], [False, (-self.speed, 0)], [False, (0, self.speed)], [False, (0, -self.speed)]]
        self.player_pos = [int(self.size[0]/2), int(self.size[1]/2)]
        self.moves_dico = {'z': 3, 'q': 1, 'd': 0, 's': 2}

    def build_img(self):
        self.wall_img = pg.image.load(self.img_path + "/wall.png")  
        self.floor_img = pg.image.load(self.img_path + "/floor.png")  
        self.personnage_img = pg.image.load(self.img_path + "/personnage.jpg")  
        self.explosion_img = pg.image.load(self.img_path + "/explosion.jpg")  
        self.personnage_img = pg.transform.scale(self.personnage_img, (self.width_case, self.height_case))
        self.explosion_img = pg.transform.scale(self.explosion_img, (10, 10))
        self.wall_img = pg.transform.scale(self.wall_img, (self.width_case, self.height_case))
        self.floor_img = pg.transform.scale(self.floor_img, (self.width_case, self.height_case))
        self.font_game_over = pg.font.SysFont('Comic Sans MS', int(self.size[0]*0.09))
        self.game_over_txt = self.font_game_over.render('Game Over', False, (200, 0, 0))
        self.font_nb_room = pg.font.SysFont('Comic Sans MS', int(30))
        


def get_param(x1, y1, x2, y2):
    m = (y1-y2)/(x1-x2)
    factor = 1
    if(x1>x2):
        m = (y2-y1)/(x2-x1)
        factor = -1
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    b = y1 - m*x1
    return m, dist, b, factor

# nb_wall = randint(10, 20)
# for i in range(nb_wall):
#     longueur = randint(10, 30)
#     dir_tab = [(1, 0), (-1, 0), (0, 1), (0, -1)]
#     direction = dir_tab[randint(0, 3)]
#     i = randint(0, self.nb_case_horizontal)
#     j = randint(0, self.nb_case_vertical)
#     k = 0
#     while(k<longueur and self.coord_valid(i, j)):
#         k += 1
#         map_tab[i][j] = 1
#         i += direction[0]
#         j += direction[1]