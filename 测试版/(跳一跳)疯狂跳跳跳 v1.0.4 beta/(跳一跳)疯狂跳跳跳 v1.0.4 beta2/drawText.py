import pygame as pg
from const import *
def DrawText(texts):
    for text,val_list in texts.items():
        pos=val_list[0]
        font=val_list[1]
        color=val_list[2]
        alignment="topleft"
        if len(val_list)>=4:
            alignment=val_list[3]
        text=font.render(text,True,color)
        if alignment=="topleft":
            window.blit(text,pos)
        elif alignment=="topright":
            window.blit(text,text.get_rect(topright=pos))
        elif alignment=="bottomleft":
            window.blit(text,text.get_rect(bottomleft=pos))
        elif alignment=="bottomright":
            window.blit(text,text.get_rect(bottomright=pos))
        elif alignment=="center":
            window.blit(text,text.get_rect(center=pos))