import tkinter as tk
import time
import random
gameWindow = tk.Tk()
gameWindow.geometry("400x400")
cnvs = tk.Canvas(master=gameWindow,width=400,height=400,bg="white")
cnvs.pack(anchor="w")
#variables
objects = []
moveUpValue = 0
totUpVal = 0
moveTup = [False,False,False] #boolean logic for right left and jump
ticks = 0 
textx = 60
lastTime = 0
fps = 0
frames = 0
#physics vars
gravityConst = 10
airResistance = 1.03
maxVelocity = 3

def sfi(string): #string > float > int converter
	try:
		return int(float(string))
	except Exception:
		return 0

highscr = sfi(open("hscr.txt","r").read())

class GameObject():
	def __init__(self,iid,ix,iy,RenderType,typeArgs,objectType,mass):
		self.x = ix
		self.y = iy
		self.width = 0
		self.height = 0
		self.id = iid
		self.type = RenderType
		self.objType = objectType
		self.velocity = 0
		self.upVel = 0
		self.mass = mass
		self.speed = 0
		self.canJump = True
		self.drawDebug = False
		if(self.type == "rect"):
			self.width = typeArgs[0]
			self.height = typeArgs[1]

	def getHitbox(self):
		return (self.x,self.y,self.x+self.width,self.y+self.height)

	def render(self):
		if(abs(self.velocity) > maxVelocity):
			if(self.velocity < 0):
				self.velocity = -maxVelocity
			else:
				self.velocity = maxVelocity
		if(self.type == "rect"):
			rect(self.x,self.y,self.width,self.height)
		if(self.drawDebug):
			rect(self.x + (self.width/2), self.y,2,2,"ff0000")
			rect(self.x + (self.width/2), self.y+self.height,2,2,"ff0000")

	def doCollision(self):
		if(self.x > 400 - self.width):
			self.x = 0
		elif(self.x < 0):
			self.x = 400 - self.width
		fullY = self.y + self.height
		fullX = self.x + self.width
		for obj in objects:
			if(obj.id != self.id):
				if(fullX > obj.x and self.x < obj.x + obj.width):
					if(fullY > obj.y and fullY < obj.y + (obj.height/2)):
						self.y = obj.y - self.height
						self.canJump = True
					if(self.y > obj.y + (obj.height/2) and self.y < (obj.y + obj.height)):
						self.upVel = 0
						self.upSpeed = 0
						self.y = obj.y + obj.height

	def countSpeed(self):
		self.speed = (1/2 * self.mass) * abs(self.velocity)
		self.x += self.speed if self.velocity > 0 else -self.speed
		if(self.velocity != 0) :
			self.velocity = int((self.velocity / airResistance) * 10) / 10
		self.upSpeed = self.upVel / self.mass
		self.y -= self.upSpeed
		self.upVel = (int((self.upVel / airResistance) * 10) / 10) - (0.05 * gravityConst)
		if(abs(self.upVel) > maxVelocity * 50):
			self.upVel = maxVelocity * 50 if self.upVel > 0 else -(maxVelocity * 15)



def rect(x, y, width, height,hexcolor="fff"):
	cnvs.create_rectangle(x, y, x + width, y + height,fill=f"#{hexcolor}")

def line(x,y,x2,y2):
	cnvs.create_line(x,y,x2,y2)

objects.append(GameObject(0,25,25,"rect",(25,55),"player",5,))
objects.append(GameObject(1,-25,335,"rect",(500,30),"ground",-1))
objects.append(GameObject(2,125,160,"rect",(75,35),"tile",-1))

def debug():
	for obj in objects:
		print(obj.objType,": ",obj.y,sep="")
	print(f"Highest (not player): {objects[findHighestObject()].y}")
	print("---------------")

def findHighestObject():
	ind = 1
	for i in range(1,len(objects)):
		if(objects[i].y < objects[ind].y):
			if (objects[i].objType != "player"):
				ind = i
	return ind

def findPlayer():
	for i in range(len(objects)):
		if(objects[i].objType == "player"):
			return i

def highest():
	return objects[findHighestObject()]

def player():
	return objects[findPlayer()]

def moveTilesUp(amount):
	global moveUpValue,totUpVal
	for obj in objects:
		if(obj.type != "player"):
			obj.y += amount
	if(amount > 0):
		if(player().y < highest().y):
			moveUpValue += amount	
			totUpVal += amount

def keypress(event):
	global moveTup
	if(event.char == "d"):
		moveTup[0] = True
	if(event.char == "a"):
		moveTup[1] = True
	if(event.char == "w"):
		moveTup[2] = True


def keyrelease(event):
	global moveTup
	if(event.char == "d"):
		moveTup[0] = False
	if(event.char == "a"):
		moveTup[1] = False
	if(event.char == "w"):
		moveTup[2] = False

gameWindow.bind("<KeyPress>",keypress)
gameWindow.bind("<KeyRelease>",keyrelease)

while True:
	cnvs.delete("all")
	for obj in objects:
		if(obj.objType == "player"):
			if(moveTup[0]):
				obj.velocity += 2
			if(moveTup[1]):
				obj.velocity -= 2
			if(moveTup[2]):
				if(obj.canJump):
					obj.upVel += 150
					obj.canJump = False
			obj.y += gravityConst
			obj.countSpeed()
			obj.doCollision()
			if(obj.y < 0):
				moveTilesUp(abs(obj.y))
				obj.y = 0
			if(obj.y + obj.height > 400):
				moveTilesUp(400-(obj.y+obj.height))
				obj.y = 400 - obj.height
		obj.render()
	if(moveUpValue > 50):
		if(player().y < objects[findHighestObject()].y):
			moveUpValue = 0
			width = random.randint(35,55)
			objects.append(GameObject(iid=len(objects), ix=random.randint(0,400-width), iy=player().y, RenderType="rect", typeArgs=(width,35), objectType="tile", mass=-1))
	cnvs.create_text(50,9,text=f"Stars passed by: {len(objects) - 3}")
	texts = f"Score: {int(totUpVal)}, Highscore: {int(float(highscr))}"
	cnvs.create_text(350,9,text=f"FPS: {fps}")
	cnvs.create_text(int(len(texts)*2.72),21,text=texts)
	if(ticks > 60):
		if(sfi(open("hscr.txt","r").read()) < totUpVal):
			file = open("hscr.txt","w")
			file.write(str(int(totUpVal)))
			file.close()
		ticks = 0
	ticks += 1
	if(int(time.time()) - int(lastTime) >= 1):
		lastTime = int(time.time())
		fps = frames
		frames = 0
	frames += 1
	cnvs.update()
	time.sleep(0.001)
