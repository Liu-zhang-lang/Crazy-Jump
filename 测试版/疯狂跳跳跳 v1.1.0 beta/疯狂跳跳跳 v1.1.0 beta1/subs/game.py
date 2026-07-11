from subs.const import *
from subs.enemy import Enemy
from subs.health import Health
from subs.player import Player
from subs.info import Info
from subs.debug import Debug
from subs.floor import Floor
from subs.rain import Rain
from subs.inputBox import InputBox
from subs.button import Button
from subs.user import User
from subs.settings import Settings
from subs.achiev import Achiev
from subs.gameStats import GameStats
from subs.boss import Boss
from subs.compend import Compend
from subs.changelog import Changelog
from subs.leaderboard import Leaderboard
import pygame as pg
import random as rd
import ctypes as cyp
import pyperclip as pc
import math
class Game:
    def __init__(self):
        rd.seed(time.time())
        self.user=User(self)
        self.settings=Settings(self)
        self.achiev=Achiev(self)
        self.compend=Compend(self)
        self.changelog=Changelog(self)
        self.auto_login=False
        self.is_f1=False
        self.is_play=False
        self.reset()
        self.leaderboard=Leaderboard(self)
    def reset(self):
        self.fps=0
        self.heart=40
        self.time=0 #真实秒数
        self.seconds=0
        self.minutes=0
        self.last_hurt=0
        self.level=1
        self.mode="normal"
        self.pro=all_pro[0]
        self.hpro=all_hpro[0]
        self.fpro=all_fpro[0]
        self.rpro=all_rpro[0]
        self.spawn_boss=False
        self.is_debug=False
        self.god_mode=False
        self.developer_mode=False
        self.new_record_tip=False
        self.debug_tip=False
        self.is_vanished_achiev=False
        self.enemy=pg.sprite.Group()
        self.health=pg.sprite.Group()
        self.player=pg.sprite.Group()
        self.info=pg.sprite.Group()
        self.floor=pg.sprite.Group()
        self.rain=pg.sprite.Group()
        self.achiev_info=pg.sprite.Group()
        self.boss=pg.sprite.Group()
        self.bullet=pg.sprite.Group()
        self.player.add(Player(self))
        self.floor.add(Floor(0,500,w,-1))
        self.floor.add(Floor(w/2-40,360,80,2))
        self.game_stats=GameStats(self)
        self.game_stats_list=[]
    def restart(self):
        self.reset()
        info=pg.sprite.Group()
        button=pg.sprite.Group()
        id=-1
        x1=w/2-200
        x2=w/2+200
        info=Info.add_info(info,"普通模式",[x1,h/2-200],align="center",font=cn_big,back_color=None)
        info=Info.append_info(info,"经典的模式，不会刷新boss",[x1,h/2-150],align="center",back_color=None,mode="back")
        info=Info.append_info(info,"坚持得越久越好",[x1,h/2-150],align="center",back_color=None,mode="back")
        button.add(Button([x1,h/2+50],100,50,"blue",text="选择",align="center"))
        info=Info.add_info(info,"打boss模式",[x2,h/2-200],align="center",font=cn_big,back_color=None)
        info=Info.append_info(info,"新模式，第八阶段会刷新boss",[x2,h/2-150],align="center",back_color=None,mode="back")
        info=Info.append_info(info,"你也可以在暂停界面提前生成boss",[x2,h/2-150],align="center",back_color=None,mode="back")
        info=Info.append_info(info,"总之，击杀boss越快越好",[x2,h/2-150],align="center",back_color=None,mode="back")
        button.add(Button([x2,h/2+50],100,50,"blue",text="选择",align="center"))
        while id==-1:
            events=self.event_handle()
            self.draw()
            window.blit(gray_img,(0,0))
            info.draw(window)
            button.draw(window)
            button.update(events)
            for bt in button:
                if bt.check_click():
                    if bt.rect.center[0]==x1:
                        id=1
                        break
                    if bt.rect.center[0]==x2:
                        id=2
                        break
            pg.display.update()
            clock.tick(60) 
        if id==1:
            self.mode="normal"
        elif id==2:
            self.mode="boss"
    def start_debug(self):
        debug=Debug(self)
        debug.start()
    def draw(self):
        window.fill("black")
        self.enemy.draw(window)
        self.health.draw(window)
        self.player.draw(window)
        self.floor.draw(window)
        self.rain.draw(window)
        self.bullet.draw(window)
        self.boss.draw(window)
        self.info.draw(window)
        self.achiev_info.draw(window)
        if self.level<len(level_up_time):
            time_remain=level_up_time[self.level][0]-self.time
            if time_remain>60:
                next_level_time=f"{time_remain//60}分{time_remain%60:.2f}秒"
            else:
                next_level_time=f"{time_remain:.2f}秒"
        else:
            next_level_time="无"
        if self.minutes>0:
            time=f"{self.minutes}分{self.seconds:.2f}秒"
        else:
            time=f"{self.seconds:.2f}秒"
        info=pg.sprite.Group()
        info=Info.add_info(info,f"时间:{time}",[0,0],back_color=None)
        info=Info.add_info(info,"FPS:",[0,cn_def_sz],back_color=None)
        if self.fps>=59:
            info=Info.add_info(info,f"{self.fps:.2f}",[50,cn_def_sz],color="green",back_color=None)
        elif self.fps>=53:
            info=Info.add_info(info,f"{self.fps:.2f}",[50,cn_def_sz],color="yellow",back_color=None)
        elif self.fps>=47:
            info=Info.add_info(info,f"{self.fps:.2f}",[50,cn_def_sz],color="orange",back_color=None)
        else:
            info=Info.add_info(info,f"{self.fps:.2f}",[50,cn_def_sz],color="red",back_color=None)
        info=Info.add_info(info,f"HP:{self.heart}",[w,0],"topright",back_color=None)
        info=Info.add_info(info,f"阶段:{self.level}",[w,cn_def_sz],"topright",back_color=None)
        info=Info.add_info(info,f"下一阶段:{next_level_time}",[w,cn_def_sz*2],"topright",back_color=None)
        if self.is_f1:
            pos1=(0,h-90)
            info=Info.append_info(info,f"pro:{self.pro*100:.2f}%",pos1,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"hpro:{self.hpro*100:.2f}%",pos1,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"fpro:{self.fpro*100:.2f}%",pos1,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"rpro:{self.rpro*100:.2f}%",pos1,font=cn_sm,mode="back",back_color=None)
            right=0
            right=max(right,cn_sm.render(f"pro:{self.pro*100:.2f}%",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"hpro:{self.hpro*100:.2f}%",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"fpro:{self.fpro*100:.2f}%",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"rpro:{self.rpro*100:.2f}%",True,"white").get_rect().width)
            right+=pos1[0]+10
            pos2=(right,h-90)
            info=Info.append_info(info,f"enemy_len:{len(self.enemy)}",pos2,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"health_len:{len(self.health)}",pos2,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"floor_len:{len(self.floor)}",pos2,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"rain_len:{len(self.rain)}",pos2,font=cn_sm,mode="back",back_color=None)
            right=0
            right=max(right,cn_sm.render(f"enemy_len:{len(self.enemy)}",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"health_len:{len(self.health)}",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"floor_len:{len(self.floor)}",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"rain_len:{len(self.rain)}",True,"white").get_rect().width)
            right+=pos2[0]+10
            pos3=(right,h-90)
            info=Info.append_info(info,f"bullet_len:{len(self.bullet)}",pos3,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"boss_len:{len(self.boss)}",pos3,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"jumps:{self.player.sprites()[0].jumping}",pos3,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"pos:[{self.player.sprites()[0].rect.x},{self.player.sprites()[0].rect.y}]",pos3,font=cn_sm,mode="back",back_color=None)
            right=0
            right=max(right,cn_sm.render(f"bullet_len:{len(self.bullet)}",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"boss_len:{len(self.boss)}",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"jumps:{self.player.sprites()[0].jumping}",True,"white").get_rect().width)
            right=max(right,cn_sm.render(f"pos:[{self.player.sprites()[0].rect.x},{self.player.sprites()[0].rect.y}]",True,"white").get_rect().width)
            right+=pos3[0]+10
            pos4=(right,h-90)
            info=Info.append_info(info,f"last_hurt:{self.last_hurt}",pos4,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"mode:{self.mode}",pos4,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"is_debug:{self.is_debug}",pos4,font=cn_sm,mode="back",back_color=None)
            info=Info.append_info(info,f"deve_mode:{self.developer_mode}",pos4,font=cn_sm,mode="back",back_color=None)
        info.draw(window)
        for a in level_up_time:
            if a[0]<=self.time<=a[1]:
                text=cn_big.render("下一阶段!",True,"white","black")
                window.blit(text,text.get_rect(center=(w/2,h/2-200)))
    def update(self,events):
        for ev in events:
            if ev.type==pg.KEYDOWN:
                if ev.key==pg.K_ESCAPE:
                    self.game_stop()
        is_level_up_time=False
        for i in range(len(level_up_time)):#难度增加
            if level_up_time[i][0]<=self.time<=level_up_time[i][1]:
                self.pro=all_pro[i]
                self.hpro=all_hpro[i]
                self.fpro=all_fpro[i]
                self.rpro=all_rpro[i]
                self.level=i+1
                if self.level==8:
                    if self.mode=="boss":
                        if self.spawn_boss==False:
                            self.spawn_boss=True
                            self.boss.add(Boss(self))
                    else:
                        self.pro=0.07
                        self.hpro=0.0075
                        self.fpro=0.0017
                        self.rpro=0.045
                is_level_up_time=True
                break
        if rd.random()<=self.pro:#生成敌人
            self.enemy.add(Enemy(draw_num=self.user.settings["enemy_show"]))
        if rd.random()<=self.hpro:#生成血包
            self.health.add(Health(draw_num=self.user.settings["health_show"]))
        if rd.random()<=self.fpro:#生成地面
            self.floor.add(Floor())
        if rd.random()<=self.rpro:#生成雨
            self.rain.add(Rain(draw_num=self.user.settings["rain_show"]))
        if len(error_msg)>0:
            for msg in error_msg:
                self.achiev_info=Info.append_info(self.achiev_info,msg,[0,cn_def_sz*2],font=cn_sm,color="red",time=3,max_len=10,back_color=None)
            error_msg.clear()
        self.fps=clock.get_fps()
        self.seconds+=1/60
        self.time+=1/60
        if self.seconds>=60:
            self.seconds-=60
            self.minutes+=1
        self.handle_key(events)
        last_jump_cnt=self.player.sprites()[0].jump_cnt
        if self.is_debug and self.debug_tip==False:
            self.debug_tip=True
            self.achiev_info=Info.append_info(self.achiev_info,"你使用了debug，将无法获得成就或创造新纪录！",[0,cn_def_sz*2],font=cn_sm,color="orange",time=3,max_len=10,back_color=None)
        if self.new_record_tip==False and self.is_debug==False and self.user.best[self.mode]["time"]>0:
            if self.mode=="normal" and self.time>self.user.best[self.mode]["time"]:
                self.new_record_tip=True
                self.achiev_info=Info.append_info(self.achiev_info,"新纪录达成！",[0,cn_def_sz*2],font=cn_sm,color="gold",time=3,max_len=10,back_color=None)
        self.enemy.update()
        self.rain.update()
        self.bullet.update()
        self.floor.update()
        self.boss.update()
        self.player.update()
        self.check_collisions()
        self.health.update()
        self.add_achiev_info()
        self.info.update()
        self.achiev_info.update()
        if self.player.sprites()[0].jump_cnt>last_jump_cnt:
            self.game_stats.add("jump",1)
        if self.heart<0:
            self.heart=0
        if self.developer_mode:
            self.game_stats.add("debug",-self.game_stats.query("debug","cnt"))
            self.is_debug=False
        self.game_stats_list.insert(0,self.game_stats.copy_stats())
        if len(self.game_stats_list)>60:
            self.game_stats_list.pop(60)
        if self.game_stats.query('hurt','sum')-self.game_stats_list[min(len(self.game_stats_list)-1,1)]['hurt']['sum']>0:
            self.last_hurt=self.game_stats.query('hurt','sum')-self.game_stats_list[min(len(self.game_stats_list)-1,1)]['hurt']['sum']
    def check_collisions(self):
        self.is_vanished_achiev=False
        co=pg.sprite.groupcollide(self.player,self.floor,False,False)
        for p,e_l in co.items():#地面碰撞检测
            for e in e_l:
                p.touch_floor(e)
                if e.is_touch==False:
                    self.game_stats.add("touch_floor",1)
                e.is_touch=True
        co=pg.sprite.groupcollide(self.boss,self.floor,False,False)
        for b,e_l in co.items():#boss和地面碰撞检测
            for e in e_l:
                b.touch_floor(e)
        co=pg.sprite.groupcollide(self.rain,self.floor,True,False,pg.sprite.collide_mask)#雨和地面碰撞检测（精确）
        co=pg.sprite.groupcollide(self.player,self.health,False,True)
        for p,e_l in co.items():#血包碰撞检测
            for e in e_l:
                if e.b==40:
                    self.hurt(-int(e.h))
                    self.game_stats.add("health/super_health",1,int(e.h))
                    for b in self.boss:
                        bhurt=b.hurt(max(int(e.h*0.25),2))
                        self.game_stats.add("attack/boss",1,bhurt)
                else:
                    self.hurt(-int(e.h))
                    self.game_stats.add("health/nor_health",1,int(e.h))
                    for b in self.boss:
                        bhurt=b.hurt(max(int(e.h*0.25),2))
                        self.game_stats.add("attack/boss",1,bhurt)
                if e.existence_time==0:
                    self.is_vanished_achiev=True
        if self.god_mode==False:
            co=pg.sprite.groupcollide(self.player,self.enemy,False,True)
            p=self.player.sprites()[0]
            for p,e_l in co.items():#敌人碰撞检测
                for e in e_l:
                    if e.is_super:
                        self.hurt(int(e.b//1.8))
                        self.game_stats.add("hurt/super_enemy",1,int(e.b//1.8))
                        for b in self.boss:
                            if b.hurt_recover_cd<=0:
                                b.hurt_recover_cd=1
                                b.recover(1)
                    else:
                        self.hurt(int(e.b//3))
                        self.game_stats.add("hurt/nor_enemy",1,int(e.b//3))
                        for b in self.boss:
                            if b.hurt_recover_cd<=0:
                                b.hurt_recover_cd=1
                                b.recover(1)
            co=pg.sprite.groupcollide(self.player,self.rain,False,True,pg.sprite.collide_mask) #pg.sprite.collide_mask是精确检测
            for p,e_l in co.items():#雨碰撞检测
                for e in e_l:
                    self.hurt(int(e.len//6.5))
                    self.game_stats.add("hurt/rain",1,int(e.len//6.5))
                    for b in self.boss:
                        if b.hurt_recover_cd<=0:
                            b.hurt_recover_cd=1
                            b.recover(1)
            co=pg.sprite.groupcollide(self.player,self.boss,False,False)
            for p,e_l in co.items():#boss碰撞检测
                for e in e_l:
                    if e.hurt_cd<=0:
                        e.touch_player=True
                        phurt=self.hurt(max(5,int(self.heart*0.1)))
                        bhurt=e.hurt(max(4,int(phurt*0.5)))
                        self.game_stats.add("hurt/boss",1,phurt)
                        self.game_stats.add("attack/boss",1,bhurt)
                        e.hurt_cd=0.5
            co=pg.sprite.groupcollide(self.player,self.bullet,False,True,pg.sprite.collide_mask)
            for p,e_l in co.items():#子弹碰撞检测
                for e in e_l:
                    self.hurt(e.damage)
                    self.game_stats.add("hurt/bullet",1,e.damage)
    def hurt(self,damage):
        hurt=self.player.sprites()[0].hurt(damage)
        return hurt
    def rules(self):
        info=pg.sprite.Group()
        info=Info.append_info(info,"使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"按下Esc暂停游戏，按下Esc或Enter继续",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"躲避红色/紫色(加强)敌人和天空中的雨水",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"拾取绿色/黄色(加强)血包",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"输入法为中文时，可能会导致部分按键失效",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"按两次跳跃可以二段跳",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"地图中会随机生成地板，可供站立3秒",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"进入游戏结束界面/暂停界面/游戏中，按Ctrl+M返回主页（不保存",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"进度），按S进入设置，按A进入成就系统，按U进入账号系统，按P",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"进入排行榜，按R重新开始，按G查看规则（当前页面），按T查看统",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"计信息，按C查看图鉴，按L查看更新内容，按F1查看额外信息",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"暂停界面下，按Ctrl+D打开debug模式（但成绩与成就将不记录）",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"若在游戏过程出现[error...]的输出、游戏崩溃或游戏bug，",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"请报告给作者",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"按下Enter键退出规则页面",[50,60],back_color=None,spacing=5,mode="back")
        self.draw()
        window.blit(gray_img,(0,0))
        info.draw(window)
        pg.display.update()
        running=True
        while running:
            events=self.event_handle()
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_RETURN:
                        running=False
                        break
            clock.tick(60)
    def main_menu(self):
        self.reset()
        info_pos=[530,110]
        info=pg.sprite.Group()
        short_info=pg.sprite.Group()
        button=pg.sprite.Group()
        info=Info.add_info(info,"疯狂跳跳跳",[w/2,70],align="center",font=cn_big,back_color=None)
        info=Info.append_info(info,f"欢迎回来，{self.user.user_name}",[50,110],spacing=5,back_color=None,mode="back")
        info=Info.append_info(info,"按U进入账号界面",[50,110],spacing=5,back_color=None,mode="back")
        info=Info.append_info(info,"按L查看更新内容",[50,110],spacing=5,back_color=None,mode="back")
        info=Info.add_info(info,"作者：Liu_zhang_lang",[750,525],font=cn_sm,align="topright",back_color=None)
        info=Info.add_info(info,f"版本号：{version}",[w/2,30],align="center",back_color=None)
        info=Info.add_info(info,"↓↓支持一下我朋友的游戏↓↓",[50,525],font=cn_fonts[18],back_color=None)
        button.add(Button((50,200),250,50,"blue",text="开始游戏"))
        button.add(Button((750,550),200,30,"blue",align="topright",text="复制github仓库链接",font=cn_sm))
        button.add(Button((50,550),260,30,"blue",text="复制chest in the maps链接",font=cn_fonts[19]))
        button.add(Button((770,50),50,30,"blue",align="topright",text="刷新"))
        text_img=(cn_def.render(slogans[rd.randint(0,len(slogans)-1)],True,"yellow"))
        if self.check_chinese():
            short_info=Info.append_info(short_info,"[警告]当前输入法为中文，",info_pos,color="orange",time=3,font=cn_sm,spacing=3,back_color=None)
            short_info=Info.append_info(short_info,"可能会使字母按键失效",info_pos,color="orange",time=3,font=cn_sm,spacing=3,back_color=None,mode="back")
        if self.auto_login:
            short_info=Info.append_info(short_info,"[账号]自动登录成功",info_pos,color="green",time=3,font=cn_sm,spacing=3,back_color=None)
            self.auto_login=False
        angle=0
        while True:
            events=self.event_handle()
            button.update(events)
            short_info.update()
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_u:
                        self.user.start()
                        self.main_menu()
                        return
                    if ev.key==pg.K_s:
                        text_img=(cn_def.render(slogans[rd.randint(0,len(slogans)-1)],True,"yellow"))
                    if ev.key==pg.K_l:
                        self.changelog.menu()
                    if ev.key==pg.K_RETURN:
                        self.rules()
                        self.restart()
                        return
                for b in button:
                    if b.text=="开始游戏" and b.check_click():
                        self.rules()
                        self.restart()
                        return
                    if b.text=="复制github仓库链接" and b.check_click():
                        pc.copy("https://github.com/Liu-zhang-lang/Crazy-Jump")
                        short_info=Info.append_info(short_info,"链接复制成功",info_pos,color="green",font=cn_sm,spacing=3,back_color=None)
                    if b.text=="复制chest in the maps链接" and b.check_click():
                        pc.copy("https://github.com/MCPlayer123-Develop/CHESTS-IN-THE-MAPS-Release-Version")
                        short_info=Info.append_info(short_info,"链接复制成功",info_pos,color="green",font=cn_sm,spacing=3,back_color=None)
                    if b.text=="刷新" and b.check_click():
                        text_img=(cn_def.render(slogans[rd.randint(0,len(slogans)-1)],True,"yellow"))
            angle+=0.1
            mul=1.0+math.sin(angle)*0.05
            self.draw()
            window.blit(gray_img,(0,0))
            info.draw(window)
            short_info.draw(window)
            button.draw(window)
            img1=pg.transform.smoothscale(text_img,(int(text_img.get_width()*mul),int(text_img.get_height()*mul)))
            img2=pg.transform.rotate(img1,12)
            window.blit(img2,img2.get_rect(center=(515,85)))
            pg.display.update()
            clock.tick(60)
    def check_chinese(self):
        user32=cyp.WinDLL('user32',use_last_error=True)
        hwnd=user32.GetForegroundWindow()
        thread_id=user32.GetWindowThreadProcessId(hwnd,None)
        hkl=user32.GetKeyboardLayout(thread_id)
        lang_id=hkl&0xFFFF
        return lang_id==0x0804 #0x0804=中文(中国)
    def add_achiev_info(self):
        achievs=self.achiev.check_all()
        for key,dct in achievs.items():
            name=dct["name"]
            desc=dct["desc"]
            color=self.achiev.get_color(dct["difficulty"])
            self.achiev_info=Info.append_info(self.achiev_info,f"获得成就[{name}]:{desc}",[0,cn_def_sz*2],font=cn_sm,color=color,time=4,max_len=10,back_color=None)
            self.user.achievs[key]=True
        self.user.update_data()
    def handle_key(self,events):
        keys=pg.key.get_pressed()
        quit=False
        for ev in events:
            if ev.type==pg.KEYDOWN:
                if ev.key==pg.K_r:
                    if self.user.settings["safe_restart"]:
                        text1=cn_def.render("按R确认重新开始",True,"yellow")
                        text2=cn_def.render("按其它按键取消",True,"yellow")
                        window.blit(gray_img,(0,0))
                        window.blit(text1,text1.get_rect(center=(w/2,h/2-17)))
                        window.blit(text2,text2.get_rect(center=(w/2,h/2+17)))
                        pg.display.update()
                        running=True
                        while running:
                            events=self.event_handle()
                            for ev in events:
                                if ev.type==pg.KEYDOWN:
                                    if ev.key==pg.K_r:
                                        self.restart()
                                        running=False
                                        quit=True
                                        break
                                    else:
                                        running=False
                                        break
                    else:
                        self.restart()
                        quit=True
                    break
                if ev.key==pg.K_g:
                    self.draw()
                    self.rules()
                    break
                if ev.key==pg.K_p:
                    self.leaderboard.menu()
                    break
                if ev.key==pg.K_u:
                    self.user.start()
                    if self.time==0:
                        self.main_menu()
                        quit=True
                    break
                if ev.key==pg.K_s:
                    self.settings.start()
                    break
                if ev.key==pg.K_a:
                    self.achiev.show_achiev()
                    break
                if ev.key==pg.K_t:
                    self.game_stats.menu()
                    break
                if ev.key==pg.K_c:
                    self.compend.menu()
                    break
                if ev.key==pg.K_l:
                    self.changelog.menu()
                    break
                if ev.key==pg.K_F1:
                    self.is_f1=not self.is_f1
        if keys[pg.K_m] and (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
            self.main_menu()
            quit=True
        return quit
    def game_start(self):
        pg.display.set_caption(f"疯狂跳跳跳 {version}")
        self.draw()
        self.user.start()
        self.main_menu()
        pg.display.update()
    def game_stop(self):
        waiting=True
        button=pg.sprite.Group()
        if self.mode=="boss" and self.spawn_boss==False:
            button.add(Button([w/2,200],150,30,"#CB5510",align="center",text="提前生成boss",font=cn_sm))
        while waiting:
            events=self.event_handle()
            self.draw()
            button.draw(window)
            gamestop_info.draw(window)
            button.update(events)
            for ev in events:
                if ev.type==pg.QUIT:
                    quit_game()
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_ESCAPE or ev.key==pg.K_RETURN:
                        waiting=False
                if self.developer_mode:
                    if ev.type==pg.MOUSEBUTTONDOWN:
                        self.achiev_info=Info.append_info(self.achiev_info,f"[开发者模式]位置：{ev.pos}",[0,cn_def_sz*2],font=cn_sm,color="yellow",time=3,max_len=10,back_color=None)   
            for bt in button:
                if bt.check_click():
                    self.spawn_boss=True
                    self.boss.add(Boss(self))
                    bt.kill()
            keys=pg.key.get_pressed()
            if (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]) and keys[pg.K_d]:
                self.start_debug()
            quit=self.handle_key(events)
            if quit:
                return
            pg.display.update()
            clock.tick(60)
    def game_over(self):
        go_info=pg.sprite.Group()
        fst_pos=[w/2,h/2-65]
        if self.mode=="boss" and self.spawn_boss==True and len(self.boss)==0:
            go_info=Info.append_info(go_info,f"你赢了！",fst_pos,"center",time=-1,font=cn_big,spacing=5,mode="back")
        else:
            go_info=Info.append_info(go_info,f"你死了！",fst_pos,"center",time=-1,font=cn_big,spacing=5,mode="back")
        if self.user.best[self.mode]["time"]==0 or self.user.best[self.mode]["time"]==inf:
            go_info=Info.append_info(go_info,f"最佳记录：暂无",fst_pos,"center",time=-1,spacing=5,mode="back")
            self.user.update_score()
        elif ((self.mode=="normal" and self.time>self.user.best[self.mode]["time"]) or (self.mode=="boss" and self.time<self.user.best[self.mode]["time"] and self.spawn_boss==True and len(self.boss)==0)) and not self.is_debug:
            go_info=Info.append_info(go_info,f"新记录！",fst_pos,"center",color="green",time=-1,spacing=5,mode="back")
            if self.user.best[self.mode]["minutes"]>0:
                go_info=Info.append_info(go_info,f"前最佳记录：{self.user.best[self.mode]["minutes"]}分{self.user.best[self.mode]["seconds"]:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
            else:
                go_info=Info.append_info(go_info,f"前最佳记录：{self.user.best[self.mode]["time"]:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
            self.user.update_score()
        else:
            if self.user.best[self.mode]["minutes"]>0:
                go_info=Info.append_info(go_info,f"最佳记录：{self.user.best[self.mode]["minutes"]}分{self.user.best[self.mode]["seconds"]:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
            else:
                go_info=Info.append_info(go_info,f"最佳记录：{self.user.best[self.mode]["time"]:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
        if self.minutes>0:
            if self.mode=="boss" and self.spawn_boss==True and len(self.boss)==0:
                go_info=Info.append_info(go_info,f"你使用了{self.minutes}分{self.seconds:.2f}秒击杀boss",fst_pos,"center",time=-1,spacing=5,mode="back")
            else:
                go_info=Info.append_info(go_info,f"你存活了{self.minutes}分{self.seconds:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
        else:
            if self.mode=="boss" and self.spawn_boss==True and len(self.boss)==0:
                go_info=Info.append_info(go_info,f"你使用了{self.seconds:.2f}秒击杀boss",fst_pos,"center",time=-1,spacing=5,mode="back")
            else:
                go_info=Info.append_info(go_info,f"你存活了{self.seconds:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
        go_info=Info.append_info(go_info,f"按Enter重新开始",fst_pos,"center",time=-1,spacing=5,mode="back")
        go_info=Info.append_info(go_info,f"按P查看排行榜",fst_pos,"center",time=-1,spacing=5,mode="back")
        go_info=Info.append_info(go_info,f"按Ctrl+M返回主页",fst_pos,"center",time=-1,spacing=5,mode="back")
        if self.is_debug:
            go_info=Info.append_info(go_info,f"（使用了debug调试，成绩不作数）",fst_pos,align="center",font=cn_sm,color="yellow",time=-1,spacing=5,mode="back")
        running=True
        while running:
            events=self.event_handle()
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_RETURN:
                        running=False
                        break
            quit=self.handle_key(events)
            if quit:
                return
            self.draw()
            go_info.draw(window)
            pg.display.update()
            clock.tick(60)
    def event_handle(self):
        events=pg.event.get()
        for ev in events:
            if ev.type==pg.QUIT:
                quit_game()
        return events
    def run(self):
        self.game_start()
        while True:
            if self.is_play:
                self.restart()
            else:
                self.is_play=True
            while True:
                events=self.event_handle()
                if self.heart<=0 or (self.mode=="boss" and len(self.boss)==0 and self.spawn_boss==True):
                    self.game_over()
                    break
                self.update(events)
                self.draw()
                pg.display.update()
                clock.tick(60)