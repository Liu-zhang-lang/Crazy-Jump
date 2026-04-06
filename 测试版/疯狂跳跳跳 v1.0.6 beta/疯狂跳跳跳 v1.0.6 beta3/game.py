from const import *
from enemy import Enemy
from health import Health
from player import Player
from info import Info
from debug import Debug
from floor import Floor
from rain import Rain
import pygame as pg
import random as rd
import sys
class Game:
    def __init__(self):
        self.reset()
    def reset(self):
        self.fps=0
        self.heart=30
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
        self.debug=Debug(self)
        self.enemy=pg.sprite.Group()
        self.health=pg.sprite.Group()
        self.player=pg.sprite.Group()
        self.info=pg.sprite.Group()
        self.floor=pg.sprite.Group()
        self.rain=pg.sprite.Group()
        self.player.add(Player())
        self.enemy.add(Enemy(1))
        self.floor.add(Floor(0,500,w))
    def drawTexts(self,texts):
        real_pos=list([0,0])
        for text,val_list in texts.items():
            pos=list(val_list[0])
            font=val_list[1]
            color=val_list[2]
            alignment="topleft"
            if len(val_list)>=4 and val_list[3]==2:
                real_pos[0]+=pos[0]
                real_pos[1]+=pos[1]
            else:
                real_pos=pos
            if len(val_list)>=5:
                alignment=val_list[4]
            text=font.render(text,True,color)
            if alignment=="topleft":
                window.blit(text,real_pos)
            elif alignment=="topright":
                window.blit(text,text.get_rect(topright=real_pos))
            elif alignment=="bottomleft":
                window.blit(text,text.get_rect(bottomleft=real_pos))
            elif alignment=="bottomright":
                window.blit(text,text.get_rect(bottomright=real_pos))
            elif alignment=="center":
                window.blit(text,text.get_rect(center=real_pos))
            else:
                print("[error:Game,drawTexts]未知的对齐方式")
    def start_debug(self):
        self.is_debug=True
        self.debug.start()
    def draw(self):
        window.fill("black")
        self.enemy.draw(window)
        self.health.draw(window)
        self.player.draw(window)
        self.info.draw(window)
        self.floor.draw(window)
        self.rain.draw(window)
        text={
            f"生命值:{self.heart}":[(w,0),chinese_font,"white",1,"topright"],
            f"FPS:{self.fps:.2f}":[(0,chinese_font_size),chinese_font,"white"],
            f"阶段:{self.level}":[(w,chinese_font_size),chinese_font,"white",1,"topright"]
        }
        self.drawTexts(text)
        if self.minutes>0:
            texts={
                f"时间:{self.minutes}分{self.seconds:.2f}秒":[(0,0),chinese_font,"white"]
            }
        else:
            texts={
                f"时间:{self.seconds:.2f}秒":[(0,0),chinese_font,"white"]
            }
        self.drawTexts(texts)
        for a in level_up_time:
            if a[0]<=self.minutes*60+self.seconds<=a[1]:
                text=chinese_font_big.render("难度升级!",True,"white")
                window.blit(text,text.get_rect(center=(w/2,h/2-200)))
        pg.display.update()
    def rules(self):
        texts={
            "游戏规则&玩法：":[(50,60),chinese_font,"white"],
            "使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃":[(0,35),chinese_font,"white",2],
            "按下Esc暂停游戏，按下Esc或Enter继续":[(0,35),chinese_font,"white",2],
            "躲避红色/紫色(加强)敌人和天空中的雨水":[(0,35),chinese_font,"white",2],
            "拾取绿色/黄色(加强)血包":[(0,35),chinese_font,"white",2],
            "输入法为中文时，可能会导致部分按键失效":[(0,35),chinese_font,"white",2],
            "按两次跳跃可以二段跳":[(0,35),chinese_font,"white",2],
            "地图中会随机生成地板，可供站立3秒":[(0,35),chinese_font,"white",2],
            "在暂停模式下，按下L查看规则，按R重开":[(0,35),chinese_font,"white",2],
            "若在运行过程中在终端发现[error...]的错误，请报告给作者":[(0,35),chinese_font,"white",2],
            "阅读完毕后，按下Enter键退出规则页面":[(0,35),chinese_font,"white",2]
        }
        self.drawTexts(texts)
        pg.display.update()
        while True:
            self.eventHandle()
            keys=pg.key.get_pressed()
            if keys[pg.K_RETURN]:
                break
            clock.tick(60)
    def gameStart(self):
        pg.display.set_caption("疯狂跳跳跳")
        self.draw()
        self.rules()
        while True:
            self.eventHandle()
            keys=pg.key.get_pressed()
            if keys[pg.K_RETURN]:
                break
            clock.tick(60)
    def gameStop(self):
        waiting=True
        texts={
            "游戏暂停":[(w/2,h/2-55),chinese_font_big,"white",1,"center"],
            "按Esc或Enter继续游戏":[(w/2,h/2),chinese_font,"white",1,"center"],
            "按R重新开始":[(w/2,h/2+35),chinese_font,"white",1,"center"],
            "按L查看规则":[(0,35),chinese_font,"white",2,"center"]
        }
        self.drawTexts(texts)
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
            if keys[pg.K_l]:
                self.draw()
                self.rules()
                self.draw()
                self.drawTexts(texts)
                pg.display.update()
            clock.tick(60)
    def gameOver(self):
        texts={
            "你死了！":[(w/2,h/2-55),chinese_font_big,"white",1,"center"],
            "按Enter重新开始":[(w/2,h/2+35),chinese_font,"white",1,"center"]
        }
        self.drawTexts(texts)
        if self.minutes>0:
            texts={
                f"你存活了{self.minutes}分{self.seconds:.2f}秒":[(w/2,h/2),chinese_font,"white",1,"center"]
            }
        else:
            texts={
                f"你存活了{self.seconds:.2f}秒":[(w/2,h/2),chinese_font,"white",1,"center"]
            }
        self.drawTexts(texts)
        if self.is_debug:
            text=chinese_font_lit.render("(使用了debug调试)",True,"yellow")
            window.blit(text,text.get_rect(center=(w/2,h/2+65)))
        pg.display.update()
        while True:
            self.eventHandle()
            keys=pg.key.get_pressed()
            if keys[pg.K_RETURN]:
                break
            clock.tick(60)
    def eventHandle(self):
        for ev in pg.event.get():
            if ev.type==pg.QUIT:
                pg.quit()
                sys.exit(0)
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
                    self.info=Info.add_info(self.info,f"生命值+25","green")
                else:
                    self.heart+=int(e.b//3)
                    self.info=Info.add_info(self.info,f"生命值+{int(e.b//3)}","green")
        if self.god_mode==False:
            co=pg.sprite.groupcollide(self.player,self.enemy,False,True)
            for p,e_l in co.items():#敌人碰撞检测
                for e in e_l:
                    if abs(e.speed)==12:
                        self.heart-=int(e.b//1.8)
                        self.info=Info.add_info(self.info,f"生命值-{int(e.b//1.8)}","red")
                    else:
                        self.heart-=int(e.b//3)
                        self.info=Info.add_info(self.info,f"生命值-{int(e.b//3)}","red")
            co=pg.sprite.groupcollide(self.player,self.rain,False,True,pg.sprite.collide_mask) #pg.sprite.collide_mask是精确检测
            for p,e_l in co.items():#雨碰撞检测
                for e in e_l:
                    self.heart-=int(e.len/6.5)
                    self.info=Info.add_info(self.info,f"生命值-{int(e.len/6.5)}","red")
    def update(self):
        self.enemy.update()
        self.health.update()
        self.player.update()
        self.floor.update()
        self.rain.update()
        self.info.update()
        is_level_up_time=False
        for i in range(len(level_up_time)):#难度增加
            if level_up_time[i][0]<=self.minutes*60+self.seconds<=level_up_time[i][1]:
                self.pro=all_pro[i]
                self.hpro=all_hpro[i]
                self.fpro=all_fpro[i]
                self.rpro=all_rpro[i]
                if self.is_update_level==False:
                    self.is_update_level=True
                    self.level+=1
                is_level_up_time=True
                break
        if is_level_up_time==False:
            self.is_update_level=False
        self.check_collisions()
        if rd.random()<=self.pro:#生成敌人
            self.enemy.add(Enemy(0))
        if rd.random()<=self.hpro:#生成血包
            self.health.add(Health(0))
        if rd.random()<=self.fpro:#生成地面
            self.floor.add(Floor(-1,-1,-1))
        if rd.random()<=self.rpro:#生成雨
            self.rain.add(Rain(-1))
        self.fps=clock.get_fps()
        if self.fps>0:
            self.seconds+=1/self.fps
        if self.seconds>=60:
            self.seconds-=60
            self.minutes+=1
        if self.heart<0:
            self.heart=0
        self.draw()
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
                if self.heart<=0 or self.is_restart==1:
                    if self.is_restart==0:
                        self.gameOver()
                    break
                clock.tick(60)