from abc import ABC, abstractmethod 
import pygame
from utils import *

#game object interface
class GameObject(ABC):
	@abstractmethod
	def update(self, dt):
		pass
	
	@abstractmethod
	def draw(self, window):
		pass

class GameObjectAdapter(Subscriber):
	def __init__(self, go: GameObject) -> None:
		self.go = go

	def onEvent(self, event):
		if event['type'] == 'draw':
			self.go.draw(event['window'])
		elif event['type'] == 'update':
			self.go.update(event['dt'])
		

class GameObjectsList(GameObject, Publisher):
	def update(self, dt):
		self.notifySubscribers({
			'type': 'update',
			'dt': dt
		})

	def draw(self, window):
		self.notifySubscribers({
			'type': 'draw',
			'window': window
		})


	def append(self, obj: GameObject):
		self.subscribe(GameObjectAdapter(obj))

	def __getitem__ (self, *args):
		if type(args[0]) == tuple:
			return map(lambda s : s.go, self.subscribers[args[0]])
		else:
			return self.subscribers[args[0]].go