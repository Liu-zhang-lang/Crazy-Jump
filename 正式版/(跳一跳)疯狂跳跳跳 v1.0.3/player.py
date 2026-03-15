import pygame as pg
from const import *
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pw=30
        self.ph=60
        self.image=pg.Surface((self.pw,self.ph))
        pg.draw.rect(self.image,"blue",(0,0,self.pw,self.ph))
        self.rect=pg.rect.Rect(0,440,self.pw,self.ph)
        self.rect.centerx=window.get_rect().centerx
        self.velocity_y=0
        self.jumping=False
    def update(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.x-=5
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.x+=5
        if self.rect.x<0:
            self.rect.x=0
        if self.rect.x+self.pw>w:
            self.rect.x=w-self.pw
        if (keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]) and self.jumping==False:
            self.jumping=True
            self.velocity_y=-14
        if self.jumping==True:
            self.rect.y+=self.velocity_y
            self.velocity_y+=0.8
        if self.rect.y>440:
            self.rect.y=440
            self.jumping=False