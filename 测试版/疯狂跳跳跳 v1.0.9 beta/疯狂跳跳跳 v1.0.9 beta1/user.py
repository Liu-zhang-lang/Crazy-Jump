import pygame as pg
import os
import json
import hashlib
from inputBox import InputBox
from info import Info
from button import Button
from achiev import Achiev
from const import *
class User:
    def __init__(self,game):
        self.game=game
        self.user_name=""
        self.best_time=0
        self.best_minutes=0
        self.best_seconds=0
        self.best_version="Unknown"
        self.settings={}
        self.achievs={}
        self.info_pos=[310,70]
        self.inputbox=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.info=pg.sprite.Group()
        achiev=Achiev(game)
        self.achievs_list=achiev.achievs_list
        os.makedirs("D:\\Crazy-Jump",exist_ok=True)
        default_json={
            "format":format,
            "version":version,
            "last_rem_user":"",
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
                print(f"游戏数据文件版本：{self.data['version']}，当前游戏版本：{self.data['version']}")
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
        if not "settings" in self.users_data[self.user_name]:
            self.users_data[self.user_name]["settings"]={
                "enemy_show":False,
                "health_show":False,
                "rain_show":False
            }
        if not "achievs" in self.users_data[self.user_name]:
            self.users_data[self.user_name]["achievs"]={}
            for ach in self.achievs_list:
                self.users_data[self.user_name]["achievs"][ach]=False
        self.best_version=self.users_data[self.user_name]["best_version"]
        self.best_time=self.users_data[self.user_name]["best_time"]
        self.best_minutes=self.users_data[self.user_name]["best_minutes"]
        self.best_seconds=self.users_data[self.user_name]["best_seconds"]
        self.achievs=self.users_data[self.user_name]["achievs"]
        self.settings=self.users_data[self.user_name]["settings"]
    def update_data(self):
        if self.user_name in self.users_data and self.game.time>=self.best_time and self.game.heart<=0:
            self.best_time=self.game.time
            self.best_minutes=self.game.minutes
            self.best_seconds=self.game.seconds
            self.best_version=version
            self.users_data[self.user_name]["best_version"]=version
            self.users_data[self.user_name]["best_time"]=self.best_time
            self.users_data[self.user_name]["best_minutes"]=self.best_minutes
            self.users_data[self.user_name]["best_seconds"]=self.best_seconds
            self.users_data[self.user_name]["best_version"]=version
        self.users_data[self.user_name]["settings"]=self.settings
        self.users_data[self.user_name]["achievs"]=self.achievs
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
            self.button.add(Button((50,30),80,30,"blue",text="登录"))
            self.button.add(Button((140,30),80,30,"blue",text="注册"))
        else:
            self.button.add(Button((50,30),80,30,"blue",text="主页"))
            self.button.add(Button((140,30),80,30,"blue",text="修改密码",font=cn_sm))
            self.button.add(Button((230,30),80,30,"blue",text="修改名字",font=cn_sm))
            self.button.add(Button((320,30),80,30,"blue",text="登出"))
            self.button.add(Button((410,30),80,30,"red",text="危险区"))
            self.button.add(Button((w-30,30),30,30,"blue",align="topright",text="×"))
    def handle_button(self):
        for bt in self.button:
            if bt.check_click():
                if bt.text=="主页" and bt.rect.y==30:
                    self.main()
                    return True
                if bt.text=="登录" and bt.rect.y==30:
                    self.login()
                    return True
                if bt.text=="登出" and bt.rect.y==30:
                    self.logout()
                    return True
                if bt.text=="注册" and bt.rect.y==30:
                    self.register()
                    return True
                if bt.text=="修改密码" and bt.rect.y==30:
                    self.change_password()
                    return True
                if bt.text=="修改名字" and bt.rect.y==30:
                    self.change_name()
                    return True
                if bt.text=="危险区" and bt.rect.y==30:
                    self.danger_operation()
                    return True
                if bt.text=="×" and bt.rect.y==30:
                    return True
        return False
    def login(self):
        self.game.reset()
        if self.data["last_rem_user"]!="" and self.data["last_rem_user"] in self.data["users"]:
            rem_user=self.data["last_rem_user"]
            self.user_name=rem_user
            self.get_user_data()
            self.game.auto_login=True
            return rem_user
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
            events=self.game.event_handle()
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
                if bt.check_click():
                    if bt.text=="登录" and bt.rect.y==250:
                        if self.user_name=="":
                            self.info=Info.append_info(self.info,"用户名不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
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
                                    self.game.event_handle()
                                    self.info.update()
                                    self.draw()
                                    pg.display.update()
                                    clock.tick(60)
                                return
                        self.info=Info.append_info(self.info,"用户名或密码错误！",self.info_pos,color="red",back_color=None)
                        bt.is_click=False
            clock.tick(60)
    def register(self):
        self.game.reset()
        if self.data["last_rem_user"]!="" and self.data["last_rem_user"] in self.data["users"]:
            rem_user=self.data["last_rem_user"]
            self.user_name=rem_user
            self.get_user_data()
            self.game.auto_login=True
            return rem_user
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
            events=self.game.event_handle()
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
                if bt.check_click():
                    if bt.text=="注册" and bt.rect.y==310:
                        if self.user_name=="":
                            self.info=Info.append_info(self.info,"用户名不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if self.user_name in self.users_data:
                            self.info=Info.append_info(self.info,"用户名已存在！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if input_confirm_psw=="":
                            self.info=Info.append_info(self.info,"确认密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if input_psw!=input_confirm_psw:
                            self.info=Info.append_info(self.info,"两个密码不一致！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        running=False
                        break
            clock.tick(60)
        self.users_data[self.user_name]={
            "password":self.encrypt_password(input_psw)
        }
        if is_remember:
            self.data["last_rem_user"]=self.user_name
        else:
            self.data["last_rem_user"]=""
        self.get_user_data()
        self.save_data()
        self.info=Info.append_info(self.info,"注册成功！",self.info_pos,color="green",back_color=None)
        while len(self.info)>0:
            self.game.event_handle()
            self.info.update()
            self.draw()
            pg.display.update()
            clock.tick(60)
        self.draw()
    def logout(self):
        self.info=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.inputbox=pg.sprite.Group()
        self.init_button()
        self.button.add(Button((50,70),250,50,"blue",text="确认登出"))
        running=True
        while running:
            events=self.game.event_handle()
            self.button.update(events)
            self.info.update()
            self.draw()
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_click():
                    if bt.text=="确认登出":
                        running=False
                        break
            clock.tick(60)
            pg.display.update()
        self.info=Info.append_info(self.info,"登出成功！",self.info_pos,color="green",back_color=None)
        while len(self.info)>0:
            self.game.event_handle()
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
            events=self.game.event_handle()
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
            events=self.game.event_handle()
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
                if bt.check_click():
                    if bt.text=="确认修改":
                        if input_old_psw=="":
                            self.info=Info.append_info(self.info,"原密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"新密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if input_confirm_psw=="":
                            self.info=Info.append_info(self.info,"确认密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if self.encrypt_password(input_old_psw)!=self.users_data[self.user_name]["password"]:
                            self.info=Info.append_info(self.info,"原密码错误！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        if input_psw!=input_confirm_psw:
                            self.info=Info.append_info(self.info,"两次输入新密码不一致！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        running=False
                        break
            clock.tick(60)
            pg.display.update()
        self.users_data[self.user_name]["password"]=self.encrypt_password(input_psw)
        self.save_data()
        self.info=Info.append_info(self.info,"密码修改成功！",self.info_pos,color="green",back_color=None)
        while len(self.info)>0:
            self.game.event_handle()
            self.info.update()
            self.draw()
            clock.tick(60)
            pg.display.update()
        self.main()
    def change_name(self):
        input_name=""
        input_psw=""
        self.inputbox.add(InputBox(50,70,250,50,"white","black","请输入密码：",is_selected=True,multiple_inputs=True,hidden_string=True))
        self.inputbox.add(InputBox(50,130,250,50,"white","black","请输入新名字：",multiple_inputs=True))
        self.button.add(Button((50,190),250,50,"blue",text="确认修改"))
        running=True
        while running:
            events=self.game.event_handle()
            self.button.update(events)
            self.inputbox.update(events)
            self.info.update()
            self.draw()
            for ib in self.inputbox:
                if ib.tip=="请输入密码：":
                    input_psw=ib.get_input_text()
                if ib.tip=="请输入新名字：":
                    input_name=ib.get_input_text()
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_click():
                    if bt.text=="确认修改":
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                        elif input_name=="":
                            self.info=Info.append_info(self.info,"新名字不能为空！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                        elif input_name in self.users_data:
                            self.info=Info.append_info(self.info,"该名字已被使用！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                            break
                        elif self.encrypt_password(input_psw)!=self.users_data[self.user_name]["password"]:
                            self.info=Info.append_info(self.info,"密码错误！",self.info_pos,color="red",back_color=None)
                            bt.is_click=False
                        else:
                            running=False
            pg.display.update()
            clock.tick(60)
        data=self.users_data[self.user_name]
        self.users_data.pop(self.user_name)
        self.users_data[input_name]=data
        if self.data["last_rem_user"]==self.user_name:
            self.data["last_rem_user"]=input_name
        self.user_name=input_name
        self.update_data()
        self.info=Info.append_info(self.info,"名字修改成功！",self.info_pos,color="green",time=1,back_color=None)
        while len(self.info)>0:
            self.game.event_handle()
            self.info.update()
            self.draw()
            clock.tick(60)
            pg.display.update()
        self.main()
    def danger_operation(self):
        cmd=""
        input_psw=""
        self.info=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.inputbox=pg.sprite.Group()
        button2=pg.sprite.Group()
        self.init_button()
        self.button.add(Button((50,70),250,50,"red",text="注销"))
        self.button.add(Button((50,130),250,50,"red",text="清除账号成绩"))
        running=True
        while running:
            events=self.game.event_handle()
            self.info.update()
            self.button.update(events)
            self.inputbox.update(events)
            button2.update(events)
            if self.handle_button():
                return
            for bt in self.button:
                if bt.check_click():
                    self.inputbox.empty()
                    self.inputbox.add(InputBox(310,70,250,50,"white","black","密码：",is_selected=True,multiple_inputs=True,hidden_string=True))
                    button2.empty()
                    button2.add(Button((310,130),250,50,"blue",text=f"确认操作"))
                    cmd=bt.text
            for bt in button2:
                if bt.check_click():
                    if bt.rect.y==130:
                        if input_psw=="":
                            self.info=Info.append_info(self.info,"密码不能为空！",[570,70],color="red",back_color=None)
                        elif self.encrypt_password(input_psw)!=self.users_data[self.user_name]["password"]:
                            self.info=Info.append_info(self.info,"密码错误！",[570,70],color="red",back_color=None)
                        else:
                            button2.add(Button((310,190),250,50,"red",text=f"二次确定进行操作"))
                    else:
                        running=False
            for ib in self.inputbox:
                if ib.tip=="密码：" and ib.get_input_text()!=input_psw:
                    input_psw=ib.get_input_text()
                    button2.empty()
                    button2.add(Button((310,130),250,50,"blue",text=f"确认操作"))
            self.draw()
            button2.draw(window)
            pg.display.update()
            clock.tick(60)
        self.info=Info.append_info(self.info,f"操作成功！",[570,70],color="green",time=1,back_color=None)
        while len(self.info)>0:
            self.game.event_handle()
            self.info.update()
            self.draw()
            button2.draw(window)
            clock.tick(60)
            pg.display.update()
        if cmd=="注销":
            self.users_data.pop(self.user_name)
            self.user_name=""
            self.save_data()
            self.start()
            self.game.is_restart=True
        elif cmd=="清除账号成绩":
            self.users_data[self.user_name]["best_time"]=0
            self.users_data[self.user_name]["best_minutes"]=0
            self.users_data[self.user_name]["best_seconds"]=0
            self.users_data[self.user_name]["best_version"]="Unknown"
            self.save_data()
            self.get_user_data()