import pygame as pg
from const import *
def DrawText(texts):
    real_pos=list()
    for text,val_list in texts.items():
        pos=list(val_list[0])
        font=val_list[1]
        color=val_list[2]
        alignment="topleft"
        if len(val_list)>=4 and val_list[3]==2:
            real_pos[0]+=pos[0]
            real_pos[1]+=pos[1]
        else:
            real_pos=pos
        if len(val_list)>=5:
            alignment=val_list[4]
        text=font.render(text,True,color)
        if alignment=="topleft":
            window.blit(text,real_pos)
        elif alignment=="topright":
            window.blit(text,text.get_rect(topright=real_pos))
        elif alignment=="bottomleft":
            window.blit(text,text.get_rect(bottomleft=real_pos))
        elif alignment=="bottomright":
            window.blit(text,text.get_rect(bottomright=real_pos))
        elif alignment=="center":
            window.blit(text,text.get_rect(center=real_pos))