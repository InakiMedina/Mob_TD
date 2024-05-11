from common import *
from sprites import *


class Map(GameObject):
	DEBUG = False

	def __init__(self, x = 0, y = 48, w = 1280 - 128) -> None:
		self.terrain = ImageFactory('terrain.jpeg', 1, 1)
		self.tools = ImageFactory('tools.jpeg', 0, 0)
		self.tileIds = []
		self.paths = []
		self.tiles = GameObjectsList()
		self.decorationData = []
		self.decorations = GameObjectsList()
		self.allInvalid = False
		self.x = x
		self.y = y
		self.w = w
		self.markerOK = ImageSprite(-1000, -1000, self.tools[0])
		self.markerNO = ImageSprite(-1000, -1000, self.tools[1])
		self.level1()
		self.load()

	def level1(self):
		self.tileIds = [0 for i in range(1000)]

		for i in range(6, 31):
			for j in [2, 6, 10, 14, 18]:
				self.tileIds[j*36 + i] = 13
				self.tileIds[(j+1)*36 + i] = 11

		for j in [6, 14]:
			self.tileIds[j*36 + 4] = 14
			self.tileIds[j*36 + 5] = 13
			self.tileIds[j*36 + 30] = 9
			self.tileIds[j*36 + 31] = 12
			self.tileIds[(j+1)*36 + 4] = 10
			self.tileIds[(j+1)*36 + 5] = 9
			self.tileIds[(j+1)*36 + 31] = 17

		for j in [2, 10, 18]:
			self.tileIds[j*36 + 4] = 10
			self.tileIds[j*36 + 5] = 9
			self.tileIds[j*36 + 30] = 13
			self.tileIds[j*36 + 31] = 15
			self.tileIds[(j+1)*36 + 4] = 16
			self.tileIds[(j+1)*36 + 5] = 11
			self.tileIds[(j+1)*36 + 30] = 9
			self.tileIds[(j+1)*36 + 31] = 12

		for j in [4, 5, 8, 9, 12, 13, 16, 17, 20, 21]:
			i = 4 if j in [8, 9, 16, 17] else 30
			self.tileIds[j*36 + i] = 10
			self.tileIds[j*36 + i + 1] = 12
				
		for i in range(6):
			self.tileIds[2*36 + i] = 13
			self.tileIds[3*36 + i] = 11

		self.decorationData.append((49, 33.5*32, 2.5*32))

		x,y = self.x, self.y
		path1 = []
		path2 = []
		for j in [2, 6, 10, 14, 18]:
			if j in [2, 10, 18]:
				first = j==2
				path1.append((-32 if first else x+4.5*32, y+(j+.5)*32))
				path1.append((x+31.5*32,y+(j+.5)*32))
				path2.append((-32 if first else x+5.5*32, y+(j+1.5)*32))
				path2.append((x+30.5*32,y+(j+1.5)*32))
			else:
				path1.append((x+30.5*32,y+(j+.5)*32))
				path1.append((x+5.5*32, y+(j+.5)*32))
				path2.append((x+31.5*32,y+(j+1.5)*32))
				path2.append((x+4.5*32, y+(j+1.5)*32))
		path1.append((x+30.5*32,y+(22)*32))
		path2.append((x+31.5*32,y+(22)*32))
		self.paths = [path1, path2]

		
	def load(self):
		x = self.x
		y = self.y
		for id in self.tileIds:
			self.tiles.append(ImageSprite(x, y, self.terrain[id]))
			x += self.tiles[-1].getImage().get_width()
			if x + 32> self.w:
				y += self.tiles[-1].image.get_height()
				x = self.x

		for d in self.decorationData:
			self.decorations.append(SpriteAdapter((self.terrain[d[0]], d[1], d[2])))

	def update(self, dt):
		pass

	def draw(self, window):
		self.tiles.draw(window)	
		self.decorations.draw(window)
		self.markerOK.draw(window)
		self.markerNO.draw(window)
		if Map.DEBUG:
			for path in self.paths:
				pygame.draw.lines(window, (255, 0, 0), False, path, 1)
	
	def validTile(self, tid):
		return not self.allInvalid and self.tileIds[tid] in [0]
	
	def pos2tile(self, pos):
		tx = (pos[0]-self.x)//32
		ty = (pos[1]-self.y)//32
		tid = ty*36+tx
		return None if tid < 0 or tid >= len(self.tileIds) else tid
	
	def tile2pos(self, tid):
		return (self.x + 32 * (tid % 36), self.y + 32 * (tid // 36))

	def onMouseMove(self, pos):
		tid = self.pos2tile(pos)
		if not tid:
			self.markerNO.setPos((-1000, -1000))
			self.markerOK.setPos((-1000, -1000))
			return
		
		marker,nomarker = (self.markerOK,self.markerNO) if self.validTile(tid) else (self.markerNO, self.markerOK)
		marker.setPos(self.tile2pos(tid))
		nomarker.setPos((-1000, -1000))

	def setAllInvalid(self, allInvalid):
		self.allInvalid = allInvalid