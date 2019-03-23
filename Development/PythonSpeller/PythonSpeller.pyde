font = PFont()
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


def blockfill(k):
    Xgrid,Ygrid = 30,40
    gridSize = 130
    gap = 1
    Xplace , Yplace = Xgrid+(k[0]*(gridSize+2*gap))+gap,Ygrid+(k[1]*(gridSize+2*gap))+gap
    alpPlaceX, alpPlaceY = Xplace+(gridSize/2)-100/4.5,(Yplace+gridSize-20)
    print(alpPlaceX)
    fill(255)
    square(Xgrid+(k[0]*140)+5,Ygrid+(k[1]*140)+5,gridSize)
    textFont(font, 100)
    fill(0)
    text(k[2],alpPlaceX,alpPlaceY)

def draw():
    global font
    textFont(font, 100)
    text("hi",30,30)
    blockfill([1,1,"Z"])
    blockfill([2,1,"X"])
    blockfill([1,2,"K"])
    blockfill([1,0,"I"])
    
