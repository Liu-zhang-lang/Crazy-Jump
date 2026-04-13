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
                },
                "set":{
                    "tag":"down",
                    "tip":"设置",
                    "print":"类型",
                    "subs":{
                        "time":{
                            "tag":"run",
                            "tip":"设置时间",
                            "params":[
                                {"type":int,"tip":"分钟"},
                                {"type":int,"tip":"秒"}
                            ],
                            "func":self.set_time
                        },
                        "heart":{
                            "tag":"run",
                            "tip":"设置生命值",
                            "params":[
                                {"type":int,"tip":"生命值"}
                            ],
                            "func":self.set_heart
                        }
                    }
                }
            }
        }
        self.cnt=0
        self.cnts={}
        self.spaces={}
        self.marks={}
        self.help_texts={}
        self.game=game
        self.is_quit=False
        self.mark_img=cn_sm.render(">",True,"green")
        self.info=pg.sprite.Group()
        self.inputbox=pg.sprite.Group()
    def draw(self):
        self.game.draw()
        self.game.drawTexts(gamestop_texts)
        window.blit(gray_img,(0,0))
        self.game.drawTexts(self.help_texts)
        self.info.draw(window)
        self.inputbox.draw(window)
        for mark in self.marks.values():
            window.blit(self.mark_img,(mark[0],mark[1]))
    def start(self):
        self.start_help()
        window.blit(gray_img,(0,0))
        self.game.drawTexts(self.help_texts)
        while not self.is_quit:
            self.marks={}
            self.exec_node(self.commands_tree)
        self.game.draw()
        self.game.drawTexts(gamestop_texts)
        pg.display.update()
    def check_type(self,type_name,data):
        try:
            type_name(data)
            return True
        except:
            return False
    def exec_node(self,node):
        if node["tag"]=="down":
            self.inputbox.add(InputBox(50,50,200,50,"white","black",node["print"]+":",is_selected=True))
            running=True
            last_info_size=-1
            while running:
                events=self.game.eventHandle()
                self.info.update()
                self.inputbox.update(events)
                if len(self.info)!=last_info_size:
                    self.draw()
                self.inputbox.draw(window)
                last_info_size=len(self.info)
                pg.display.update()
                for ib in self.inputbox:
                    if ib.check_finished():
                        cmd=ib.get_input_text()
                        ib.kill()
                        running=False
                        break
                clock.tick(60)
            if cmd in node["subs"]:
                window.blit(self.mark_img,(257+self.spaces[cmd],50+self.cnts[cmd]*30))
                self.marks[cmd]=[257+self.spaces[cmd],50+self.cnts[cmd]*30]
                pg.display.update()
                self.exec_node(node["subs"][cmd])
            else:
                self.info=Info.append_info(self.info,node["print"]+"不存在！",[50,110],font=cn_sm,color="red")
        elif node["tag"]=="run":
            data=[]
            for lst in node["params"]:
                typ=lst["type"]
                tip=lst["tip"]
                self.inputbox.add(InputBox(50,50,200,50,"white","black",tip+":",is_selected=True))
                running=True
                last_info_size=-1
                text=""
                while running:
                    events=self.game.eventHandle()
                    self.info.update()
                    self.inputbox.update(events)
                    if len(self.info)!=last_info_size:
                        self.draw()
                    self.inputbox.draw(window)
                    last_info_size=len(self.info)
                    pg.display.update()
                    for ib in self.inputbox:
                        if ib.check_finished():
                            text=ib.get_input_text()
                            ib.kill()
                            running=False
                            break
                    clock.tick(60)
                if self.check_type(typ,text):
                    data.append(typ(text))
                else:
                    self.info=Info.append_info(self.info,"数据类型错误！",[50,110],font=cn_sm,color="red")
                    return
            try:
                node["func"](*data)
                self.info=Info.append_info(self.info,"成功！",[50,110],font=cn_sm,color="green")
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
    def set_time(self,m,s):
        self.game.time=m*60+s
        self.game.minutes=m
        self.game.seconds=s
        for i in range(len(level_up_time)):
            l=level_up_time[i][0]
            if i<len(level_up_time)-1:
                n=level_up_time[i+1][0]
            else:
                n=114514
            if self.game.time>=l and self.game.time<n:
                self.game.level=i+2
                self.game.pro=all_pro[i]
                self.game.hpro=all_hpro[i]
                self.game.fpro=all_fpro[i]
                self.game.rpro=all_rpro[i]
                break
    def set_heart(self,h):
        self.game.heart=h
    def start_help(self):
        self.cnt=-1
        for sub in self.commands_tree["subs"]:
            self.get_help_texts(self.commands_tree["subs"][sub],"",sub)
        self.game.drawTexts(self.help_texts)
    def get_help_texts(self,node,space,name):
        self.cnt+=1
        self.cnts[name]=self.cnt
        self.spaces[name]=cn_sm.size(space)[0]
        if node["tag"]=="down":
            text=space+"- "+name+"["+node["tip"]+"]"
            self.help_texts[text]=[(270,self.cnt*30+50),cn_sm,"white"]
            for sub in node["subs"]:
               self.get_help_texts(node["subs"][sub],space+"  ",sub)
        elif node["tag"]=="run":
            text=space+"- "+name+"["+node["tip"]+"]"
            for lst in node["params"]:
                text+="+"+lst["tip"]
            self.help_texts[text]=[(270,self.cnt*30+50),cn_sm,"white"]