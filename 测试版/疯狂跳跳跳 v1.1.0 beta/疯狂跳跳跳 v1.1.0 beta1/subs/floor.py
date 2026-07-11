import pygame as pg
import random as rd
from subs.const import *
class Floor(pg.sprite.Sprite):
    def __init__(self,x=-1,y=-1,len=-1,time=3,align="topleft"):
        super().__init__()
        self.x=x
        self.y=y
        self.len=len
        self.existence_time=0
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
        if align=="topleft":
            self.rect=pg.rect.Rect(self.x,self.y,self.len,5)
        elif align=="topright":
            self.rect=pg.rect.Rect(self.x-self.len,self.y,self.len,5)
        elif align=="center":
            self.rect=pg.rect.Rect(self.x-self.len/2,self.y,self.len,5)
        else:
            add_error(f"[error:Floor/__init__]align({align})不存在")
        self.is_touch=False
    def update(self):
        self.existence_time+=1/60
        if self.is_touch==False or self.time<=-1:
            return
        self.time-=1/60
        if self.time/self.time2>2/3 and self.time<self.time2:
            pg.draw.rect(self.image,"green",(0,0,self.len,5))
        elif self.time/self.time2>1/3 and self.time<=self.time2*2/3:
            pg.draw.rect(self.image,"yellow",(0,0,self.len,5))
        elif self.time>0.5 and self.time<=self.time2/3:
            pg.draw.rect(self.image,"orange",(0,0,self.len,5))
        elif self.time>0 and self.time<=0.5:
            pg.draw.rect(self.image,"red",(0,0,self.len,5))
        else:
            self.kill()