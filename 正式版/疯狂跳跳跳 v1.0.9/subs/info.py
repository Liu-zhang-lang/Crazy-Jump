import pygame as pg
from subs.const import *
class Info(pg.sprite.Sprite):
    def __init__(self,text,font,fst_pos,pos,color,align,time,back_color,len=1,max_len=114514,spacing=0):
        super().__init__()
        self.spacing=spacing
        self.align=align
        self.time=time
        self.font_size=font.get_height()
        self.image=font.render(text,True,color,back_color)
        self.fst_pos=fst_pos
        self.max_len=max_len
        self.len=len
        self.text=text
        self.w=self.image.get_width()
        self.h=self.image.get_height()
        if align=="topright":
            self.rect=pg.rect.Rect(pos[0]-self.w,pos[1],self.w,self.h)
        elif align=="topleft":
            self.rect=pg.rect.Rect(pos[0],pos[1],self.w,self.h)
        elif align=="center":
            self.rect=pg.rect.Rect(pos[0]-self.w/2,pos[1]-self.h/2,self.w,self.h)
        else:
            add_error("[error:Info,__init__]align不存在")
            self.rect=pg.rect.Rect(pos[0]-self.w,pos[1],self.w,self.h)
    def update(self):
        self.time-=1/60
        if self.time<=0 and self.time>-1:
            self.kill()
        if self.len>self.max_len:
            self.kill()
    @staticmethod
    def add_info(info,text,pos,align="topleft",font=cn_def,color="white",back_color="black",time=2):
        info.add(Info(text,font,pos,pos,color,align,time,back_color))
        return info
    @staticmethod
    def append_info(info,text,fst_pos,align="topleft",font=cn_def,color="white",back_color="black",time=2,spacing=0,max_len=114514,mode="front"):
        sum=0
        len=1
        fst_spacing=999
        fst_y=999
        for i in info:
            if i.align==align and i.fst_pos==fst_pos:
                if mode=="front":
                    i.rect.y+=i.font_size+i.spacing+spacing
                    i.len+=1
                else:
                    if i.rect.y<fst_y:
                        fst_y=i.rect.y
                        fst_spacing=i.spacing
                    sum+=i.font_size+i.spacing
                    len+=1
        if fst_spacing==999 or mode=="front":
            fst_spacing=spacing
        sum-=fst_spacing
        if mode=="back" and len<=max_len:
            info.add(Info(text,font,fst_pos,[fst_pos[0],fst_pos[1]+sum+spacing],color,align,time,back_color,len=len,max_len=max_len,spacing=spacing))
        elif mode=="front" and len<=max_len:
            info.add(Info(text,font,fst_pos,fst_pos,color,align,time,back_color,len=len,max_len=max_len,spacing=spacing))
        elif len<=max_len:
            add_error("[error:Info,append_info]mode不存在")
        return info