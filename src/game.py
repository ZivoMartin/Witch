import pygame as pg
from random import randint
import math
from src.player import Player
from src.bullet import Bullet
from src.monster import Monster

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
        self.player.spawn()
        self.generate_ennemies()
        clock = pg.time.Clock()
        
        while self.running:
            self.iter += 1
            self.screen.fill(self.bg_color)
            self.event_gestion()
            if(self.player.get_hp() <= 0):
                self.screen.blit(self.game_over_txt, (int(self.size[0]*0.35), int(self.size[1]*0.4)))
            elif(self.choix_en_cours):
                self.display_choose_menu()
            else:
                if(len(self.monsters) == 0):
                    self.out_open = True
                else:
                    self.out_open = False
                self.display_map()
                self.display_room_number()
                pg.draw.rect(self.screen, self.health_bar_color, (0, self.size[1]-8, self.player.get_hp()*self.size[0]/self.player.get_max_hp(), self.menu_bar_height+8))
                self.display_bullets()
                self.move_player()
                self.display_monsters()
                self.move_monsters()
                self.player.draw()
            pg.display.flip()
            clock.tick(60)
        pg.quit()
        
        


    def event_gestion(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if(self.player.hp > 0):
                if(event.type == pg.KEYDOWN):
                    if(event.unicode in self.moves_dico):
                        self.moves[self.moves_dico[event.unicode]][0] = True
                elif(event.type == pg.KEYUP and event.unicode in self.moves_dico):
                    self.moves[self.moves_dico[event.unicode]][0] = False
                elif(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                    if(not self.choix_en_cours):
                        if(self.player.get_x() != event.pos[0]):
                            self.bullets.append(Bullet(self, self.player, event.pos[0], event.pos[1]))
                    else:
                        x, y = event.pos[0], event.pos[1]
                        if(y>=self.size[1]*0.1 and y<=self.size[1]*0.3):
                            self.choix_en_cours = False
                            self.player.set_speed(int(self.player.get_speed()*1.2))
                            self.moves = [[False, (self.player.get_speed(), 0)], [False, (-self.player.get_speed(), 0)], [False, (0, self.player.get_speed())], [False, (0, -self.player.get_speed())]]
                        elif(y>=self.size[1]*0.3 and y<=self.size[1]*0.6):
                            self.choix_en_cours = False
                            self.bullet_damage += 2
                        elif(y>=self.size[1]*0.7 and y<=self.size[1]*0.9):
                            self.choix_en_cours = False
                            self.player.regen()

                        
    def display_bullets(self):
        for i in range(len(self.bullets)):
            if(i>=len(self.bullets)):
                break
            self.bullets[i].draw()
            self.bullets[i].move()
            if(self.bullets[i].get_count() == 0):
                self.bullets.pop(i)
            elif(self.bullets[i].is_alive() and (self.its_a_wall(self.bullets[i].get_x(), self.bullets[i].get_y(), self.bullets[i].get_height()) or self.monster_touched_by_bullet(i))):
                self.bullets[i].kill()
                
                
                
                    
    def move_player(self):
        for i in range(4):
            if(self.moves[i][0] and not self.its_a_wall(self.player.get_x()+self.moves[i][1][0], self.player.get_y()+self.moves[i][1][1], self.player.height)):
                self.player.set_pos(self.moves[i][1][0], self.moves[i][1][1])
                self.try_to_switch_map()  
                
    def move_monsters(self):
        nb_monster = len(self.monsters)
        for i in range(nb_monster):
            if(self.wall_between_monster_player(i)):
                self.monsters[i].random_move()
            else:
                self.monsters[i].move_on_player()
    
    def wall_between_monster_player(self, i):
        x_p, y_p, x_m, y_m = self.player.get_x(), self.player.get_y(), self.monsters[i].get_x(), self.monsters[i].get_y()
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


    
            

    def display_choose_menu(self):
        pg.draw.rect(self.screen, self.augment_case_color, (0, int(self.size[1]*0.1), self.size[0], int(self.size[1]*0.3-self.size[1]*0.1))) 
        pg.draw.rect(self.screen, self.augment_case_color, (0, int(self.size[1]*0.4), self.size[0], int(self.size[1]*0.6-self.size[1]*0.4))) 
        pg.draw.rect(self.screen, self.augment_case_color, (0, int(self.size[1]*0.7), self.size[0], int(self.size[1]*0.9-self.size[1]*0.7))) 
        txt = self.font_nb_room.render('Augmenter votre vitesse', False, (0, 0, 200))
        self.screen.blit(txt, (int(self.size[0]*0.4), int(self.size[1]*0.2)))
        txt = self.font_nb_room.render('Augmenter vos dégats', False, (0, 0, 200))
        self.screen.blit(txt, (int(self.size[0]*0.4), int(self.size[1]*0.5)))
        txt = self.font_nb_room.render('Récuperez votre vie', False, (0, 0, 200))
        self.screen.blit(txt, (int(self.size[0]*0.4), int(self.size[1]*0.8)))

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
        for monster in self.monsters:
            monster.draw()

    def generate_ennemies(self):
        self.monsters = []
        for i in range(self.nb_monster_per_room):
            x, y = randint(0, self.size[0]-1), randint(0, self.size[1]-1)
            while(self.its_a_wall(x, y, self.height_monster)):
                x, y = randint(0, self.size[0]-1), randint(10, self.size[1]-10)
            self.monsters.append(Monster(self, self.player, x, y))
            
    def monster_touched_by_bullet(self, indice_bullet):
        x, y = self.bullets[indice_bullet].get_x(), self.bullets[indice_bullet].get_y()
        nb_monster = len(self.monsters)
        for i in range(nb_monster):
            x_m, y_m, h = self.monsters[i].get_x(), self.monsters[i].get_y(), self.monsters[i].get_height()
            if(x < x_m+h and x>x_m-h and y < y_m+h and y>y_m-h):
                self.monsters[i].take_damage(self.bullet_damage)
                if(self.monsters[i].get_hp() <= 0):
                    self.monsters.pop(i)
                return True
        return False
        
    
    def its_a_wall(self, i, j, h):
        h = int(h*0.7)
        x_t, y_t, result = [i, i-h, i+h], [j, j-h, j+h], []
        for k in range(3):
            for l in range(3):
                x, y = self.convert(x_t[k], y_t[l])
                result.append(not self.coord_valid(x, y) or self.map_tab[x][y] == 1)
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
    
    def brut_coord_valid(self, i, j):
        i, j = self.convert(i, j)
        return self.coord_valid(i, j)
        
    def there_is_a_wall_near(self, map_tab, i, j):  
        return (i-1>=0 and map_tab[i-1][j] == 1) or (i+1<self.nb_case_horizontal and map_tab[i+1][j] == 1) or (j+1<self.nb_case_vertical and map_tab[i][j+1] == 1) or (j-1>=0 and map_tab[i][j-1] == 1)
    

            
    def try_to_switch_map(self):
        if(self.out_open and self.its_change_room_case(self.player.get_x(), self.player.get_y())):
            self.choix_en_cours = True
            self.monster_speed += 2
            self.current_room += 1
            self.map_tab = self.generate_random_map()
            self.player.spawn()
            self.generate_ennemies()
            self.augment_choosed = False

    
    def display_room_number(self):
        nb_room_txt = self.font_nb_room.render('Room '+str(self.current_room), False, (0, 0, 200))
        self.screen.blit(nb_room_txt, (self.size[0]-150, 30))

    
    def init_const(self):    
        self.bullets = []
        self.explosions = []
        self.monsters = []
        self.base_hp_monsters = 10
        self.nb_monster_per_room = 6
        self.bg_color = (0, 0, 0)
        self.health_bar_color = (150, 0, 0)
        self.next_room_color = (255, 246, 159)
        self.augment_case_color = (230, 0, 0)
        self.iter = 0
        self.current_room = 1
        self.damage_monster = 1
        self.running = True
        self.out_open = False
        self.choix_en_cours = False
        self.nb_case_vertical = 30
        self.nb_case_horizontal = 50
        self.width_case = self.size[0]//self.nb_case_horizontal
        self.height_case = self.size[1]//self.nb_case_vertical
        self.bullet_damage = 2
        self.moves_dico = {'z': 3, 'q': 1, 'd': 0, 's': 2}
        self.monster_speed = 5
        self.height_monster = 20
        self.player = Player(self)
        self.moves = [[False, (self.player.get_speed(), 0)], [False, (-self.player.get_speed(), 0)], [False, (0, self.player.get_speed())], [False, (0, -self.player.get_speed())]]

    def build_img(self):
        self.wall_img = pg.image.load(self.img_path + "/wall.png")  
        self.floor_img = pg.image.load(self.img_path + "/floor.png")  
        self.personnage_img = pg.image.load(self.img_path + "/personnage.jpg")  
        self.personnage_img = pg.transform.scale(self.personnage_img, (self.width_case, self.height_case))
        self.wall_img = pg.transform.scale(self.wall_img, (self.width_case, self.height_case))
        self.floor_img = pg.transform.scale(self.floor_img, (self.width_case, self.height_case))
        self.font_game_over = pg.font.SysFont('Comic Sans MS', int(self.size[0]*0.09))
        self.game_over_txt = self.font_game_over.render('Game Over', False, (200, 0, 0))
        self.font_nb_room = pg.font.SysFont('Comic Sans MS', 30)
        self.font_augment = pg.font.SysFont('Comic Sans MS', 100)