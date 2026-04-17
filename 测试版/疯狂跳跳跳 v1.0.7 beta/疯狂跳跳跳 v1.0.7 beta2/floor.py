import pygame as pg
import random as rd
from const import *
class Floor(pg.sprite.Sprite):
    def __init__(self,x,y,len):
        super().__init__()
        self.x=x
        self.y=y
        self.len=len
        if x==-1:
            self.x=rd.randint(0,700)
        if y==-1:
            self.y=rd.randint(250,400)
        if len==-1:
            self.len=rd.randint(60,150)
        self.image=pg.Surface((self.len,5))
        self.time=3
        if self.len==w:
            self.time=-2
        pg.draw.rect(self.image,"white",(0,0,self.len,5))
        self.rect=pg.rect.Rect(self.x,self.y,self.len,5)
        self.is_touch=False
    def update(self):
        if self.is_touch==False:
            return
        if self.time>0:
            self.time-=1/60
        if self.time>2 and self.time<=3:
            pg.draw.rect(self.image,"green",(0,0,self.len,5))
        elif self.time>1 and self.time<=2:
            pg.draw.rect(self.image,"yellow",(0,0,self.len,5))
        elif self.time>0 and self.time<=1:
            pg.draw.rect(self.image,"red",(0,0,self.len,5))
        if self.time<=0 and self.time>=-1:
            self.kill()