import random
font = PFont()
Xgrid,Ygrid = 30,40
gridSize = 100
gap = 30
nowgrid = ""
blinksq = "r0,r1,r2,c0,c1,c2".split(",")
fsize = 100
tablen = 3*(gridSize+2*gap)

def setup():
    global font
    font = createFont("Arial",fsize)
    size(1900,1000)
    background(255)
    blinksq = "r0,r1,r2,c0,c1,c2".split(",")
    
    
    
def alpSet(*s):
    global font
    for i in s:
        blockfill(i[:1])
        textFont(font, fsize)
        text(i[2],Xgrid+(k[0]*140)+5,Ygrid+(k[1]*140)+5,130)
        


def blocks(*l):
    for i in l:
        blockfill(i)
def blockpos(x,y):
    global Xgrid,Ygrid,gridSize,gap
    Xplace , Yplace = Xgrid+(x*(gridSize+2*gap))+gap,Ygrid+(y*(gridSize+2*gap))+gap
    alpPlaceX, alpPlaceY = Xplace+(gridSize/2)-fsize/3.5,(Yplace+gridSize/2+fsize/3)
    return Xplace, Yplace, alpPlaceX,alpPlaceY

def blockfill(x,y,c):
    Xplace , Yplace ,alpPlaceX, alpPlaceY = blockpos(x,y)
    fill(255)
    square(Xplace,Yplace,gridSize)
    textFont(font, fsize)
    fill(0)
    text(c,alpPlaceX,alpPlaceY)
    
    
def setGrid(a9):
    for y in range(3):
        for x in range(3):
            blockfill(x,y,a9[3*y+x])
    global nowgrid
    nowgrid = a9
    
def unblink(inp):
    global nowgrid  
    pos = inp[1]  
    if inp[0] == "r":
        blockfill(pos,0,nowgrid[pos])
        blockfill(pos,1,nowgrid[pos+3])
        blockfill(pos,2,nowgrid[pos+6])
        
    elif inp[0] == "c":
        blockfill(0,pos,nowgrid[pos*3])
        blockfill(1,pos,nowgrid[pos*3+1])
        blockfill(2,pos,nowgrid[pos*3+2])

def blink (inp):

    r=((0,0),(0,1),(0,2),
       (1,0),(1,1),(1,2),
       (2,0),(2,1),(2,2))
    
    c = ((0,0),(1,0),(2,0),
        (0,1),(1,1),(2,1),
        (0,2),(1,2),(2,2))
    if inp[0] == "r":
        pos = int(inp[1])
        blockfill(pos,0," ")
        blockfill(pos,1," ")
        blockfill(pos,2," ")
        
    elif inp[0] == "c":
        pos = int(inp[1])
        blockfill(0,pos," ")
        blockfill(1,pos," ")
        blockfill(2,pos," ")
        
    
bs = False
client = True
bstate = 0
blinksq = ['r0', 'r1', 'r2', 'c0', 'c1', 'c2']

def draw():
    global font,bs,bstate,blinksq
    
    if bs:
        if bstate==0:
            delay(920)
        blink(blinksq[bstate])
        print(bstate)
        bstate+=1
        delay(30)
        if bstate==6:
            bstate=0
            random.shuffle(blinksq)
            print(blinksq)
        delay(80)
    #if (client):
        #set input
        
    else:
        setGrid("ABCDEFGHI")
        delay(80)
    bs = not bs
    
            
    
    
    textFont(font, fsize)
    fill(255)
    noStroke()
    square(Xgrid+tablen+500,Ygrid,400)
    fill(0)
    text("ABC"+str(bstate),Xgrid+tablen+500,Ygrid+gridSize)

def mouseReleased():
    setGrid("XYZWLMNOP")
    delay(1000)
    
