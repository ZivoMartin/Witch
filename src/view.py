import pygame as pg
from random import randint
import math

class View():
    
    
    def __init__(self, img_path):
        self.img_path = img_path
        self.size = (2000, 1050)
        self.bg_color = (0, 0, 0)
        self.next_room_color = (255, 246, 159)
        self.bullets_color = (228, 91, 0)
        self.dt = 0
        self.iter = 0
        running = True
        self.out_open = True
        self.nb_case_vertical = 40
        self.nb_case_horizontal = 60
        self.width_case = int(self.size[0]/self.nb_case_horizontal)
        self.height_case = int(self.size[1]/self.nb_case_vertical)
        self.map_tab = self.generate_random_map()
        self.player_pos = [int(self.size[0]/2), int(self.size[1]/2)]
        self.spawn_player()
        self.speed = 4
        self.moves = [[False, (self.speed, 0)], [False, (-self.speed, 0)], [False, (0, self.speed)], [False, (0, -self.speed)]]
        self.wall_img = pg.image.load(img_path + "/wall.png")  
        self.floor_img = pg.image.load(img_path + "/floor.png")  
        self.personnage_img = pg.image.load(img_path + "/personnage.jpg")  
        self.personnage_img = pg.transform.scale(self.personnage_img, (30, 70))
        self.explosion_img = pg.image.load(img_path + "/explosion.jpg")  
        self.explosion_img = pg.transform.scale(self.explosion_img, (10, 10))
        self.wall_img = pg.transform.scale(self.wall_img, (self.width_case, self.height_case))
        self.floor_img = pg.transform.scale(self.floor_img, (self.width_case, self.height_case))
        self.bullets = []
        self.explosions = []
        self.life_time_explosions = 20
        self.bullets_speed = 10
        self.moves_dico = {'z': 3, 'q': 1, 'd': 0, 's': 2}
        pg.init()
        self.screen = pg.display.set_mode(self.size)
        clock = pg.time.Clock()


        while running:
            self.screen.fill(self.bg_color)
            self.iter += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if(event.type == pg.KEYDOWN):
                    if(event.unicode in self.moves_dico):
                        self.moves[self.moves_dico[event.unicode]][0] = True
                elif(event.type == pg.KEYUP and event.unicode in self.moves_dico):
                    self.moves[self.moves_dico[event.unicode]][0] = False
                elif(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                    x1, y1, x2, y2 = self.player_pos[0], self.player_pos[1], event.pos[0], event.pos[1]
                    m, d, b, f = get_param(x1, y1, x2, y2)
                    self.bullets.append({"x": x1, "y": y1, "m": m, "dist": d-self.bullets_speed, "b": b, "f": f, "x2": x2, "y2": y2})

                    
            # if(self.iter % 100 == 0):
            #     self.map_tab = self.generate_random_map()
            self.display_map()
                                            
            # print(self.moves)
            
                
            
            self.display_bullets()
            self.display_explosions()
            self.move_player()

            pg.draw.circle(self.screen, "black", self.player_pos, 20)
            # self.screen.blit(self.personnage_img, self.player_pos)
            
            pg.display.flip()
            clock.tick(60)

        pg.quit()
        
        
    def display_bullets(self):
        for i in range(len(self.bullets)):
            if(i>=len(self.bullets)):
                break
            pg.draw.circle(self.screen, self.bullets_color, (self.bullets[i]["x"], self.bullets[i]["y"]), 10)
            self.bullets[i]["dist"] -= self.bullets_speed
            self.bullets[i]["x"] = self.bullets[i]["x2"] - int(self.bullets[i]["f"]*(self.bullets[i]["dist"]/math.sqrt(self.bullets[i]["m"]**2 + 1)))
            self.bullets[i]["y"] = int(self.bullets[i]["x"]*self.bullets[i]["m"] + self.bullets[i]["b"])
            if(self.its_a_wall(self.bullets[i]["x"], self.bullets[i]["y"])):
                self.explosions.append([self.bullets[i]["x"], self.bullets[i]["y"], 10])
                self.bullets.pop(i)
                    
    def move_player(self):
        for i in range(4):
            if(self.moves[i][0] and not self.its_a_wall(self.player_pos[0]+self.moves[i][1][0], self.player_pos[1]+self.moves[i][1][1])):
                self.player_pos[0] += self.moves[i][1][0]
                self.player_pos[1] += self.moves[i][1][1]
                self.try_to_switch_map()  
                
    def display_map(self):
        for i in range(self.nb_case_horizontal):
            for j in range(self.nb_case_vertical):
                if(self.map_tab[i][j] == 0):
                    self.screen.blit(self.floor_img, (i*self.width_case, j*self.height_case))
                elif(self.map_tab[i][j] == 1):
                    self.screen.blit(self.wall_img, (i*self.width_case, j*self.height_case))
                elif(self.map_tab[i][j] == 2):
                    pg.draw.rect(self.screen, self.next_room_color, (i*self.width_case, j*self.height_case, self.width_case, self.height_case)) 
                
    
    def display_explosions(self):
        for i in range(len(self.explosions)):
            if(i>=len(self.explosions)):
                break
            self.screen.blit(self.explosion_img, (self.explosions[i][0], self.explosions[i][1]))
            self.explosions[i][2] += 1
            if(self.explosions[i][2] == self.life_time_explosions):
                self.explosions.pop(i)
    
    def its_a_wall(self, i, j):
        i, j = self.convert(i, j)
        return not self.coord_valid(i, j) or self.map_tab[i][j] == 1

    def its_change_room_case(self, i, j):
        i, j = self.convert(i, j)
        return self.coord_valid(i, j) and self.map_tab[i][j] == 2
    
    def convert(self, i, j):
        return int(i/self.width_case), int(j/self.height_case)
        
    def generate_random_coord(self):
        return [randint(0, self.size[0]), randint(0, self.size[1])]

    def generate_random_map(self):
        map_tab = [None]*self.nb_case_horizontal
        
        for i in range(self.nb_case_horizontal):
            map_tab[i] = [0]*self.nb_case_vertical
        
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
              
        for i in range(self.nb_case_horizontal):
            for j in range(self.nb_case_vertical):
                if(self.there_is_a_wall_near(map_tab, i, j) and randint(1, 3) == 1):
                    map_tab[i][j] = 1
                elif(randint(1, 14) == 1):
                    map_tab[i][j] = 1
        i = randint(0, self.nb_case_horizontal-1)
        j = randint(0, self.nb_case_vertical-1)
        if(self.out_open):
            while(map_tab[i][j] == 1):
                i = randint(0, self.nb_case_horizontal-1)
                j = randint(0, self.nb_case_vertical-1)
            map_tab[i][j] = 2      
        return map_tab
    
    def coord_valid(self, i, j):
        return i>=0 and j>=0 and i<self.nb_case_horizontal and j<self.nb_case_vertical
        
    def there_is_a_wall_near(self, map_tab, i, j):  
        return (i-1>=0 and map_tab[i-1][j] == 1) or (i+1<self.nb_case_horizontal and map_tab[i+1][j] == 1) or (j+1<self.nb_case_vertical and map_tab[i][j+1] == 1) or (j-1>=0 and map_tab[i][j-1] == 1)
    
    def spawn_player(self):
        i, j = self.convert(self.player_pos[0], self.player_pos[1])
        while(self.map_tab[i][j]):
            self.player_pos[0] = randint(10, self.size[0]-10)
            self.player_pos[1] = randint(10, self.size[1]-10)
            i, j = self.convert(self.player_pos[0], self.player_pos[1])
            
    def try_to_switch_map(self):
        if(self.its_change_room_case(self.player_pos[0], self.player_pos[1])):
            self.map_tab = self.generate_random_map()
            self.spawn_player()
    
def get_param(x1, y1, x2, y2):
    m = (y1-y2)/(x1-x2)
    factor = 1
    if(x1>x2):
        m = (y2-y1)/(x2-x1)
        factor = -1
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    b = y1 - m*x1
    return m, dist, b, factor


# keys = pg.key.get_pressed()
# if keys[pg.K_w]:
#     player_pos[0][1] -= 300 * dt
# if keys[pg.K_s]:
#     player_pos[0][1] += 300 * dt
# if keys[pg.K_a]:
#     player_pos[0][0] -= 300 * dt
# if keys[pg.K_d]:
#     player_pos[0][0] += 300 * dt
# pg.draw.rect(self.screen, "red", (300, 300, 50, 50))
# nb_circle = len(self.circles)
# for i in range(nb_circle):
#     pg.draw.circle(self.screen, "red", self.circles[i], 40)