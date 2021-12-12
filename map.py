#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import player

#grids={1:'開始',2:'設備更汰',3:'貨物銷售',4:'擴大行銷',5:'財務壓力',6:'機會',7:'自我合理化'}

def __init__(self):
    self.grids={1:'開始',2:'設備更汰',3:'財務壓力',4:'股票'}
    self.entries={'設備更汰':5000,'貨物銷售':3000,'擴大行銷':2000}
    self.cards=['財務壓力','機會','自我合理化']

def getGrids():
    return grids

def entry(who,entry):
    player.changeMoney(who,entries[entry])
def fraud(who,entry,card):
    if card=='財務壓力':
        who.changeMoney(entries[entry]*0.3)




