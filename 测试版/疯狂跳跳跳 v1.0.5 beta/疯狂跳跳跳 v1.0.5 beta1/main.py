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
from draw import Draw
from gameStop import GameStop
from gameOver import GameOver
from drawText import DrawText
from rain import Rain
import pygame as pg
import random as rd
import sys
pg.init()
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
Draw(g,he,player,inf,seconds,floor,rain,heart)
texts={
    "游戏规则&玩法：":[(50,50),chinese_font,"white"],
    "1：使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃":[(50,85),chinese_font,"white"],
    "2：按下ESC暂停游戏，再次按下ESC继续":[(50,120),chinese_font,"white"],
    "3：躲避红色/紫色(加强)敌人和天空中的雨水":[(50,155),chinese_font,"white"],
    "4：拾取绿色/黄色(加强)血包":[(50,190),chinese_font,"white"],
    "5：输入法为中文时，可能会导致部分按键失效":[(50,225),chinese_font,"white"],
    "6：按两次跳跃可以二段跳":[(50,260),chinese_font,"white"],
    "7：地图中会随机生成地板，可供站立3秒":[(50,295),chinese_font,"white"],
    "阅读完毕后，按下回车键开始游戏":[(50,330),chinese_font,"white"]
}
DrawText(texts)
pg.display.update()
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
                    debug,god_mode,g,he,player,is_restart=GameStop(debug,god_mode,g,he,player)
        g.update()
        player.update()
        inf.update()
        floor.update()
        rain.update()
        co=pg.sprite.groupcollide(player,he,False,True)
        for p,e_l in co.items():#血包碰撞检测
            for e in e_l:
                if e.b==40:
                    heart+=25
                    inf=Information.add_inf(inf,f"生命值+25","green")
                else:
                    heart+=int(e.b//3)
                    inf=Information.add_inf(inf,f"生命值+{int(e.b//3)}","green")
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
        co=pg.sprite.groupcollide(player,floor,False,False)
        for p,e_l in co.items():#地面碰撞检测
            for e in e_l:
                p.touch_floor(e)
                e.is_touch=True
        co=pg.sprite.groupcollide(player,rain,False,True,pg.sprite.collide_mask) #pg.sprite.collide_mask是精确检测
        for p,e_l in co.items():#雨碰撞检测
            for e in e_l:
                heart-=5
                inf=Information.add_inf(inf,"生命值-5","red")
        seconds+=1/60
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
        Draw(g,he,player,inf,seconds,floor,rain,heart)
        pg.display.update()
        if heart==0 or is_restart==1:
            if is_restart==0:
                GameOver(seconds,debug)
            break
        clock.tick(60)