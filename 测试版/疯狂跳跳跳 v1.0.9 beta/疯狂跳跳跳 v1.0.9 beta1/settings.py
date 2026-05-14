import pygame as pg
from button import Button
from info import Info
from const import *
class Settings:
    def __init__(self,game):
        self.game=game
        self.button=pg.sprite.Group()
        self.info=pg.sprite.Group()
    def init_button(self):
        self.button.empty()
        self.button.add(Button((50,30),80,30,"blue",text="游戏设置",font=cn_sm))
        self.button.add(Button((w-30,30),30,30,"blue",text="×",align="topright"))
    def handle_button(self):
        for bt in self.button:
            if bt.check_click():
                if bt.text=="游戏设置":
                    self.game_settings()
                    return True
                elif bt.text=="×":
                    return True
        return False
    def draw(self):
        self.game.draw()
        window.blit(gray_img,(0,0))
        self.button.draw(window)
        self.info.draw(window)
    def start(self):
        self.game_settings()
    def game_settings(self):
        self.info.empty()
        self.button.empty()
        self.init_button()
        self.button.add(Button((50,70),150,50,"blue",text="敌人显示攻击力",font=cn_sm))
        self.button.add(Button((50,130),150,50,"blue",text="血包显示加血量",font=cn_sm))
        self.button.add(Button((50,190),150,50,"blue",text="雨滴显示攻击力",font=cn_sm))
        window.blit(cn_big.render(("开" if self.game.user.settings["enemy_show"] else "关"),True,"white"),(210,70))
        window.blit(cn_big.render(("开" if self.game.user.settings["health_show"] else "关"),True,"white"),(210,130))
        window.blit(cn_big.render(("开" if self.game.user.settings["rain_show"] else "关"),True,"white"),(210,190))
        window.blit(cn_fonts[15].render("该选项会导致雨点碰撞体积增大",True,"red"),(50,260))
        while True:
            events=self.game.event_handle()
            if self.handle_button():
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
            self.button.update(events)
            self.draw()
            window.blit(cn_big.render(("开" if self.game.user.settings["enemy_show"] else "关"),True,"white"),(210,70))
            window.blit(cn_big.render(("开" if self.game.user.settings["health_show"] else "关"),True,"white"),(210,130))
            window.blit(cn_big.render(("开" if self.game.user.settings["rain_show"] else "关"),True,"white"),(210,190))
            window.blit(cn_fonts[17].render("该选项将使雨点碰撞体积增大",True,"orange"),(50,240))
            pg.display.update()
            clock.tick(60)