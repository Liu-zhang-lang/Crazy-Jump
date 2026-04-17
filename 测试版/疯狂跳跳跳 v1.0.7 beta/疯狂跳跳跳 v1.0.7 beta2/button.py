import pygame as pg
from const import *
class Button(pg.sprite.Sprite):
    def __init__(self,pos,width,height,fill_color,outline_color=None,outline_width=2,align="topleft",text="",text_color="white",font=cn_def,mode=1,click_color=None):
        # mode1:点击消失,2:点击不消失
        super().__init__()
        self.w=width
        self.h=height
        self.is_clicked=False
        self.text=text
        if outline_color==None:
            outline_color=fill_color
        if click_color==None:
            click_color=fill_color
        self.click_color=click_color
        self.outline_width=outline_width
        self.outline_color=outline_color
        self.fill_color=fill_color
        self.mode=mode
        self.image=pg.Surface((width,height))
        self.image.fill(outline_color)
        pg.draw.rect(self.image,fill_color,self.image.get_rect(),outline_width)
        self.text_img=font.render(text,True,text_color)
        self.image.blit(self.text_img,self.text_img.get_rect(center=(width/2,height/2)))
        if align=="topleft":
            self.rect=self.image.get_rect(topleft=pos)
        elif align=="topright":
            self.rect=self.image.get_rect(topright=pos)
        elif align=="center":
            self.rect=self.image.get_rect(center=pos)
        else:
            print("[error:Button,__init__]align不存在")
    def update(self,events):
        if self.is_clicked and self.mode==1:
            return
        for event in events:
            if event.type==pg.MOUSEBUTTONDOWN:
                self.image.fill(self.outline_color)
                if self.rect.collidepoint(event.pos):
                    self.is_clicked=True
                    pg.draw.rect(self.image,self.click_color,self.image.get_rect(),self.outline_width)
                    self.image.blit(self.text_img,self.text_img.get_rect(center=(self.w/2,self.h/2)))
                else:
                    self.is_clicked=False
                    pg.draw.rect(self.image,self.fill_color,self.image.get_rect(),self.outline_width)
                    self.image.blit(self.text_img,self.text_img.get_rect(center=(self.w/2,self.h/2)))
    def check_clicked(self):
        return self.is_clicked