import pygame as pg
from const import *
def Draw(g,he,player,inf,seconds,heart):
    window.fill("black")
    g.update()
    g.draw(window)
    player.update()
    player.draw(window)
    he.draw(window)
    inf.update()
    inf.draw(window)
    pg.draw.line(window,"white",(0,500),(w,500),5)
    time=chinese_font.render(f"时间:{seconds:.1f}",True,"white")
    window.blit(time,(0,0))
    t=chinese_font.render(f"生命值:{heart}",True,"white")
    window.blit(t,t.get_rect(topright=(w,0)))
    for a in level_up_time:
        if a[0]<=seconds<=a[1]:
            text=chinese_font.render("难度升级!",True,"white")
            window.blit(text,text.get_rect(center=(w/2,h/2-200)))
    pg.display.update()
    return g,he,player,inf,seconds,heart