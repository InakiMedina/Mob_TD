from abc import ABC, abstractmethod 

class Subscriber(ABC):
	@abstractmethod
	def onEvent(self, event):
		pass


class Publisher:
	def __init__(self) -> None:
		self.subscribers = []

	def subscribe(self, s: Subscriber):
		self.subscribers.append(s)

	def unsubscribe(self, s: Subscriber):
		self.subscribers.remove(s)

	def notifySubscribers(self, event):
		for sub in self.subscribers:
			sub.onEvent(event)