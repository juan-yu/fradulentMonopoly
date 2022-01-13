#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random,pygame,sys #使用的套件(sys是system，在遊戲結束時用來關閉程式)
class player:
    def __init__(self,token,winCard,num):
        self.token=token#棋子圖片
        self.num=num
        self.winCard=winCard#勝利圖片
        self.money=0#當前擁有金錢
        self.position=0#當前位置
        #self.lastPos=0
        self.fraudHave=[]#當前擁有舞弊卡
        self.stockHave=[0,0,0,0]#當前擁有股票
        self.diceLeft=0

    def changePosition(self,steps):
        '''
        self.lastPos=self.position
        for j in range(1,121):
            oneFrame=(round((gridPos[self.position][self.num][0]-gridPos[self.lastPos][self.num][0])/120),round((gridPos[self.position][self.num][1]-gridPos[self.lastPos][self.num][1])/120))
            nextPos=(gridPos[self.lastPos][self.num][0]+oneFrame[0]*j,gridPos[self.position][self.num][1]+oneFrame[1]*j)
            print(self.num,'to',nextPos)
            screen.blit(self.token,nextPos)
            pygame.display.flip()
            '''
        while steps>0:
            self.position+=1
            steps-=1
            screen.blit(bg,(0,0))
            for i in range(4):
                if i!=self.num:
                    screen.blit(players[i].token,gridPos[players[i].position][i])
                screen.blit(pygame.font.SysFont(None, 40).render('{:d}'.format(players[i].money), True,(0, 0, 0)), moneyPos[i])
                screen.blit(pygame.font.SysFont(None, 40).render('{:d}'.format(len(players[i].fraudHave)), True,(0, 0, 0)), fraudPos[i])
                screen.blit(pygame.font.SysFont('Microsoft JhengHei', 18).render(f'威:{players[i].stockHave[0]}普:{players[i].stockHave[1]}德:{players[i].stockHave[2]}安:{players[i].stockHave[3]}', True,(0, 0, 0)), stockPos[i])
                screen.blit(pygame.font.SysFont(None, 40).render('{:d}'.format(stockPrice[i]), True,(0, 0, 0)), stockPricePos[i])
                screen.blit(indicator,(1322,18+counter*200))
                  
            if self.position>29:
                self.position-=30
                event=random.choice(['bonusDice','bonusF','get6000','nothing','ranStock','rob','skipSB','stockUp'])
                screen.blit(pygame.transform.smoothscale(pygame.image.load(event+".PNG"), (400,400)), (350,324))
                screen.blit(pygame.transform.smoothscale(pygame.image.load("ranEvent.PNG"), (500,200)), (300,78))
                pygame.display.flip()
                if event=='nothing':
                    pygame.mixer.Sound('nothing.mp3').play()
                else:
                    pygame.mixer.Sound('goodThing.mp3').play()
                pygame.time.wait(2200)
                updateGUI()
                if event=='bonusDice':#再骰一次
                    self.diceLeft+=1
                    print('player',counter,' dice+1 to',self.diceLeft)
                elif event=='bonusF':
                    getFraud(self)
                elif event=='get6000':#每人偷2000
                    i=0
                    for player in players[:players.index(self)]+players[players.index(self)+1:]:
                        if player.money>=2000:
                            self.money+=2000
                            player.money-=2000
                        else:
                            self.money+=player.money
                            player.money=0
                        i+=1
                elif event=='ranStock':
                    got=random.randrange(4)
                    screen.blit(pygame.transform.smoothscale(pygame.image.load('c'+str(got)+".PNG"), (542,750)), (412,9))
                    pygame.display.flip()
                    self.stockHave[got]+=1
                    pygame.time.wait(1500)
                elif event=='rob':#指定搶一人5000
                    rects=[]
                    j=0
                    for i in [x for x in range(4) if x!=players.index(self)]:
                        rects.append([i,screen.blit(pygame.transform.smoothscale(pygame.image.load("rob"+str(i)+".PNG"), (330,458)), (59+j*330,174))])
                        j+=1
                    pygame.display.flip()
                    listen=True
                    while listen:
                        for event in pygame.event.get():
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                for rect in rects:
                                    if rect[1].collidepoint(event.pos):
                                        if players[rect[0]].money>=5000:
                                            self.money+=5000
                                            players[rect[0]].money-=5000
                                            listen=False
                                        else:
                                            self.money+=players[rect[0]].money
                                            players[rect[0]].money=0
                                            listen=False
                elif event=='skipSB':#指定跳過回合
                    rects=[]
                    j=0
                    for i in [x for x in range(4) if x!=players.index(self)]:
                        rects.append([i,screen.blit(pygame.transform.smoothscale(pygame.image.load("rob"+str(i)+".PNG"), (330,458)), (59+j*330,174))])
                        j+=1
                    pygame.display.flip()
                    listen=True
                    while listen:
                        for event in pygame.event.get():
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                for rect in rects:
                                    if rect[1].collidepoint(event.pos):
                                        players[rect[0]].diceLeft-=1
                                        print('player '+str(rect[0])+' dice-1 to '+str(players[rect[0]].diceLeft))
                                        listen=False
                elif event=='stockUp':#擁有股價上漲
                    i=0
                    for stock in self.stockHave:
                        if stock>0:
                            up=random.randrange(1000,3001)
                            stockPrice[i]+=up
                            print('stock',i,'Up',up)
                        i+=1
                updateGUI()
            screen.blit(self.token,gridPos[self.position][self.num])
            pygame.display.flip()
            pygame.mixer.Sound('moveChess.mp3').play()
            pygame.time.wait(200) 
        return self.position

    def useFraud(self,entry):
        screen.blit(pygame.transform.smoothscale(pygame.image.load('e'+str(entry)+".PNG"), (542,750)), (112,9))
        screen.blit(pygame.font.SysFont('simsun', 60).render('選擇舞弊卡', True,(255, 255, 255),(0,0,0)), (30,30))
        i=1
        toF1,toF2,toF3=None,None,None
        for f in self.fraudHave:
            if i==1:
                toF1=pygame.transform.smoothscale(pygame.image.load('f'+str(f)+".PNG").convert(), (267,369))
                screen.blit(toF1, (675,10))
            elif i==2:
                toF2=pygame.transform.smoothscale(pygame.image.load('f'+str(f)+".PNG").convert(), (267,369))
                screen.blit(toF2, (675,389))
            elif i==3:
                toF3=pygame.transform.smoothscale(pygame.image.load('f'+str(f)+".PNG").convert(), (267,369))
                screen.blit(toF3, (952,195))
            i+=1
        pygame.display.flip()
        listen=True
        while listen:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if toF1!=None and toF1.get_rect(topleft=(675,10)).collidepoint(event.pos):
                        pygame.mixer.Sound('earnFromFraud.mp3').play()
                        self.money+=int(allEntry[entry-1]*1000*allFraud[self.fraudHave[0]-1])
                        del self.fraudHave[0]
                        listen=False
                    elif toF2!=None and toF2.get_rect(topleft=(675,389)).collidepoint(event.pos):
                        pygame.mixer.Sound('earnFromFraud.mp3').play()
                        self.money+=int(allEntry[entry-1]*1000*allFraud[self.fraudHave[1]-1])
                        del self.fraudHave[1]
                        listen=False
                    elif toF3!=None and toF3.get_rect(topleft=(952,195)).collidepoint(event.pos):
                        pygame.mixer.Sound('earnFromFraud.mp3').play()
                        self.money+=int(allEntry[entry-1]*1000*allFraud[self.fraudHave[2]-1])
                        del self.fraudHave[2]
                        listen=False
    def buyStock(self,company):
        if self.money-stockPrice[company]<0:
            updateGUI()
            pygame.mixer.Sound('cantBuySell.mp3').play()
            screen.blit(pygame.font.SysFont('simsun', 90).render('錢不夠:)', True,(255, 255, 255),(0,0,0)), (400,290))
            pygame.display.flip()
            pygame.time.wait(1700)
            updateGUI()
            return True
        else:
            self.stockHave[company]+=1
            self.money-=stockPrice[company]
            for i in range(4):
                res=int(stockPrice[i]+random.randrange(-2000,2001))
                stockPrice[i]=res if res>=0 else 0
            pygame.mixer.Sound('stockPriceChange.mp3').play()
            return False
    def sellStock(self,company):
        if self.stockHave[company]>=1:
            self.stockHave[company]-=1
            self.money+=stockPrice[company]
            for i in range(4):
                res=int(stockPrice[i]+random.randrange(-2000,2001))
                stockPrice[i]=res if res>=0 else 0
            pygame.mixer.Sound('stockPriceChange.mp3').play()
            return False
        else:
            updateGUI()
            pygame.mixer.Sound('cantBuySell.mp3').play()
            screen.blit(pygame.font.SysFont('simsun', 90).render('你沒這家的股票啦:P', True,(255, 255, 255),(0,0,0)), (200,290))
            pygame.display.flip()
            pygame.time.wait(2000)
            updateGUI()
            return True

allFraud=[0.2,0.3,0.1,0.2,0.1,0.2,0.3,0.3,0.1,0.2]
allEntry=[10,50,40,20,50,40,80,10,60,10]
allSalary=[5,3,2,1,5,4,6,3,2,4]
pygame.init()
screen = pygame.display.set_mode((1366,768))
bg=pygame.image.load("bg.PNG").convert()
bl=pygame.transform.smoothscale(pygame.image.load("blue.png").convert_alpha(), (200, 200))
red=pygame.transform.smoothscale(pygame.image.load("red.png").convert_alpha(), (200, 200))
gr=pygame.transform.smoothscale(pygame.image.load("green.png").convert_alpha(), (200, 200))
y=pygame.transform.smoothscale(pygame.image.load("yellow.png").convert_alpha(), (200, 200))
indicator=pygame.transform.smoothscale(pygame.image.load("indicator.png").convert_alpha(), (20, 20))
pygame.display.set_caption("舞弊大富翁")
gridPos=[[(890,550),(940,550),(890,600),(940,600)]#0   共30格，每格都有4個座標，分別給4個棋子，以免圖片重疊
         ,[(790,550),(840,550),(790,600),(840,600)]#1
         ,[(690,550),(740,550),(690,600),(740,600)]#2
         ,[(590,550),(640,550),(590,600),(640,600)]#3
         ,[(480,550),(530,550),(480,600),(530,600)]#4
         ,[(370,550),(420,550),(370,600),(420,600)]#5
         ,[(270,550),(320,550),(270,600),(320,600)]#6
         ,[(170,550),(220,550),(170,600),(220,600)]#7
         ,[(70,550),(120,550),(70,600),(120,600)]#8
         ,[(-50,550),(0,550),(-50,600),(0,600)]#9
         ,[(-50,440),(0,440),(-50,480),(0,480)]#10
         ,[(-50,340),(0,340),(-50,380),(0,380)]#11
         ,[(-50,240),(0,240),(-50,280),(0,280)]#12
         ,[(-50,140),(0,140),(-50,180),(0,180)]#13
         ,[(-50,40),(0,40),(-50,80),(0,80)]#14
         ,[(-50,-60),(0,-60),(-50,-20),(0,-20)]#15
         ,[(70,-60),(120,-60),(70,-20),(120,-20)]#16
         ,[(170,-60),(220,-60),(170,-20),(220,-20)]#17
         ,[(270,-60),(320,-60),(270,-20),(320,-20)]#18
         ,[(370,-60),(420,-60),(370,-20),(420,-20)]#19
         ,[(470,-60),(520,-60),(470,-20),(520,-20)]#20
         ,[(580,-60),(630,-60),(580,-20),(630,-20)]#21
         ,[(680,-60),(730,-60),(680,-20),(730,-20)]#22
         ,[(780,-60),(830,-60),(780,-20),(830,-20)]#23
         ,[(890,-60),(940,-60),(890,-20),(940,-20)]#24
         ,[(890,40),(940,40),(890,80),(940,80)]#25
         ,[(890,140),(940,140),(890,180),(940,180)]#26
         ,[(890,240),(940,240),(890,280),(940,280)]#27
         ,[(890,340),(940,340),(890,380),(940,380)]#28
         ,[(890,440),(940,440),(890,480),(940,480)]#29
        ]
moneyPos=[(1212, 80),(1212, 270),(1212, 468),(1212, 658)]
fraudPos=[(1212, 115),(1212, 305),(1212, 505),(1212, 695)]
stockPos=[(1212, 153),(1212, 343),(1212, 540),(1212, 736)]
stockPricePos=[(526,174),(526,264),(526,363),(526,454)]
players=[player(red,'w0.png',0),player(y,"w1.png",1),player(gr,"w2.png",2),player(bl,"w3.png",3)]
counter=0
stockPrice=[5000,5000,5000,5000]
pygame.mixer.music.load('bgMusic.mp3')
pygame.mixer.music.play(-1)

def updateGUI():
    screen.blit(bg,(0,0))
    for i in range(4):
        screen.blit(players[i].token,gridPos[players[i].position][i])
        screen.blit(pygame.font.SysFont(None, 40).render('{:d}'.format(players[i].money), True,(0, 0, 0)), moneyPos[i])
        screen.blit(pygame.font.SysFont(None, 40).render('{:d}'.format(len(players[i].fraudHave)), True,(0, 0, 0)), fraudPos[i])
        screen.blit(pygame.font.SysFont('Microsoft JhengHei', 18).render(f'威:{players[i].stockHave[0]}普:{players[i].stockHave[1]}德:{players[i].stockHave[2]}安:{players[i].stockHave[3]}', True,(0, 0, 0)), stockPos[i])
        screen.blit(pygame.font.SysFont(None, 40).render('{:d}'.format(stockPrice[i]), True,(0, 0, 0)), stockPricePos[i])
        screen.blit(indicator,(1322,18+counter*200))
        pygame.display.flip()

def stockBuySell(player,company):
    updateGUI()
    y=screen.blit(pygame.transform.smoothscale(pygame.image.load("b.PNG"), (150,150)), (175,320))
    n=screen.blit(pygame.transform.smoothscale(pygame.image.load("s.PNG"), (150,150)), (794,320))
    back=screen.blit(pygame.transform.smoothscale(pygame.image.load('back.PNG'),(150,100)),(525,550))
    pygame.display.flip()
    listen=True
    while listen:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if y.collidepoint(event.pos):
                    print('click buy')
                    listen=False
                    return player.buyStock(company)
                elif n.collidepoint(event.pos):
                    listen=False
                    return player.sellStock(company)
                elif back.collidepoint(event.pos):
                    updateGUI()
                    return True
def getFraud(player):
    if len(player.fraudHave)>=3:
            pygame.mixer.Sound('fraudFull.mp3').play()
            screen.blit(pygame.font.SysFont('simsun', 70).render('最多只能有3張舞弊卡 別貪心唷^^', True,(255, 255, 255),(0,0,0)), (170,290))
            pygame.display.flip()
            pygame.time.wait(1500)
            updateGUI()
    else:
        fraud=random.choice(range(1,11))
        player.fraudHave.append(fraud)
        pygame.mixer.Sound('draw.mp3').play()
        screen.blit(pygame.transform.smoothscale(pygame.image.load('f'+str(fraud)+".PNG"), (542,750)), (412,9))
        screen.blit(pygame.font.SysFont('simsun', 60).render('按滑鼠以繼續', True,(255, 255, 255),(0,0,0)), (30,30))
        pygame.display.flip()
        listen=True
        while listen:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    listen=False
        updateGUI()
    
#開始
while True:
    updateGUI()
    pygame.event.clear()
    
    if players[counter].diceLeft>=0:
        listen = True
        while listen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    listen = False
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        steps=random.randrange(1,7)
                        listen = False
                        pygame.mixer.Sound('dice.mp3').play()
                        screen.blit(pygame.transform.smoothscale(pygame.image.load(str(steps)+".PNG"), (400,400)), (412,200))
                        pygame.display.flip()
                        pygame.time.wait(500)
        
        players[counter].changePosition(steps)
        updateGUI()
        pygame.time.wait(500)

        #記帳
        if players[counter].position in[1,2,4,6,7,10,13,14,16,17,20,21,23,26,27]:
            entry=random.choice(range(1,11))
            pygame.mixer.Sound('draw.mp3').play()
            screen.blit(pygame.transform.smoothscale(pygame.image.load('e'+str(entry)+".PNG"), (542,750)), (412,9))
            screen.blit(pygame.font.SysFont('simsun', 60).render('按滑鼠以繼續', True,(255, 255, 255),(0,0,0)), (30,30))
            pygame.display.flip()
            listen=True
            while listen:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        listen=False
            updateGUI()
            if len(players[counter].fraudHave)>=1:
                screen.blit(pygame.transform.smoothscale(pygame.image.load("useF.PNG"), (900,360)), (158,70))
                y=pygame.transform.smoothscale(pygame.image.load("y.PNG"), (150,150))
                n=pygame.transform.smoothscale(pygame.image.load("n.PNG"), (150,150))
                screen.blit(y, (348,450))
                screen.blit(n, (700,450))
                pygame.display.flip()
                listen=True
                while listen:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if y.get_rect(topleft=(348,450)).collidepoint(event.pos):
                                updateGUI()
                                players[counter].useFraud(entry)
                                listen=False
                            elif n.get_rect(topleft=(700,450)).collidepoint(event.pos):
                                print('NuseF')
                                listen=False
            players[counter].money+=allSalary[entry-1]*1000
            print(players[counter].money,'元')
            updateGUI()

        #舞弊
        if players[counter].position in [3,9,12,15,19,24,28]:
            getFraud(players[counter])

        #股票
        if players[counter].position in [5,8,11,18,22,25,29]:
            listen=True
            while listen:
                screen.blit(pygame.font.SysFont('simsun', 60).render('選擇重骰或按圓形公司標誌以買賣', True,(255, 255, 255),(0,0,0)), (30,30))
                reDice=screen.blit(pygame.transform.smoothscale(pygame.image.load("reDice.PNG"), (150,100)), (786,346))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if reDice.collidepoint(event.pos):
                            players[counter].diceLeft+=1
                            listen=False
                        elif pygame.Rect((350, 135), (95, 95)).collidepoint(event.pos):
                            listen=stockBuySell(players[counter],0)
                        elif pygame.Rect((350, 230), (95, 95)).collidepoint(event.pos):
                            listen=stockBuySell(players[counter],1)
                        elif pygame.Rect((350, 325), (95, 95)).collidepoint(event.pos):
                            listen=stockBuySell(players[counter],2)
                        elif pygame.Rect((350, 420), (95, 95)).collidepoint(event.pos):
                            listen=stockBuySell(players[counter],3)
            updateGUI()

        if players[counter].money>=100000:
            updateGUI()
            pygame.mixer.Sound('win.mp3').play()
            screen.blit(pygame.transform.smoothscale(pygame.image.load(players[counter].winCard), (542, 750)), (412,9))
            screen.blit(pygame.font.SysFont('simsun', 60).render('按滑鼠以結束遊戲', True,(255, 255, 255),(0,0,0)), (30,30))
            pygame.display.flip()
            listen=True
            while listen:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        listen=False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.QUIT:
                        listen = False
                        pygame.quit()
                        sys.exit()
            break
    if players[counter].diceLeft==0:
        if counter+1==len(players):
            counter=0
        else:
            counter+=1
    elif players[counter].diceLeft>=1:
        players[counter].diceLeft-=1
        print('player '+str(counter)+' dice-1 to '+str(players[counter].diceLeft))
    else:
        players[counter].diceLeft+=1
        print('player '+str(counter)+' dice+1 to '+str(players[counter].diceLeft))
        if counter+1==len(players):
            counter=0
        else:
            counter+=1


# In[ ]:




