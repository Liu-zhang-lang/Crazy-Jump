import pygame as pg
from const import *
class Info(pg.sprite.Sprite):
    def __init__(self,inf_string,right_top_pos,col):
        super().__init__()
        self.image=chinese_font.render(inf_string,True,col)
        self.rect=pg.rect.Rect(right_top_pos[0]-self.image.get_width(),right_top_pos[1],self.image.get_width(),self.image.get_height())
        self.time=2
    def update(self):
        self.time-=1/60
        if self.time<=0:
            self.kill()
    @staticmethod
    def add_info(info,info_string,col):
        for i in info:
            i.rect.top+=chinese_font_size
        info.add(Info(info_string,[w,chinese_font_size*2],col))
        return info