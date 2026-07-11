import pygame as pg
import copy
from subs.info import Info
from subs.const import *
from subs.button import Button
class Achiev:
    def __init__(self,game):
        self.game=game
        self.achievs={
            "first_game":{
                "name":"梦开始的地方",
                "desc":"玩一局游戏",
                "difficulty":"easy"
            },
            "new_record":{
                "name":"打破新纪录",
                "desc":"打破一次自己的最佳纪录",
                "difficulty":"easy"
            },
            "quick_died":{
                "name":"速战速决",
                "desc":"在10秒内死亡",
                "difficulty":"normal"
            },
            "crazy_jump":{
                "name":"疯狂跳跳跳",
                "desc":"在一局游戏内跳跃超过100次",
                "difficulty":"normal"
            },
            "can't_died":{
                "name":"把血包当饭吃",
                "desc":"血量达到150",
                "difficulty":"normal"
            },
            "survival_1m":{
                "name":"生存小师",
                "desc":"生存1分钟",
                "difficulty":"easy"
            },
            "survival_2m":{
                "name":"生存中师",
                "desc":"生存2分钟",
                "difficulty":"normal"
            },
            "survival_3m":{
                "name":"生存大师",
                "desc":"生存3分钟",
                "difficulty":"hard"
            },
            "survival_4m":{
                "name":"生存之神",
                "desc":"生存4分钟",
                "difficulty":"hard"
            },
            "jump_out":{
                "name":"看看外面的世界",
                "desc":"向上跳出屏幕",
                "difficulty":"normal"
            },
            "didn't_hurt_in_60s":{
                "name":"身法这一块",
                "desc":"在前60秒没有掉血",
                "difficulty":"hard"
            },
            "hurt_50_times":{
                "name":"行走的沙包",
                "desc":"受伤50次",
                "difficulty":"normal"
            },
            "hurt_40_in_0.1s":{
                "name":"疼疼疼！",
                "desc":"在0.1秒内受到40点伤害",
                "difficulty":"normal"
            },
            "hurt_outside":{
                "name":"天外来敌！！！",
                "desc":"在屏幕外受到雨点伤害",
                "difficulty":"hard"
            },
            "touch_head_hurt":{
                "name":"地板，我谢谢你！",
                "desc":"被刷新出来的地板顶头后受伤",
                "difficulty":"hard"
            },
            "4_floor":{
                "name":"运气感人",
                "desc":"场上同时存在4个地板（不包括底部地板）",
                "difficulty":"hard"
            },
            "meet_boss":{
                "name":"什么？",
                "desc":"遇到boss",
                "difficulty":"normal"
            },
            "kill_boss":{
                "name":"我成功了！！！",
                "desc":"击杀boss",
                "difficulty":"hard"
            },
            "vanished":{
                "name":"得来全不费工夫",
                "desc":"瞬捡血包",
                "difficulty":"hard"
            }
        }
        self.achievs_list=[]
        for achiev in self.achievs.keys():
            self.achievs_list.append(achiev)
        self.maxline=15
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
        if self.game.is_debug and not self.game.developer_mode:
            return False
        if achiev not in self.achievs_list:
            add_error(f"[error:Achiev/check]({achiev})不存在")
            return False
        if achiev not in self.game.user.achievs:
            self.game.user.achievs[achiev]=False
        p=self.game.player.sprites()[0]
        if self.game.user.achievs[achiev]:
            return False
        elif achiev=="new_record":
            if self.game.mode=="normal" and self.game.time>self.game.user.best["normal"]["time"] and self.game.user.best["normal"]["time"]>0:
                return True
            elif self.game.mode=="boss" and self.game.time<self.game.user.best["boss"]["time"] and self.game.user.best["boss"]["time"]<inf and self.game.spawn_boss==True and len(self.game.boss.sprites())==0:
                return True
        elif achiev=="quick_died":
            if self.game.time<=10 and self.game.heart<=0:
                return True
        elif achiev=="can't_died":
            if self.game.heart>=150:
                return True
        elif achiev=="first_game":
            if self.game.time>0:
                return True
        elif achiev=="survival_1m":
            if self.game.time>=60:
                return True
        elif achiev=="survival_2m":
            if self.game.time>=120:
                return True
        elif achiev=="survival_3m":
            if self.game.time>=180:
                return True
        elif achiev=="survival_4m":
            if self.game.time>=240:
                return True
        elif achiev=="crazy_jump":
            if p.jump_cnt>=100:
                return True
        elif achiev=="jump_out":
            if p.rect.top<=0:
                return True
        elif achiev=="didn't_hurt_in_60s":
            if self.game.time>=60 and self.game.game_stats.query("hurt","cnt")==0:
                return True
        elif achiev=="hurt_50_times":
            if self.game.game_stats.query("hurt","cnt")>=50:
                return True
        elif achiev=="hurt_40_in_0.1s":
            if self.game.time>0.1 and self.game.game_stats.query("hurt","sum")-self.game.game_stats_list[min(5,len(self.game.game_stats_list)-1)]["hurt"]["sum"]>=40:
                return True
        elif achiev=="4_floor":
            if len(self.game.floor.sprites())-1>=4:
                return True
        elif achiev=="meet_boss":
            if len(self.game.boss.sprites())>=1:
                return True
        elif achiev=="kill_boss":
            if self.game.game_stats.query("kill/boss","cnt")>=1:
                return True
        elif achiev=="touch_head_hurt":
            if self.game.time>0.1 and p.touch_head_achiev_cd>0 and self.game.game_stats.query("hurt","cnt")-self.game.game_stats_list[min(5,len(self.game.game_stats_list)-1)]["hurt"]["cnt"]>=1:
                return True
        elif achiev=="hurt_outside":
            if self.game.time>0.1 and self.game.game_stats.query("hurt/rain","cnt")-self.game.game_stats_list[0]["hurt"]["subs"]["rain"]["cnt"]>=1 and p.rect.top<=0:
                return True
        elif achiev=="vanished":
            return self.game.is_vanished_achiev
        elif achiev in self.achievs_list:
            add_error(f"[error:Achiev/check]achiev({achiev})未被判断")
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
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_LEFT:
                        if index>0:
                            index-=1
                    elif ev.key==pg.K_RIGHT:
                        if index<self.maxpage-1:
                            index+=1
            pg.display.update()
            clock.tick(60)
    def get_color(self,difficulty):
        if difficulty=="easy":
            return "green"
        elif difficulty=="normal":
            return "yellow"
        elif difficulty=="hard":
            return "darkorange"
        else:
            add_error(f"[error:Achiev/get_color]difficulty({difficulty})不存在！")
            return "green"
    def get_achiev_info(self):
        page=1
        line=0
        fst_pos=[50,70]
        fst_pos2=[170,70]
        for key,ach in self.achievs.items():
            line+=1
            if line>self.maxline:
                page+=1
                line=1
            if self.game.user.achievs[key]:
                self.achievs_info[page-1]=Info.append_info(self.achievs_info[page-1],"（已达成）",fst_pos,color="gold",back_color=None,mode="back",spacing=5)
                self.achievs_info[page-1]=Info.append_info(self.achievs_info[page-1],f"[{ach['name']}]:{ach['desc']}",fst_pos2,color=self.get_color(ach['difficulty']),back_color=None,mode="back",spacing=5)
            else:
                self.achievs_info[page-1]=Info.append_info(self.achievs_info[page-1],"（未达成）",fst_pos,color="gray",back_color=None,mode="back",spacing=5)
                self.achievs_info[page-1]=Info.append_info(self.achievs_info[page-1],f"[{ach['name']}]:{ach['desc']}",fst_pos2,color=self.get_color(ach['difficulty']),back_color=None,mode="back",spacing=5)
