font = PFont()
Xgrid,Ygrid = 30,40
gridSize = 130
gap = 30
nowgrid = ""

def setup():
    global font
    font = createFont("Arial",100)
    size(1500,900)
    background(0)
    
    
    
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
    
    
def blink (inp):
    global nowgrid
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
        delay(80)
        blockfill(pos,0,nowgrid[pos])
        blockfill(pos,1,nowgrid[pos+3])
        blockfill(pos,2,nowgrid[pos+6])
        
    elif inp[0] == "c":
        pos = int(inp[1])
        blockfill(0,pos,"X")
        blockfill(1,pos,"X")
        blockfill(2,pos,"X")
        delay(80)
        blockfill(0,pos,nowgrid[pos*3])
        blockfill(1,pos,nowgrid[pos*3+1])
        blockfill(2,pos,nowgrid[pos*3+2])
    print("hi")
        
    
tog = True

def draw():
    global font,tog
    
    if tog:
        setGrid("ABCDEFGHI")
        fill(255)
        square (500,500,50)
    
    elif not tog:
        setGrid("XYZWLMNOP")
    tog = not tog
    delay(200)
    

def mouseReleased():
    setGrid("XYZWLMNOP")
    delay(1000)
    
