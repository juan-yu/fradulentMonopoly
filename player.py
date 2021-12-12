#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import map


def __init__(self):
    self.moneyA=0
    self.moneyB=0
    self.positionA=1
    self.positionB=1
    self.fraudCardsA=[]
    self.fraudCardsB=[]

def getMoney(who):
    if who=='A':
        return moneyA
    if who=='B':
        return moneyB

def changeMoney(who,money):
    if who=='A':
        moneyA+=money
    if who=='B':
        moneyB+=money
        
def getPosition(who):
    if who=='A':
        return positionA
    if who=='B':
        return positionB
    
def changePosition(who,steps):
    if who=='A':
        positionA+=steps
        if positionA>4:
            positionA-=4
    if who=='B':
        positionB+=steps
        if positionB>4:
            positionB-=4

def addFraudCard(who,card):
    if who=='A':
        fraudCardsA.append(card)
    if who=='B':
        fraudCardsB.append(card)
    
def useFraudCard(who,card):
    if who=='A':
        fraudCardsA.remove(card)
        map.fraud(who,card)
    if who=='B':
        fraudCardsB.remove(card)
        map.fraud(who,card)