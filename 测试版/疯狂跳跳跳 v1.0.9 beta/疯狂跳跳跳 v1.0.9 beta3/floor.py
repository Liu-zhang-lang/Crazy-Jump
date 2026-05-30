import pygame as pg
import random as rd
from const import *
class Floor(pg.sprite.Sprite):
    def __init__(self,x=-1,y=-1,len=-1,time=3):
        super().__init__()
        self.x=x
        self.y=y
        self.len=len
        if x==-1:
            self.x=rd.randint(0,700)
        if y==-1:
            self.y=rd.randint(240,400)
        if len==-1:
            self.len=rd.randint(60,150)
        self.image=pg.Surface((self.len,5))
        self.time=time
        self.time2=time
        pg.draw.rect(self.image,"white",(0,0,self.len,5))
        self.rect=pg.rect.Rect(self.x,self.y,self.len,5)
        self.is_touch=False
    def update(self):
        if self.is_touch==False or self.time<=-1:
            return
        self.time-=1/60
        if self.time/self.time2>2/3 and self.time<self.time2:
            pg.draw.rect(self.image,"green",(0,0,self.len,5))
        elif self.time/self.time2>1/3 and self.time<=self.time2*2/3:
            pg.draw.rect(self.image,"yellow",(0,0,self.len,5))
        elif self.time>0 and self.time<=self.time2/3:
            pg.draw.rect(self.image,"red",(0,0,self.len,5))
        else:
            self.kill()