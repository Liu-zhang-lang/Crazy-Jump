import pygame as pg
from const import *
def GameOver(seconds,debug):
    text1=chinese_font_big.render(f"你死了！",True,"white")
    text2=chinese_font.render(f"你存活了{seconds:.1f}秒",True,"white")
    text3=chinese_font.render(f"按下回车键重新开始",True,"white")
    window.blit(text1, text1.get_rect(center=(w/2+15,h/2-70)))
    window.blit(text2, text2.get_rect(center=(w/2,h/ 2)))
    window.blit(text3,text3.get_rect(center=(w/2,h/2+50)))
    if debug:
        text=chinese_font_lit.render("(使用了debug调试)",True,"yellow")
        window.blit(text,text.get_rect(center=(w/2,h/2+85)))
    pg.display.update()
    waiting=True
    while waiting:
        for ev in pg.event.get():
            if ev.type==pg.QUIT:
                pg.quit()
                exit()
        keys=pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            waiting=False
        clock.tick(60)