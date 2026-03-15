from daoRuKu import DaoRuKu
#################################检查库#################################
needPackages={
    "pygame":"pg",
}
DaoRuKu(needPackages)
input("按下enter键开始游玩")
print("游戏开始，请进入弹出的窗口")
#################################初始化#################################
from const import *
from enemy import Enemy
from health import Health
from player import Player
from information import Information
from floor import Floor
from rain import Rain
from draw import Draw
from gameStop import GameStop
from gameOver import GameOver
from drawText import DrawText
from rules import Rules
import pygame as pg
import random as rd
import sys
pg.init()
fps=0
is_restart=0
pro=0.005
hpro=0.0015
fpro=0.0001
rpro=0
seconds=0
heart=30
debug=False
god_mode=False
g=pg.sprite.Group()
he=pg.sprite.Group()
player=pg.sprite.Group()
inf=pg.sprite.Group()
floor=pg.sprite.Group()
rain=pg.sprite.Group()
g.add(Enemy(1))
player.add(Player())
floor.add(Floor(0,500,w))
pg.display.set_caption("疯狂跳跳跳")
#################################主程序#################################
Draw(g,he,player,inf,seconds,floor,rain,heart,fps)
Rules()
while True:#等待开始
    for ev in pg.event.get():
        if ev.type==pg.QUIT:
            pg.quit()
            sys.exit(0)
    keys=pg.key.get_pressed()
    if keys[pg.K_RETURN]:
        break
    clock.tick(60)
while True:#每次开始重置
    fps=0
    is_restart=0
    heart=30
    seconds=0
    pro=0.004
    hpro=0.0015
    fpro=0.0001
    rpro=0
    debug=False
    g=pg.sprite.Group()
    he=pg.sprite.Group()
    player=pg.sprite.Group()
    inf=pg.sprite.Group()
    floor=pg.sprite.Group()
    rain=pg.sprite.Group()
    player.add(Player())
    g.add(Enemy(1))
    floor.add(Floor(0,500,w))
    while True:#游戏主循环
        for ev in pg.event.get():
            if ev.type==pg.QUIT:
                pg.quit()
                sys.exit(0)
            if ev.type==pg.KEYDOWN:
                if ev.key==pg.K_ESCAPE:
                    debug,god_mode,g,he,player,is_restart=GameStop(g,he,player,inf,seconds,floor,rain,heart,debug,god_mode,fps)
        g.update()
        player.update()
        inf.update()
        floor.update()
        rain.update()
        fps=clock.get_fps()
        co=pg.sprite.groupcollide(player,he,False,True)
        for p,e_l in co.items():#血包碰撞检测
            for e in e_l:
                if e.b==40:
                    heart+=25
                    inf=Information.add_inf(inf,f"生命值+25","green")
                else:
                    heart+=int(e.b//3)
                    inf=Information.add_inf(inf,f"生命值+{int(e.b//3)}","green")
        co=pg.sprite.groupcollide(player,floor,False,False)
        for p,e_l in co.items():#地面碰撞检测
            for e in e_l:
                p.touch_floor(e)
                e.is_touch=True
        if god_mode==False:
            co=pg.sprite.groupcollide(player,g,False,True)
            for p,e_l in co.items():#敌人碰撞检测
                for e in e_l:
                    if abs(e.speed)==12:
                        heart-=int(e.b//1.8)
                        inf=Information.add_inf(inf,f"生命值-{int(e.b//1.8)}","red")
                    else:
                        heart-=int(e.b//3)
                        inf=Information.add_inf(inf,f"生命值-{int(e.b//3)}","red")
            co=pg.sprite.groupcollide(player,rain,False,True,pg.sprite.collide_mask) #pg.sprite.collide_mask是精确检测
            for p,e_l in co.items():#雨碰撞检测
                for e in e_l:
                    heart-=5
                    inf=Information.add_inf(inf,"生命值-5","red")
        seconds+=1/fps
        for i in range(len(level_up_time)):#难度增加
            if level_up_time[i][0]<=seconds<=level_up_time[i][1]:
                pro=all_pro[i]
                hpro=all_hpro[i]
                fpro=all_fpro[i]
                rpro=all_rpro[i]
                break
        if rd.random()<=pro:#生成敌人
            g.add(Enemy(0))
        if rd.random()<=hpro:#生成血包
            he.add(Health(0))
        if rd.random()<=fpro:#生成地面
            floor.add(Floor(-1,-1,-1))
        if rd.random()<=rpro:#生成雨
            rain.add(Rain(-1))
        if heart<0:
            heart=0
        Draw(g,he,player,inf,seconds,floor,rain,heart,fps)
        pg.display.update()
        if heart==0 or is_restart==1:
            if is_restart==0:
                GameOver(seconds,debug)
            break
        clock.tick(60)