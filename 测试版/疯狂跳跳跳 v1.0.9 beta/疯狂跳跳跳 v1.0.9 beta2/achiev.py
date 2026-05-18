import pygame as pg
import copy
from info import Info
from const import *
from button import Button
class Achiev:
    def __init__(self,game):
        self.game=game
        self.achievs={
            "first_game":{
                "name":"游戏开始",
                "desc":"第一次开始游戏"
            },
            "new_record":{
                "name":"打破新纪录",
                "desc":"打破一次自己的最佳纪录"
            },
            "quick_died":{
                "name":"速战速决",
                "desc":"在10秒内死亡"
            },
            "crazy_jump":{
                "name":"疯狂跳跳跳",
                "desc":"在一局游戏内跳跃超过100次"
            },
            "can't_died":{
                "name":"这能死？",
                "desc":"血量达到150"
            },
            "survival_1m":{
                "name":"生存小师",
                "desc":"生存1分钟"
            },
            "survival_2m":{
                "name":"生存中师",
                "desc":"生存2分钟"
            },
            "survival_3m":{
                "name":"生存大师",
                "desc":"生存3分钟"
            },
        }
        self.achievs_list=[]
        for achiev in self.achievs.keys():
            self.achievs_list.append(achiev)
        self.maxline=13
        self.maxpage=int((len(self.achievs_list)+self.maxline-1)/self.maxline)
        self.achievs_info=[pg.sprite.Group() for _ in range(self.maxpage+5)]
        self.backup_achievs_info=copy.deepcopy(self.achievs_info)
        self.title=cn_big.render("成就",True,"white")
        self.button=pg.sprite.Group()
    def check_all(self):
        tmp={}
        for key,achiev in self.achievs.items():
            if self.check(key):
                tmp[key]=achiev
        return tmp
    def check(self,achiev):
        if self.game.is_debug:
            return False
        if achiev not in self.achievs_list:
            print("[error:achiev,check]achiev不存在！")
            return False
        if achiev not in self.game.user.achievs:
            self.game.user.achievs[achiev]=False
        if self.game.user.achievs[achiev]:
            return False
        if achiev=="new_record":
            if self.game.time>self.game.user.best_time and self.game.user.best_time>0 and self.game.heart<=0:
                return True
        elif achiev=="quick_died":
            if self.game.time<10 and self.game.heart<=0:
                return True
        elif achiev=="can't_died":
            if self.game.heart>=150:
                return True
        elif achiev=="first_game" and self.game.time>0:
            return True
        elif achiev=="survival_1m" and self.game.time>=60:
            return True
        elif achiev=="survival_2m" and self.game.time>=120:
            return True
        elif achiev=="survival_3m" and self.game.time>=180:
            return True
        elif achiev=="crazy_jump" and self.game.player.sprites()[0].jump_cnt>=100:
            return True
        return False
    def init_button(self):
        self.button.add(Button((w-30,30),30,30,"blue",align="topright",text="×"))
    def button_handle(self,events):
        for bt in self.button:
            if bt.check_click() and bt.rect.y==30:
                if bt.text=="×":
                    return True
        for ev in events:
            if ev.type==pg.KEYDOWN:
                if ev.key==pg.K_ESCAPE:
                    return True
    def draw(self):
        self.game.draw()
        window.blit(gray_img,(0,0))
        self.button.draw(window)
    def show_achiev(self):
        self.achievs_info=copy.deepcopy(self.backup_achievs_info)
        self.init_button()
        self.get_achiev_info()
        index=0
        self.button.add(Button((50,550),30,30,"blue",align="topleft",text="<-"))
        self.button.add(Button((w-50,550),30,30,"blue",align="topright",text="->"))
        while True:
            events=self.game.event_handle()
            self.button.update(events)
            self.draw()
            self.achievs_info[index].draw(window)
            img=cn_def.render(f"第{index+1}/{self.maxpage}页",True,"white")
            window.blit(img,img.get_rect(center=(w/2,565)))
            window.blit(self.title,self.title.get_rect(center=(w/2,40)))
            if self.button_handle(events):
                return
            for bt in self.button:
                if bt.check_click() and bt.rect.y!=30:
                    if bt.text=="<-":
                        if index>0:
                            index-=1
                    elif bt.text=="->":
                        if index<self.maxpage-1:
                            index+=1
            pg.display.update()
            clock.tick(60)
    def get_achiev_info(self):
        page=1
        line=0
        fst_pos=[50,70]
        for key,ach in self.achievs.items():
            line+=1
            if line>self.maxline:
                page+=1
                line=1
            if self.game.user.achievs[key]:
                self.achievs_info[page-1]=Info.append_info(self.achievs_info[page-1],f"（已达成）[{ach['name']}]:{ach['desc']}",fst_pos,color="gold",back_color=None,mode="back",spacing=5)
            else:
                self.achievs_info[page-1]=Info.append_info(self.achievs_info[page-1],f"（未达成）[{ach['name']}]:{ach['desc']}",fst_pos,color="gray",back_color=None,mode="back",spacing=5)
