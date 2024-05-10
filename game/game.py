import pygame
from pygame.locals import *
from common import GameObject
from level import Level
from ui import UI
from utils import *

class Game (GameObject, Publisher):
	def __init__(self) -> None:
		super().__init__()
		pygame.init()
		self.window_width = 1280
		self.window_height = 800
		self.window = pygame.display.set_mode((self.window_width, self.window_height))
		pygame.display.set_caption("My First Game")
		self.running = True
		self.level = Level(1)
		self.ui = UI()
		self.subscribe(self.ui)
		self.notifySubscribers({'type': 'update_lives', 'lives': self.level.lives})

	def run(self):
		self.lastFrameTime = pygame.time.get_ticks()
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:  
					self.running = False
			currentTime = pygame.time.get_ticks()
			dt = currentTime - self.lastFrameTime
			self.lastFrameTime = currentTime
			self.update(dt)
			self.draw(self.window)
			pygame.display.update()

	def update(self, dt):
		self.level.update(dt)
		self.notifySubscribers(self.level.checkFinishLine())
		

	def draw(self, window):
		window.fill([0, 0, 0])
		self.level.draw(window)
		self.ui.draw(window)

	
if __name__ == '__main__':
	game = Game()
	game.run()