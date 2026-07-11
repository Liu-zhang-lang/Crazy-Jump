import pygame as pg
from subs.button import Button
from subs.info import Info
from subs.const import *
class Test:
    def __init__(self,game):
        self.info=[pg.sprite.Group() for _ in range(10)]
        self.game=game
        self.button=pg.sprite.Group()
        self.title=cn_big.render("测试",True,"white") 
        self.maxpage=9
    def init_button(self):
        self.button.empty()
        self.button.add(Button((w-30,30),30,30,"blue",text="×",align="topright"))
    def button_handle(self):
        for bt in self.button:
            if bt.check_click():
                if bt.text=="×":
                    return True
    def draw(self):
        self.game.draw()
        window.blit(gray_img,(0,0))
        window.blit(self.title,self.title.get_rect(center=(w/2,40)))
        self.button.draw(window)
    def menu(self):
        self.init_button()
        self.button.add(Button((50,550),30,30,"blue",align="topleft",text="<-"))
        self.button.add(Button((w-50,550),30,30,"blue",align="topright",text="->"))
        index=0
        while True:
            events=self.game.event_handle()
            self.button.update(events)
            self.draw()
            self.info[index].draw(window)
            img=cn_def.render(f"第{index+1}/{self.maxpage}页",True,"white")
            window.blit(img,img.get_rect(center=(w/2,565)))
            if self.button_handle():
                return
            for bt in self.button:
                if bt.check_click() and bt.rect.y!=30:
                    if bt.text=="<-":
                        if index>0:
                            index-=1
                    elif bt.text=="->":
                        if index<self.maxpage-1:
                            index+=1
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_LEFT:
                        if index>0:
                            index-=1
                    elif ev.key==pg.K_RIGHT:
                        if index<self.maxpage-1:
                            index+=1
                    elif ev.key==pg.K_ESCAPE:
                        return True
            pg.display.update()
            clock.tick(60)