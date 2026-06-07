import pygame as pg
import copy
from subs.button import Button
from subs.info import Info
from subs.const import *
class GameStats:
    def __init__(self,game):
        self.game=game
        self.game_stats={
            "name":"虚拟节点",
            "cnt":0,
            "sum":0,
            "subs":{
                "jump":{
                    "name":"跳跃",
                    "cnt":0
                },
                "hurt":{
                    "name":"受伤",
                    "cnt":0,
                    "sum":0,
                    "subs":{
                        "nor_enemy":{
                            "name":"普通敌人",
                            "cnt":0,
                            "sum":0
                        },
                        "super_enemy":{
                            "name":"超级敌人",
                            "cnt":0,
                            "sum":0
                        },
                        "rain":{
                            "name":"雨",
                            "cnt":0,
                            "sum":0
                        }
                    }
                },
                "health":{
                    "name":"回血",
                    "cnt":0,
                    "sum":0,
                    "subs":{   
                        "nor_health":{
                            "name":"普通血包",
                            "cnt":0,
                            "sum":0
                        },
                        "super_health":{
                            "name":"超级血包",
                            "cnt":0,
                            "sum":0
                        }
                    }
                },
                "touch_floor":{
                    "name":"触碰地板",
                    "cnt":0
                },
                "debug":{
                    "name":"使用调试",
                    "cnt":0
                }
            }
        }
        self.maxline=13
        self.maxpage=1
        self.stats_info=[pg.sprite.Group() for _ in range(100)]
        self.stats_info_backup=copy.deepcopy(self.stats_info)
        self.cnt=0
    def copy_stats(self):
        return copy.deepcopy(self.game_stats["subs"])
    def get_stats_info(self,node,space):
        self.cnt+=1
        page=int((self.cnt+self.maxline-1)/self.maxline)
        self.maxpage=max(self.maxpage,page)
        text=space+"- "+node["name"]+"：次数="+str(node["cnt"])
        if "sum" in node:
            text+=f"，总和={node["sum"]}"
        self.stats_info[page-1]=Info.append_info(self.stats_info[page-1],text,[50,80],back_color=None,spacing=5,mode="back")
        if "subs" in node:
            for sub in node["subs"]:
                self.get_stats_info(node["subs"][sub],space+"  ")
    def menu(self):
        button=pg.sprite.Group()
        button.add(Button((w-30,30),30,30,"blue",align="topright",text="×"))
        button.add(Button((50,550),30,30,"blue",align="topleft",text="<-"))
        button.add(Button((w-50,550),30,30,"blue",align="topright",text="->"))
        index=0 
        self.stats_info=copy.deepcopy(self.stats_info_backup)
        self.cnt=0
        for s in self.game_stats["subs"]:
            self.get_stats_info(self.game_stats["subs"][s],"")
        for i in range(0,self.maxpage):
            self.stats_info[i]=Info.add_info(self.stats_info[i],"统计信息",[w/2,50],align="center",font=cn_big,color="white",back_color=None,time=-1)
        while True:
            events=self.game.event_handle()
            button.update(events)
            self.game.draw()
            window.blit(gray_img,(0,0))
            self.stats_info[index].draw(window)
            button.draw(window)
            img=cn_def.render(f"第{index+1}/{self.maxpage}页",True,"white")
            window.blit(img,img.get_rect(center=(w/2,565)))
            for bt in button:
                if bt.check_click():
                    if bt.text=="<-":
                        if index>0:
                            index-=1
                    elif bt.text=="->":
                        if index<self.maxpage-1:
                            index+=1
                    elif bt.text=="×":
                        return
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_LEFT:
                        if index>0:
                            index-=1
                    elif ev.key==pg.K_RIGHT:
                        if index<self.maxpage-1:
                            index+=1
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_ESCAPE:
                        return
            pg.display.update()
            clock.tick(60)
    def add(self,path,cnt,sum=None,tree=None,first=True):
        if tree==None:
            tree=self.game_stats
        if path=="" or path=="/":
            tree["cnt"]+=cnt
            if sum!=None:
                tree["sum"]+=sum
            return tree
        if path[0]=="/":
            path=path[1:]
        if path[len(path)-1]!="/":
            path=path+"/"
        next=path.split("/")[0]
        path=path.split("/",1)[1]
        if "subs" not in tree:
            add_error(f"[error:GameStats,add]未找到路径{path}(未找到\"subs\"参数)")
        if next in tree["subs"]:
            tree["subs"][next]=self.add(path,cnt,sum=sum,tree=tree["subs"][next],first=False)
        else:
            add_error(f"[error:GameStats,add]未找到路径{path}(未找到{next})")
        tree["cnt"]+=cnt
        if sum!=None:
            tree["sum"]+=sum
        if first:
            self.game_stats=tree
        return tree
    def query(self,path,param,tree=None):
        if tree==None:
            tree=self.game_stats
        if path=="" or path=="/":
            if param not in tree:
                add_error(f"[error:GameStats,query]未找到参数{param}")
                return None
            return tree[param]
        if path[0]=="/":
            path=path[1:]
        if path[len(path)-1]!="/":
            path=path+"/"
        next=path.split("/")[0]
        path=path.split("/",1)[1]
        if "subs" not in tree:
            add_error(f"[error:GameStats,query]未找到路径{path}(未找到\"subs\"参数)")
            return None
        if next in tree["subs"]:
            return self.query(path,param,tree["subs"][next])
        else:
            add_error(f"[error:GameStats,query]未找到路径{path}(未找到{next})")
            return None