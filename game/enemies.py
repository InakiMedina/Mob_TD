import pygame
import math
from abc import ABC
from sprites import *
from save_data import *

class Enemy(AnimatedSprite):
	def __init__(self, x=0, y=0, speed=3, dir=0, hp=30):
		super().__init__(x, y, speed, dir)

		self.alive = True
		self.reachedEnd = False
		self.path = []
		
		self.full_hp = hp
		self.hp = self.full_hp
		self.hp_bar_width = 30
		self.hp_bar_height = 5
		self.hp_bar_distance = 10
		self.hp_bar_thick = 1

	def setPath(self, path):
		self.path = path
		self.i = 0
		self.facePath()

	def facePath(self):
		self.setCenter((self.path[self.i][0], self.path[self.i][1]))
		if self.i >= len(self.path) - 1:
			self.reachedEnd = True
			return
		
		dx = self.path[self.i+1][0] - self.path[self.i][0]
		dy = self.path[self.i][1] - self.path[self.i+1][1]
		if dx == 0:
			dir = math.pi * (0.5 if dy > 0 else 1.5)
		else:
			dir = math.atan (dy / dx) + (0 if dx > 0 else math.pi)
		if dir > 2*math.pi:
			dir -= 2*math.pi
		self.dir = dir
		self.i += 1

		
	def inRange(self, pos, range):
		return math.dist(self.getCenter(), pos) <= range
	
	def hit(self, damage):
		self.hp -= min(self.hp, damage)
		self.alive = self.alive and self.hp > 0
		return not self.alive
	
	def update(self, dt):
		if not self.alive or self.reachedEnd: return
		super().update(dt)

		dist = math.dist(self.path[self.i], self.getCenter())

		if dist < dt:
			self.facePath()

	def draw(self, window):
		if not self.alive:
			return
		super().draw(window)
		white_color = (255, 255, 255)
		green_color = (0, 255, 0)
		pygame.draw.rect(window, white_color, [self.pos[0] - self.hp_bar_width/2 + self.images[0].get_width()/2, self.pos[1] - self.hp_bar_distance, self.hp_bar_width , self.hp_bar_height], self.hp_bar_thick)
		pygame.draw.rect(window, green_color, [self.pos[0] - self.hp_bar_width/2 + self.images[0].get_width()/2 + 2 * self.hp_bar_thick, self.pos[1] - self.hp_bar_distance + 2 * self.hp_bar_thick, (self.hp_bar_width - 4 * self.hp_bar_thick) * self.hp / self.full_hp, (self.hp_bar_height - 4 * self.hp_bar_thick)], self.hp_bar_thick)

class EnemyBuilder():
	def __init__(self) -> None:
		self.factories = {
			"wolf1": ImageFactory("wolf1.png", 0, 0, 32, 32)
		}
		
	def createEnemy(self, type, x, y, dir = 0):
		if type == "wolf1":
			enemy = Enemy(x, y, 0.3, dir, 30)
			enemy.setSpeed(.1)
		else:
			assert False, "unimplemented enemy type {}".format(type)
		
		
		enemy.setImages(self.factories[type][:])
		return enemy

class Horde(GameObject):
	def __init__(self, type, numOfEnemies, numPerGroup, paths, spawnTo, spawnDT):
		self.type = type
		self.numOfEnemies = numOfEnemies
		self.numPerGroup = numPerGroup
		self.paths = paths
		self.spawnTo = spawnTo
		self.spawnDT = spawnDT
		self.spawnI = 0.0
		self.enemyBuilder = EnemyBuilder()

	def update(self, dt):
		if self.numOfEnemies == 0:
			return
		
		self.spawnI += dt 
		if self.spawnI >= self.spawnDT:
			self.spawn()
			self.spawnI -= self.spawnDT

	def spawn(self):
		for i in range(self.numPerGroup):
			enemy = self.enemyBuilder.createEnemy(self.type, 0, 0)
			enemy.setPath(self.paths[i])
			self.spawnTo.append(enemy)
			self.numOfEnemies -= 1
			assert self.numOfEnemies >= 0

	def draw(self, window):
		pass