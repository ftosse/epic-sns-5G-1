#import
import numpy as np
import math
#como esto no usa submodulos, no necesito hacer try catch en esos modulos.
#en el futuro si puede ocurrir, asi que:

#try:
	#aqui van los submodulos.
#except:
	#pass


class Modelo_canal:
	"""Clase que define el modelo del canal, calcula las perdidas del sistema"""
	def __init__(self, frecuencia, distancia):
		self.frecuencia=frecuencia
		self.distancia=distancia
		self.path_loss=0


	def perdidas_espacio_libre_ghz(self):
		'''Funcion que calcula las perdidas de espacio libre en dB'''
		self.path_loss=92.4+20*np.log10(self.frecuencia)+20*np.log10(self.distancia)


def prueba_interna_path_loss():
	'''Funcion que prueba el concepto de perdidas de espacio libre con numpy'''
	freq=10 #en gigas
	distancias_km=np.array([0.1, 1, 2, 3, 4, 5, 6])
	modelo=Modelo_canal(freq, distancias_km)
	modelo.perdidas_espacio_libre_ghz()
	l_bs=modelo.path_loss
	print(l_bs)



if __name__=="__main__":
	#Prototipo:
	#import #aqui van los submodulos nuevamente para envitar errores
	
	#prueba interna 1.
	prueba_interna_path_loss()
else:
	print("Modulo <escribir_nombre> importado")
