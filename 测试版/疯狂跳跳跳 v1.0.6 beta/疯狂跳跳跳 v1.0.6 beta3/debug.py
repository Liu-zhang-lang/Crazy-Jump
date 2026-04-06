from enemy import Enemy
from health import Health
from player import Player
from floor import Floor
from rain import Rain
class Debug:
    def __init__(self,game):
        self.game=game
        self.is_quit=False
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
                "help":{
                    "tag":"run",
                    "tip":"帮助",
                    "params":[],
                    "func":self.start_help
                }
            }
        }
    def start(self):
        while not self.is_quit:
            self.exec_node(self.commands_tree)
    def check_type(self,type_name,data):
        try:
            type_name(data)
            return True
        except:
            return False
    def exec_node(self,node):
        if node["tag"]=="down":
            cmd=input("> "+node["print"]+"：")
            if cmd in node["subs"]:
                self.exec_node(node["subs"][cmd])
            else:
                print("命令不存在！")
        elif node["tag"]=="run":
            data=[]
            for lst in node["params"]:
                typ=lst["type"]
                tip=lst["print"]
                t=input("> "+tip+"：")
                if self.check_type(typ,t):
                    data.append(typ(t))
                else:
                    print("数据类型错误！")
                    return
            try:
                node["func"](*data)
                print("成功！")
            except TypeError:
                print("[error:Debug,exec_node]数据类型错误")
            except NameError:
                print("[error:Debug,exec_node]函数不存在")
            except:
                print("[error:Debug,exec_node]未知错误/help内部错误")
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
        for sub in self.commands_tree["subs"]:
            self.help(self.commands_tree["subs"][sub],"",sub)
    def help(self,node,space,name):
        if node["tag"]=="down":
            print(space+"- "+name+"["+node["tip"]+"]")
            for sub in node["subs"]:
                self.help(node["subs"][sub],space+"  ",sub)
        elif node["tag"]=="run":
            print(space+"- "+name+"["+node["tip"]+"]",end="")
            for lst in node["params"]:
                print("+"+lst["tip"],end="")
            print()