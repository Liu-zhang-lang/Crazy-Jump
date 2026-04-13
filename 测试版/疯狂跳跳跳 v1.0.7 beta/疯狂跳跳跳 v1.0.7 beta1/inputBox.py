import pygame as pg
from const import *
class InputBox(pg.sprite.Sprite):
    def __init__(self,x,y,width,height,outline_color,fill_color,tip,align="topleft",is_selected=False,outline_width=2,font=cn_def,font_size=cn_def_sz,multiple_inputs=False,hidden_string=False):
        super().__init__()
        self.is_selected=is_selected
        self.hidden_string=hidden_string
        self.multiple_inputs=multiple_inputs
        self.is_finished=False
        self.cursor_pos=0
        self.cursor_change_time=0.5
        self.cursor_is_show=False
        self.cursor_left_text_width=0
        self.cd_keys_time={}
        self.pressing_keys=[]
        self.other_keys=[pg.K_LEFT,pg.K_RIGHT,pg.K_BACKSPACE,pg.K_RETURN,pg.K_DELETE]
        self.w=width
        self.h=height
        self.outline_color=outline_color
        self.fill_color=fill_color
        self.outline_width=outline_width
        self.font=font
        self.font_size=font_size
        self.tip=tip
        self.input_text=""
        self.image=pg.Surface((self.w,self.h))
        self.image_rect=self.image.get_rect()
        self.tip_img=font.render(tip,True,"gray")
        self.input_text_img=font.render(self.input_text,True,"white")
        if align=="topright":
            x-=self.w
        elif align=="topleft":
            pass
        elif align=="center":
            x-=self.w/2
            y-=self.h/2
        else:
            print("[error:InputBox,__init__]align不存在")
        self.rect=pg.rect.Rect(x,y,self.w,self.h)
        self.draw_picture()
    def draw_picture(self):
        self.image.fill(self.fill_color)
        pg.draw.rect(self.image,self.outline_color,self.image_rect,self.outline_width)
        if self.input_text=="":
            self.image.blit(self.tip_img,self.tip_img.get_rect(center=(self.w/2,self.h/2)))
        else:
            if self.hidden_string:
                self.input_text_img=self.font.render("*"*len(self.input_text),True,"white")
            else:
                self.input_text_img=self.font.render(self.input_text,True,"white")
            self.image.blit(self.input_text_img,self.input_text_img.get_rect(center=(self.w/2,self.h/2)))
        if self.cursor_is_show:
            input_text_left=self.input_text_img.get_rect(center=(self.w/2,self.h/2)).x
            if self.hidden_string:
                input_text_left=self.font.render("*"*len(self.input_text),True,"white").get_rect(center=(self.w/2,self.h/2)).x
            cursor_x=input_text_left+self.cursor_left_text_width
            pg.draw.line(self.image,"white",(cursor_x,self.h/2-self.font_size/2),(cursor_x,self.h/2+self.font_size/2),2)
    def handle_key(self,key):
        is_valid=True
        if key==pg.K_RETURN:
            self.is_selected=False
            self.is_finished=True
        elif key==pg.K_BACKSPACE:
            if self.input_text!="" and self.cursor_pos>0:
                img=self.font.render(self.input_text[self.cursor_pos-1],True,"white")
                if self.hidden_string:
                    img=self.font.render("*",True,"white")
                self.cursor_left_text_width-=img.get_width()
                self.input_text=self.input_text[:self.cursor_pos-1]+self.input_text[self.cursor_pos:]
                self.cursor_pos-=1
        elif key==pg.K_DELETE:
            if self.cursor_pos<len(self.input_text):
                self.input_text=self.input_text[:self.cursor_pos]+self.input_text[self.cursor_pos+1:]
        elif key==pg.K_LEFT:
            if self.cursor_pos>0:
                img=self.font.render(self.input_text[self.cursor_pos-1],True,"white")
                if self.hidden_string:
                    img=self.font.render("*",True,"white")
                self.cursor_left_text_width-=img.get_width()
                self.cursor_pos-=1
        elif key==pg.K_RIGHT:
            if self.cursor_pos<len(self.input_text):
                img=self.font.render(self.input_text[self.cursor_pos-1+1],True,"white")
                if self.hidden_string:
                    img=self.font.render("*",True,"white")
                self.cursor_left_text_width+=img.get_width()
                self.cursor_pos+=1
        else:
            is_valid=False
        return is_valid
    def update(self,events):
        if self.is_finished and not self.multiple_inputs:
            return
        for ev in events:
            if ev.type==pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(ev.pos):
                    self.is_selected=True
                    self.cursor_pos=len(self.input_text)
                else:
                    self.is_selected=False
                    self.cursor_is_show=False
                    self.cursor_change_time=0.5
        if not self.is_selected:
            self.draw_picture()
            return
        self.cursor_change_time-=1/60
        if self.cursor_change_time<=0:
            self.cursor_change_time=0.5
            self.cursor_is_show=not self.cursor_is_show
        keys=pg.key.get_pressed()
        backup_cd_keys_time=self.cd_keys_time.copy()
        for key in backup_cd_keys_time:
            if keys[key]:
                self.cd_keys_time[key]-=1/60
                if self.cd_keys_time[key]<=0:
                    self.pressing_keys.append(key)
                    self.cd_keys_time.pop(key)
            else:
                self.cd_keys_time.pop(key)
        backup_pressing_keys=self.pressing_keys.copy()
        for key in backup_pressing_keys:
            if keys[key]:
                if 32<=key<=126:
                    self.input_text=self.input_text[:self.cursor_pos]+chr(key)+self.input_text[self.cursor_pos:]
                    if self.hidden_string:
                        key=ord("*")
                    self.cursor_pos+=1
                    img=self.font.render(chr(key),True,"white")
                    self.cursor_left_text_width+=img.get_width()
                else:
                    self.handle_key(key)
            else:
                self.pressing_keys.remove(key)
        for ev in events:
            if ev.type==pg.KEYDOWN:
                is_valid=False
                if ev.unicode and (not (ev.key in self.other_keys)):
                    self.input_text=self.input_text[:self.cursor_pos]+ev.unicode+self.input_text[self.cursor_pos:]
                    if self.hidden_string:
                        ev.unicode="*"
                    self.cursor_pos+=1
                    img=self.font.render(ev.unicode,True,"white")
                    self.cursor_left_text_width+=img.get_width()
                    is_valid=True
                else:
                    is_valid=self.handle_key(ev.key)
                if is_valid:
                    self.cd_keys_time[ev.key]=0.5
        self.draw_picture()
    def get_input_text(self):
        return self.input_text
    def check_finished(self):
        return self.is_finished