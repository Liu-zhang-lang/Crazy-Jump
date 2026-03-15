import pygame as pg
from const import *
from drawText import DrawText
def Draw(g,he,player,inf,seconds,floor,rain,heart,fps):
    window.fill("black")
    g.draw(window)
    he.draw(window)
    player.draw(window)
    inf.draw(window)
    floor.draw(window)
    rain.draw(window)
    text={
        f"时间:{seconds:.2f}":[(0,0),chinese_font,"white"],
        f"生命值:{heart}":[(w,0),chinese_font,"white",1,"topright"],
        f"FPS:{fps:.2f}":[(0,chinese_font_size),chinese_font,"white"]
    }
    DrawText(text)
    for a in level_up_time:
        if a[0]<=seconds<=a[1]:
            text=chinese_font_big.render("难度升级!",True,"white")
            window.blit(text,text.get_rect(center=(w/2,h/2-200)))