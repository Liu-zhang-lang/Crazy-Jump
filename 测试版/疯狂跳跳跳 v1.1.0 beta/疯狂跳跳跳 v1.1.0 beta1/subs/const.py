import pygame as pg
import os
import sys
import inspect as ins
import time
pg.init()
version="v1.1.0 beta1"
format=3
w,h=800,600
level_up_time=[
    [-1,-1],
    [15,17],
    [30,32],
    [45,47],
    [70,72],
    [90,92],
    [150,152],
    [210,212]
]
all_pro=[
    0.004,
    0.008,
    0.016,
    0.028,
    0.037,
    0.043,
    0.056,
    0.04
]
all_hpro=[
    0.0015,
    0.0015,
    0.0025,
    0.0035,
    0.0055,
    0.0065,
    0.007,
    0.0075
]
all_fpro=[
    0.0001,
    0.0005,
    0.001,
    0.0012,
    0.0013,
    0.0016,
    0.0017,
    0.0017
]
all_rpro=[
    0,
    0,
    0.002,
    0.005,
    0.011,
    0.02,
    0.039,
    0.025
]
inf=0x3f3f3f3f3f3f3f3f
clock=pg.time.Clock()
window=pg.display.set_mode((w,h))
font_file=os.path.join(os.path.dirname(__file__),"fonts","simsun.ttc") #加载字体
cn_sm=pg.font.Font(font_file,20)
cn_sm_sz=20
cn_def=pg.font.Font(font_file,25)
cn_def_sz=25
cn_big=pg.font.Font(font_file,45)
cn_big_sz=45
cn_fonts=[]
cn_fonts_sz=[]
def_settings={
    "enemy_show": False,
    "health_show": False,
    "rain_show": False,
    "bullet_show": False,
    "safe_restart": True
}
for i in range(1,100):
    cn_fonts.append(pg.font.Font(font_file,i))
    cn_fonts_sz.append(i)
info_st_pos=(w,cn_def_sz*3)
gray_img=pg.Surface((w,h),pg.SRCALPHA)
gray_img.fill((128,128,128,220))
slogans=[
    "疯狂跳跳跳！",
    "这怪怎么会变向？？？",
    "Ohhhhhhhhhh！",
    "主页按Enter也可以开始游戏哦！",
    "Do you know chinglish？",
    "我爱C++！",
    "MC真好玩！",
    "猜猜你多久才能再次看到这个标语？",
    "这什么逆天bug？",
    "Hello World!",
    "x=x+2,x=-1？",
    "3m=2m,3m/m=2m/m,3=2？",
    "这土豆长得好像马铃薯啊！",
    'if(false) cout<<"世界已毁灭";',
    "well的中文：井",
    "super idol的笑容~",
    "我不想上学……",
    "《证明1+1=2的100种方法》",
    "咕咕嘎嘎！",
    "我去，怎么有蟑螂？？？",
    "加油，奥里给！",
    "阿巴阿巴……",
    "哦→哎↘哦→饿→↗啊↘~",
    "善用暂停键，可以坚持得更久",
    "也试一试chest in the maps！",
    "蟑螂出品，必属精品！",
    "请输入文本",
    "Happy every day!",
    "这游戏有Boss？真的假的？",
    "雨天路滑，小心慢行",
    "(ErRo$}闪@乐%吾#裁^失拜?",
    "你的血包已送达，请及时签收",
    "本次更新增加了一些bug",
    "Delay no more!"
]
error_msg=[]
error_msg_all=[]
error_msg_map={}
is_info=False
for s in ins.stack()[::-1]:
    if os.path.basename(s.filename)=="info.py":
        is_info=True
        break
def add_error(msg):
    if msg in error_msg_map:
        error_msg_map[msg]+=1
        return
    error_msg_map[msg]=1
    error_msg_all.append(msg)
    error_msg.append(msg)
    print(msg)
if not is_info:
    from subs.info import Info
    fst_pos=[w/2,h/2-60]
    gamestop_info=pg.sprite.Group()
    gamestop_info=Info.append_info(gamestop_info,"游戏暂停",fst_pos,"center",cn_big,time=-1,spacing=5,mode="back")
    gamestop_info=Info.append_info(gamestop_info,"按Esc或Enter继续游戏",fst_pos,"center",time=-1,spacing=5,mode="back")
    gamestop_info=Info.append_info(gamestop_info,"按R重新开始",fst_pos,"center",time=-1,spacing=5,mode="back")
    gamestop_info=Info.append_info(gamestop_info,"按G查看规则",fst_pos,"center",time=-1,spacing=5,mode="back")
def quit_game():
    if len(error_msg_all)>0:
        print("本次运行发生了错误：")
        for msg in error_msg_all:
            print(msg)
        print("错误文件已保存至D:\\Crazy-Jump\\error.txt")
        os.makedirs("D:\\Crazy-Jump",exist_ok=True)
        if not os.path.exists("D:\\Crazy-Jump\\error.txt"):
            with open("D:\\Crazy-Jump\\error.txt","w",encoding="utf-8") as f:
                pass
        with open("D:\\Crazy-Jump\\error.txt","a",encoding="utf-8") as f:
            f.write("-----------------------------\n")
            f.write("游戏版本："+version+"\n")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"\n")
            for msg in error_msg_all:
                f.write(msg+"（"+str(error_msg_map[msg])+"次）\n")
    print("游戏退出！")
    pg.quit()
    sys.exit(0)