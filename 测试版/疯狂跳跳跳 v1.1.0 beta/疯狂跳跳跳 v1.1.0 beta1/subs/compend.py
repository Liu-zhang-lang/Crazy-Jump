import pygame as pg
from subs.button import Button
from subs.info import Info
from subs.const import *
class Compend:
    def __init__(self,game):
        self.info=[pg.sprite.Group() for _ in range(10)]
        self.imgs=[]
        big_pos=[50,80]
        self.img_pos=[50,130]
        def_pos=[50,210]
        id=0
        base_dir=os.path.dirname(os.path.abspath(__file__))
        self.info[id]=Info.add_info(self.info[id],"普通实体",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"基本信息：从1~8阶段的每帧生成概率分别为：0.4%,0.8%,1.6%,2.",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"8%,3.7%,4.3%,5.6%,7%（打boss模式为4%）。生成时随机从地板的",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"两侧出现，其大小是边长为15~35的正方形（随机），速度为2~6像素",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"/帧（随机），其攻击力为边长÷3。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"机制：每帧有0.15%的概率变向，随后边长-5，速度-1；若边长<15",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"或速度<3则无法变向。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/nor_enemy.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/nor_enemy.png）")
        id=1
        self.info[id]=Info.add_info(self.info[id],"超级实体",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"基本信息：生成普通实体时有6%的概率变异成超级实体。生成时随机",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"从地板的两侧出现，其大小是边长为15~35的正方形（随机），速度",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"为12像素/帧，其攻击力为边长÷1.8。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"机制：每帧有0.15%的概率变向，随后边长-5，速度-1；若边长<15",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"或速度<3则无法变向。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/super_enemy.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/super_enemy.png）")
        id=2
        self.info[id]=Info.add_info(self.info[id],"普通血包",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"基本信息：从1~8阶段的每帧生成概率分别为：0.15%,0.15%,0.25%,",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"0.35%,0.55%,0.65%,0.7%,0.75%。生成时随机在y坐标200~450的",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"地方出现，其大小是变长15~35的正方形（随机），其加血量为边长",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"÷3。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"机制：暂无。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/nor_health.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/nor_health.png）")
        id=3
        self.info[id]=Info.add_info(self.info[id],"超级血包",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"基本信息：生成普通血包时有5%的概率变异成超级血包。生成时随机",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"在y坐标200~450的地方出现，其大小为40的正方形，其加血量为40。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"机制：暂无。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/super_health.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/super_health.png）")
        id=4
        self.info[id]=Info.add_info(self.info[id],"雨滴",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"基本信息：从1~8阶段的每帧生成概率分别为：0%,0%,0.2%,0.5%,1",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],".1%,2%,3.9%,4.5%（打boss模式为2.5%）。生成时会在y坐标为0的",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"位置出现，图形是由长为20~50，宽为8的长方形旋转45°形成，速",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"度为向左向下各5像素/帧，攻击力为长度÷6.5。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"机制：碰到地板会消失。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/rain.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/rain.png）")
        id=5
        self.info[id]=Info.add_info(self.info[id],"地板",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"基本信息：从1~8阶段的每帧生成概率分别为：0.01%,0.05%,0.01",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"%,0.12%,0.13%,0.16%,0.17%,0.17%。生成时会在y坐标240~400",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"的位置出现，图形是一个长为60~150，宽为5的长方形。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"机制：玩家碰到地板时，地板开始3秒计时，且会变为绿色；剩余时",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"间为总剩余时间的2/3时，地板变为黄色；地板剩余时间为总剩余时",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"间1/3时，地板变为橙色；地板剩余时间<=0.5秒时，地板变为红色；",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"地板剩余时间<0，地板消失。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/floor.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/floor.png）")
        id=6
        self.info[id]=Info.add_info(self.info[id],"boss",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"基本信息：boss只会在第8阶段生成，生成时随机从地板的两侧出",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"现，其大小是边长为40的正方形，速度在1.8/帧~2.2/帧之间波动，",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"初始生命值为46，且拥有二段跳的能力。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"机制：自动向玩家移动、跳跃，普通跳和二段跳cd均为1.5s，变向c",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"d为1s。boss拥有与玩家同样的地板碰撞逻辑，但碰到地板不会导致",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"地板计时。当boss和玩家持续碰撞时，每0.5s，玩家生命值减少10",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"%，最少受到5点伤害，boss受到玩家受伤值的40%，最少受到4点伤",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"害。boss血量<=25时，每7秒回复2滴血；boss血量<=10，获得40%",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"伤害减免，且所有回血量*2；当boss血量<=0时，boss被击杀。玩",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"家受到伤害（boss造成的除外）时，boss回复1滴血，该回复cd为1",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"s。boss每25s会从所有技能中随机释放一个技能，进场时会在10s后",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"开始释放技能。玩家回血时，boss受到玩家回血量25%的伤害，最少",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/boss.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/boss.png）")
        id=7
        self.info[id]=Info.add_info(self.info[id],"boss",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"受到2点伤害。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"技能1：释放技能后玩家禁止移动1.5s。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"技能2：对玩家发射5颗子弹，偏移度分别为-10°,-5°,0°,5°,10",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"°。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/boss.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/boss.png）")
        id=8
        self.info[id]=Info.add_info(self.info[id],"子弹",big_pos,font=cn_big,back_color=None)
        self.info[id]=Info.append_info(self.info[id],"基本信息：子弹只会由boss发射，图形由长为30，宽为7的长方形",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"旋转形成，速度为9。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        self.info[id]=Info.append_info(self.info[id],"机制：碰到玩家消失，且对玩家造成8点伤害。",def_pos,font=cn_def,back_color=None,spacing=3,mode="back")
        try:
            self.imgs.append(pg.image.load(base_dir+"/images/bullet.png"))
        except:
            add_error("[error:Compend/__init__]图片加载失败（/images/bullet.png）")
        self.game=game
        self.button=pg.sprite.Group()
        self.title=cn_big.render("图鉴",True,"white")
        self.maxpage=9
    def init_button(self):
        self.button.empty()
        self.button.add(Button((w-30,70),30,30,"blue",text="×",align="topright"))
    def button_handle(self):
        for bt in self.button:
            if bt.check_click():
                if bt.text=="×":
                    return True
    def draw(self):
        self.game.draw()
        window.blit(gray_img,(0,0))
        window.blit(self.title,self.title.get_rect(center=(w/2,40)))
        self.button.draw(window)
    def menu(self):
        self.init_button()
        self.button.add(Button((50,550),30,30,"blue",align="topleft",text="<-"))
        self.button.add(Button((w-50,550),30,30,"blue",align="topright",text="->"))
        index=0
        while True:
            events=self.game.event_handle()
            self.button.update(events)
            self.draw()
            self.info[index].draw(window)
            img=cn_def.render(f"第{index+1}/{self.maxpage}页",True,"white")
            window.blit(img,img.get_rect(center=(w/2,565)))
            if index<len(self.imgs):
                window.blit(self.imgs[index],self.img_pos)
            if self.button_handle():
                return
            for bt in self.button:
                if bt.check_click() and bt.rect.y!=30:
                    if bt.text=="<-":
                        if index>0:
                            index-=1
                    elif bt.text=="->":
                        if index<self.maxpage-1:
                            index+=1
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_LEFT:
                        if index>0:
                            index-=1
                    elif ev.key==pg.K_RIGHT:
                        if index<self.maxpage-1:
                            index+=1
                    elif ev.key==pg.K_ESCAPE:
                        return True
            pg.display.update()
            clock.tick(60)