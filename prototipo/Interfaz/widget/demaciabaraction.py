from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
kv ='''


BoxLayout:
	padding: 20
	canvas:
		Color:
			rgb: 1,1,1
		Rectangle:
			pos:self.pos
			size:self.size

	BoxLayout:
		padding: 5
		orientation: 'vertical'


		ActionBar:
			pos_hint: {'top': 1}
			ActionView:
				ActionPrevious:
					title: 'Simulador Tools'
					with_previous: False
				ActionOverflow:
				ActionButton:
					text: 'Guardar datos'
				ActionButton:
					text: 'Cobertura'
				ActionButton:
					text: 'resultados'
		BoxLayout:
			padding: 5	
			orientation: 'horizontal'

			BoxLayout:

				padding: 5
				orientation: 'vertical'


				BoxLayout:
					orientation: 'horizontal'			
					Label:
						canvas.before:
							Color:
								rgba: 0,0,.57,.8
							Rectangle:
								pos:self.pos
								size:self.size
						text: "Nivel"
					TextInput:
						multiline: False


				BoxLayout:
					orientation: 'horizontal'
					Label:
						canvas.before:
							Color:
								rgba: 0,0,255,.8
							Rectangle:
								pos:self.pos
								size:self.size
						text: "Radio celdas"
					TextInput:
						multiline: False

				
				
				BoxLayout:
					orientation: 'horizontal'
					Label:
						canvas.before:
							Color:
								rgba: 0,.57,0,.8
							Rectangle:
								pos:self.pos
								size:self.size
						text: "Intensidad puntos Poisson"
					TextInput:
						multiline: False



				Button:
					canvas.before:
						Color:
							rgba: 0,0,1,1
						Rectangle:
							pos:self.pos
							size:self.size
					text: "Calcular"
					
			BoxLayout:
				orientation: 'horizontal'
				padding: 5 


				AnchorLayout:
					anchor_x: 'right'
					anchor_y: 'bottom'
					Button:
						text: 'A1'
						size_hint: 1 , 1
					

'''



class testApp(App):
	def build(self):

		return Builder.load_string(kv)



if __name__ == '__main__':
	testApp().run()



