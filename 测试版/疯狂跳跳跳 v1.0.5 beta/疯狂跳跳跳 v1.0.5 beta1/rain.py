import pygame as pg
import random as rd
from const import *
class Rain(pg.sprite.Sprite):
    def __init__(self,len):
        pg.sprite.Sprite.__init__(self)
        self.len=len
        if self.len==-1:
            self.len=rd.randint(20,50)
        self.image=pg.Surface((8,self.len),pg.SRCALPHA)
        pg.draw.rect(self.image,"#27A2D7",(0,0,8,self.len))
        self.image=pg.transform.rotate(self.image,-45)
        pg.transform.rotate(self.image,45)
        self.rect=self.image.get_rect()
        self.rect.x=rd.randint(100,w)
        self.rect.y=-50
    def update(self):
        self.rect.y+=5
        self.rect.x-=5
        if self.rect.y>=h+50 or self.rect.x<-50 or self.rect.x>w+50:
            self.kill()