import pygame as pg
import random as rd
import math
from subs.const import *
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,angle,speed,damage,draw_num=False):
        super().__init__()
        if x==-1:
            x=rd.randint(0,w)
        if y==-1:
            y=rd.randint(0,h)
        if angle==-1:
            angle=rd.randint(0,360)
        if speed==-1:
            speed=rd.randint(5,11)
        if damage==-1:
            damage=rd.randint(5,10)
        self.x=x
        self.y=y
        self.w=30
        self.h=7
        self.angle=angle
        self.speed=speed
        self.damage=damage
        rad=math.radians(angle)
        self.vx=self.speed*math.cos(rad)
        self.vy=self.speed*math.sin(rad)
        self.image=pg.Surface((self.w,self.h),pg.SRCALPHA)
        self.image.fill("orange")
        self.image=pg.transform.rotate(self.image,-self.angle)
        self.rect=self.image.get_rect(center=(self.x,self.y))
        self.bullet_img=self.image.copy()
        self.number_text=cn_def.render(str(int(self.damage)),True,"white")
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
        self.x+=self.vx
        self.y+=self.vy
        self.rect.center=(self.x,self.y)
        if self.rect.left<-100 or self.rect.right>w+100 or self.rect.top<-100 or self.rect.bottom>h+100:
            self.kill()
    def draw_pic(self,draw_num=False):
        self.image=self.bullet_img.copy()
        if draw_num:
            self.image.blit(self.number_text,self.number_text.get_rect(center=(self.image.get_width()/2,self.image.get_height()/2)))