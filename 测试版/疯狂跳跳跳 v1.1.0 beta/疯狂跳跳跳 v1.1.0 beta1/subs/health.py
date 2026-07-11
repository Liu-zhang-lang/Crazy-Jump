import pygame as pg
import random as rd
from subs.const import *
class Health(pg.sprite.Sprite):
    def __init__(self,f=0,x=-1,y=-1,h=-1,draw_num=False):
        super().__init__()
        if (rd.random()<=0.05 and f!=1) or f==2:
            self.b=40
        else:
            self.b=rd.randint(15,35)
        if x==-1:
            x=rd.randint(0,w-self.b)
        if y==-1:
            y=rd.randint(200,450)
        if h==-1:
            if self.b!=40:
                self.h=self.b//3
            else:
                self.h=25
        else:
            self.h=h
        if self.b!=40:
            self.number_text=cn_def.render(str(self.h),True,"white")
        else:
            self.number_text=cn_def.render(str(self.h),True,"red")
        img_w,img_h=self.number_text.get_size()
        time=min(self.b/img_w,self.b/img_h)
        img_w*=time
        img_h*=time
        img_w=int(img_w)
        img_h=int(img_h)
        self.number_text=pg.transform.scale(self.number_text,(img_w,img_h))
        self.rect=pg.Rect((x,y),(self.b,self.b))
        self.image=pg.Surface((self.b,self.b))
        if self.b!=40:
            pg.draw.rect(self.image,"green",(0,0,self.b,self.b))
        else:
            pg.draw.rect(self.image,"yellow",(0,0,self.b,self.b))
        self.health_img=self.image.copy()
        self.existence_time=0
        if draw_num:
            self.draw_pic(True)
    def update(self):
        self.existence_time+=1/60
    def draw_pic(self,show_number=False):
        self.image=self.health_img.copy()
        if show_number:
            self.image.blit(self.number_text,self.number_text.get_rect(center=(self.b/2,self.b/2)))