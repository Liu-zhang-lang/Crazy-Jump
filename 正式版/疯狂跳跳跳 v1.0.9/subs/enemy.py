import pygame as pg
import random as rd
from subs.const import *
class Enemy(pg.sprite.Sprite):
    def __init__(self,f=0,draw_num=False):
        super().__init__()
        self.minspeed=2
        self.maxspeed=6
        self.show_number=False
        self.b=rd.randint(15,35)
        self.image=pg.Surface((self.b,self.b))
        pg.draw.rect(self.image,"red",(0,0,self.b,self.b))
        self.is_super=False
        if rd.random()>0.5:
            self.rect=pg.rect.Rect(w,500-self.b,self.b,self.b)
            self.speed=rd.randint(self.minspeed,self.maxspeed)
            if (rd.random()<=0.05 and f!=1) or f==2:
                self.image.fill("purple")
                self.speed=12
                self.is_super=True
        else:
            self.rect=pg.rect.Rect(-self.b,500-self.b,self.b,self.b)
            self.speed=-rd.randint(self.minspeed,self.maxspeed)
            if(rd.random()<=0.05 and f!=1) or f==2:
                self.image.fill("purple")
                self.speed=-12
                self.is_super=True
        self.enemy_img=self.image.copy()
        if self.speed==12 or self.speed==-12:
            self.number_text=cn_def.render(str(int(self.b//1.8)),True,"white")
        else:
            self.number_text=cn_def.render(str(int(self.b//3)),True,"white")
        img_w,img_h=self.number_text.get_size()
        t=min(self.b/img_w,self.b/img_h)
        img_w*=t
        img_h*=t
        img_w=int(img_w)
        img_h=int(img_h)
        self.number_text=pg.transform.scale(self.number_text,(img_w,img_h))
        if draw_num:
            self.draw_pic(True)
    def update(self):
        self.rect.x-=self.speed
        if self.rect.x+self.b<0 or self.rect.x>w:
            self.kill()
        if rd.random()<=0.0015 and self.b-5>=10 and abs(self.speed)-1>=2:
            self.speed=-self.speed
            self.b-=5
            if self.is_super:
                self.number_text=cn_def.render(str(int(self.b//1.8)),True,"white")
            else:
                self.number_text=cn_def.render(str(int(self.b//3)),True,"white")
            img_w,img_h=self.number_text.get_size()
            t=min(self.b/img_w,self.b/img_h)
            img_w*=t
            img_h*=t
            img_w=int(img_w)
            img_h=int(img_h)
            self.number_text=pg.transform.scale(self.number_text,(img_w,img_h))
            self.enemy_img=pg.transform.scale(self.enemy_img,(self.b,self.b))
            self.rect=pg.rect.Rect(self.rect.x,500-self.b,self.b,self.b)
            self.draw_pic(self.show_number)
            if self.speed>0:
                self.speed-=1
            else:
                self.speed+=1
    def draw_pic(self,draw_number=False):
        self.image=self.enemy_img.copy()
        self.show_number=False
        if draw_number:
            self.image.blit(self.number_text,self.number_text.get_rect(center=(self.b/2,self.b/2)))
            self.show_number=True
