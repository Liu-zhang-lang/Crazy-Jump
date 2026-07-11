import pygame as pg
import random as rd
from subs.const import *
class Rain(pg.sprite.Sprite):
    def __init__(self,len=-1,draw_num=False):
        super().__init__()
        self.len=len
        if self.len==-1:
            self.len=rd.randint(20,50)
        self.image=pg.Surface((8,self.len),pg.SRCALPHA)
        pg.draw.rect(self.image,"#27A2D7",(0,0,8,self.len))
        self.image=pg.transform.rotate(self.image,-45)
        self.rect=self.image.get_rect()
        self.rect.x=rd.randint(100,w)
        self.rect.bottom=0
        self.rain_img=self.image.copy()
        self.number_text=cn_def.render(str(int(self.len//6.5)),True,"white")
        img_w,img_h=self.number_text.get_size()
        t=min(self.image.get_width()/img_w/1.2,self.image.get_height()/img_h/1.2)
        img_w*=t
        img_h*=t
        img_w=int(img_w)
        img_h=int(img_h)
        self.number_text=pg.transform.scale(self.number_text,(img_w,img_h))
        if draw_num:
            self.draw_pic(True)
    def update(self):
        self.rect.y+=5
        self.rect.x-=5
        if self.rect.y>=h+50 or self.rect.x<-50 or self.rect.x>w+50:
            self.kill()
    def draw_pic(self,draw_num=False):
        self.image=self.rain_img.copy()
        if draw_num:
            self.image.blit(self.number_text,self.number_text.get_rect(center=(self.image.get_width()/2,self.image.get_height()/2)))
