import pygame as pg
from const import *
class Button(pg.sprite.Sprite):
    def __init__(self,pos,width,height,fill_color,outline_color=None,outline_width=2,align="topleft",text="",text_color="white",font=cn_def): 
        super().__init__()
        self.is_clicked=False
        self.text=text
        if outline_color==None:
            outline_color=fill_color
        self.image=pg.Surface((width,height))
        self.image.fill(outline_color)
        pg.draw.rect(self.image,fill_color,self.image.get_rect(),outline_width)
        text_img=font.render(text,True,text_color)
        self.image.blit(text_img,text_img.get_rect(center=(width/2,height/2)))
        if align=="topleft":
            self.rect=self.image.get_rect(topleft=pos)
        elif align=="topright":
            self.rect=self.image.get_rect(topright=pos)
        elif align=="center":
            self.rect=self.image.get_rect(center=pos)
        else:
            print("[error:Button,__init__]align不存在")
    def update(self,events):
        if self.is_clicked:
            return
        for event in events:
            if event.type==pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.is_clicked=True
    def check_clicked(self):
        return self.is_clicked