import pygame as pg
import copy
from enemy import Enemy
from health import Health
from info import Info
from floor import Floor
from rain import Rain
from inputBox import InputBox
from button import Button
from const import *
class Debug:
    def __init__(self,game):
        self.commands_tree={
            "tag":"down",
            "tip":"输入命令",
            "print":"命令",
            "nor_val":"quit",
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
                                {"type":int,"tip":"个数","range":(0,inf),"nor_val":1}
                            ],
                            "func":self.spawn_enemy
                        },
                        "nor_enemy":{
                            "tag":"run",
                            "tip":"生成普通敌人",
                            "params":[
                                {"type":int,"tip":"个数","range":(0,inf),"nor_val":1}
                            ],
                            "func":self.spawn_nor_enemy
                        },
                        "super_enemy":{
                            "tag":"run",
                            "tip":"生成超级敌人",
                            "params":[
                                {"type":int,"tip":"个数","range":(0,inf),"nor_val":1}
                            ],
                            "func":self.spawn_super_enemy
                        },
                        "health":{
                            "tag":"run",
                            "tip":"生成(随机)血包",
                            "params":[
                                {"type":int,"tip":"个数","range":(0,inf),"nor_val":1},
                                {"type":int,"tip":"x坐标","range":(-1,w),"nor_val":-1},
                                {"type":int,"tip":"y坐标","range":(-1,h),"nor_val":-1},
                                {"type":int,"tip":"加血量","range":(-1,inf),"nor_val":-1}
                            ],
                            "func":self.spawn_health
                        },
                        "nor_health":{
                            "tag":"run",
                            "tip":"生成普通血包",
                            "params":[
                                {"type":int,"tip":"个数","range":(0,inf),"nor_val":1},
                                {"type":int,"tip":"x坐标","range":(-1,w),"nor_val":-1},
                                {"type":int,"tip":"y坐标","range":(-1,h),"nor_val":-1},
                                {"type":int,"tip":"加血量","range":(-1,inf),"nor_val":-1}
                            ],
                            "func":self.spawn_nor_health
                        },
                        "super_health":{
                            "tag":"run",
                            "tip":"生成超级血包",
                            "params":[
                                {"type":int,"tip":"个数","range":(0,inf),"nor_val":1},
                                {"type":int,"tip":"x坐标","range":(-1,w),"nor_val":-1},
                                {"type":int,"tip":"y坐标","range":(-1,h),"nor_val":-1},
                                {"type":int,"tip":"加血量","range":(-1,inf),"nor_val":-1}
                            ],
                            "func":self.spawn_super_health
                        },
                        "rain":{
                            "tag":"run",
                            "tip":"生成雨",
                            "params":[
                                {"type":int,"tip":"个数","range":(0,inf),"nor_val":1},
                                {"type":int,"tip":"长度","range":(-1,inf),"nor_val":-1}
                            ],
                            "func":self.spawn_rain
                        },
                        "floor":{
                            "tag":"run",
                            "tip":"生成地面",
                            "params":[
                                {"type":int,"tip":"个数","range":(0,inf),"nor_val":1},
                                {"type":int,"tip":"x坐标","range":(-1,w),"nor_val":-1},
                                {"type":int,"tip":"y坐标","range":(-1,h),"nor_val":-1},
                                {"type":int,"tip":"长度","range":(-1,inf),"nor_val":-1}
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
                                {"type":int,"tip":"分钟","range":(0,inf),"nor_val":0},
                                {"type":int,"tip":"秒","range":(0,59.99),"nor_val":0}
                            ],
                            "func":self.set_time
                        },
                        "heart":{
                            "tag":"run",
                            "tip":"设置生命值",
                            "params":[
                                {"type":int,"tip":"生命值","range":(0,inf),"nor_val":0}
                            ],
                            "func":self.set_heart
                        }
                    }
                },
                "clear":{
                    "tag":"down",
                    "tip":"清除",
                    "print":"类型",
                    "subs":{
                        "enemy":{
                            "tag":"run",
                            "tip":"清除敌人",
                            "params":[],
                            "func":self.clear_enemy
                        },
                        "health":{
                            "tag":"run",
                            "tip":"清除血包",
                            "params":[],
                            "func":self.clear_health
                        },
                        "rain":{
                            "tag":"run",
                            "tip":"清除雨",
                            "params":[],
                            "func":self.clear_rain
                        },
                        "floor":{
                            "tag":"run",
                            "tip":"清除地面(不含平台)",
                            "params":[],
                            "func":self.clear_floor
                        },
                    }
                }
            }
        }
        self.cnt=0
        self.max_page=0
        self.pos={}
        self.spaces={}
        self.button=pg.sprite.Group()
        self.button.add(Button([270,480],50,30,"blue",text="<-"))
        self.button.add(Button([720,480],50,30,"blue",text="->"))
        self.help_texts=[]
        self.marks=[]
        for i in range(20):
            self.help_texts.append(pg.sprite.Group())
            self.marks.append({})
        self.backup_marks=copy.deepcopy(self.marks)
        self.help_index=0
        self.help_len=0
        self.game=game
        self.is_quit=False
        self.mark_img=cn_fonts[18].render(">",True,"green")
        for _ in range(8):
            self.mark_img.blit(self.mark_img,(0,0))
        self.page_img=cn_def.render(f"页数：{self.help_index+1}/{self.max_page}",True,"white")
        self.info=pg.sprite.Group()
        self.inputbox=pg.sprite.Group()
        self.tips=pg.sprite.Group()
        font=cn_fonts[17]
        self.tips=Info.append_info(self.tips,"小贴士：",[270,520],font=font,back_color=None,mode="back")
        self.tips=Info.append_info(self.tips,"若参数有默认值，按下Enter则视为输入默认值",[270,520],font=font,back_color=None,mode="back")
        self.tips=Info.append_info(self.tips,"若输入的参数(个数除外)为-1，则随机取一个正常范围内的数",[270,520],font=font,back_color=None,mode="back")
    def draw(self):
        self.page_img=cn_def.render(f"页数：{self.help_index+1}/{self.max_page}",True,"white")
        self.game.draw()
        window.blit(gray_img,(0,0))
        self.help_texts[self.help_index].draw(window)
        window.blit(self.page_img,self.page_img.get_rect(center=(520,495)))
        self.info.draw(window)
        self.inputbox.draw(window)
        self.button.draw(window)
        self.tips.draw(window)
        for mark in self.marks[self.help_index].values():
            window.blit(self.mark_img,(mark[0],mark[1]))
    def start(self):
        self.start_help()
        while not self.is_quit:
            self.marks=copy.deepcopy(self.backup_marks)
            self.exec_node(self.commands_tree,"")
        self.game.draw()
        pg.display.update()
    def handle_button(self):
        for bt in self.button:
            if bt.check_click():
                if bt.text=="<-" and self.help_index>0:
                    self.help_index-=1
                    self.draw()
                    self.help_texts[self.help_index].draw(window)
                elif bt.text=="->" and self.help_index<self.help_len-1:
                    self.help_index+=1
                    self.draw()
                    self.help_texts[self.help_index].draw(window)
    def check_type(self,type_name,data):
        try:
            type_name(data)
            return True
        except:
            return False
    def exec_node(self,node,path):
        if node["tag"]=="down":
            if "nor_val" in node:
                self.inputbox.add(InputBox(50,50,200,50,"white","black",node["print"]+":(默认为"+node["nor_val"]+")",tip_font=cn_sm,is_selected=True))
            else:
                self.inputbox.add(InputBox(50,50,200,50,"white","black",node["print"],is_selected=True,tip_font=cn_sm))
            running=True
            while running:
                events=self.game.event_handle()
                self.info.update()
                self.inputbox.update(events)
                self.button.update(events)
                self.handle_button()
                self.draw()
                pg.display.update()
                for ib in self.inputbox:
                    if ib.check_finished():
                        cmd=ib.get_input_text()
                        ib.kill()
                        running=False
                        break
                clock.tick(60)
            if cmd=="" and "nor_val" in node:
                cmd=node["nor_val"]
            if cmd in node["subs"]:
                path2=path+cmd+"/"
                self.marks[self.pos[path2][0]-1][path2]=[257+self.spaces[path2],50+(self.pos[path2][1]-1)*(cn_fonts_sz[18]+5)]
                self.exec_node(node["subs"][cmd],path2)
            elif cmd=="Liu_zhang_lang" and node["tip"]=="输入命令":
                self.spawn_nor_health(22222,w/2-200,h/2,1)
                self.info=Info.append_info(self.info,"诶？怎么多了一个血包？",[50,110],font=cn_sm,color="green",back_color=None)
            else:
                self.info=Info.append_info(self.info,node["print"]+"不存在！",[50,110],font=cn_sm,color="red",back_color=None)
        elif node["tag"]=="run":
            data=[]
            for lst in node["params"]:
                typ=lst["type"]
                tip=lst["tip"]
                range=lst["range"]
                nor_val=lst["nor_val"]
                self.inputbox.add(InputBox(50,50,200,50,"white","black",tip+":(默认为"+str(nor_val)+")",is_selected=True,tip_font=cn_sm))
                running=True
                text=""
                while running:
                    events=self.game.event_handle()
                    self.info.update()
                    self.inputbox.update(events)
                    self.button.update(events)
                    self.handle_button()
                    self.draw()
                    pg.display.update()
                    for ib in self.inputbox:
                        if ib.check_finished():
                            text=ib.get_input_text()
                            ib.kill()
                            running=False
                            break
                    clock.tick(60)
                if text=="":
                    text=nor_val
                if not self.check_type(typ,text):
                    self.info=Info.append_info(self.info,"数据类型错误！",[50,110],font=cn_sm,color="red",back_color=None)
                    return
                elif not (typ(text)>=range[0] and typ(text)<=range[1]):
                    self.info=Info.append_info(self.info,"数据不在范围内！",[50,110],font=cn_sm,color="red",back_color=None)
                    return
                else:
                    data.append(typ(text))
            try:
                node["func"](*data)
                self.info=Info.append_info(self.info,"成功！",[50,110],font=cn_sm,color="green",back_color=None)
                if node["tip"]!="退出debug模式":
                    self.game.game_stats["debug"]["cnt"]+=1
                self.game.is_debug=True
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
            self.game.enemy.add(Enemy(0,draw_num=self.game.user.settings["enemy_show"]))
    def spawn_nor_enemy(self,n):
        for i in range(n):
            self.game.enemy.add(Enemy(1,draw_num=self.game.user.settings["enemy_show"]))
    def spawn_super_enemy(self,n):
        for i in range(n):
            self.game.enemy.add(Enemy(2,draw_num=self.game.user.settings["enemy_show"]))
    def spawn_health(self,n,x,y,h):
        for i in range(n):
            self.game.health.add(Health(0,x,y,h,draw_num=self.game.user.settings["health_show"]))
    def spawn_nor_health(self,n,x,y,h):
        for i in range(n):
            self.game.health.add(Health(1,x,y,h,draw_num=self.game.user.settings["health_show"]))
    def spawn_super_health(self,n,x,y,h):
        for i in range(n):
            self.game.health.add(Health(2,x,y,h,draw_num=self.game.user.settings["health_show"]))
    def spawn_rain(self,l,n):
        for i in range(n):
            self.game.rain.add(Rain(l,draw_num=self.game.user.settings["rain_show"]))
    def spawn_floor(self,x,y,l,n):
        for i in range(n):
            self.game.floor.add(Floor(x,y,l))
    def god(self):
        self.game.god_mode=not self.game.god_mode
    def quit(self):
        self.is_quit=True
    def clear_enemy(self):
        self.game.enemy.empty()
    def clear_health(self):
        self.game.health.empty()
    def clear_rain(self):
        self.game.rain.empty()
    def clear_floor(self):
        self.game.floor.empty()
        self.game.floor.add(Floor(0,500,w,-1))
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
        self.cnt=0
        for sub in self.commands_tree["subs"]:
            self.get_help_texts(self.commands_tree["subs"][sub],"",sub,"")
        self.help_len=int((self.cnt+17)/18)
    def get_help_texts(self,node,space,name,path):
        self.cnt+=1
        page=int((self.cnt+17)/18)
        self.max_page=max(self.max_page,page)
        self.pos[path+name+"/"]=[page,(self.cnt-1)%18+1]
        self.spaces[path+name+"/"]=cn_fonts[18].size(space)[0]
        if node["tag"]=="down":
            text=space+"- "+name+"["+node["tip"]+"]"
            self.help_texts[page-1]=Info.append_info(self.help_texts[page-1],text,[270,50],font=cn_fonts[18],back_color=None,spacing=5,mode="back")
            for sub in node["subs"]:
               self.get_help_texts(node["subs"][sub],space+"  ",sub,path+name+"/")
        elif node["tag"]=="run":
            text=space+"- "+name+"["+node["tip"]+"]"
            for lst in node["params"]:
                text+="+"+lst["tip"]
            self.help_texts[page-1]=Info.append_info(self.help_texts[page-1],text,[270,50],font=cn_fonts[18],back_color=None,spacing=5,mode="back")
