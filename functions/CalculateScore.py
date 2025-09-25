from functions.Buffs import *#type:ignore

def caclculate_score(current_score,buffs):
    value = 1
    for buff in buffs:
        if BUFF.X2SCOREMULTIPLIER == buff:value*=2
        elif BUFF.X3SCOREMULTIPLIER == buff:value*=3
        elif BUFF.X4SCOREMULTIPLIER == buff:value*=4
        elif BUFF.X5SCOREMULTIPLIER == buff:value*=5
        elif BUFF.X6SCOREMULTIPLIER == buff:value*=6
        elif BUFF.X7SCOREMULTIPLIER == buff:value*=7
        elif BUFF.X8SCOREMULTIPLIER == buff:value*=8
        elif BUFF.X9SCOREMULTIPLIER == buff:value*=9
        elif BUFF.X10SCOREMULTIPLIER == buff:value*=10
    return current_score + value