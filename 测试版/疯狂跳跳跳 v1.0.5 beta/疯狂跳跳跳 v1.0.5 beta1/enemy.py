import pygame as pg
import random as rd
from const import *
class Enemy(pg.sprite.Sprite):
    def __init__(self,f):
        super().__init__()
        self.minspeed=2
        self.maxspeed=6
        self.b=rd.randint(15,35)
        self.image=pg.Surface((self.b,self.b))
        pg.draw.rect(self.image,"red",(0,0,self.b,self.b))
        if rd.random()>0.5:
            self.rect=pg.rect.Rect(w,500-self.b,self.b,self.b)
            self.speed=rd.randint(self.minspeed,self.maxspeed)
            if (rd.random()<=0.05 and f!=1) or f==2:
                pg.draw.rect(self.image,"purple",(0,0,self.b,self.b))
                self.speed=12
        else:
            self.rect=pg.rect.Rect(-self.b,500-self.b,self.b,self.b)
            self.speed=-rd.randint(self.minspeed,self.maxspeed)
            if(rd.random()<=0.05 and f!=1) or f==2:
                pg.draw.rect(self.image,"purple",(0,0,self.b,self.b))
                self.speed=-12
    def update(self):
        self.rect.x-=self.speed
        if self.rect.x+self.b<0 or self.rect.x>w:
            self.kill()
        if rd.random()<=0.0015 and self.b-5>=10 and abs(self.speed)-1>=2:
            self.speed=-self.speed
            self.b-=5
            self.image=pg.transform.scale(self.image,(self.b,self.b))
            self.rect=pg.rect.Rect(self.rect.x,500-self.b,self.b,self.b)
            if self.speed>0:
                self.speed-=1
            else:
                self.speed+=1