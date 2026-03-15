import pygame as pg
import sys
from const import *
from enemy import Enemy
from health import Health
from drawText import DrawText
def GameStop(debug,god_mode,g,he,player):
    waiting=True
    is_restart=0
    texts={
        "游戏暂停":[(w/2,h/2-55),chinese_font_big,"white","center"],
        "按ESC继续游戏":[(w/2,h/2),chinese_font,"white","center"],
        "按R重新开始":[(w/2,h/2+35),chinese_font,"white","center"]
    }
    DrawText(texts)
    pg.display.update()
    while waiting:
        for ev in pg.event.get():
            if ev.type==pg.QUIT:
                pg.quit()
                sys.exit(0)
            if ev.type==pg.KEYDOWN:
                if ev.key==pg.K_ESCAPE:
                    waiting=False
        keys=pg.key.get_pressed()
        if keys[pg.K_LCTRL] and keys[pg.K_d]:
            debug=True
            s=input("请输入指令：")
            if s=="god":
                god_mode=not god_mode
                print("成功！")
            elif s=="gen":
                s=input("请输入类型：")
                if s=="enemy":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        g.add(Enemy(0))
                    print("成功！")
                elif s=="ord_enemy":
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
                elif s=="ord_health":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        he.add(Health(1))
                    print("成功！")
                elif s=="super_health":
                    n=int(input("请输入个数："))
                    for i in range(n):
                        he.add(Health(2))
                    print("成功！")
                else:
                    print("未知的指令")
            else:
                print("未知的指令")
        if(keys[pg.K_r]):
            is_restart=1
            break
        clock.tick(60)
    return debug,god_mode,g,he,player,is_restart