
import random
import socket
import os

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000        # The port used by the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = None

font = PFont()
Xgrid,Ygrid = 30,40
gridSize = 260
gap = 25
nowgrid = ""
fsize = 200
tablen = 3*(gridSize+2*gap)

def setup():
    path = sketchPath("")
    os.chdir(path+"/../Speller.py")
    repath = os.getcwd()
    os.system("start; CMD /k PrototypefromBatchPhasePower.py")

    global font,client,conn
    font = createFont("Arial",fsize)
    size(1900,1000)
    background(255)
    fill(255)
    stroke(0)
    rect(Xgrid+tablen+200,Ygrid+130,800,150)
    blinksq = "r0,r1,r2,c0,c1,c2".split(",")
    
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 5000        # The port used by the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    while True:
        if client.recv(1024) == b"ready":
            print("ready")
            break

    
def waitsign(b):
    if b:
        textFont(font, 100)
        fill(255,0,0)
        text("wait",Xgrid+tablen+500,Ygrid+gridSize+400)
    else:
        fill(255)
        noStroke()
        rect(Xgrid+tablen+500,Ygrid+500,800,400)
        
    
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
            noStroke()
            blockfill(x,y,a9[3*y+x])
    global nowgrid
    nowgrid = a9
    


def blink (inp):

    r=((0,0),(0,1),(0,2),
       (1,0),(1,1),(1,2),
       (2,0),(2,1),(2,2))
    
    c = ((0,0),(1,0),(2,0),
        (0,1),(1,1),(2,1),
        (0,2),(1,2),(2,2))
    noStroke()
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
        
typed = ""
client = True
bstate = 0
ostate = False
inlet=[]
#blinksq = ['r0', 'r1', 'r2', 'c0', 'c1', 'c2']

def UI(alp9,blinksq):
    global font,bstate,ostate,typed,Xgrid,Ygrid,gridSize
    if bstate%2 == 1:
        if bstate==len(blinksq)*2+1:
            setGrid("         ")
            waitsign(True)
            client.send(b"finished")
            typing = str(client.recv(1024).decode("utf-8")).split(" ")[1]
            typed += typing
            textFont(font, 100)
            fill(255)
            stroke(0)
            rect(Xgrid+tablen+200,Ygrid+130,800,150)
            fill(0)
            text(typed,Xgrid+tablen+200,Ygrid+gridSize)
        
            delay(500) # p300 pause
        else:
            blink(blinksq[bstate//2])
            print(bstate)
            delay(30)
            delay(80)
        
    #if (client):
        #set input
        
    else:
        setGrid(alp9)
        delay(80)
        if bstate==len(blinksq)*2+2:
            bstate=0
            print(blinksq)
            setGrid("         ")
            delay(1000) # p300 pause
            return True
        elif bstate == 0:
            delay(1000)
    bstate+=1
    return False
    
            
    
    
    

def draw():
    waitsign(False)
    global ostate,client,inlet,typed
    """textFont(font, 100)
    fill(255)
    noStroke()
    rect(Xgrid+tablen+200,Ygrid,800,400)
    fill(0)
    text(typed,Xgrid+tablen+200,Ygrid+gridSize)
    stroke(0)"""
    if not ostate:
        client.sendall(b"collect")
        print("hi")
        inlet= str(client.recv(1024).decode("utf-8"))
        inlet = inlet.split(' ')
        print(inlet)
        ostate = True
        setGrid(inlet[0])
    else:
        newloop = UI(inlet[0],inlet[1].split(","))
        if newloop:
            #client.send(b"finished")
            #typing = str(client.recv(1024).decode("utf-8")).split(" ")[1]
            #typed += typing
            print("br")
            print("aftype")
            ostate = False
            

        
