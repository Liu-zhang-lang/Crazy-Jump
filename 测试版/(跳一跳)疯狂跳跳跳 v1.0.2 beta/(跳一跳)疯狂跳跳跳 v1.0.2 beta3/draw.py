import pygame as pg
from const import *
def Draw(g,he,player,seconds,heart,jia,jian,jia_ans,jian_ans):
    window.fill("black")
    player.update()
    g.update()
    player.draw(window)
    g.draw(window)
    he.draw(window)
    pg.draw.line(window,"white",(0,500),(w,500),5)
    time=chinese_font.render(f"时间:{seconds:.1f}",True,"white")
    window.blit(time,(0,0))
    t=chinese_font.render(f"生命值:{heart}",True,"white")
    window.blit(t,t.get_rect(topright=(w,0)))
    for a in level_up_time:
        if a[0]<=seconds<=a[1]:
            text=chinese_font.render("难度升级!",True,"white")
            window.blit(text,text.get_rect(center=(w/2,h/2-200)))
    if jia>jian:
        tt=chinese_font.render(f"生命值+{jia_ans}",True,"green")
        window.blit(tt,tt.get_rect(topright=(w,25)))
        jian_ans=0
    elif jian>0:
        tt=chinese_font.render(f"生命值-{jian_ans}",True,"red")
        window.blit(tt,tt.get_rect(topright=(w,25)))
        jia_ans=0
    if jia==0:
        jia_ans=0
    if jian==0:
        jian_ans=0
    pg.display.update()
    return g,he,player,seconds,heart,jia,jian,jia_ans,jian_ans