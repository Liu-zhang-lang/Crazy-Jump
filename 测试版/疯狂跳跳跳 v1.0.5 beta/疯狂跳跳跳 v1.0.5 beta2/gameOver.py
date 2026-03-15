import pygame as pg
import sys
from drawText import DrawText
from const import *
def GameOver(seconds,debug):
    texts={
        "你死了！":[(w/2,h/2-55),chinese_font_big,"white",1,"center"],
        f"你存活了{seconds:.2f}秒":[(w/2,h/2),chinese_font,"white",1,"center"],
        "按R重新开始":[(w/2,h/2+35),chinese_font,"white",1,"center"]
    }
    DrawText(texts)
    if debug:
        text=chinese_font_lit.render("(使用了debug调试)",True,"yellow")
        window.blit(text,text.get_rect(center=(w/2,h/2+65)))
    pg.display.update()
    waiting=True
    while waiting:
        for ev in pg.event.get():
            if ev.type==pg.QUIT:
                pg.quit()
                sys.exit(0)
        keys=pg.key.get_pressed()
        if keys[pg.K_r]:
            break
        clock.tick(60)