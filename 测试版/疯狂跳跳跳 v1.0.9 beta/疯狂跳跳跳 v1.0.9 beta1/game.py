from const import *
from enemy import Enemy
from health import Health
from player import Player
from info import Info
from debug import Debug
from floor import Floor
from rain import Rain
from inputBox import InputBox
from button import Button
from user import User
from settings import Settings
from achiev import Achiev
import pygame as pg
import random as rd
import sys
import ctypes as cyp
import pyperclip as pc
import math
class Game:
    def __init__(self):
        self.user=User(self)
        self.settings=Settings(self)
        self.achiev=Achiev(self)
        self.auto_login=False
        self.chinese_warning=False
        self.reset()
    def reset(self):
        self.fps=0
        self.heart=30
        self.time=0 #真实秒数
        self.seconds=0
        self.minutes=0
        self.level=1
        self.pro=0.004
        self.hpro=0.0015
        self.fpro=0.0001
        self.rpro=0
        self.is_restart=False
        self.is_debug=False
        self.god_mode=False
        self.is_update_level=False
        self.game_stats={
            "jump":{"name":"跳跃次数","cnt":0},
            "touch_nor_enemy":{"name":"触碰普通敌人次数","cnt":0},
            "touch_super_enemy":{"name":"触碰超级敌人次数","cnt":0},
            "touch_nor_health":{"name":"触碰普通血包次数","cnt":0},
            "touch_super_health":{"name":"触碰超级血包次数","cnt":0},
            "touch_floor":{"name":"触碰地板次数","cnt":-1},
            "touch_rain":{"name":"触碰雨次数","cnt":0},
            "debug":{"name":"使用调试次数","cnt":0}
        }
        self.enemy=pg.sprite.Group()
        self.health=pg.sprite.Group()
        self.player=pg.sprite.Group()
        self.info=pg.sprite.Group()
        self.floor=pg.sprite.Group()
        self.rain=pg.sprite.Group()
        self.achiev_info=pg.sprite.Group()
        self.player.add(Player())
        self.floor.add(Floor(0,500,w,-1))
    def start_debug(self):
        debug=Debug(self)
        debug.start()
    def draw(self):
        window.fill("black")
        self.enemy.draw(window)
        self.health.draw(window)
        self.player.draw(window)
        self.info.draw(window)
        self.achiev_info.draw(window)
        self.floor.draw(window)
        self.rain.draw(window)
        if self.level-1<len(level_up_time):
            time_remain=level_up_time[self.level-1][0]-self.time
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
        info=Info.append_info(info,f"时间:{time}",[0,0])
        info=Info.append_info(info,f"FPS:{self.fps:.2f}",[0,cn_def_sz])
        info=Info.append_info(info,f"生命值:{self.heart}",[w,0],"topright")
        info=Info.append_info(info,f"阶段:{self.level}",[w,cn_def_sz],"topright")
        info=Info.append_info(info,f"下一阶段:{next_level_time}",[w,cn_def_sz*2],"topright")
        info.draw(window)
        for a in level_up_time:
            if a[0]<=self.time<=a[1]:
                text=cn_big.render("难度升级!",True,"white")
                window.blit(text,text.get_rect(center=(w/2,h/2-200)))
    def rules(self):
        info=pg.sprite.Group()
        info=Info.append_info(info,"使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"按下Esc暂停游戏，按下Esc或Enter继续",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"躲避红色/紫色(加强)敌人和天空中的雨水",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"拾取绿色/黄色(加强)血包",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"输入法为中文时，可能会导致部分按键失效",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"按两次跳跃可以二段跳",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"地图中会随机生成地板，可供站立3秒",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"进入游戏结束/暂停界面，按Ctrl+M返回主页（不保存进度），按S",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"进入设置，按A进入成就系统，按U进入账号系统，按P进入排行榜，",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"按R重新开始，按G查看规则（当前页面），按S查看统计信息",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"暂停界面下，按Ctrl+D打开debug模式（但成绩与成就将不记录）",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"若在终端发现[error...]的输出、编译错误、游戏崩溃或游戏",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"bug，请报告给作者",[50,60],back_color=None,spacing=5,mode="back")
        info=Info.append_info(info,"阅读完毕后，按下Enter键退出规则页面",[50,60],back_color=None,spacing=5,mode="back")
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
    def leaderboard(self):
        ldb=pg.sprite.Group()
        ldb=Info.append_info(ldb,f"排行榜",[50,50],time=-1,back_color=None,spacing=5,mode="back")
        users={}
        for name in self.user.users_data:
            u=self.user.users_data[name]
            users[name]={
                "best_time":u["best_time"],
                "best_minutes":u["best_minutes"],
                "best_seconds":u["best_seconds"],
                "best_version":u["best_version"]
            }
        users=sorted(users.items(),key=lambda x:x[1]["best_time"],reverse=True)
        index=0
        for u in users:
            index+=1
            name=u[0]
            u=u[1]
            if index==1:
                color="gold"
            elif index==2:
                color=(160,160,160)
            elif index==3:
                color=(205,127,50)
            else:
                color="white"
            if u["best_minutes"]>0:
                st=f"{u['best_minutes']}分{u['best_seconds']:.2f}秒（{u['best_version']}）"
            else:
                st=f"{u['best_seconds']:.2f}秒（{u['best_version']}）"
            ldb=Info.append_info(ldb,f"{index}. {name}:{st}",[50,50],color=color,back_color=None,time=-1,spacing=5,mode="back")
        ldb=Info.append_info(ldb,f"按Enter退出排行榜",[50,50],time=-1,back_color=None,spacing=5,mode="back")
        window.blit(gray_img,(0,0))
        ldb.draw(window)
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
        info_pos=[530,110]
        info=pg.sprite.Group()
        short_info=pg.sprite.Group()
        button=pg.sprite.Group()
        info=Info.add_info(info,"疯狂跳跳跳",[w/2,70],align="center",font=cn_big,back_color=None)
        info=Info.append_info(info,f"欢迎回来，{self.user.user_name}",[50,110],spacing=5,back_color=None,mode="back")
        info=Info.append_info(info,"按U进入账号界面",[50,110],spacing=5,back_color=None,mode="back")
        info=Info.add_info(info,"作者：Liu_zhang_lang",[750,520],font=cn_sm,align="topright",back_color=None)
        info=Info.add_info(info,f"版本号：{version}",[50,550],back_color=None)
        button.add(Button((50,180),250,50,"blue",text="开始游戏"))
        button.add(Button((750,550),200,30,"blue",align="topright",text="复制github仓库链接",font=cn_sm))
        button.add(Button((770,50),50,30,"blue",align="topright",text="刷新"))
        text_img=(cn_def.render(slogans[rd.randint(0,len(slogans)-1)],True,"yellow"))
        if self.check_chinese() and not self.chinese_warning:
            short_info=Info.append_info(short_info,"[警告]当前输入法为中文，",info_pos,color="orange",time=3,font=cn_sm,spacing=5,back_color=None)
            short_info=Info.append_info(short_info,"可能会使字母按键失效",info_pos,color="orange",time=3,font=cn_sm,spacing=5,back_color=None,mode="back")
            self.chinese_warning=True
        if self.auto_login:
            short_info=Info.append_info(short_info,"[账号]自动登录成功",info_pos,color="green",time=3,font=cn_sm,spacing=5,back_color=None)
            self.auto_login=False
        angle=0
        while True:
            events=self.event_handle()
            button.update(events)
            short_info.update()
            for ev in events:
                if ev.type==pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_u:
                        self.user.start()
                        short_info.empty()
                    if ev.key==pg.K_s:
                        self.main_menu()
                        return
                    if ev.key==pg.K_RETURN:
                        return
                for b in button:
                    if b.text=="开始游戏" and b.check_click():
                        return
                    if b.text=="复制github仓库链接" and b.check_click():
                        pc.copy("https://github.com/Liu-zhang-lang/Crazy-Jump")
                        short_info=Info.append_info(short_info,"链接复制成功",info_pos,color="green",font=cn_sm,spacing=5,back_color=None)
                    if b.text=="刷新" and b.check_click():
                        self.main_menu()
                        return
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
    def game_stats_menu(self):
        button=pg.sprite.Group()
        button.add(Button((w-30,30),30,30,"blue",align="topright",text="×"))
        button.add(Button((50,550),30,30,"blue",align="topleft",text="<-"))
        button.add(Button((w-50,550),30,30,"blue",align="topright",text="->"))
        fst_pos=[50,80]
        maxline=13
        maxpage=int((len(self.game_stats)+maxline-1)/maxline)
        line=0
        index=0
        stats_info=[pg.sprite.Group() for _ in range(maxpage+5)]
        stats_info[0]=Info.add_info(stats_info[0],"统计信息",[w/2,50],align="center",font=cn_big,back_color=None)
        for dct in self.game_stats.values():
            line+=1
            if line>maxline:
                index+=1
                line=1
                stats_info[index]=Info.add_info(stats_info[index],"统计信息",[w/2,50],align="center",font=cn_big,back_color=None)
            stats_info[index]=Info.append_info(stats_info[index],f"{dct['name']}：{dct['cnt']}",fst_pos,spacing=5,back_color=None)
        while True:
            events=self.event_handle()
            button.update(events)
            self.draw()
            window.blit(gray_img,(0,0))
            stats_info[index].draw(window)
            button.draw(window)
            img=cn_def.render(f"第{index+1}/{maxpage}页",True,"white")
            window.blit(img,img.get_rect(center=(w/2,565)))
            for bt in button:
                if bt.check_click():
                    if bt.text=="<-":
                        if index>0:
                            index-=1
                    elif bt.text=="->":
                        if index<maxpage-1:
                            index+=1
                    elif bt.text=="×":
                        return
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
            self.achiev_info=Info.append_info(self.achiev_info,f"获得成就[{name}]:{desc}",[0,cn_def_sz*2],font=cn_sm,color="green",time=4,spacing=5,max_len=10)
            self.user.achievs[key]=True
        self.user.update_data()
    def handle_key(self):
        keys=pg.key.get_pressed()
        flag=False
        if keys[pg.K_r]:
            self.is_restart=1
            flag=True
        if keys[pg.K_g]:
            self.draw()
            self.rules()
            flag=True
        if keys[pg.K_p]:
            self.draw()
            self.leaderboard()
            flag=True
        if keys[pg.K_u]:
            self.user.start()
            flag=True
        if keys[pg.K_m] and (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
            self.reset()
            self.main_menu()
            flag=True
        if keys[pg.K_s]:
            self.settings.start()
            flag=True
        if keys[pg.K_a]:
            self.achiev.show_achiev()
            flag=True
        if keys[pg.K_t]:
            self.game_stats_menu()
            flag=True
        return flag
    def game_start(self):
        pg.display.set_caption(f"疯狂跳跳跳 {version}")
        self.draw()
        self.user.start()
        self.main_menu()
        self.draw()
        self.rules()
        pg.display.update()
    def game_stop(self):
        waiting=True
        gamestop_info.draw(window)
        pg.display.update()
        while waiting:
            for ev in pg.event.get():
                if ev.type==pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_ESCAPE or ev.key==pg.K_RETURN:
                        waiting=False
            user_name=self.user.user_name
            keys=pg.key.get_pressed()
            if (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]) and keys[pg.K_d]:
                self.start_debug()
            self.handle_key()
            if self.time==0 and user_name!=self.user.user_name:
                self.main_menu()
                return
            self.draw()
            gamestop_info.draw(window)
            pg.display.update()
            clock.tick(60)
    def game_over(self):
        go_info=pg.sprite.Group()
        fst_pos=[w/2,h/2-65]
        go_info=Info.append_info(go_info,f"你死了！",fst_pos,"center",time=-1,font=cn_big,spacing=5,mode="back")
        if self.user.best_time==0:
            go_info=Info.append_info(go_info,f"最佳记录：暂无",fst_pos,"center",time=-1,spacing=5,mode="back")
        elif self.time>self.user.best_time and not self.is_debug:
            go_info=Info.append_info(go_info,f"新记录！",fst_pos,"center",color="green",time=-1,spacing=5,mode="back")
            if self.user.best_minutes>0:
                go_info=Info.append_info(go_info,f"前最佳记录：{self.user.best_minutes}分{self.user.best_seconds:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
            else:
                go_info=Info.append_info(go_info,f"前最佳记录：{self.user.best_time:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
        else:
            if self.user.best_minutes>0:
                go_info=Info.append_info(go_info,f"最佳记录：{self.user.best_minutes}分{self.user.best_seconds:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
            else:
                go_info=Info.append_info(go_info,f"最佳记录：{self.user.best_time:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
        if self.minutes>0:
            go_info=Info.append_info(go_info,f"你存活了{self.minutes}分{self.seconds:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
        else:
            go_info=Info.append_info(go_info,f"你存活了{self.seconds:.2f}秒",fst_pos,"center",time=-1,spacing=5,mode="back")
        go_info=Info.append_info(go_info,f"按Enter重新开始",fst_pos,"center",time=-1,spacing=5,mode="back")
        go_info=Info.append_info(go_info,f"按P查看排行榜",fst_pos,"center",time=-1,spacing=5,mode="back")
        go_info=Info.append_info(go_info,f"按Ctrl+M返回主页",fst_pos,"center",time=-1,spacing=5,mode="back")
        if self.is_debug:
            go_info=Info.append_info(go_info,f"（使用了debug调试，成绩不作数）",fst_pos,align="center",font=cn_sm,color="yellow",time=-1,spacing=5,mode="back")
        go_info.draw(window)
        pg.display.update()
        self.user.update_data()
        running=True
        while running:
            events=self.event_handle()
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_RETURN:
                        running=False
                        break
            self.handle_key()
            clock.tick(60)
    def event_handle(self):
        events=pg.event.get()
        for ev in events:
            if ev.type==pg.QUIT:
                pg.quit()
                sys.exit(0)
        return events
    def check_collisions(self):
        co=pg.sprite.groupcollide(self.player,self.floor,False,False)
        for p,e_l in co.items():#地面碰撞检测
            for e in e_l:
                p.touch_floor(e)
                if e.is_touch==False:
                    self.game_stats["touch_floor"]["cnt"]+=1
                e.is_touch=True
        co=pg.sprite.groupcollide(self.rain,self.floor,True,False,pg.sprite.collide_mask)#雨和地面碰撞检测（精确）
        co=pg.sprite.groupcollide(self.player,self.health,False,True)
        for p,e_l in co.items():#血包碰撞检测
            for e in e_l:
                if e.b==40:
                    self.heart+=25
                    self.info=Info.append_info(self.info,f"生命值+25",info_st_pos,"topright",color="green",time=2,max_len=10)
                    self.game_stats["touch_super_health"]["cnt"]+=1
                else:
                    self.heart+=int(e.h)
                    self.info=Info.append_info(self.info,f"生命值+{int(e.h)}",info_st_pos,"topright",color="green",time=2,max_len=10)
                    self.game_stats["touch_nor_health"]["cnt"]+=1
        if self.god_mode==False:
            co=pg.sprite.groupcollide(self.player,self.enemy,False,True)
            for p,e_l in co.items():#敌人碰撞检测
                for e in e_l:
                    if abs(e.speed)==12:
                        self.heart-=int(e.b//1.8)
                        self.info=Info.append_info(self.info,f"生命值-{int(e.b//1.8)}",info_st_pos,"topright",color="red",time=2,max_len=10)
                        self.game_stats["touch_super_enemy"]["cnt"]+=1
                    else:
                        self.heart-=int(e.b//3)
                        self.info=Info.append_info(self.info,f"生命值-{int(e.b//3)}",info_st_pos,"topright",color="red",time=2,max_len=10)
                        self.game_stats["touch_nor_enemy"]["cnt"]+=1
            co=pg.sprite.groupcollide(self.player,self.rain,False,True,pg.sprite.collide_mask) #pg.sprite.collide_mask是精确检测
            for p,e_l in co.items():#雨碰撞检测
                for e in e_l:
                    self.heart-=int(e.len//6.5)
                    self.info=Info.append_info(self.info,f"生命值-{int(e.len//6.5)}",info_st_pos,"topright",color="red",time=2,max_len=10)
                    self.game_stats["touch_rain"]["cnt"]+=1
    def update(self):
        is_level_up_time=False
        for i in range(len(level_up_time)):#难度增加
            if level_up_time[i][0]<=self.time<=level_up_time[i][1]:
                self.pro=all_pro[i]
                self.hpro=all_hpro[i]
                self.fpro=all_fpro[i]
                self.rpro=all_rpro[i]
                if self.is_update_level==False:
                    self.is_update_level=True
                    self.level=i+2
                is_level_up_time=True
                break
        if is_level_up_time==False:
            self.is_update_level=False
        if rd.random()<=self.pro:#生成敌人
            self.enemy.add(Enemy(draw_num=self.user.settings["enemy_show"]))
        if rd.random()<=self.hpro:#生成血包
            self.health.add(Health(draw_num=self.user.settings["health_show"]))
        if rd.random()<=self.fpro:#生成地面
            self.floor.add(Floor())
        if rd.random()<=self.rpro:#生成雨
            self.rain.add(Rain(draw_num=self.user.settings["rain_show"]))
        self.game_stats["jump"]["cnt"]=self.player.sprites()[0].jump_cnt
        self.fps=clock.get_fps()
        self.seconds+=1/60
        self.time+=1/60
        if self.seconds>=60:
            self.seconds-=60
            self.minutes+=1
        self.enemy.update()
        self.rain.update()
        self.floor.update()
        self.player.update()
        self.check_collisions()
        self.add_achiev_info()
        self.info.update()
        self.achiev_info.update()
        if self.heart<0:
            self.heart=0
    def run(self):
        self.game_start()
        while True:
            self.reset()
            while True:
                for ev in pg.event.get():
                    if ev.type==pg.QUIT:
                        pg.quit()
                        sys.exit(0)
                    if ev.type==pg.KEYDOWN:
                        if ev.key==pg.K_ESCAPE:
                            self.game_stop()
                self.update()
                self.draw()
                pg.display.update()
                if self.heart<=0 or self.is_restart==1:
                    if self.is_restart==0:
                        self.game_over()
                    break
                clock.tick(60)