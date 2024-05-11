import pygame
from pygame.locals import *
from common import *
from enemies import *
from player import *
from map import Map

class Level(GameObject):
	def __init__(self, number) -> None:
		self.ended = False
		self.number = number
		self.hordes = GameObjectsList()
		self.enemies = GameObjectsList()
		self.bullets = GameObjectsList()
		self.structs = GameObjectsList()
		self.player = Player(self.enemies, self.bullets)
		self.towerBuilder = TowerBuilder(self.player, self.enemies, self.bullets) 
		self.map = Map()
		self.selTowerType = 'tower1'
		self.lvl1()

	def lvl1(self):
		self.hordes.append(Horde('wolf1', 20, 2, self.map.paths, self.enemies, 500))
		self.player.setCenter((31*32, 23*32))

	def checkFinishLine(self):
		event = {'type': 'none'}
		for e in self.enemies:
			if e.reachedEnd and e.alive:
				e.alive = False
				if self.player.lives > 0:
					self.player.lives -= 1
					event = {'type': 'update_lives', 'lives': self.player.lives}
					return event
		if self.player.isDead():
			self.ended = True
			event = {'type': 'game_ended'}

		return event

	def update(self, dt):
		if self.ended:
			return
		self.map.update(dt)
		self.hordes.update(dt)
		self.enemies.update(dt)
		self.bullets.update(dt)
		self.structs.update(dt)
		self.player.update(dt)

		self.map.setAllInvalid(not self.player.enoughMoneyFor(self.selTowerType))

	
	def draw(self, window):
		self.map.draw(window)
		self.enemies.draw(window)
		self.structs.draw(window)
		self.player.draw(window)
		self.bullets.draw(window)

	def addTower(self, type, tid):
		x,y = self.map.tile2pos(tid)
		tower = ImageSprite(x,y)
		tower.load

	def onMouseMove(self, pos):
		self.map.onMouseMove(pos)

	def onMouseClick(self, pos):
		tid = self.map.pos2tile(pos)
		if not tid or not self.map.validTile(tid):
			return
		corner = self.map.tile2pos(tid)
		self.structs.append(self.towerBuilder.createTower(self.selTowerType, corner[0], corner[1]))
		self.player.boughtTower(self.selTowerType)