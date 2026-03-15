import pygame as pg
import sys
from const import *
from enemy import Enemy
from health import Health
from draw import Draw
from drawText import DrawText
from floor import Floor
from rain import Rain
from rules import Rules
def GameStop(g,he,player,inf,seconds,floor,rain,heart,debug,god_mode,fps):
    waiting=True
    is_restart=0
    texts={
        "游戏暂停":[(w/2,h/2-55),chinese_font_big,"white",1,"center"],
        "按Esc或Enter继续游戏":[(w/2,h/2),chinese_font,"white",1,"center"],
        "按R重新开始":[(w/2,h/2+35),chinese_font,"white",1,"center"],
        "按L查看规则":[(0,35),chinese_font,"white",2,"center"]
    }
    DrawText(texts)
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
        if keys[pg.K_LCTRL] and keys[pg.K_d]:
            debug=True
            s=input("请输入指令：")
            if s=="god":
                god_mode=not god_mode
                print("成功！")
            elif s=="spawn":
                s=input("请输入类型：")
                if s=="enemy":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        g.add(Enemy(0))
                    print("成功！")
                elif s=="nor_enemy":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        g.add(Enemy(1))
                    print("成功！")
                elif s=="super_enemy":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        g.add(Enemy(2))
                    print("成功！")
                elif s=="health":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        he.add(Health(0))
                    print("成功！")
                elif s=="nor_health":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        he.add(Health(1))
                    print("成功！")
                elif s=="super_health":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        he.add(Health(2))
                    print("成功！")
                elif s=="floor":
                    x=int(input("请输入x坐标："))
                    y=int(input("请输入y坐标："))
                    l=int(input("请输入长度："))
                    n=int(input("请输入个数："))
                    for i in range(n):
                        floor.add(Floor(x,y,l))
                    print("成功！")
                elif s=="rain":
                    l=int(input("请输入长度："))
                    n=int(input("请输入个数："))
                    for i in range(n):
                        rain.add(Rain(l))
                    print("成功！")
                else:
                    print("未知的指令")
            else:
                print("未知的指令")
        if(keys[pg.K_r]):
            is_restart=1
            break
        if keys[pg.K_l]:
            Draw(g,he,player,inf,seconds,floor,rain,heart,fps)
            Rules()
            Draw(g,he,player,inf,seconds,floor,rain,heart,fps)
            DrawText(texts)
            pg.display.update()
        clock.tick(60)
    return debug,god_mode,g,he,player,is_restart