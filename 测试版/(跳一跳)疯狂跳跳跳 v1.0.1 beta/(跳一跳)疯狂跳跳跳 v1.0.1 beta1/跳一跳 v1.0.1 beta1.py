import pygame as pg
import random as rd
from pygame.sprite import Sprite
#################################类#################################
class health(Sprite):
    def __init__(self):
        super().__init__()
        self.b=rd.randint(15,35)
        self.rect=pg.Rect((rd.randint(0,w-self.b),rd.randint(300,450)),(self.b,self.b))
        self.image=pg.Surface((self.b,self.b))
        pg.draw.rect(self.image,"green",(0,0,self.b,self.b))
class enemy(Sprite):
    def __init__(self):
        super().__init__()
        self.minspeed=2
        self.maxspeed=6
        self.b=rd.randint(15,35)
        self.image=pg.Surface((self.b,self.b))
        pg.draw.rect(self.image,"red",(0,0,self.b,self.b))
        if rd.random()>0.5:
            self.rect=pg.rect.Rect(w,500-self.b,self.b,self.b)
            self.speed=rd.randint(self.minspeed,self.maxspeed)
            if rd.random()<=0.05:
                pg.draw.rect(self.image,"purple",(0,0,self.b,self.b))
                self.speed=12
        else:
            self.rect=pg.rect.Rect(-self.b,500-self.b,self.b,self.b)
            self.speed=-rd.randint(self.minspeed,self.maxspeed)
            if rd.random()<=0.05:
                pg.draw.rect(self.image,"purple",(0,0,self.b,self.b))
                self.speed=-12
    def update(self):
        self.rect.x-=self.speed
        if self.rect.x+self.b<0 or self.rect.x>w:
            self.kill()
        if rd.random()<=0.0022:
            if self.speed>0:
                self.speed=-self.speed
            else:
                self.speed=abs(self.speed)
class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.pw=30
        self.ph=60
        self.image=pg.Surface((self.pw,self.ph))
        pg.draw.rect(self.image,"blue",(0,0,self.pw,self.ph))
        self.rect=pg.rect.Rect(0,440,self.pw,self.ph)
        self.rect.centerx=window.get_rect().centerx
        self.velocity_y=0
        self.jumping=False
    def update(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.x-=5
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.x+=5
        if self.rect.x<0:
            self.rect.x=0
        if self.rect.x+self.pw>w:
            self.rect.x=w-self.pw
        if (keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]) and self.jumping==False:
            self.jumping=True
            self.velocity_y=-14
        if self.jumping==True:
            self.rect.y+=self.velocity_y
            self.velocity_y+=0.8
        if self.rect.y>440:
            self.rect.y=440
            self.jumping=False
#################################初始化#################################
pg.init()
rd.seed()
w,h=800,600
pro=0.005
hpro=0.002
seconds=0
heart=1
jia=0
jian=0
jia_ans=0
jian_ans=0
running=True
window=pg.display.set_mode((w,h))
pg.display.set_caption("跳一跳")
clock=pg.time.Clock()
chinese_font=pg.font.Font(r"C:\Windows\Fonts\simsun.ttc",25)
chinese_font_big=pg.font.Font(r"C:\Windows\Fonts\simsun.ttc",50)
g=pg.sprite.Group()
he=pg.sprite.Group()
player=pg.sprite.Group()
player.add(Player())
#################################函数#################################
def game_over():
    global seconds
    text1=chinese_font_big.render(f"你死了！",True,"white")
    text2=chinese_font.render(f"你存活了{seconds/60:.1f}秒",True,"white")
    text3=chinese_font.render(f"按下回车键重新开始",True,"white")
    window.blit(text1,text1.get_rect(center=(w/2+15,h/2-70)))
    window.blit(text2,text2.get_rect(center=(w/2,h/2)))
    window.blit(text3,text3.get_rect(center=(w/2,h/2+50)))
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
def game_stop():
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
def draw():
    global pro,seconds,jia_ans,jian_ans
    window.fill("black")
    player.update()
    g.update()
    player.draw(window)
    g.draw(window)
    he.draw(window)
    pg.draw.line(window,"white",(0,500),(w,500),5)
    time=chinese_font.render(f"时间:{seconds/60:.1f}",True,"white")
    window.blit(time,(0,0))
    t=chinese_font.render(f"生命值:{heart}",True,"white")
    window.blit(t,t.get_rect(topright=(w,0)))
    if seconds/60>15 and seconds/60<=17:
        text=chinese_font.render("难度升级!",True,"white")
        window.blit(text,text.get_rect(center=(w/2,h/2-200)))
    if seconds/60>30 and seconds/60<=32:
        text=chinese_font.render("难度升级!",True,"white")
        window.blit(text,text.get_rect(center=(w/2,h/2-200)))
    if seconds/60>45 and seconds/60<=47:
        text=chinese_font.render("难度升级!",True,"white")
        window.blit(text,text.get_rect(center=(w/2,h/2-200)))
    if jia>jian:
        tt=chinese_font.render(f"生命值+{jia_ans}",True,"green")
        window.blit(tt,tt.get_rect(topright=(w,25)))
    elif jian>0:
        tt=chinese_font.render(f"生命值-{jian_ans}",True,"red")
        window.blit(tt,tt.get_rect(topright=(w,25)))
    if jia==0:
        jia_ans=0
    if jian_ans==0:
        jian_ans=0
    pg.display.update()
#################################主程序#################################
text1=chinese_font.render("游戏规则&玩法：",True,"white")
text2=chinese_font.render("1：使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃",True,"white")
text3=chinese_font.render("2：按下ESC暂停游戏 ，再次按下ESC继续",True,"white")
text4=chinese_font.render("3：躲避红色敌人，拾取绿色血包，看看你能坚持多久",True,"white")
text5=chinese_font.render("4：输入法为中文时，可能会导致部分按键失效",True,"white")
text6=chinese_font.render("阅读完毕后，按下回车键开始游戏",True,"white")
draw()
window.blit(text1,(50,50))
window.blit(text2,(50,90))
window.blit(text3,(50,130))
window.blit(text4,(50,170))
window.blit(text5,(50,210))
window.blit(text6,(50,250))
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
                game_stop()
    seconds+=1
    if seconds/60<=15:
        pro=0.005
        hpro=0.0015
    elif seconds/60<=30:
        pro=0.01
    elif seconds/60<=45:
        pro=0.02
        hpro=0.003
    else:
        pro=0.04
    if rd.random()<=pro or len(g)==0:
        g.add(Enemy())
    if rd.random()<=hpro and len(he)<3:
        he.add(health())
    if pg.sprite.groupcollide(player,he,False,True):
        heart+=1
        jia=120
        jia_ans+=1
    co=pg.sprite.groupcollide(player,g,False,True)
    for p,e_l in co.items():
        for e in e_l:
            if abs(e.speed)==12:
                heart-=2
                jian=120
                jian_ans+=2
            else:
                heart-=1
                jian=120
                jian_ans+=1
    if heart<0:
        heart=0
    draw()
    if heart==0:
        game_over()
        heart=1
        seconds=0
        jia=0
        jian=0
        jia_ans=0
        jian_ans=0
        g=pg.sprite.Group()
        he=pg.sprite.Group()
        player=pg.sprite.Group()
        player.add(Player())
    if jia>0:
        jia-=1
    if jian>0:
        jian-=1
    clock.tick(60)
pg.quit()