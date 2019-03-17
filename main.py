import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pytesseract

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import os

fig, ax = plt.subplots()

class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)
	cwdir = ObjectProperty(None)

class CheckApp(App):
	def build(self):
		self.title='Check'
		root = GridLayout(cols=1)

		# Set Image Label
		label = Label(text='Image', font_size='20sp', size_hint_y=None, height=50, markup=True)
		root.add_widget(label)

		# Set figure area
		ax.axis('off')
		root.add_widget(FigureCanvasKivyAgg(fig))

		# Set Open File button and Analyze button
		btn = GridLayout(cols=2)
		openBTN = Button(text = 'Open', size_hint_y=None, height=50)
		openBTN.bind(on_release=self.show_load)
		btn.add_widget(openBTN)
		analyzeBTN = Button(text = 'Analyze', size_hint_y=None, height=50)
		btn.add_widget(analyzeBTN)

		root.add_widget(btn)
		self.imgG = None
		return root

	def show_load(self, obj):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		#, cwdir=os.getcwd())
		self._popup = Popup(title='Load File', content=content, size_hint=(0.9,0.9))
		self._popup.open()

	def load(self, path, filename):
		if filename:
			img = Image.open(os.path.join(path, filename[0]))
			ax.imshow(np.array(img))
			ax.axis('off')
			fig.canvas.draw()
			self.dismiss_popup()
			self.imgG=img

	def dismiss_popup(self):
		self._popup.dismiss()

Factory.register('LoadDialog', cls = LoadDialog)
if __name__ == '__main__':
	CheckApp().run()