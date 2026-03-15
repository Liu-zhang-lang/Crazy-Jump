import pygame as pg
import sys
from const import *
from drawText import DrawText
def Rules():
    texts={
        "游戏规则&玩法：":[(50,70),chinese_font,"white"],
        "使用左右键或AD键进行左右移动，空格键、W键或上键进行跳跃":[(0,35),chinese_font,"white",2],
        "按下Esc暂停游戏，按下Esc或Enter继续":[(0,35),chinese_font,"white",2],
        "躲避红色/紫色(加强)敌人和天空中的雨水":[(0,35),chinese_font,"white",2],
        "拾取绿色/黄色(加强)血包":[(0,35),chinese_font,"white",2],
        "输入法为中文时，可能会导致部分按键失效":[(0,35),chinese_font,"white",2],
        "按两次跳跃可以二段跳":[(0,35),chinese_font,"white",2],
        "地图中会随机生成地板，可供站立3秒":[(0,35),chinese_font,"white",2],
        "在暂停模式下，按下L查看规则":[(0,35),chinese_font,"white",2],
        "阅读完毕后，按下Enter键退出规则页面":[(0,35),chinese_font,"white",2]
    }
    DrawText(texts)
    pg.display.update()
    while True:
        for ev in pg.event.get():
            if ev.type==pg.QUIT:
                pg.quit()
                sys.exit(0)
        keys=pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            break
        clock.tick(60)