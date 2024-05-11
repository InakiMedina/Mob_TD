from sprites import *

class Player(ImageSprite, Subscriber, Publisher):
    def __init__(self, x=0, y=0, time=0, lives=5, money=500) -> None:
        super().__init__(x, y)
        Publisher.__init__(self)
        self.setFileName('player.png')
        self.time = time
        self.lives = lives
        self.setMoney(money)
		
    def setMoney(self, money):
        self.money = money
        self.notifySubscribers({
			'type': 'update_money',
			'money': money
        })
		
    def boughtTower(self, tower):
        self.setMoney(self.money - 200)

    def isDead(self):
        return self.lives == 0
	
    def enoughMoneyFor(self, tower):
        return self.money >= 200
	
    def onEvent(self, event):
        if event['type'] == 'killed':
            self.setMoney(self.money + 20)


class Bullet(ImageSprite, Publisher):
	def __init__(self, pos, speed, enemy):
		ImageSprite.__init__(self, pos[0], pos[1])
		Publisher.__init__(self)
		self.speed = speed
		self.enemy = enemy
		self.alive = True
		self.damage = 15
		self.faceEnemy()
		
	def update(self, dt):
		if not self.alive: return
		super().update(dt)
		
		if not self.enemy.alive:
			self.die()
			return

		dist = math.dist(self.enemy.getCenter(), self.getCenter())
		if dist < dt:
			self.hitEnemy()
			return
		
		self.faceEnemy()
		
	def draw(self, window):
		if not self.alive: return
		super().draw(window)
			
	def die(self):
		self.alive = False
		self.notifySubscribers({
			'type': 'died',
			'go': self
        })
			
	def hitEnemy(self):
		self.alive = False
		if self.enemy.hit(self.damage):
			self.notifySubscribers({
                'type': 'killed',
                'go': self
            })

	def faceEnemy(self):
		bx, by = self.getCenter()
		ex, ey = self.enemy.getCenter()
		
		dx = ex - bx
		dy = by - ey
		if dx == 0:
			dir = math.pi * (0.5 if dy > 0 else 1.5)
		else:
			dir = math.atan (dy / dx) + (0 if dx > 0 else math.pi)
		if dir > 2*math.pi:
			dir -= 2*math.pi
		self.dir = dir
	
    
class Tower(ImageSprite):
	def __init__(self, player, enemies, bullets, bulletType, reloadTime, range):
		super().__init__(0, 0)
		self.bulletType = bulletType
		self.fireDT = reloadTime # Begin ready to fire
		self.reloadTime = reloadTime
		self.range = range
		self.player = player
		self.enemies = enemies
		self.bullets = bullets
		
	def moveToTile(self, pos, size):
		newPos = (pos[0]+size[0]/2 - self.image.get_width()/2, pos[1] + size[1] - self.image.get_height())
		self.setPos(newPos)
		
	def update(self, dt):
		self.fireDT += dt
		if self.fireDT >= self.reloadTime:
			if self.fireBullet():
				self.fireDT = 0
				
	def draw(self, window):
		super().draw(window)
		pygame.draw.circle(window, 'purple', self.getCenter(), self.range, 1)
				
	def fireBullet(self):
		for enemy in self.enemies:
			if enemy.alive and enemy.inRange(self.getCenter(), self.range):
				bullet = Bullet(self.getCenter(), 0.2, enemy)
				bullet.setFileName('bullet1.jpg')
				bullet.subscribe(self.player)
				self.bullets.append(bullet)
				return True
		return False
			
class TowerBuilder():
	def __init__(self, player, enemies, bullets):
		self.player = player
		self.enemies = enemies
		self.bullets = bullets
		self.factories = {
			"tower1": ImageSprite("0, 0")
		}
		for factory in self.factories:
			self.factories[factory].setFileName(factory + '.png')
		
	def createTower(self, type, x, y):
		if type == "tower1":
			tower = Tower(self.player, self.enemies, self.bullets, 'bullet1', 800, 100)
		else:
			assert False, "unimplemented tower type {}".format(type)
		
		tower.setImage(self.factories[type].image)
		tower.moveToTile((x,y),(32,32))
		return tower