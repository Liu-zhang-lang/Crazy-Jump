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
from draw import Draw
from gameStop import GameStop
from gameOver import GameOver
from drawText import DrawText
import pygame as pg
import random as rd
pg.init()
is_restart=0
pro=0.005
hpro=0.0015
seconds=0
heart=30
debug=False
god_mode=False
g=pg.sprite.Group()
he=pg.sprite.Group()
player=pg.sprite.Group()
inf=pg.sprite.Group()
g.add(Enemy(1))
player.add(Player())
pg.display.set_caption("跳一跳 v1.0.3 beta2")
#################################主程序#################################
Draw(g,he,player,inf,seconds,heart)
texts={
    "游戏规则&玩法：":[(50,50),chinese_font,"white"],
    "1：使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃":[(50,90),chinese_font,"white"],
    "2：按下ESC暂停游戏，再次按下ESC继续":[(50,130),chinese_font,"white"],
    "3：躲避红色/紫色(加强)敌人，拾取绿色/黄色(加强)血包，看看":[(50,170),chinese_font,"white"],
    "你能坚持多久":[(50,210),chinese_font,"white"],
    "4：输入法为中文时，可能会导致部分按键失效":[(50,250),chinese_font,"white"],
    "阅读完毕后，按下回车键开始游戏":[(50,290),chinese_font,"white"]
}
DrawText(texts)
pg.display.update()
while True:#等待开始
    for ev in pg.event.get():
        if ev.type==pg.QUIT:
            pg.quit()
            exit()
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
    debug=False
    g=pg.sprite.Group()
    he=pg.sprite.Group()
    player=pg.sprite.Group()
    inf=pg.sprite.Group()
    player.add(Player())
    g.add(Enemy(1))
    while True:#游戏主循环
        for ev in pg.event.get():
            if ev.type==pg.QUIT:
                pg.quit()
                exit()
            if ev.type==pg.KEYDOWN:
                if ev.key==pg.K_ESCAPE:
                    debug,god_mode,g,he,player,is_restart=GameStop(debug,god_mode,g,he,player)
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
        seconds+=1/60
        for i in range(len(level_up_time)):#难度增加
            if level_up_time[i][0]<=seconds<=level_up_time[i][1]:
                pro=all_pro[i]
                hpro=all_hpro[i]
        if rd.random()<=pro:#增加敌人
            g.add(Enemy(0))
        if rd.random()<=hpro:#增加血包
            he.add(Health(0))
        if heart<0:
            heart=0
        g.update()
        player.update()
        inf.update()
        Draw(g,he,player,inf,seconds,heart)
        pg.display.update()
        if heart==0 or is_restart==1:
            if is_restart==0:
                GameOver(seconds,debug)
            break
        clock.tick(60)