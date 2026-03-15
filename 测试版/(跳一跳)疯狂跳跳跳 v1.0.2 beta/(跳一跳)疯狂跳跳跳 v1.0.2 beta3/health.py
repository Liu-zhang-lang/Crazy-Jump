import pygame as pg
import random as rd
from const import *
class Health(pg.sprite.Sprite):
    def __init__(self,f):
        super().__init__()
        if (rd.random()<=0.05 and f!=1) or f==2:
            self.b=40
            self.number_text=chinese_font.render("25",True,"red")
        else:
            self.b=rd.randint(15,35)
            self.number_text=chinese_font.render(str(self.b//3),True,"white")
        pg.transform.scale(self.number_text,(self.b,self.b))
        self.rect=pg.Rect((rd.randint(0,w-self.b),rd.randint(300,450)),(self.b,self.b))
        self.image=pg.Surface((self.b,self.b))
        if self.b!=40:
            pg.draw.rect(self.image,"green",(0,0,self.b,self.b))
        else:
            pg.draw.rect(self.image,"yellow",(0,0,self.b,self.b))
        self.image.blit(self.number_text,self.number_text.get_rect(center=(self.b//2,self.b//2)))