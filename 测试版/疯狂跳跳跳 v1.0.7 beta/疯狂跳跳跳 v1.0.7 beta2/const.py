import pygame as pg
import os
import inspect as ins
pg.init()
w,h=800,600
level_up_time=[
    [15,17],
    [30,32],
    [45,47],
    [70,72],
    [90,92]
]
all_pro=[
    0.008,
    0.016,
    0.032,
    0.045,
    0.052
]
all_hpro=[
    0.0015,
    0.003,
    0.004,
    0.006,
    0.007
]
all_fpro=[
    0.0005,
    0.001,
    0.00125,
    0.0014,
    0.0017
]
all_rpro=[
    0,
    0.002,
    0.004,
    0.01,
    0.03
]
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
for i in range(1,100):
    cn_fonts.append(pg.font.Font(font_file,i))
    cn_fonts_sz.append(i)
info_st_pos=(w,cn_def_sz*3)
gray_img=pg.Surface((w,h),pg.SRCALPHA)
gray_img.fill((128,128,128,200))
is_info=False
for s in ins.stack()[::-1]:
    if os.path.basename(s.filename)=="info.py":
        is_info=True
        break
if not is_info:
    from info import Info
    fst_pos=[w/2,h/2-80]
    gamestop_info=pg.sprite.Group()
    gamestop_info=Info.append_info(gamestop_info,"游戏暂停",fst_pos,"center",cn_big,time=-1,spacing=5,mode="back")
    gamestop_info=Info.append_info(gamestop_info,"按Esc或Enter继续游戏",fst_pos,"center",time=-1,spacing=5,mode="back")
    gamestop_info=Info.append_info(gamestop_info,"按R重新开始",fst_pos,"center",time=-1,spacing=5,mode="back")
    gamestop_info=Info.append_info(gamestop_info,"按G查看规则",fst_pos,"center",time=-1,spacing=5,mode="back")
    gamestop_info=Info.append_info(gamestop_info,"按P查看排行榜",fst_pos,"center",time=-1,spacing=5,mode="back")
    gamestop_info=Info.append_info(gamestop_info,"按U进入账号页面",fst_pos,"center",time=-1,spacing=5,mode="back")