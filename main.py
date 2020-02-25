from tkinter import *
import PIL
from time import sleep
from PIL import ImageTk
from PIL import Image
from math import sqrt
import configparser
from functools import partial

def sign(num):
    return -1 if num < 0 else 1
    
    
def len2d(x1,y1,x2,y2):
  return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

x=30;
y=30;
res=0;
enec=1;

types=dict()

root = Tk()
root.geometry('500x500')
config=configparser.ConfigParser()
canvas = Canvas(root,width=500,height=500,bg='white')
canvas.pack()
config.read('config.ini')
l1=Label(fg="#eee", bg="#333")
l1.place(x=0,y=0)

units=list()
sel=0

root.update()


def smake(typea,x1,y2,ene=0):
  global config;global res
  units.append(unit())
  units[len(units)-1].attach(typea)
  units[len(units)-1].yold=y2;units[len(units)-1].yn=y2
  units[len(units)-1].xold=x1;units[len(units)-1].xn=x1
  res-=int(config.get(typea, "cost"))
  if(ene==1):
    units[len(units)-1].isenemy=1
  
def make(typea,x1,y2):
  global config;global res;global sel;global units
  if(int(config.get(typea, "cost"))<res and (typea in (config.get(units[sel].fname, "can").split(',')))):
    units.append(unit())
    units[len(units)-1].attach(typea)
    units[len(units)-1].yold=y2;units[len(units)-1].yn=y2
    units[len(units)-1].xold=x1;units[len(units)-1].xn=x1
    res-=int(config.get(typea, "cost"))

def spenemy():
  global enec
  for i in range(enec):
    smake('enemy',300,300-i*30,1)
  for i in range(int(round((enec/4)))):
    smake('boss',400,400,1)
  enec+=1

def product(typea):
  global sel;global units
  units[sel].product(typea)
  spenemy()
  
class unit:
  xn=30
  yn=30
  xold=30
  yold=30
  hp=10
  maxhp=10
  vel=1
  vlc=0
  
  
  gains=0
  gtime=0
  
  damage=1
  rech=0
  trech=1
  
  
  l=list()
  load=0
  
  gc=0
  fname='soldier'
  type=0
  isenemy=0
  img=Image.open(fname+'.png')
  fimg=ImageTk.PhotoImage(img)
  
  rq=''
  ptime=0
  
  def update(self):
    global canvas;global res
    self.img=Image.open(self.fname+'.png')
    self.fimg=ImageTk.PhotoImage(self.img)
    if(self.vel>0 and self.vlc==self.vel):
      self.xold+=min((abs(self.xold-self.xn)),1)*sign(self.xold-self.xn)*-1
      self.yold+=min((abs(self.yold-self.yn)),1)*sign(self.yold-self.yn)*-1
      self.vlc=0
    if(self.vel>0):
      self.vlc+=1
    
    if(self.gains>0):
      if(self.gc==0):
        res=res+self.gains
        self.gc=self.gtime
      else:
        self.gc-=1
    
    if(self.ptime<0 and self.rq!=''):
      make(self.rq,self.xold+30,self.yold+30)
      self.rq=''
    elif(self.rq!=''):
      self.ptime-=1
    if(self.rech==0):
      if(len(units)>0):
        for e in units:
          if(e.isenemy!=self.isenemy and len2d(self.xold,self.yold,e.xold,e.yold)<self.range):
            e.hp-=self.damage
            if(config.get(self.fname, "type")=='bomb'):
              self.hp=-1
    
      self.rech=self.trech
    else:
      self.rech-=1
    if(len(units)>0):
        for e in units:
          if(e.isenemy==self.isenemy and len2d(self.xold,self.yold,e.xold,e.yold)<self.range):
            e.hp+=self.heal
            if(e.hp>e.maxhp):
              e.hp=e.maxhp
    canvas.create_rectangle(self.xold-10,self.yold-20,self.xold+self.hp-10,self.yold-25,fill='green')
    if(len(self.l)>0):
      canvas.create_rectangle(self.xold-10,self.yold-30,self.xold+len(self.l)*5-10,self.yold-35,fill='blue')
    canvas.create_image(self.xold,self.yold,image=self.fimg)
    
    
  def readF(self):
    global config
    
    self.vel=int(config.get(self.fname, "velocity"))
    self.hp=int(config.get(self.fname, "hp"))
    self.maxhp=int(config.get(self.fname, "hp"))
    self.damage=int(config.get(self.fname, "damage"))
    self.gains=int(config.get(self.fname, "gains"))
    self.heal=int(config.get(self.fname, "heal"))
    self.load=int(config.get(self.fname, "load"))
    if(self.gains>0):
      self.gtime=int(config.get(self.fname, "gtime"))
    self.range=int(config.get(self.fname, "range"))
    self.trech=int(config.get(self.fname, "time_recharge"))
  def attach(self,filen):
    self.fname=filen
    self.l=list()
    self.readF()
    
  
  
  def product(self,typea):
    self.rq=typea
    self.ptime=int(config.get(typea, "time"))
    
    
def load():
  for e in units:
    if(e.isenemy==units[sel].isenemy and units[sel].isenemy==0 and len2d(units[sel].xold,units[sel].yold,e.xold,e.yold)<25):
        if(len(e.l)<e.load and e.load>0 and units[sel]!=e):
          e.l.append(units[sel])
          units.remove(units[sel])
          print('a')
          break

def unload():
  for e in units[sel].l:
    units.append(e)
    units[len(units)-1].yold=units[sel].yold+30;units[len(units)-1].yn=units[sel].yold+30
    units[len(units)-1].xold=units[sel].xold+30;units[len(units)-1].xn=units[sel].xold+30
  units[sel].l.clear()
def ai():
  global units
  for i in units:
    if(i.isenemy==1):
      for j in units:
        if(j.fname==config.get(i.fname, "interested")):
          if(j.vel==0):
            i.xn=j.xold
            i.yn=j.yold
          else:
            i.xn=j.xn
            i.yn=j.yn
        




res=1000
for i in range(4):
  smake('soldier',i*20+30,30)
smake('base',100,200)
smake('worker',200,200)
#smake('enemy',300,300,1)
res=0

mainmenu = Menu(root) 
root.config(menu=mainmenu) 
prodmenu=Menu(mainmenu,tearoff=0)
buildmenu=Menu(mainmenu,tearoff=0)

def b1(event):
  global x
  global y
  global units
  
  
  if(units[sel].isenemy==0):
    units[sel].xn=x;
    units[sel].yn=y;


  
def b2(event):
  global x
  x = event.x
  global y
  y=event.y
  

def b3(event):
  global x;global y;global units;global sel
  
  a=0
  for i in range(len(units)):
    if(len2d(units[a].xold,units[a].yold,x,y)>len2d(units[i].xold,units[i].yold,x,y)):
      a=i
  sel=a
  
  global prodmenu;global buildmenu;global types
  prodmenu.delete(0, 'end')
  buildmenu.delete(0, 'end')
  
  ll=config.get(units[sel].fname, "can").split(',')
  if(len(ll)>0):
    for i in ll:
      if(i!=''):
        if(types[i]=='building'):
          buildmenu.add_command(label=i,command=partial(product,i))
        if(types[i]=='people'):
          prodmenu.add_command(label=i,command=partial(product,i))
        if(types[i]=='bomb'):
          buildmenu.add_command(label=i,command=partial(product,i))
  
def ml():
  global res
  c=0
  canvas.delete("all")
  for i in units:
    i.update()
    if(i.hp<0):
      units.remove(i)
    if(i.fname=='base'):
      c+=1
  if(c==0):
    exit()
  ai()
  l1['text']=res
  root.update()
  sleep(0.01)


sel=0

mainmenu.add_cascade(label="product", menu=prodmenu)
mainmenu.add_cascade(label="build", menu=buildmenu)
mainmenu.add_command(label="load",command=load)
mainmenu.add_command(label="unload",command=unload)

root.bind('<Button-1>', b1)

root.bind('<Motion>', b2)

root.bind('<Button-3>', b3)



for i in config.sections():
  types[i]=config.get(i,'type')

while(1):
 

  ml()

root.mainloop()


