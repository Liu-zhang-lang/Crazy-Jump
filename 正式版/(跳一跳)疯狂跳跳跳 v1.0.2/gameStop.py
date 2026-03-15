import pygame as pg
from const import *
from enemy import Enemy
from health import Health
from player import Player
def GameStop(debug,god_mode,g,he,player):
    waiting=True
    text=chinese_font.render("游戏暂停",True,"white")
    window.blit(text,text.get_rect(center=(w/2,h/2)))
    pg.display.update()
    while waiting:
        for ev in pg.event.get():
            if ev.type==pg.QUIT:
                pg.quit()
                exit()
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
        clock.tick(60)
    return debug,god_mode,g,he,player