import pygame as pg
import random as rd
import math
from subs.bullet import Bullet
from subs.const import *
class Boss(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game=game
        self.b=40
        self.heart=46
        self.image=pg.Surface((self.b,self.b))
        self.recover_cd=7
        self.jumping=2 #剩余跳跃次数
        self.next_jumping_cd=0 #二段跳冷却时间
        self.jumping_cd=0 #跳跃冷却时间
        self.velocity_y=0
        self.hurt_cd=0
        self.change_dir_cd=0
        self.hurt_recover_cd=0
        self.skill_cd=10
        self.skill_cd_tip=False
        self.dir=1 #1:右,-1:左
        self.last_move_dis=0 #上一次移动距离
        self.last_move_dir="" #上一次移动方向
        pg.draw.rect(self.image,"orange",(0,0,self.b,self.b))
        self.is_super=False
        if rd.random()>0.5:
            self.rect=pg.rect.Rect(w,500-self.b,self.b,self.b)
        else:
            self.rect=pg.rect.Rect(-self.b,500-self.b,self.b,self.b)
        self.miny=self.rect.bottom
        self.maxy=self.rect.bottom
        self.boss_img=self.image.copy()
        self.number_text=cn_def.render(str(self.heart),True,"white")
        img_w,img_h=self.number_text.get_size()
        t=min(self.b/img_w,self.b/img_h)
        img_w*=t
        img_h*=t
        img_w=int(img_w)
        img_h=int(img_h)
        self.number_text=pg.transform.scale(self.number_text,(img_w,img_h))
        self.max_hp=46
        self.draw_pic()
    def hurt(self,damage):
        if damage>8:
            damage=8
        if self.heart<=20:
            damage=int(damage*0.6)
        self.heart-=damage
        if self.heart<=0:
            damage+=self.heart
            self.heart=0
            self.game.game_stats.add("kill/boss",1)
            self.game.achiev_info=Info.append_info(self.game.achiev_info,"你击败了boss！",[0,cn_def_sz*2],font=cn_sm,color="gold",max_len=10,time=3,back_color=None)
            self.kill()
            return damage
        self.number_text=cn_def.render(str(int(self.heart)),True,"white")
        img_w,img_h=self.number_text.get_size()
        t=min(self.b/img_w,self.b/img_h)
        img_w*=t
        img_h*=t
        img_w=int(img_w)
        img_h=int(img_h)
        self.number_text=pg.transform.scale(self.number_text,(img_w,img_h))
        self.draw_pic()
        return damage
    def recover(self,hp):
        if self.heart<=10:
            hp*=2
        self.heart+=hp
        if self.heart>self.max_hp:
            self.heart=self.max_hp
        self.number_text=cn_def.render(str(self.heart),True,"white")
        img_w,img_h=self.number_text.get_size()
        t=min(self.b/img_w,self.b/img_h)
        img_w*=t
        img_h*=t
        img_w=int(img_w)
        img_h=int(img_h)
        self.number_text=pg.transform.scale(self.number_text,(img_w,img_h))
        self.draw_pic()
    def draw_pic(self):
        self.image=self.boss_img.copy()
        self.image.blit(self.number_text,self.number_text.get_rect(center=(self.image.get_width()/2,self.image.get_height()/2)))
    def update(self):
        self.recover_cd-=1/60
        self.last_move_dis=self.rect.x
        p=self.game.player.sprites()[0]
        if p.rect.left<self.rect.left:
            if self.dir==-1:
                self.rect.x-=2*rd.uniform(0.9,1.1)
                self.dir=-1
            elif self.change_dir_cd<=0:
                self.change_dir_cd=1.5
                self.dir=-1
        if p.rect.right>self.rect.right:
            if self.dir==1:
                self.rect.x+=2*rd.uniform(0.9,1.1)
                self.dir=1
            elif self.change_dir_cd<=0:
                self.change_dir_cd=1.5
                self.dir=1
        if self.rect.x<0:
            self.rect.x=0
        if self.rect.x+self.b>w:
            self.rect.x=w-self.b
        if p.rect.bottom<self.rect.bottom and self.jumping==2 and self.jumping_cd<=0 and self.rect.top-p.rect.bottom<=150:
            self.jumping-=1
            self.jumping_cd=1.5
            self.next_jumping_cd=0.2
            self.velocity_y=-11
        elif p.rect.bottom<self.rect.bottom and self.jumping==1 and self.next_jumping_cd<=0 and self.rect.top-p.rect.bottom<=75:
            self.jumping_cd=1.5
            self.velocity_y=-11
            self.jumping-=1
        if self.jumping_cd>0:
            self.jumping_cd-=1/60
        if self.next_jumping_cd>0:
            self.next_jumping_cd-=1/60
        if self.hurt_cd>0:
            self.hurt_cd-=1/60
        if self.change_dir_cd>0:
            self.change_dir_cd-=1/60
        if self.hurt_recover_cd>0:
            self.hurt_recover_cd-=1/60
        if self.skill_cd>0:
            self.skill_cd-=1/60
            if self.skill_cd<=3 and not self.skill_cd_tip:
                self.skill_cd_tip=True
                self.game.achiev_info=Info.append_info(self.game.achiev_info,"boss即将释放技能！",[0,cn_def_sz*2],font=cn_sm,color="orange",max_len=10,time=3,back_color=None)
        else:
            t=rd.randint(1,2)
            if t==1:
                self.game.achiev_info=Info.append_info(self.game.achiev_info,"boss释放技能1：禁止移动1.5s",[0,cn_def_sz*2],font=cn_sm,color="orange",max_len=10,time=3,back_color=None)
                p.stop_move_time=1.5
            else:
                self.game.achiev_info=Info.append_info(self.game.achiev_info,"boss释放技能2：发射子弹",[0,cn_def_sz*2],font=cn_sm,color="orange",max_len=10,time=3,back_color=None)
                px,py=p.rect.center
                bx,by=self.rect.center
                self.game.bullet.add(Bullet(bx,by,math.degrees(math.atan2(py-by,px-bx)),9,8))
                self.game.bullet.add(Bullet(bx,by,math.degrees(math.atan2(py-by,px-bx))-5,9,8))
                self.game.bullet.add(Bullet(bx,by,math.degrees(math.atan2(py-by,px-bx))+5,9,8))
                self.game.bullet.add(Bullet(bx,by,math.degrees(math.atan2(py-by,px-bx))-10,9,8))
                self.game.bullet.add(Bullet(bx,by,math.degrees(math.atan2(py-by,px-bx))+10,9,8))
            self.skill_cd_tip=False
            self.skill_cd=25
        self.rect.y+=self.velocity_y
        self.velocity_y+=0.8
        if self.heart<=25:
            if self.recover_cd<=0:
                self.recover(2)
                self.recover_cd=7
        else:
            self.recover_cd=7
        if self.rect.x<0:
            self.rect.x=0
        if self.rect.x+self.b>w:
            self.rect.x=w-self.b
        self.last_move_dis=self.rect.x-self.last_move_dis
        if self.last_move_dis>0:
            self.last_move_dir="right"
        elif self.last_move_dis<0:
            self.last_move_dir="left"
        else:
            self.last_move_dir=""
        self.last_move_dis=abs(self.last_move_dis)
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
        elif floor.existence_time<=0.2 and (self.last_move_dir=="" or (self.last_move_dir=="right" and self.rect.left-self.last_move_dis>floor.rect.left) or (self.last_move_dir=="left" and self.rect.right+self.last_move_dis<floor.rect.right)):
            self.rect.bottom=floor.rect.top
            self.jumping=2
            self.velocity_y=0
        elif self.last_move_dir=="right":
            self.rect.right=floor.rect.left
        else:
            self.rect.left=floor.rect.right