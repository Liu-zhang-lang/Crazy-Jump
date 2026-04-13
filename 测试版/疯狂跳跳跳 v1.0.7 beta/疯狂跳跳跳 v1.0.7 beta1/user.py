import pygame as pg
import os
import json
import hashlib
from inputBox import InputBox
from info import Info
from button import Button
from const import *
class User:
    def __init__(self,game):
        self.game=game
        self.user_name=""
        self.input_psw=""
        self.best_time=0
        self.best_minutes=0
        self.best_seconds=0
        self.inputbox=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.info=pg.sprite.Group()
        os.makedirs("D:\\Crazy-Jump",exist_ok=True)
        with open("D:\\Crazy-Jump\\userdata.json","r",encoding="utf-8") as f:
            self.users_data=json.load(f)
    def encrypt_password(self,psw):
        salt="Crazy-Jump"
        psw=salt+psw
        psw=hashlib.sha256(psw.encode("utf-8")).hexdigest()
        return psw
    def draw(self):
        self.game.draw()
        window.blit(gray_img,(0,0))
        self.inputbox.draw(window)
        self.button.draw(window)
        self.info.draw(window)
    def get_user_data(self):
        if "best_time" in self.users_data[self.user_name]:
            self.best_time=self.users_data[self.user_name]["best_time"]
        if "best_minutes" in self.users_data[self.user_name]:
            self.best_minutes=self.users_data[self.user_name]["best_minutes"]
        if "best_seconds" in self.users_data[self.user_name]:
            self.best_seconds=self.users_data[self.user_name]["best_seconds"]
    def update_data(self):
        if self.game.time>self.best_time:
            self.best_time=self.game.time
            self.best_minutes=self.game.minutes
            self.best_seconds=self.game.seconds
            self.users_data[self.user_name]["best_time"]=self.best_time
            self.users_data[self.user_name]["best_minutes"]=self.best_minutes
            self.users_data[self.user_name]["best_seconds"]=self.best_seconds
        with open("D:\\Crazy-Jump\\userdata.json","w",encoding="utf-8") as f:
            json.dump(self.users_data,f,ensure_ascii=False,indent=4)
    def login(self):
        self.user_name=""
        self.input_psw=""
        self.inputbox=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.inputbox.add(InputBox(50,50,250,50,"white","black","用户名：",is_selected=True,multiple_inputs=True))
        self.inputbox.add(InputBox(50,110,250,50,"white","black","密码：",multiple_inputs=True,hidden_string=True))
        self.button.add(Button((50,170),250,50,"blue",text="登录"))
        self.button.add(Button((50,230),250,50,"blue",text="没有账号？跳转至注册",font=cn_sm))
        while True:
            events=self.game.eventHandle()
            self.inputbox.update(events)
            self.button.update(events)
            self.info.update()
            self.draw()
            pg.display.update()
            for ib in self.inputbox:
                if ib.tip=="用户名：":
                    self.user_name=ib.get_input_text()
                else:
                    self.input_psw=ib.get_input_text()
            for bt in self.button:
                if bt.check_clicked():
                    if bt.text=="没有账号？跳转至注册":
                        self.register()
                        return
                    if bt.text=="登录":
                        if self.user_name=="":
                            self.info=Info.append_info(self.info,"用户名不能为空！",(310,50),font=cn_sm,color="red",time=1)
                            bt.is_clicked=False
                            break
                        if self.input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",(310,50),font=cn_sm,color="red",time=1)
                            bt.is_clicked=False
                            break
                        if self.user_name in self.users_data:
                            if self.encrypt_password(self.input_psw)==self.users_data[self.user_name]["password"]:
                                self.get_user_data()
                                self.info=Info.append_info(self.info,"登录成功！",(310,50),color="green",time=1)
                                while len(self.info.sprites())>0:
                                    self.game.eventHandle()
                                    self.info.update()
                                    self.draw()
                                    pg.display.update()
                                    clock.tick(60)
                                return
                        self.info=Info.append_info(self.info,"用户名或密码错误！",(310,50),font=cn_sm,color="red",time=1)
                        bt.is_clicked=False
            clock.tick(60)
    def register(self):
        self.inputbox=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.inputbox.add(InputBox(50,50,250,50,"white","black","用户名：",is_selected=True,multiple_inputs=True))
        self.inputbox.add(InputBox(50,110,250,50,"white","black","密码：",multiple_inputs=True,hidden_string=True))
        self.inputbox.add(InputBox(50,170,250,50,"white","black","确认密码：",multiple_inputs=True,hidden_string=True))
        self.button.add(Button((50,230),250,50,"blue",text="注册"))
        self.button.add(Button((50,290),250,50,"blue",text="已有账号？跳转至登录",font=cn_sm))
        self.user_name=""
        self.input_psw=""
        self.input_confirm_psw=""
        running=True
        while running:
            events=self.game.eventHandle()
            self.inputbox.update(events)
            self.button.update(events)
            self.info.update()
            self.draw()
            pg.display.update()
            for ib in self.inputbox:
                if ib.tip=="用户名：":
                    self.user_name=ib.get_input_text()
                elif ib.tip=="密码：":
                    self.input_psw=ib.get_input_text()
                else:
                    self.input_confirm_psw=ib.get_input_text()
            for bt in self.button:
                if bt.check_clicked():
                    if bt.text=="已有账号？跳转至登录":
                        self.login()
                        return
                    else:
                        if self.user_name=="":
                            self.info=Info.append_info(self.info,"用户名不能为空！",(310,50),font=cn_sm,color="red",time=1)
                            bt.is_clicked=False
                            break
                        if self.user_name in self.users_data:
                            self.info=Info.append_info(self.info,"用户名已存在！",(310,50),font=cn_sm,color="red",time=1)
                            bt.is_clicked=False
                            break
                        if self.input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",(310,50),font=cn_sm,color="red",time=1)
                            bt.is_clicked=False
                            break
                        if self.input_confirm_psw=="":
                            self.info=Info.append_info(self.info,"确认密码不能为空！",(310,50),font=cn_sm,color="red",time=1)
                            bt.is_clicked=False
                            break
                        if self.input_psw!=self.input_confirm_psw:
                            self.info=Info.append_info(self.info,"两个密码不一致！",(310,50),font=cn_sm,color="red",time=1)
                            bt.is_clicked=False
                            break
                        running=False
                        break
            clock.tick(60)
        self.users_data[self.user_name]={"password":self.encrypt_password(self.input_psw)}
        with open("D:\\Crazy-Jump\\userdata.json","w",encoding="utf-8") as f:
            json.dump(self.users_data,f,ensure_ascii=False,indent=4)
        self.info=Info.append_info(self.info,"注册成功！",(310,50),font=cn_sm,color="green",time=1)
        self.update_data()
        while len(self.info)>0:
            self.game.eventHandle()
            self.info.update()
            self.draw()
            pg.display.update()
            clock.tick(60)
        self.draw()