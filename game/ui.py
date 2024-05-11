import pygame
import pygame.freetype
import math
from common import *

class UI(GameObject, Subscriber):
	def __init__(self, level = 1, money = 500, lives = 5) -> None:
		self.font = pygame.font.match_font('franklingothicmedium')
		self.uiFont = pygame.freetype.Font(self.font, 24)
		self.buttons = [{'text': self.uiFont.render('Start', (255, 255, 255))[0], 
				   		 'rect': pygame.Rect(700, 9, 120, 30),
						 'background': (51, 51, 255),
						 'action': None}]
		self.time = 0
		self.timeText, _ = self.uiFont.render(f'Time: 00:00', (255, 255, 255))
		self.setMoney(money)
		self.setLives(lives)
		self.setLevel(level)

	def setLives(self, lives):
		self.lives = lives
		self.livesText,_ = self.uiFont.render(f'Lives: {self.lives}', (255, 255, 255)) 
	
	def setMoney(self, money):
		self.money = money
		self.moneyText,_ = self.uiFont.render(f'Money: ${self.money}', (255, 255, 255))

	def setLevel(self, level):
		self.level = level 
		self.levelText,_ = self.uiFont.render(f'Level {self.level}', (255, 255, 255))

	def setTime(self, time):
		if time - self.lastT >= 1000:
			self.lastT = time % 1000
			timeInS = math.floor(time/1000)
			s = timeInS % 60
			sU = s%10
			sD = math.floor(s/10)
			m = math.floor(timeInS / 60)
			mU = m%10
			mD = math.floor(m/10)
			timeString = f'{mD}{mU}:{sD}{sU}'
			self.timeText, _ = self.uiFont.render(f'Time: {timeString}', (255, 255, 255))


	def onEvent(self, event):
		if event['type'] == 'update_lives':
			self.setLives(event['lives'])
		elif event['type'] == 'update_money':
			self.setMoney(event['money'])

	def update(self, dt):
		pass

	def draw(self, window):
		pygame.draw.rect(window, (64, 64, 64), pygame.Rect(0, 0, 1280, 48))
		pygame.draw.rect(window, (64, 64, 64), pygame.Rect(1280-128, 48, 128, 800-48))

		window.blit(self.levelText, (100, 24 - self.levelText.get_height()/2))
		window.blit(self.livesText, (300, 24 - self.livesText.get_height()/2))
		window.blit(self.moneyText, (500, 24 - self.moneyText.get_height()/2))
		window.blit(self.timeText, (900, 24 - self.timeText.get_height()/2))

		for button in self.buttons:
			pygame.draw.rect(window, button['background'], button['rect'])
			window.blit(button['text'], (button['rect'][0] + button['rect'][2]/2 - button['text'].get_width()/2, 
										 button['rect'][1] + button['rect'][3]/2 - button['text'].get_height()/2))


	

		
