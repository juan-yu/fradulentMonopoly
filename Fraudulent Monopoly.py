#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random,pygame,threading

pygame.init()
pygame.display.init()
bg=pygame.image.load("bg.jpg")
bl=pygame.transform.scale(pygame.image.load("blue.png"), (100, 100))
red=pygame.transform.scale(pygame.image.load("red.png"), (100, 100))
pygame.display.set_caption("Fraudulent Monopoly")
screen = pygame.display.set_mode((1012,720))
screen.blit(bg,(0,0))
screen.blit(bl,(880,570))
screen.blit(red,(930,570))
pygame.display.flip()
#grids={1:'開始',2:'設備更汰',3:'貨物銷售',4:'擴大行銷',5:'財務壓力',6:'機會',7:'自我合理化'}
grids={1:'開始',2:'設備更汰',3:'財務壓力',4:'股票'}
counter=0

def GUI():
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
display=threading.Thread(target=GUI)
display.start()

def showMoney():
    for player in players:
        print(f'{player.token}現在有{player.money}元')


class player:
    
    entries={'設備更汰':{'金額':10000,'薪水':5000},'貨物銷售':3000,'擴大行銷':2000}
    allFraud=['財務壓力','機會','自我合理化']
    
    
    def __init__(self,token):
        self.token=token
        self.money=0
        self.position=1
        self.fraudHave=[]
        
    def changePosition(self,steps):
        self.position+=steps
        if self.position>4:
            self.position-=4
        return self.position

    def useFraud(self,entry,card):
        if card==0:
            return True
        usedCard=self.fraudHave.pop(card-1)
        stolenMoney=0
        entryAmount=self.entries[entry]['金額']
        if usedCard=='財務壓力':
            stolenMoney=int(entryAmount*0.3)
        self.money+=stolenMoney
        print(f'你偷了{stolenMoney}元')
        return True
    
    def entry(self,entry):
        salary=self.entries[entry]['薪水']
        self.money+=salary
        print(f'你賺了{salary}元')
        return self.entries[entry]['金額']


players=[player(token='A'),player(token='B')]

while True:
    print(f'{players[counter].token}:')
    steps=random.randrange(1,5)
    print('步數:',steps)
    positionName=grids[players[counter].changePosition(steps)]
    print('你到了:',positionName)
    if positionName=='開始':
        print('沒事')
    if positionName=='設備更汰':
        players[counter].entry('設備更汰')
        showMoney()
        if players[counter].money>20000:
            print(f'{players[counter].token}贏了!!!!!!!')
            break
        for player in players:
            print(f'{player.token}有以下舞弊卡：{player.fraudHave}')
        if len(players[counter].fraudHave)>=1:
            finish=None
            while finish is None:
                try:
                    finish=players[counter].useFraud('設備更汰',int(input('你要用哪張舞弊卡? 第1張輸入1，第2張輸入2，以此類推，不使用請輸入0\n')))
                except (ValueError,IndexError)as e:
                    print('再試一次')
            showMoney()
        if players[counter].money>20000:
            print(f'{players[counter].token}贏了!!!!!!!')
            break
    if positionName=='財務壓力':
        players[counter].fraudHave.append('財務壓力')
        for player in players:
            print(f'{player.token}累積的舞弊卡：{player.fraudHave}')
    if positionName=='股票':
        print('買賣股票，並二選一觸發一則股價波動事件')
    if counter+1==len(players):
        counter=0
    else:
        counter+=1
    input()
    

pygame.display.quit()


# In[ ]:




