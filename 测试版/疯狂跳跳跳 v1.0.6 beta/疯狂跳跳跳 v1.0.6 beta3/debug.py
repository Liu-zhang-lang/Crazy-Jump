import pygame as pg
from enemy import Enemy
from health import Health
from info import Info
from floor import Floor
from rain import Rain
from inputBox import InputBox
from const import *
class Debug:
    def __init__(self,game):
        self.commands_tree={
            "tag":"down",
            "tip":"输入命令",
            "print":"命令",
            "subs":{
                "spawn":{
                    "tag":"down",
                    "tip":"生成物体",
                    "print":"类型",
                    "subs":{
                        "enemy":{
                            "tag":"run",
                            "tip":"生成(随机)敌人",
                            "params":[
                                {"type":int,"tip":"个数"}
                            ],
                            "func":self.spawn_enemy
                        },
                        "nor_enemy":{
                            "tag":"run",
                            "tip":"生成普通敌人",
                            "params":[
                                {"type":int,"tip":"个数"}
                            ],
                            "func":self.spawn_nor_enemy
                        },
                        "super_enemy":{
                            "tag":"run",
                            "tip":"生成超级敌人",
                            "params":[
                                {"type":int,"tip":"个数"}
                            ],
                            "func":self.spawn_super_enemy
                        },
                        "health":{
                            "tag":"run",
                            "tip":"生成(随机)血包",
                            "params":[
                                {"type":int,"tip":"个数"}
                            ],
                            "func":self.spawn_health
                        },
                        "nor_health":{
                            "tag":"run",
                            "tip":"生成普通血包",
                            "params":[
                                {"type":int,"tip":"个数"}
                            ],
                            "func":self.spawn_nor_health
                        },
                        "super_health":{
                            "tag":"run",
                            "tip":"生成超级血包",
                            "params":[
                                {"type":int,"tip":"个数"}
                            ],
                            "func":self.spawn_super_health
                        },
                        "rain":{
                            "tag":"run",
                            "tip":"生成雨",
                            "params":[
                                {"type":int,"tip":"长度"},
                                {"type":int,"tip":"个数"}
                            ],
                            "func":self.spawn_rain
                        },
                        "floor":{
                            "tag":"run",
                            "tip":"生成地面",
                            "params":[
                                {"type":int,"tip":"x坐标"},
                                {"type":int,"tip":"y坐标"},
                                {"type":int,"tip":"长度"},
                                {"type":int,"tip":"个数"}
                            ],
                            "func":self.spawn_floor
                        }
                    }
                },
                "god":{
                    "tag":"run",
                    "tip":"无敌与正常模式切换",
                    "params":[],
                    "func":self.god
                },
                "quit":{
                    "tag":"run",
                    "tip":"退出debug模式",
                    "params":[],
                    "func":self.quit
                }
            }
        }
        self.help_texts={}
        self.game=game
        self.is_quit=False
        self.info=pg.sprite.Group()
    def start(self):
        self.start_help()
        self.gray_img=pg.Surface((w,h),pg.SRCALPHA)
        self.gray_img.fill((128,128,128,200))
        window.blit(self.gray_img,(0,0))
        self.game.drawTexts(self.help_texts)
        while not self.is_quit:
            self.exec_node(self.commands_tree)
        self.game.draw()
        self.game.drawTexts(gamestop_texts)
    def check_type(self,type_name,data):
        try:
            type_name(data)
            return True
        except:
            return False
    def exec_node(self,node):
        if node["tag"]=="down":
            inputbox=pg.sprite.Group()
            inputbox.add(InputBox(50,50,200,50,"white","black",node["print"]+":",is_selected=True))
            running=True
            last_info_size=len(self.info)
            while running:
                events=self.game.eventHandle()
                self.info.update()
                self.info.draw(window)
                if len(self.info)!=last_info_size:
                    self.game.draw()
                    self.game.drawTexts(gamestop_texts)
                    window.blit(self.gray_img,(0,0))
                    self.game.drawTexts(self.help_texts)
                last_info_size=len(self.info)
                inputbox.update(events)
                inputbox.draw(window)
                pg.display.update()
                for ib in inputbox:
                    if ib.check_finished():
                        cmd=ib.get_input_text()
                        ib.kill()
                        running=False
                        break
                clock.tick(60)
            if cmd in node["subs"]:
                self.exec_node(node["subs"][cmd])
            else:
                self.info=Info.append_info(self.info,node["print"]+"不存在！",[50,110],font=chinese_font_lit,color="red")
        elif node["tag"]=="run":
            data=[]
            for lst in node["params"]:
                typ=lst["type"]
                tip=lst["tip"]
                inputbox=pg.sprite.Group()
                inputbox.add(InputBox(50,50,200,50,"white","black",tip+":",is_selected=True))
                running=True
                last_info_size=len(self.info)
                text=""
                while running:
                    events=self.game.eventHandle()
                    self.info.update()
                    self.info.draw(window)
                    if len(self.info)!=last_info_size:
                        self.game.draw()
                        self.game.drawTexts(gamestop_texts)
                        window.blit(self.gray_img,(0,0))
                        self.game.drawTexts(self.help_texts)
                    last_info_size=len(self.info)
                    inputbox.update(events)
                    inputbox.draw(window)
                    pg.display.update()
                    for ib in inputbox:
                        if ib.check_finished():
                            text=ib.get_input_text()
                            ib.kill()
                            running=False
                            break
                    clock.tick(60)
                if self.check_type(typ,text):
                    data.append(typ(text))
                else:
                    self.info=Info.append_info(self.info,"数据类型错误！",[50,110],font=chinese_font_lit,color="red")
                    return
            try:
                node["func"](*data)
                self.info=Info.append_info(self.info,"成功！",[50,110],font=chinese_font_lit,color="green")
            except TypeError:
                print("[error:Debug,exec_node]数据类型错误？")
            except NameError:
                print("[error:Debug,exec_node]函数不存在")
            except:
                print(f"[error:Debug,exec_node]未知错误/(提示："+node["tip"]+")内部错误")
        else:
            print("[error:Debug,exec_node]未知的tag")
    def spawn_enemy(self,n):
        for i in range(n):
            self.game.enemy.add(Enemy(0))
    def spawn_nor_enemy(self,n):
        for i in range(n):
            self.game.enemy.add(Enemy(1))
    def spawn_super_enemy(self,n):
        for i in range(n):
            self.game.enemy.add(Enemy(2))
    def spawn_health(self,n):
        for i in range(n):
            self.game.health.add(Health(0))
    def spawn_nor_health(self,n):
        for i in range(n):
            self.game.health.add(Health(1))
    def spawn_super_health(self,n):
        for i in range(n):
            self.game.health.add(Health(2))
    def spawn_rain(self,l,n):
        for i in range(n):
            self.game.rain.add(Rain(l))
    def spawn_floor(self,x,y,l,n):
        for i in range(n):
            self.game.floor.add(Floor(x,y,l))
    def god(self):
        self.game.god_mode=not self.game.god_mode
    def quit(self):
        self.is_quit=True
    def start_help(self):
        self.cnt=-1
        for sub in self.commands_tree["subs"]:
            self.get_help_texts(self.commands_tree["subs"][sub],"",sub)
        self.game.drawTexts(self.help_texts)
    def get_help_texts(self,node,space,name):
        self.cnt+=1
        if node["tag"]=="down":
            text=space+"- "+name+"["+node["tip"]+"]"
            self.help_texts[text]=[(270,self.cnt*30+50),chinese_font_lit,"white"]
            for sub in node["subs"]:
                self.get_help_texts(node["subs"][sub],space+"  ",sub)
        elif node["tag"]=="run":
            text=space+"- "+name+"["+node["tip"]+"]"
            for lst in node["params"]:
                text+="+"+lst["tip"]
            self.help_texts[text]=[(270,self.cnt*30+50),chinese_font_lit,"white"]