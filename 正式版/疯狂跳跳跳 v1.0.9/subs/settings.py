import pygame as pg
from subs.button import Button
from subs.const import *
class Settings:
    def __init__(self,game):
        self.game=game
        self.button=pg.sprite.Group()
        self.info=pg.sprite.Group()
        self.title=cn_big.render("游戏设置",True,"white")
    def init_button(self):
        self.button.empty()
        self.button.add(Button((50,70),80,30,"blue",text="游戏设置",font=cn_sm))
        self.button.add(Button((w-30,70),30,30,"blue",text="×",align="topright"))
    def handle_button(self,events):
        for bt in self.button:
            if bt.check_click():
                if bt.text=="游戏设置":
                    self.game_settings()
                    return True
                elif bt.text=="×":
                    return True
        for ev in events:
            if ev.type==pg.KEYDOWN:
                if ev.key==pg.K_ESCAPE:
                    return True
        return False
    def draw(self):
        self.game.draw()
        window.blit(gray_img,(0,0))
        window.blit(self.title,self.title.get_rect(center=(w/2,40)))
        self.button.draw(window)
        self.info.draw(window)
    def start(self):
        self.game_settings()
    def game_settings(self):
        self.info.empty()
        self.button.empty()
        self.init_button()
        y1=110
        y2=180
        y3=250
        y4=320
        tip3=cn_fonts[17].render("开启后会导致雨点碰撞体积增大",True,"orange")
        tip4=cn_fonts[17].render("开启后需按两次R键才能重开",True,"white")
        self.button.add(Button((50,y1),150,50,"blue",text="敌人显示攻击力",font=cn_sm))
        self.button.add(Button((50,y2),150,50,"blue",text="血包显示加血量",font=cn_sm))
        self.button.add(Button((50,y3),150,50,"blue",text="雨滴显示攻击力",font=cn_sm))
        self.button.add(Button((50,y4),150,50,"blue",text="重开按键防误触",font=cn_sm))
        if "enemy_show" not in self.game.user.settings:
            self.game.user.settings["enemy_show"]=False
        if "health_show" not in self.game.user.settings:
            self.game.user.settings["health_show"]=False
        if "rain_show" not in self.game.user.settings:
            self.game.user.settings["rain_show"]=False
        if "safe_restart" not in self.game.user.settings:
            self.game.user.settings["safe_restart"]=True
        while True:
            events=self.game.event_handle()
            if self.handle_button(events):
                return
            for bt in self.button:
                if bt.check_click():
                    if bt.text=="敌人显示攻击力":
                        self.game.user.settings["enemy_show"]=not self.game.user.settings["enemy_show"]
                        for enemy in self.game.enemy:
                            enemy.draw_pic(self.game.user.settings["enemy_show"])
                        self.game.user.update_data()
                    elif bt.text=="血包显示加血量":
                        self.game.user.settings["health_show"]=not self.game.user.settings["health_show"]
                        for health in self.game.health:
                            health.draw_pic(self.game.user.settings["health_show"])
                        self.game.user.update_data()
                    elif bt.text=="雨滴显示攻击力":
                        self.game.user.settings["rain_show"]=not self.game.user.settings["rain_show"]
                        for rain in self.game.rain:
                            rain.draw_pic(self.game.user.settings["rain_show"])
                        self.game.user.update_data()
                    elif bt.text=="重开按键防误触":
                        self.game.user.settings["safe_restart"]=not self.game.user.settings["safe_restart"]
                        self.game.user.update_data()
            self.button.update(events)
            self.draw()
            window.blit(cn_big.render(("开" if self.game.user.settings["enemy_show"] else "关"),True,"white"),(210,y1))
            window.blit(cn_big.render(("开" if self.game.user.settings["health_show"] else "关"),True,"white"),(210,y2))
            window.blit(cn_big.render(("开" if self.game.user.settings["rain_show"] else "关"),True,"white"),(210,y3))
            window.blit(tip3,(50,y3+50))
            window.blit(cn_big.render(("开" if self.game.user.settings["safe_restart"] else "关"),True,"white"),(210,y4))
            window.blit(tip4,(50,y4+50))
            pg.display.update()
            clock.tick(60)