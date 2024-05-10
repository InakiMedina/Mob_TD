from abc import ABC
import json

class save_data(ABC):

	def readJsonFile(self, filename, tag):
		f = open(filename, 'r')
		json_data = f.read()
		return json_data[tag]

	def writeJsonFile(self, filename, object, tag):
		f = open(filename, 'w')
		json_data = json.loads(f)
		json_data[tag].append(object)
		json.dump(json_data, f, )
		