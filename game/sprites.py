import pygame
import os
from common import *
import math
import json

class Sprite(GameObject):
	def __init__(self, x = 0, y = 0, speed = 0, dir = 0) -> None:
		self.setPos((x, y))
		self.speed = speed
		self.dir = dir

	def copy(self):
		return Sprite(None, self.pos[0], self.pos[1])

	def setPos(self, pos):
		self.pos = pos

	def setSpeed(self, speed):
		self.speed = speed

	def update(self, dt):
		if self.speed == 0:
			return
		x = self.pos[0] + dt*self.speed*math.cos(-self.dir)
		y = self.pos[1] + dt*self.speed*math.sin(-self.dir)
		self.setPos((x, y))

	def draw(self, window):
		pass


class ImageSprite(Sprite):
	def __init__(self, x=0, y=0, speed = 0, dir = 0 , image = None) -> None:
		super().__init__(x, y, speed, dir)
		self.filename = None
		self.image = image
		
	def setFileName(self, filename):
		self.filename = filename
		self.setImage(pygame.image.load(os.path.join('images', filename)).convert_alpha())

	def setImage(self, image):
		self.image = image

	def getImage(self):
		return self.image

	def draw(self, window):
		if (self.image):
			window.blit(self.image, self.pos)

	def setCenter(self, center):
		self.pos = center if not self.image else (center[0]-self.image.get_width()/2, center[1]-self.image.get_height()/2)
	
	def getCenter(self):
		return self.pos if not self.image else (self.pos[0]+self.image.get_width()/2, self.pos[1]+self.image.get_height()/2)


class ImageFactory():
	def __init__(self, filename, border = 1, gap = 1, w = 32, h = 32):
		self.map = pygame.image.load(os.path.join("images", filename)).convert_alpha()
		self.mapWidth = self.map.get_width()
		self.mapHeight = self.map.get_height()
		self.border = border
		self.gap = gap
		self.w = w
		self.h = h
		self.images = []
		self.splitMap()

	def splitMap(self):
		y = self.border

		while (y + self.h <= self.mapHeight):
			x = self.border

			while (x + self.w <= self.mapWidth):
				self.images.append(self.map.subsurface(x, y,self.w, self.h))
				x += self.w + self.gap

			y += self.h + self.gap	

	def __getitem__(self, *args):
		return self.images[args[0]].copy()

class AnimatedSprite(Sprite):
	def __init__(self, x=0, y=0, speed = 0, angle = 0, animationSpeed = 0.01) -> None:
		super().__init__(x, y, speed, angle)
		self.images = []
		self.imageI = 0.0
		self.animationSpeed = animationSpeed
	
	def setCenter(self, center):
		image = None if len(self.images) == 0 else self.images[0]
		self.pos = center if not image else (center[0]-image.get_width()/2, center[1]-image.get_height()/2)
	
	def getCenter(self):
		image = None if len(self.images) == 0 else self.images[0]
		return self.pos if not image else (self.pos[0]+image.get_width()/2, self.pos[1]+image.get_height()/2)

	def setImages(self, images):
		self.images = images

	def update(self, dt):
		super().update(dt)
		self.imageI += dt * self.animationSpeed
		while self.imageI >= len(self.images):
			self.imageI -= len(self.images)
		
	def draw(self, window):
		window.blit(self.images[int(self.imageI)], self.pos)
