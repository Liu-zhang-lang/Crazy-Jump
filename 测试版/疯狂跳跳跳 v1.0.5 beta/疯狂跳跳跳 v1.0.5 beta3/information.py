import pygame as pg
from const import *
class Information(pg.sprite.Sprite):
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
    def add_inf(inf,inf_string,col):
        for i in inf:
            i.rect.top+=chinese_font_size
        inf.add(Information(inf_string,[w,chinese_font_size],col))
        return inf