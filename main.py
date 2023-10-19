from src.game import Game
import os
import pygame as pg
from src.bullet import Bullet

def main():
    pg.init()
    pg.font.init()
    game = Game("./img")
    clock = pg.time.Clock()
    while game.running:
        game.iter += 1
        game.screen.fill(game.bg_color)
        event_gestion(game)
        if(game.player.get_hp() <= 0):
            game.screen.blit(game.game_over_txt, (int(game.size[0]*0.35), int(game.size[1]*0.4)))
        elif(game.choix_en_cours):
            game.display_choose_menu()
        else:
            if(len(game.monsters) == 0):
                game.out_open = True
            else:
                game.out_open = False
            
            game.display_map()
            game.display_room_number()
            pg.draw.rect(game.screen, game.health_bar_color, (0, game.size[1]-8, game.player.get_hp()*game.size[0]/game.player.get_max_hp(), game.menu_bar_height+8))
            game.display_bullets()
            game.move_player()
            if(game.start_count < 50):
                game.start_count += 1
            elif(game.start_count == 50):
                game.generate_ennemies()
                game.start_count += 1
            else:
                game.display_monsters()
                if(game.current_room != 5):
                    game.move_monsters()
                else:
                    game.monsters[0].move()
            game.player.draw()
        pg.display.flip()
        clock.tick(60)
    pg.quit()


def event_gestion(game):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.running = False
        if(game.player.hp > 0):
            if(event.type == pg.KEYDOWN):
                if(event.unicode in game.moves_dico):
                    game.moves[game.moves_dico[event.unicode]][0] = True
            elif(event.type == pg.KEYUP and event.unicode in game.moves_dico):
                game.moves[game.moves_dico[event.unicode]][0] = False
            elif(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                if(not game.choix_en_cours):
                    if(game.player.get_x() != event.pos[0]):
                        game.bullets.append(Bullet(game, game.player, event.pos[0], event.pos[1]))
                else:
                    x, y = event.pos[0], event.pos[1]
                    if(y>=game.size[1]*0.1 and y<=game.size[1]*0.3):
                        game.choix_en_cours = False
                        game.player.set_speed(int(game.player.get_speed()*1.2))
                        game.moves = [[False, (game.player.get_speed(), 0)], [False, (-game.player.get_speed(), 0)], [False, (0, game.player.get_speed())], [False, (0, -game.player.get_speed())]]
                    elif(y>=game.size[1]*0.3 and y<=game.size[1]*0.6):
                        game.choix_en_cours = False
                        game.bullet_damage += 2
                    elif(y>=game.size[1]*0.7 and y<=game.size[1]*0.9):
                        game.choix_en_cours = False
                        game.player.regen()

if(__name__ == "__main__"):
    main()