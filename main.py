import sys
sys.path.append('./')

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

e_res=0;
enec=1;
ex_flag=0


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
	
	units[len(units)-1].yold=y2;units[len(units)-1].yn=y2
	units[len(units)-1].xold=x1;units[len(units)-1].xn=x1
	units[len(units)-1].attach(typea)
	res-=int(config.get(typea, "cost"))
	if(ene==1):
		units[len(units)-1].isenemy=1
	
def make(typea,x1,y2):
	global config;global res;global sel;global units
	if(int(config.get(typea, "cost"))<res and (typea in (config.get(units[sel].fname, "can").split(',')))):
		units.append(unit())
		
		units[len(units)-1].yold=y2;units[len(units)-1].yn=y2
		units[len(units)-1].xold=x1;units[len(units)-1].xn=x1
		units[len(units)-1].attach(typea)
		res-=int(config.get(typea, "cost"))
		
		
def emake(typea,x1,y2):
	global config;global e_res;global sel;global units
	units.append(unit())
	units[len(units)-1].isenemy=1
	units[len(units)-1].yold=y2;units[len(units)-1].yn=y2
	units[len(units)-1].xold=x1;units[len(units)-1].xn=x1
	units[len(units)-1].attach(typea)
	print('OK')

def spenemy():
	global enec;global root;global units;global config
	global e_res
	cost=0
	'''
	for i in range(enec):
		smake('enemy',300,300-i*30,1)
	
	if(enec>2):
		smake('boss',400,400,1)
	for i in range(int(round((enec/6)))):
		smake('e_art',400,400-i*30,1)
		
	enec+=1
	'''
	for i in units:
		if(config.get(i.fname, "type")=='enemy' and i.rq==''):
			for j in (config.get(i.fname, "can").split(',')):
				if(j!=''):
					cost+=int(config.get(j, "cost"))
	if(e_res>cost):
	
		for i in units:
			if(config.get(i.fname, "type")=='enemy' and i.rq==''):
				for j in (config.get(i.fname, "can").split(',')):
					if(j!='' and i.rq==''):
						i.product(j)
						e_res-=int(config.get(j, "cost"))
						break
		


def product(typea):
	global units;global sel
	units[sel].product(typea)
	

	
	
class unit:
	xn=30
	yn=30
	xold=30
	yold=30
	hp=10
	maxhp=10
	vel=1
	vlc=0
	
	tod=0
	
	gains=0
	gtime=0
	
	damage=1
	rech=0
	trech=1
	range=0

	win=0
	
	l=list()
	load=0
	
	gc=0
	fname='soldier'
	type=0
	isenemy=0
	img=Image.open(fname+'.png')
	fimg=ImageTk.PhotoImage(img)
	sprite=canvas.create_image(xold,yold,image=fimg)
	
	hpr=0
	lpr=0
	rq=''
	ptime=0
	
	def update(self):
		global res;global canvas;global e_res
		if(self.vel>0 and self.vlc==self.vel):
			self.xold+=min((abs(self.xold-self.xn)),1)*sign(self.xold-self.xn)*-1
			self.yold+=min((abs(self.yold-self.yn)),1)*sign(self.yold-self.yn)*-1
			canvas.move(self.sprite,min((abs(self.xold-self.xn)),1)*sign(self.xold-self.xn)*-1,min((abs(self.yold-self.yn)),1)*sign(self.yold-self.yn)*-1)
			canvas.move(self.lpr,min((abs(self.xold-self.xn)),1)*sign(self.xold-self.xn)*-1,min((abs(self.yold-self.yn)),1)*sign(self.yold-self.yn)*-1)
			canvas.move(self.hpr,min((abs(self.xold-self.xn)),1)*sign(self.xold-self.xn)*-1,min((abs(self.yold-self.yn)),1)*sign(self.yold-self.yn)*-1)
			
			self.vlc=0
		if(self.vel>0):
			self.vlc+=1
		
		if(self.gains>0):
			if(self.gc==0):
				if(self.isenemy==0):
					res=res+self.gains
				else:
					e_res=e_res+self.gains
				self.gc=self.gtime
			else:
				self.gc-=1
		
		if(self.ptime<0 and self.rq!=''):
			
			if(self.isenemy==0):
				make(self.rq,self.xold+30,self.yold+30)
			else:
				
				emake(self.rq,self.xold+30,self.yold+30)
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
						self.dhp()
						e.dhp()
		
			self.rech=self.trech
		else:
			self.rech-=1
		if(len(units)>0):
				for e in units:
					if(e.isenemy==self.isenemy and len2d(self.xold,self.yold,e.xold,e.yold)<self.range):
						e.hp+=self.heal
						if(e.hp>e.maxhp):
							e.hp=e.maxhp
						e.dhp()
		
	def dhp(self):
		global canvas
		canvas.coords(self.hpr, self.xold-10,self.yold-20,self.xold+self.hp-10,self.yold-25)
	
	def dl(self):
		canvas.coords(self.lpr,self.xold-10,self.yold-30,self.xold+len(self.l)*5-10,self.yold-35)
	
	def draw(self):
		global canvas
		self.img=Image.open(self.fname+'.png')
		self.fimg=ImageTk.PhotoImage(self.img)
		canvas.delete(self.sprite)
		canvas.delete(self.hpr)
		canvas.delete(self.lpr)
		self.hpr=canvas.create_rectangle(self.xold-10,self.yold-20,self.xold+self.hp-10,self.yold-25,fill='green')
		self.lpr=canvas.create_rectangle(self.xold-10,self.yold-30,self.xold+len(self.l)*5-10,self.yold-35,fill='blue')
		
		self.sprite=canvas.create_image(self.xold,self.yold,image=self.fimg)
		
	def readF(self):
		global config
		self.win=int(config.get(self.fname,"win"))
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
		self.draw()
		
	
	
	def product(self,typea):
		
		self.rq=typea
		self.ptime=int(config.get(typea, "time"))
		
		
def load():
	for e in units:
		if(e.isenemy==units[sel].isenemy and units[sel].isenemy==0 and len2d(units[sel].xold,units[sel].yold,e.xold,e.yold)<25):
				if(len(e.l)<e.load and e.load>0 and units[sel]!=e):
					e.l.append(units[sel])
					units[sel].tod=1
							
					e.dl()
					print('a')
					break

def unload():
	for e in units[sel].l:
		units.append(e)
		units[len(units)-1].tod=0
		units[len(units)-1].yold=units[sel].yold+30;units[len(units)-1].yn=units[sel].yold+30
		units[len(units)-1].xold=units[sel].xold+30;units[len(units)-1].xn=units[sel].xold+30
		units[len(units)-1].draw()
		
	print('b')	
	units[sel].l.clear()
	units[sel].dl()



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
	spenemy()





res=1000
for i in range(4):
	smake('soldier',i*20+50,50)

smake('base',10,20)

smake('worker',200,20)

smake('e_art_s',400,200,1)
smake('e_art_s',200,400,1)
smake('e_base',300,300,1)
smake('e_base',300,400,1)
smake('e_base',400,300,1)
smake('boss_s',400,400,1)
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
	global ex_flag;global canvas;global units
	global res;global l1
	while(1):
		c=0
		
		for i in units:
			i.update()
			
			if(i.fname=='base' and i.hp>0):
				c+=1
			if(i.hp<0):
				
				i.tod=1
			else:
				if(i.win==1):
					print("YOU WIN!")
					ex_flag=1
		for i in units:
			if(i.tod==1):
				canvas.delete(i.sprite)
				canvas.delete(i.hpr)
				canvas.delete(i.lpr)
				units.remove(i)
																
		if(c==0):
			ex_flag=1
			print("GAME OVER")
		if(ex_flag==1):
			return
		ai()
		l1['text']=str(res)+' '+str(e_res)
		root.update()
		sleep(0.005)


def on_closing():
	global ex_flag
	ex_flag=1
	root.quit()
	exit()

sel=0

mainmenu.add_cascade(label="product", menu=prodmenu)
mainmenu.add_cascade(label="build", menu=buildmenu)
mainmenu.add_command(label="load",command=load)
mainmenu.add_command(label="unload",command=unload)

root.bind('<Button-1>', b1)

root.bind('<Motion>', b2)

root.bind('<Button-3>', b3)


root.protocol("WM_DELETE_WINDOW", on_closing)
spenemy()
ml()


