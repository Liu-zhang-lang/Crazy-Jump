import pygame as pg
import copy
from subs.button import Button
from subs.info import Info
from subs.const import *
class Leaderboard:
    def __init__(self,game):
        self.info={}
        self.info["normal"]=[pg.sprite.Group() for _ in range(10)]
        self.info["boss"]=[pg.sprite.Group() for _ in range(10)]
        self.info_backup=copy.deepcopy(self.info)
        self.game=game
        self.button=pg.sprite.Group()
        self.title=cn_big.render("排行榜",True,"white") 
        self.maxpage=1
        self.max_line=15
        self.mode=self.game.mode
    def init_button(self):
        self.button.empty()
        self.button.add(Button((50,70),100,30,"blue",text="普通模式",font=cn_sm))
        self.button.add(Button((160,70),100,30,"blue",text="打boss模式",font=cn_sm))
        self.button.add(Button((w-30,70),30,30,"blue",text="×",align="topright"))
    def button_handle(self):
        for bt in self.button:
            if bt.check_click():
                if bt.text=="普通模式":
                    self.mode="normal"
                elif bt.text=="打boss模式":
                    self.mode="boss"
                elif bt.text=="×":
                    return True
    def draw(self):
        self.game.draw()
        window.blit(gray_img,(0,0))
        window.blit(self.title,self.title.get_rect(center=(w/2,40)))
        self.button.draw(window)
    def menu(self):
        self.get_leaderboard()
        self.init_button()
        self.button.add(Button((50,550),30,30,"blue",align="topleft",text="<-"))
        self.button.add(Button((w-50,550),30,30,"blue",align="topright",text="->"))
        index=0
        while True:
            events=self.game.event_handle()
            self.button.update(events)
            self.draw()
            self.info[self.mode][index].draw(window)
            st="Unknown"
            if self.mode=="normal":
                st="普通模式"
            elif self.mode=="boss":
                st="打boss模式"
            img=cn_def.render(f"{st}：第{index+1}/{self.maxpage}页",True,"white")
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
    def get_leaderboard(self):
        self.info=copy.deepcopy(self.info_backup)
        cnt=0
        users={}
        for name in self.game.user.users_data:
            u=self.game.user.users_data[name]
            users[name]=u["best"]
        users2=sorted(users.items(),key=lambda x:x[1]["normal"]["time"],reverse=True)
        self.maxpage=(len(users2)-1)//self.max_line+1
        for name,u in users2:
            cnt+=1
            if u["normal"]["time"]==0:
                st="暂无"
            elif u["normal"]["minutes"]>0:
                st=f"{u['normal']['minutes']}分{u['normal']['seconds']:.2f}秒（{u['normal']['version']}）"
            else:
                st=f"{u['normal']['seconds']:.2f}秒（{u['normal']['version']}）"
            if cnt==1:
                color="gold"
            elif cnt==2:
                color="#B5B5B5"
            elif cnt==3:
                color=(205,127,50)
            else:
                color="white"
            self.info["normal"][(cnt-1)//self.max_line]=Info.append_info(self.info["normal"][(cnt-1)//self.max_line],f"{cnt}.{name}:{st}",[50,110],color=color,back_color=None,mode="back")
        users2=sorted(users.items(),key=lambda x:x[1]["boss"]["time"])
        cnt=0
        for name,u in users2:
            cnt+=1
            if u["boss"]["time"]==inf:
                st="暂无"
            elif u["boss"]["minutes"]>0:
                st=f"{u['boss']['minutes']}分{u['boss']['seconds']:.2f}秒（{u['boss']['version']}）"
            else:
                st=f"{u['boss']['seconds']:.2f}秒（{u['boss']['version']}）"
            if cnt==1:
                color="gold"
            elif cnt==2:
                color="#B5B5B5"
            elif cnt==3:
                color=(205,127,50)
            else:
                color="white"
            self.info["boss"][(cnt-1)//self.max_line]=Info.append_info(self.info["boss"][(cnt-1)//self.max_line],f"{cnt}.{name}:{st}",[50,110],color=color,back_color=None,mode="back")
