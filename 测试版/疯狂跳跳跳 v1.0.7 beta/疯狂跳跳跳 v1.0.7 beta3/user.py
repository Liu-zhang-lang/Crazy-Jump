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
        self.best_time=0
        self.best_minutes=0
        self.best_seconds=0
        self.best_version="Unknown"
        self.info_pos=[310,70]
        self.inputbox=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.info=pg.sprite.Group()
        os.makedirs("D:\\Crazy-Jump",exist_ok=True)
        default_json={
            "format":format,
            "version":version,
            "users":{}
        }
        if not os.path.exists("D:\\Crazy-Jump\\userdata.json"):
            with open("D:\\Crazy-Jump\\userdata.json","w",encoding="utf-8") as f:
                json.dump(default_json,f,ensure_ascii=False,indent=4)
        with open("D:\\Crazy-Jump\\userdata.json","r",encoding="utf-8") as f:
            self.data=json.load(f)
            self.migrate_version()
            self.users_data=self.data["users"]
            self.version=self.data["version"]
            self.format=self.data["format"]
            self.save_data()
    def migrate_version(self):
        if not "format" in self.data:
            self.format=1
        else:
            self.format=self.data["format"]
        if self.format!=format:
            if self.format==1:
                users=self.data
                self.data={}
                self.data["users"]=users
                self.data["version"]=version
                self.data["format"]=format
                self.data["last_rem_user"]=""
            else:
                print("游戏数据文件在创建时的游戏版本过高，版本迁移失败")
                print(f"游戏数据文件版本：{self.data["version"]}，当前游戏版本：{self.data["version"]}")
                print("游戏已退出")
                pg.quit()
                exit()
        if self.data["version"]!=version:
            self.data["version"]=version
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
        if not "best_time" in self.users_data[self.user_name]:
            self.users_data[self.user_name]["best_time"]=0
        if not "best_minutes" in self.users_data[self.user_name]:
            self.users_data[self.user_name]["best_minutes"]=0
        if not "best_seconds" in self.users_data[self.user_name]:
            self.users_data[self.user_name]["best_seconds"]=0
        if not "best_version" in self.users_data[self.user_name]:
            self.users_data[self.user_name]["best_version"]=version
        self.best_version=self.users_data[self.user_name]["best_version"]
        self.best_time=self.users_data[self.user_name]["best_time"]
        self.best_minutes=self.users_data[self.user_name]["best_minutes"]
        self.best_seconds=self.users_data[self.user_name]["best_seconds"]
    def update_data(self):
        if self.user_name in self.users_data and self.game.time>=self.best_time:
            self.best_time=self.game.time
            self.best_minutes=self.game.minutes
            self.best_seconds=self.game.seconds
            self.best_version=version
            self.users_data[self.user_name]["best_version"]=version
            self.users_data[self.user_name]["best_time"]=self.best_time
            self.users_data[self.user_name]["best_minutes"]=self.best_minutes
            self.users_data[self.user_name]["best_seconds"]=self.best_seconds
            self.users_data[self.user_name]["best_version"]=version
            self.data["users"]=self.users_data
        self.save_data()
    def save_data(self):
        self.data["users"]=self.users_data
        with open("D:\\Crazy-Jump\\userdata.json","w",encoding="utf-8") as f:
            json.dump(self.data,f,ensure_ascii=False,indent=4)
    def start(self):
        self.init_button()
        if self.user_name=="":
            self.login()
        else:
            self.main()
    def init_button(self):
        self.button=pg.sprite.Group()
        if self.user_name=="":
            self.button.add(Button((50,30),80,30,"blue",text="登录",mode=2))
            self.button.add(Button((140,30),80,30,"blue",text="注册",mode=2))
        else:
            self.button.add(Button((50,30),80,30,"blue",text="主页",mode=2))
            self.button.add(Button((140,30),80,30,"blue",text="修改密码",font=cn_sm,mode=2))
            self.button.add(Button((230,30),80,30,"blue",text="登出",mode=2))
            self.button.add(Button((320,30),80,30,"blue",text="注销",mode=2))
            self.button.add(Button((w-30,30),30,30,"blue",align="topright",text="×",mode=2))
    def handle_button(self):
        for bt in self.button:
            if bt.check_clicked():
                if bt.text=="主页" and bt.mode==2:
                    self.main()
                    return True
                if bt.text=="登录" and bt.mode==2:
                    self.login()
                    return True
                if bt.text=="登出" and bt.mode==2:
                    self.logout()
                    return True
                if bt.text=="注册" and bt.mode==2:
                    self.register()
                    return True
                if bt.text=="注销" and bt.mode==2:
                    self.unregister()
                    return True
                if bt.text=="修改密码" and bt.mode==2:
                    self.change_password()
                    return True
                if bt.text=="×" and bt.mode==2:
                    return True
        return False
    def login(self):
        if self.data["last_rem_user"]!="" and self.data["last_rem_user"] in self.data["users"]:
            rem_user=self.data["last_rem_user"]
            self.user_name=rem_user
            self.get_user_data()
            return
        self.user_name=""
        input_psw=""
        is_remember=False
        self.init_button()
        self.inputbox=pg.sprite.Group()
        self.info=pg.sprite.Group()
        self.inputbox.add(InputBox(50,70,250,50,"white","black","用户名：",is_selected=True,multiple_inputs=True))
        self.inputbox.add(InputBox(50,130,250,50,"white","black","密码：",multiple_inputs=True,hidden_string=True))
        self.inputbox.add(InputBox(50,190,250,50,"white","black","输入1则下次自动登录",font=cn_sm,multiple_inputs=True))
        self.button.add(Button((50,250),250,50,"blue",text="登录"))
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
                elif ib.tip=="密码：":
                    input_psw=ib.get_input_text()
                else:
                    if ib.get_input_text()=="1":
                        is_remember=True
                    else:
                        is_remember=False
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_clicked():
                    if bt.text=="登录" and bt.mode==1:
                        if self.user_name=="":
                            self.info=Info.append_info(self.info,"用户名不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if self.user_name in self.users_data:
                            if self.encrypt_password(input_psw)==self.users_data[self.user_name]["password"]:
                                if is_remember:
                                    self.data["last_rem_user"]=self.user_name
                                else:
                                    self.data["last_rem_user"]=""
                                self.get_user_data()
                                self.save_data()
                                self.info=Info.append_info(self.info,"登录成功！",self.info_pos,color="green",back_color=None)
                                while len(self.info.sprites())>0:
                                    self.game.eventHandle()
                                    self.info.update()
                                    self.draw()
                                    pg.display.update()
                                    clock.tick(60)
                                return
                        self.info=Info.append_info(self.info,"用户名或密码错误！",self.info_pos,color="red",back_color=None)
                        bt.is_clicked=False
            clock.tick(60)
    def register(self):
        if self.data["last_rem_user"]!="" and self.data["last_rem_user"] in self.data["users"]:
            rem_user=self.data["last_rem_user"]
            self.user_name=rem_user
            self.get_user_data()
            return
        self.user_name=""
        input_psw=""
        input_confirm_psw=""
        is_remember=False
        self.init_button()
        self.inputbox=pg.sprite.Group()
        self.info=pg.sprite.Group()
        self.inputbox.add(InputBox(50,70,250,50,"white","black","用户名：",is_selected=True,multiple_inputs=True))
        self.inputbox.add(InputBox(50,130,250,50,"white","black","密码：",multiple_inputs=True,hidden_string=True))
        self.inputbox.add(InputBox(50,190,250,50,"white","black","确认密码：",multiple_inputs=True,hidden_string=True))
        self.inputbox.add(InputBox(50,250,250,50,"white","black","输入1则下次自动登录",font=cn_sm,multiple_inputs=True))
        self.button.add(Button((50,310),250,50,"blue",text="注册"))
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
                    input_psw=ib.get_input_text()
                elif ib.tip=="确认密码：":
                    input_confirm_psw=ib.get_input_text()
                else:
                    if ib.get_input_text()=="1":
                        is_remember=True
                    else:
                        is_remember=False
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_clicked():
                    if bt.text=="注册" and bt.mode==1:
                        if self.user_name=="":
                            self.info=Info.append_info(self.info,"用户名不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if self.user_name in self.users_data:
                            self.info=Info.append_info(self.info,"用户名已存在！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if input_confirm_psw=="":
                            self.info=Info.append_info(self.info,"确认密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if input_psw!=input_confirm_psw:
                            self.info=Info.append_info(self.info,"两个密码不一致！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        running=False
                        break
            clock.tick(60)
        self.users_data[self.user_name]={"password":self.encrypt_password(input_psw)}
        if is_remember:
            self.data["last_rem_user"]=self.user_name
        else:
            self.data["last_rem_user"]=""
        self.get_user_data()
        self.save_data()
        self.info=Info.append_info(self.info,"注册成功！",self.info_pos,color="green",back_color=None)
        while len(self.info)>0:
            self.game.eventHandle()
            self.info.update()
            self.draw()
            pg.display.update()
            clock.tick(60)
        self.draw()
    def unregister(self,input_psw=""):
        input_confirm_psw=""
        self.info=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.inputbox=pg.sprite.Group()
        self.init_button()
        self.inputbox.add(InputBox(50,70,250,50,"white","black","密码：",text=input_psw,is_selected=True,multiple_inputs=True,hidden_string=True))
        self.button.add(Button((50,130),250,50,"blue",text="注销"))
        running=True
        while running:
            events=self.game.eventHandle()
            self.inputbox.update(events)
            self.button.update(events)
            self.info.update()
            self.draw()
            for ib in self.inputbox:
                if ib.tip=="密码：":
                    input_psw=ib.get_input_text()
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_clicked():
                    if bt.text=="注销" and bt.mode==1:
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if self.users_data[self.user_name]["password"]!=self.encrypt_password(input_psw):
                            self.info=Info.append_info(self.info,"密码错误！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        running=False
                        break
            clock.tick(60)
            pg.display.update()
        self.inputbox.add(InputBox(50,190,250,50,"white","black","再次输入密码：",is_selected=True,multiple_inputs=True,hidden_string=True))
        self.button.add(Button((50,250),250,50,"red",text="确认注销"))
        running=True
        while running:
            events=self.game.eventHandle()
            self.inputbox.update(events)
            self.button.update(events)
            self.info.update()
            self.draw()
            for ib in self.inputbox:
                if ib.tip=="密码：" and ib.get_input_text()!=input_psw:
                    input_psw=ib.get_input_text()
                    self.unregister(input_psw)
                    return
                if ib.tip=="再次输入密码：":
                    input_confirm_psw=ib.get_input_text()
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_clicked():
                    if bt.text=="确认注销":
                        if input_confirm_psw=="":
                            self.info=Info.append_info(self.info,"确认密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if self.users_data[self.user_name]["password"]!=self.encrypt_password(input_confirm_psw):
                            self.info=Info.append_info(self.info,"确认密码错误！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        running=False
                        break
            clock.tick(60)
            pg.display.update()
        self.info=Info.append_info(self.info,"注销成功！",self.info_pos,color="green",back_color=None)
        while len(self.info)>0:
            self.game.eventHandle()
            self.info.update()
            self.draw()
            pg.display.update()
            clock.tick(60)
        self.users_data.pop(self.user_name)
        self.user_name=""
        self.save_data()
        self.start()
        self.game.is_restart=True
    def logout(self):
        self.info=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.inputbox=pg.sprite.Group()
        self.init_button()
        self.button.add(Button((50,70),250,50,"blue",text="确认登出"))
        running=True
        while running:
            events=self.game.eventHandle()
            self.button.update(events)
            self.info.update()
            self.draw()
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_clicked():
                    if bt.text=="确认登出":
                        running=False
                        break
            clock.tick(60)
            pg.display.update()
        self.info=Info.append_info(self.info,"登出成功！",self.info_pos,color="green",back_color=None)
        while len(self.info)>0:
            self.game.eventHandle()
            self.info.update()
            self.draw()
            clock.tick(60)
            pg.display.update()
        self.user_name=""
        self.data["last_rem_user"]=""
        self.start()
    def main(self):
        self.info=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.inputbox=pg.sprite.Group()
        self.init_button()
        fst_pos=[50,70]
        self.info=Info.append_info(self.info,f"{self.user_name}的用户主页",fst_pos,back_color=None,spacing=5,mode="back")
        if self.best_minutes>0:
            self.info=Info.append_info(self.info,f"最佳成绩：{self.best_minutes}分{self.best_seconds:.2f}秒",fst_pos,back_color=None,spacing=5,mode="back")
        else:
            self.info=Info.append_info(self.info,f"最佳成绩：{self.best_seconds:.2f}秒",fst_pos,back_color=None,spacing=5,mode="back")
        running=True
        while running:
            events=self.game.eventHandle()
            self.button.update(events)
            self.draw()
            if self.handle_button():
                return
            pg.display.update()
    def change_password(self):
        input_old_psw=""
        input_psw=""
        input_confirm_psw=""
        self.info=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.inputbox=pg.sprite.Group()
        self.init_button()
        self.inputbox.add(InputBox(50,70,250,50,"white","black","请输入原密码：",is_selected=True,multiple_inputs=True,hidden_string=True))
        self.inputbox.add(InputBox(50,130,250,50,"white","black","请输入新密码：",multiple_inputs=True,hidden_string=True))
        self.inputbox.add(InputBox(50,190,250,50,"white","black","请再次输入新密码：",multiple_inputs=True,hidden_string=True))
        self.button.add(Button((50,250),250,50,"blue",text="确认修改"))
        running=True
        while running:
            events=self.game.eventHandle()
            self.button.update(events)
            self.inputbox.update(events)
            self.info.update()
            self.draw()
            for ib in self.inputbox:
                if ib.tip=="请输入原密码：":
                    input_old_psw=ib.get_input_text()
                if ib.tip=="请输入新密码：":
                    input_psw=ib.get_input_text()
                if ib.tip=="请再次输入新密码：":
                    input_confirm_psw=ib.get_input_text()
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_clicked():
                    if bt.text=="确认修改":
                        if input_old_psw=="":
                            self.info=Info.append_info(self.info,"原密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"新密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if input_confirm_psw=="":
                            self.info=Info.append_info(self.info,"确认密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if self.encrypt_password(input_old_psw)!=self.users_data[self.user_name]["password"]:
                            self.info=Info.append_info(self.info,"原密码错误！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        if input_psw!=input_confirm_psw:
                            self.info=Info.append_info(self.info,"两次输入新密码不一致！",self.info_pos,color="red",back_color=None)
                            bt.is_clicked=False
                            break
                        running=False
                        break
            clock.tick(60)
            pg.display.update()
        self.users_data[self.user_name]["password"]=self.encrypt_password(input_psw)
        self.save_data()
        self.info=Info.append_info(self.info,"密码修改成功！",self.info_pos,color="green",back_color=None)
        while len(self.info)>0:
            self.game.eventHandle()
            self.info.update()
            self.draw()
            clock.tick(60)
            pg.display.update()
        self.main()