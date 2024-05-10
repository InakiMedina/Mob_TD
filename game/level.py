import pygame
from pygame.locals import *
from common import *
from enemies import *
from map import Map

class Level(GameObject):
	def __init__(self, number) -> None:
		self.ended = False
		self.number = number
		self.hordes = GameObjectsList()
		self.enemies = GameObjectsList()
		self.structs = GameObjectsList()
		self.map = Map()
		self.time = 0
		self.lives = 5
		self.money = 300
		self.lvl1()

	def lvl1(self):
		self.hordes.append(Horde('wolf1', 20, 2, self.map.paths, self.enemies, 500))

	def checkFinishLine(self):
		event = {'type': 'none'}
		for e in self.enemies:
			if e.reachedEnd and e.alive:
				e.alive = False
				if self.lives > 0:
					self.lives -= 1
					event = {'type': 'update_lives', 'lives': self.lives}
					return event
		if self.lives == 0:
			self.ended = True
			event = {'type': 'game_ended'}

		return event

	def update(self, dt):
		if self.ended:
			return
		self.map.update(dt)
		self.hordes.update(dt)
		self.enemies.update(dt)
		self.structs.update(dt)
	
	def draw(self, window):
		self.map.draw(window)
		self.enemies.draw(window)
		self.structs.draw(window)

