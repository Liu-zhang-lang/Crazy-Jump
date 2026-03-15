from dao_ru_ku import DaoRuKu
#################################检查库#################################
needPackages={
    "pygame":"pg",
}
DaoRuKu(needPackages)
input("按下enter键开始游玩")
print("开始游戏")
from const import *
from enemy import Enemy
from health import Health
from player import Player
from information import Information
from draw import Draw
from gameStop import GameStop
from gameOver import GameOver
#################################初始化#################################
import pygame as pg
import random as rd
pro=0.005
hpro=0.0015
seconds=0
heart=30
debug=False
god_mode=False
running=True
pg.display.set_caption("跳一跳")
g=pg.sprite.Group()
he=pg.sprite.Group()
player=pg.sprite.Group()
inf=pg.sprite.Group()
g.add(Enemy(1))
player.add(Player())
#################################主程序#################################
g,he,player,inf,seconds,heart=Draw(g,he,player,inf,seconds,heart)
text1=chinese_font.render("游戏规则&玩法：",True,"white")
text2=chinese_font.render("1：使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃",True,"white")
text3=chinese_font.render("2：按下ESC暂停游戏，再次按下ESC继续",True,"white")
text4=chinese_font.render("3：躲避红色/紫色(加强)敌人，拾取绿色/黄色(加强)血包，看看",True,"white")
text4_2=chinese_font.render("你能坚持多久",True,"white")
text5=chinese_font.render("4：输入法为中文时，可能会导致部分按键失效",True,"white")
text6=chinese_font.render("阅读完毕后，按下回车键开始游戏",True,"white")
window.blit(text1,(50,50))
window.blit(text2,(50,90))
window.blit(text3,(50,130))
window.blit(text4,(50,170))
window.blit(text4_2,(50,210))
window.blit(text5,(50,250))
window.blit(text6,(50,290))
pg.display.update()
while running:
    for ev in pg.event.get():
        if ev.type==pg.QUIT:
            pg.quit()
            exit()
    keys=pg.key.get_pressed()
    if keys[pg.K_RETURN]:
        running=False
running=True
while running:
    for ev in pg.event.get():
        if ev.type==pg.QUIT:
            pg.quit()
            exit()
        if ev.type==pg.KEYDOWN:
            if ev.key==pg.K_ESCAPE:
                debug,god_mode,g,he,player=GameStop(debug,god_mode,g,he,player)
    seconds+=1/60
    for i in range(len(level_up_time)):
        if level_up_time[i][0]<=seconds<=level_up_time[i][1]:
            pro=all_pro[i]
            hpro=all_hpro[i]
    if rd.random()<=pro:
        g.add(Enemy(0))
    if rd.random()<=hpro:
        he.add(Health(0))
    co=pg.sprite.groupcollide(player,he,False,True)
    for p,e_l in co.items():
        for e in e_l:
            if e.b==40:
                heart+=25
                inf=Information.add_inf(inf,f"生命值+25","green")
            else:
                heart+=int(e.b//3)
                inf=Information.add_inf(inf,f"生命值+{int(e.b//3)}","green")
    if god_mode==False:
        co=pg.sprite.groupcollide(player,g,False,True)
        for p,e_l in co.items():
            for e in e_l:
                if abs(e.speed)==12:
                    heart-=int(e.b//1.8)
                    inf=Information.add_inf(inf,f"生命值-{int(e.b//1.8)}","red")
                else:
                    heart-=int(e.b//3)
                    inf=Information.add_inf(inf,f"生命值-{int(e.b//3)}","red")
    if heart<0:
        heart=0
    g,he,player,inf,seconds,heart=Draw(g,he,player,inf,seconds,heart)
    if heart==0:
        GameOver(seconds,debug)
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
    clock.tick(60)
pg.quit()