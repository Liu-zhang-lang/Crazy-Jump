import pygame as pg
from subs.const import *
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game=game
        self.pw=30
        self.ph=60
        self.image=pg.Surface((self.pw,self.ph))
        pg.draw.rect(self.image,"blue",(0,0,self.pw,self.ph))
        self.rect=pg.rect.Rect(w/2-self.pw/2,300,self.pw,self.ph)
        self.velocity_y=0
        self.jumping=2 #剩余跳跃次数
        self.jumping_cd=0 #跳跃冷却时间
        self.jump_cnt=0 #跳跃次数
        self.touch_head_achiev_cd=0
        self.last_move_dis=0 #上一次x坐标移动距离
        self.last_move_dir="" #上一次移动方向
        self.stop_move_time=0 #停止移动时间
    def update(self):
        if self.stop_move_time>0:
            self.stop_move_time-=1/60
        if self.touch_head_achiev_cd>0:
            self.touch_head_achiev_cd-=1/60
        self.last_move_dis=self.rect.x
        keys=pg.key.get_pressed()
        if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.stop_move_time<=0:
            self.rect.x-=5
        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.stop_move_time<=0:
            self.rect.x+=5
        if self.rect.x<0:
            self.rect.x=0
        if self.rect.x+self.pw>w:
            self.rect.x=w-self.pw
        if (keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]) and self.jumping>0 and self.jumping_cd<=0 and self.stop_move_time<=0:
            self.jumping-=1
            self.jumping_cd=0.3
            self.velocity_y=-14
            self.jump_cnt+=1
        if self.jumping_cd>0:
            self.jumping_cd-=1/60
        self.rect.y+=self.velocity_y
        self.velocity_y+=0.8
        self.last_move_dis=self.rect.x-self.last_move_dis
        if self.last_move_dis>0:
            self.last_move_dir="right"
        elif self.last_move_dis<0:
            self.last_move_dir="left"
        else:
            self.last_move_dir=""
        self.last_move_dis=abs(self.last_move_dis)
    def hurt(self,damage):
        self.game.heart-=damage
        if damage>0:
            self.game.info=Info.append_info(self.game.info,f"HP-{damage}",info_st_pos,"topright",color="red",time=2,max_len=10)
        else:
            self.game.info=Info.append_info(self.game.info,f"HP+{-damage}",info_st_pos,"topright",color="green",time=2,max_len=10)
        return damage
    def touch_floor(self,floor):
        if pg.sprite.collide_rect(self,floor)==False:
            return
        if self.rect.bottom-self.velocity_y<=floor.rect.top:
            self.rect.bottom=floor.rect.top
            self.jumping=2
            self.velocity_y=0
        elif self.rect.top-self.velocity_y>=floor.rect.bottom:
            self.rect.top=floor.rect.bottom
            self.velocity_y=0
            if floor.existence_time<=0.5:
                self.touch_head_achiev_cd=0.3
        elif floor.existence_time<=0.2 and (self.last_move_dir=="" or (self.last_move_dir=="right" and self.rect.left-self.last_move_dis>floor.rect.left) or (self.last_move_dir=="left" and self.rect.right+self.last_move_dis<floor.rect.right)):
            self.rect.bottom=floor.rect.top
            self.jumping=2
            self.velocity_y=0
        elif self.last_move_dir=="right":
            self.rect.right=floor.rect.left
        else:
            self.rect.left=floor.rect.right