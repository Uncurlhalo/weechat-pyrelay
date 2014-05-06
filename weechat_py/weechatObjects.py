import relay
import color

class WeechatBuffer():
	def __init__(self, path, name):
		self.lines = []
		self.path = path
		self.name = name

	def __str__(self):
		# since I want to be able to utilize the weechat color codes
		# have a __str__ function is useful since it will allow me to test 
		# parsing the color codes and turning them into logical python
		# for generating color.