import pygame as pg
from const import *
class Info(pg.sprite.Sprite):
    def __init__(self,info_string,font,fst_pos,pos,color,align,time,spacing=0):
        super().__init__()
        self.spacing=spacing
        self.align=align
        self.time=time
        self.font_size=font.get_height()
        self.image=font.render(info_string,True,color)
        self.fst_pos=fst_pos
        self.w=self.image.get_width()
        self.h=self.image.get_height()
        if align=="topright":
            self.rect=pg.rect.Rect(pos[0]-self.w,pos[1],self.w,self.h)
        elif align=="topleft":
            self.rect=pg.rect.Rect(pos[0],pos[1],self.w,self.h)
        elif align=="center":
            self.rect=pg.rect.Rect(pos[0]-self.w/2,pos[1]-self.h/2,self.w,self.h)
        else:
            print("[error:Info,__init__]align不存在")
    def update(self):
        self.time-=1/60
        if self.time<=0 and self.time>-1:
            self.kill()
    @staticmethod
    def add_info(info,info_string,pos,align="topleft",font=cn_def,color="white",time=2):
        info.add(Info(info_string,font,pos,pos,color,align,time))
        return info
    @staticmethod
    def append_info(info,info_string,fst_pos,align="topleft",font=cn_def,color="white",time=2,spacing=0,mode="front"):
        sum=0
        for i in info:
            if i.align==align and i.fst_pos==fst_pos:
                if mode=="front":
                    i.rect.y+=i.font_size+i.spacing+spacing
                else:
                    sum+=i.font_size+i.spacing
        if mode=="back":
            info.add(Info(info_string,font,fst_pos,[fst_pos[0],fst_pos[1]+sum+spacing],color,align,time,spacing))
        elif mode=="front":
            info.add(Info(info_string,font,fst_pos,fst_pos,color,align,time,spacing))
        else:
            print("[error:Info,append_info]mode不存在")
        return info