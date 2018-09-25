import pygame
from pygame.sprite import Sprite
from time import sleep
class Bullet(Sprite):
    def __init__(self,screen,ai_settings,ship):
        super().__init__()
        self.screen=screen

        #画出一个矩形
        self.rect=pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx=ship.rect.centerx
        self.rect.top=ship.rect.top

        self.y=float(self.rect.y)
        self.color=ai_settings.bullet_color
        self.speed_factor=ai_settings.bullet_speed_factor

        self.is_continue_fire=False


    def update(self):
        self.y -= self.speed_factor

        #更新子弹的位置
        self.rect.y=self.y


    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)


