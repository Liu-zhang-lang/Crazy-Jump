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
        self.enemy=pg.sprite.Group()
        self.health=pg.sprite.Group()
        self.player=pg.sprite.Group()
        self.info=pg.sprite.Group()
        self.floor=pg.sprite.Group()
        self.rain=pg.sprite.Group()
        self.player.add(Player())
        self.floor.add(Floor(0,500,w,-1))
    def start_debug(self):
        self.is_debug=True
        debug=Debug(self)
        debug.start()
    def draw(self):
        window.fill("black")
        self.enemy.draw(window)
        self.health.draw(window)
        self.player.draw(window)
        self.info.draw(window)
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
        info=Info.append_info(info,"使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"按下Esc暂停游戏，按下Esc或Enter继续",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"躲避红色/紫色(加强)敌人和天空中的雨水",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"拾取绿色/黄色(加强)血包",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"输入法为中文时，可能会导致部分按键失效",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"按两次跳跃可以二段跳",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"地图中会随机生成地板，可供站立3秒",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"在暂停模式下，按下G查看规则，按R重开，按P查看排行榜，按U",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"进入账号界面，按Ctrl+M返回主页（不保存进度），按S进入设",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"置，按Ctrl+D打开debug模式（但成绩将不记录）",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"在游戏结束后，按下G查看规则",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"若在终端发现[error...]的输出、编译错误、游戏崩溃或游戏",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"bug，请报告给作者",[50,60],spacing=5,mode="back")
        info=Info.append_info(info,"阅读完毕后，按下Enter键退出规则页面",[50,60],spacing=5,mode="back")
        info.draw(window)
        pg.display.update()
        running=True
        while running:
            events=self.eventHandle()
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_RETURN:
                        running=False
                        break
            clock.tick(60)
    def leaderboard(self):
        ldb=pg.sprite.Group()
        ldb=Info.append_info(ldb,f"排行榜",[50,50],time=-1,spacing=5,mode="back")
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
            ldb=Info.append_info(ldb,f"{index}. {name}:{st}",[50,50],color=color,time=-1,spacing=5,mode="back")
        ldb=Info.append_info(ldb,f"按Enter退出排行榜",[50,50],time=-1,spacing=5,mode="back")
        ldb.draw(window)
        pg.display.update()
        running=True
        while running:
            events=self.eventHandle()
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
            events=self.eventHandle()
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
    def check_chinese(self):
        user32=cyp.WinDLL('user32',use_last_error=True)
        hwnd=user32.GetForegroundWindow()
        thread_id=user32.GetWindowThreadProcessId(hwnd,None)
        hkl=user32.GetKeyboardLayout(thread_id)
        lang_id=hkl&0xFFFF
        return lang_id==0x0804 #0x0804=中文(中国)
    def gameStart(self):
        pg.display.set_caption(f"疯狂跳跳跳 {version}")
        self.draw()
        self.user.start()
        self.main_menu()
        self.draw()
        self.rules()
        pg.display.update()
    def gameStop(self):
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
            keys=pg.key.get_pressed()
            if (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]) and keys[pg.K_d]:
                self.start_debug()
            if keys[pg.K_r]:
                self.is_restart=1
                break
            if keys[pg.K_g]:
                self.draw()
                self.rules()
                self.draw()
                gamestop_info.draw(window)
                pg.display.update()
            if keys[pg.K_p]:
                self.draw()
                self.leaderboard()
                self.draw()
                gamestop_info.draw(window)
                pg.display.update()
            if keys[pg.K_u]:
                self.user.start()
                self.draw()
                if self.time==0:
                    self.rules()
                    break
                gamestop_info.draw(window)
                pg.display.update()
            if keys[pg.K_m] and (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
                self.reset()
                self.main_menu()
                waiting=False
            if keys[pg.K_s]:
                self.settings.start()
                self.draw()
                gamestop_info.draw(window)
                pg.display.update()
            clock.tick(60)
    def gameOver(self):
        go_info=pg.sprite.Group()
        fst_pos=[w/2,h/2-65]
        go_info=Info.append_info(go_info,f"你死了！",fst_pos,"center",time=-1,font=cn_big,spacing=5,mode="back")
        if self.time>self.user.best_time and not self.is_debug:
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
            go_info=Info.append_info(go_info,f"（使用了debug调试，成绩不作数）",fst_pos,"center",cn_sm,"yellow","black",-1,5,"back")
        go_info.draw(window)
        pg.display.update()
        self.user.update_data()
        running=True
        while running:
            events=self.eventHandle()
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_RETURN:
                        running=False
                        break
            keys=pg.key.get_pressed()
            if keys[pg.K_p]:
                self.draw()
                self.leaderboard()
                self.draw()
                go_info.draw(window)
                pg.display.update()
            if keys[pg.K_m] and (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
                self.reset()
                self.main_menu()
                return
            clock.tick(60)
    def eventHandle(self):
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
                e.is_touch=True
        co=pg.sprite.groupcollide(self.rain,self.floor,True,False,pg.sprite.collide_mask)#雨和地面碰撞检测（精确）
        co=pg.sprite.groupcollide(self.player,self.health,False,True)
        for p,e_l in co.items():#血包碰撞检测
            for e in e_l:
                if e.b==40:
                    self.heart+=25
                    self.info=Info.append_info(self.info,f"生命值+25",info_st_pos,"topright",color="green",time=2,max_len=10)
                else:
                    self.heart+=int(e.h)
                    self.info=Info.append_info(self.info,f"生命值+{int(e.h)}",info_st_pos,"topright",color="green",time=2,max_len=10)
        if self.god_mode==False:
            co=pg.sprite.groupcollide(self.player,self.enemy,False,True)
            for p,e_l in co.items():#敌人碰撞检测
                for e in e_l:
                    if abs(e.speed)==12:
                        self.heart-=int(e.b//1.8)
                        self.info=Info.append_info(self.info,f"生命值-{int(e.b//1.8)}",info_st_pos,"topright",color="red",time=2,max_len=10)
                    else:
                        self.heart-=int(e.b//3)
                        self.info=Info.append_info(self.info,f"生命值-{int(e.b//3)}",info_st_pos,"topright",color="red",time=2,max_len=10)
            co=pg.sprite.groupcollide(self.player,self.rain,False,True,pg.sprite.collide_mask) #pg.sprite.collide_mask是精确检测
            for p,e_l in co.items():#雨碰撞检测
                for e in e_l:
                    self.heart-=int(e.len//6.5)
                    self.info=Info.append_info(self.info,f"生命值-{int(e.len//6.5)}",info_st_pos,"topright",color="red",time=2,max_len=10)
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
        self.fps=clock.get_fps()
        self.seconds+=1/60
        self.time+=1/60
        if self.seconds>=60:
            self.seconds-=60
            self.minutes+=1
        if self.heart<0:
            self.heart=0
        self.enemy.update()
        self.rain.update()
        self.floor.update()
        self.player.update()
        self.check_collisions()
        self.info.update()
    def run(self):
        self.gameStart()
        while True:
            self.reset()
            while True:
                for ev in pg.event.get():
                    if ev.type==pg.QUIT:
                        pg.quit()
                        sys.exit(0)
                    if ev.type==pg.KEYDOWN:
                        if ev.key==pg.K_ESCAPE:
                            self.gameStop()
                self.update()
                self.draw()
                pg.display.update()
                if self.heart<=0 or self.is_restart==1:
                    if self.is_restart==0:
                        self.gameOver()
                    break
                clock.tick(60)