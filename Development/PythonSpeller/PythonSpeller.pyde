import random
font = PFont()
Xgrid,Ygrid = 30,40
gridSize = 130
gap = 30
nowgrid = ""
blinksq = "r0,r1,r2,c0,c1,c2".split(",")



def setup():
    global font
    font = createFont("Arial",100)
    size(1500,900)
    background(0)
    blinksq = "r0,r1,r2,c0,c1,c2".split(",")
    
    
    
def alpSet(*s):
    global font
    for i in s:
        blockfill(i[:1])
        textFont(font, 100)
        text(i[2],Xgrid+(k[0]*140)+5,Ygrid+(k[1]*140)+5,130)
        


def blocks(*l):
    for i in l:
        blockfill(i)
def blockpos(x,y):
    global Xgrid,Ygrid,gridSize,gap
    Xplace , Yplace = Xgrid+(x*(gridSize+2*gap))+gap,Ygrid+(y*(gridSize+2*gap))+gap
    alpPlaceX, alpPlaceY = Xplace+(gridSize/2)-100/4.5,(Yplace+gridSize-20)
    return Xplace, Yplace, alpPlaceX,alpPlaceY

def blockfill(x,y,c):
    Xplace , Yplace ,alpPlaceX, alpPlaceY = blockpos(x,y)
    fill(255)
    square(Xplace,Yplace,gridSize)
    textFont(font, 100)
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
        blockfill(0,pos,"X")
        blockfill(1,pos,"X")
        blockfill(2,pos,"X")
        
    
bs = False
client = True
bstate = 0
blinksq = ['r0', 'r1', 'r2', 'c0', 'c1', 'c2']

def draw():
    global font,bs,bstate,blinksq
    
    if bs:
        print(blinksq)
        blink(blinksq[bstate])
        if bstate>5:
            bstate=0
        else:
            bstate+=1
        
    #if (client):
        #set input
        
    else:
        setGrid("ABCDEFGHI")
        random.shuffle(blinksq)
    bs = not bs
    delay(80)

def mouseReleased():
    setGrid("XYZWLMNOP")
    delay(1000)
    