class FileLetters:

	def __init__(self, filename, letters = []):
		self.filename = filename
		self.letters = letters

	def addToList(self, obj):
		self.letters.append(obj)

	def sortLetters(self):
		oldOrder = self.letters
		newOrder = [(i.minX, i) for i in oldOrder]
		newOrder.sort()
		newOrder = [i[1] for i in newOrder]
		self.letters = newOrder

	def stand_dev():
		pass