import pygame as pg
from subs.button import Button
from subs.info import Info
from subs.const import *
class Changelog:
    def __init__(self,game):
        texts=[
            "【新增/修改/删除内容】",
            "- 新增第八阶段",
            "- 新增boss及其相关debug命令、统计信息",
            "- 新增打破新纪录，击杀boss和使用debug命令的提醒",
            "- 新增图鉴",
            "- 新增特性：游戏中可以打开设置、排行榜等功能",
            "- 新增悬停在按钮上时的边框",
            "- 新增子弹以及其debug命令",
            "- 新增F1按键",
            "- 新增帧率的颜色变化",
            "- 新增chest in the maps链接",
            "- 修改了版本号显示的位置",
            "- 新增了几条闪烁标语",
            "- 新增了更新内容的显示",
            "- 新增成就的难度区分",
            "- 新增普通模式和打Boss模式",
            '- 修改"打破新纪录"成就的检测逻辑',
            "- 修改了一项成就的名字",
            "- 修改了规则",
            "- 让地板的碰撞逻辑更加合理",
            '- 将"难度升级！"改为了"下一阶段!"',
            "- 降低游戏整体难度",
            "- 将生命值改为了HP",
            "- 更新了json文本的格式",
            "- 升级了排行榜",
            "【修复问题】",
            "- 修复了打破新纪录和生存之神成就可能无法获得的bug",
            "- 修复了打破新纪录可能会导致游戏崩溃或无法更新新纪录的bug",
            "- 修复了超级血包无法自定义加血量的bug",
            "- 修复了超级实体变向后统计信息会将其识别成普通实体的bug",
            "- 修复了在主页切换账号点击游戏开始页面错误的bug",
            "- 修复了一个文件名拼写错误的bug",
            "- 修复了修改名字时可能导致界面残留，按钮混乱潜在bug",
            "- 修复了生成floor时floor的位置不符合的bug",
            "- 修复了规则中“按S查看统计信息”应为“按T查看统计信息”的bug",
            "- 修复了输入框的光标位置可能不对应的bug",
            "- 修复了成就[梦开始的地方]可能无法显示的bug",
            "- 修复了debug中使用quit也会被认定为使用了debug的bug",
            "【备注】",
            "- 发布时间：2026/7/11"
        ]
        self.info=[pg.sprite.Group() for _ in range(10)]
        self.game=game
        self.button=pg.sprite.Group()
        self.title=cn_big.render("更新内容",True,"white")
        self.maxline=17
        self.maxpage=int((len(texts)+self.maxline-1)/self.maxline)
        for i,text in enumerate(texts):
            self.info[i//self.maxline]=Info.append_info(self.info[i//self.maxline],text,[50,70],back_color=None,spacing=3,mode="back")
    def init_button(self):
        self.button.empty()
        self.button.add(Button((w-30,30),30,30,"blue",text="×",align="topright"))
    def button_handle(self):
        for bt in self.button:
            if bt.check_click():
                if bt.text=="×":
                    return True
    def draw(self):
        self.game.draw()
        window.blit(gray_img,(0,0))
        window.blit(self.title,self.title.get_rect(center=(w/2,40)))
        self.button.draw(window)
    def menu(self):
        self.init_button()
        self.button.add(Button((50,550),30,30,"blue",align="topleft",text="<-"))
        self.button.add(Button((w-50,550),30,30,"blue",align="topright",text="->"))
        index=0
        while True:
            events=self.game.event_handle()
            self.button.update(events)
            self.draw()
            self.info[index].draw(window)
            img=cn_def.render(f"第{index+1}/{self.maxpage}页",True,"white")
            window.blit(img,img.get_rect(center=(w/2,565)))
            if self.button_handle():
                return
            for bt in self.button:
                if bt.check_click() and bt.rect.y!=30:
                    if bt.text=="<-":
                        if index>0:
                            index-=1
                    elif bt.text=="->":
                        if index<self.maxpage-1:
                            index+=1
            for ev in events:
                if ev.type==pg.KEYDOWN:
                    if ev.key==pg.K_LEFT:
                        if index>0:
                            index-=1
                    elif ev.key==pg.K_RIGHT:
                        if index<self.maxpage-1:
                            index+=1
                    elif ev.key==pg.K_ESCAPE:
                        return True
            pg.display.update()
            clock.tick(60)