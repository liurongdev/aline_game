

import sys
import pygame
from settings import  Settings
from ship import Ship
import game_functions as gf
from game_states import GameStates
from buttton import  Button
from alien import Alien
from pygame.sprite import Group
from time import sleep

from scoreboard import ScoreBoard


def run_game():
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_hight))
    pygame.display.set_caption("Aline avision")

    ship=Ship(ai_settings,screen)
    bullets=Group()
    bullets.is_continue_fire=False
    #alien=Alien(ai_settings,screen)

    button=Button(ai_settings,screen,"Play")
    states=GameStates(ai_settings)

    aliens=Group()

    gf.create_fleet(ai_settings,screen,ship,aliens)

    sb=ScoreBoard(ai_settings,screen,states)
    while True:
        gf.check_events(ai_settings,screen,states,sb,button,ship,aliens,bullets)
        if states.game_active:
            ship.update()

            #gf.bullet_update(bullets)
            gf.update_aliens(ai_settings,states,screen,sb,ship,aliens,bullets)
            gf.update_bullets(ai_settings,screen,states,sb,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,states ,sb,ship,aliens,bullets,button)





run_game()