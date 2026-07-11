import pygame as pg
from subs.const import *
class Button(pg.sprite.Sprite):
    def __init__(self,pos,width,height,fill_color,outline_color=None,outline_width=2,align="topleft",text="",text_color="white",font=cn_def,hover_color="white"):
        super().__init__()
        self.w=width
        self.h=height
        self.is_click=False
        self.is_hover=False
        self.text=text
        if outline_color==None:
            outline_color=fill_color
        if hover_color==None:
            hover_color=fill_color
        self.hover_color=hover_color
        self.outline_width=outline_width
        self.outline_color=outline_color
        self.fill_color=fill_color
        self.image=pg.Surface((width,height))
        self.image.fill(outline_color)
        pg.draw.rect(self.image,fill_color,self.image.get_rect(),outline_width)
        self.text_img=font.render(text,True,text_color,None)
        self.image.blit(self.text_img,self.text_img.get_rect(center=(width/2,height/2)))
        if align=="topleft":
            self.rect=self.image.get_rect(topleft=pos)
        elif align=="topright":
            self.rect=self.image.get_rect(topright=pos)
        elif align=="center":
            self.rect=self.image.get_rect(center=pos)
        else:
            add_error(f"[error:Button/__init__]align({align})不存在")
            self.rect=self.image.get_rect(topleft=pos)
    def update(self,events):
        self.is_click=False
        for ev in events:
            if ev.type==pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(ev.pos):
                    self.is_click=True
        flag=self.rect.collidepoint(pg.mouse.get_pos())
        if flag and not self.is_hover:
            self.is_hover=True
            self.image.fill(self.outline_color)
            pg.draw.rect(self.image,self.hover_color,self.image.get_rect(),self.outline_width)
            self.image.blit(self.text_img,self.text_img.get_rect(center=(self.w/2,self.h/2)))
        elif not flag and self.is_hover:
            self.is_hover=False
            self.image.fill(self.outline_color)
            pg.draw.rect(self.image,self.fill_color,self.image.get_rect(),self.outline_width)
            self.image.blit(self.text_img,self.text_img.get_rect(center=(self.w/2,self.h/2)))
    def check_click(self):
        return self.is_click
