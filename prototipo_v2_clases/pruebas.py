# import
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
#
import pk_red_dispositivos.celda as pkcel
import utilidades.savedata as persistencia
import pk_modelo_canal.Modelo_CI_UMa as cim

#http://research.iac.es/sieinvens/python-course/source/matplotlib.html #graficar datos
#me ga bru tal https://jakevdp.github.io/PythonDataScienceHandbook/04.05-histograms-and-binnings.html
#https://stackabuse.com/python-data-visualization-with-matplotlib/


def prueba_pk_dispositivos(celdas, radio, intensidad):
	'''Prueba para observar funcionamiento de graficas basicas'''
	intensidad = intensidad/radio**2
	colmena = pkcel.Celdas(celdas, radio, distribucion=("ppp", intensidad))
	colmena.ver_estaciones_base()
	colmena.ver_celdas()
	colmena.ver_sectores()
	colmena.ver_usuarios()

	# colmena.ver_todo()
	# plt.axis("equal")
	# plt.grid(True)
	# plt.savefig("base_datos/img_pruebas/ppp_4.png")
	# plt.show()


def prueba_funcion_aux(cordx, cordy):
	pass

def prueba_guardar_datos():
	'''Prueba para observar comportamiento de guardado de datos'''
	# procedimiento
	# 1. obtener todos los arrays en la posision x o y.
	# 2. juntar todos los arrays en un solo array
	# 3. usar metodo correspondiente para guardar el array
	# 4. abrir el archivo con el metodo correspondiente.
	# Nota: resulta un paso extra por el hecho
	# de que los datos ya estan juntos en una sola variable, asi:
	#  [c1x1, c1x2, c1x3,...,c1xn,c2x2,c2x3,...,c2xn,.. ] pero no
	# estan separados por celda, esta es la razon de procesamiento
	radio = 20
	intensidad = 7
	intensidad = intensidad/radio**2
	celdas = 13
	frecuencia= 28000000000

	colmena = pkcel.Celdas(celdas, radio, distribucion=("ppp", intensidad))
	# colmena.cluster --> se encuentra cada celda, y cada celda tiene las coordenadas x.
	# si iteramos sobre cada celda y obtenemos cada x, los podemos agrupar en una lista
	# en lo que podemos aplicar el metodo presente en savedata.
	print(len(colmena.cluster))
	#data = colmena.cluster[0].user_x
	#print(data)

	coordenadas_x = [celula.user_x for celula in colmena.cluster]
	coordenadas_y = [celula.user_y for celula in colmena.cluster]

	data_x = coordenadas_x[0] #inicializamos el primer valor
	data_y = coordenadas_y[0]

	tamano_cluster=len(coordenadas_x)
	for i in range(tamano_cluster-1):
		try:
			data_x=np.column_stack((data_x,coordenadas_x[i+1]))
			data_y=np.column_stack((data_y,coordenadas_y[i+1]))
		except Exception as esx:
			print(esx) #esta excepcion ocurre por el [i+1], cuando llega a 3+1=4; de 0 a 4, el 4 seria el 5

	header_x="cel1, cel2, ..., cel{}".format(celdas)
	nombre_archivo=persistencia.nombre_extension("base_datos","txt","reconocimientox")
	nombre_archivo2=persistencia.nombre_extension("base_datos","txt","reconocimientoy")
	persistencia.guardar_archivo(data_x, nombre_archivo, header_x)
	persistencia.guardar_archivo(data_y, nombre_archivo2, header_x)


def prueba_distancia_celdas():
	'''Funcion de prueba para observar el comportamiento del algoritmo de distancias'''
	#frecuencia en Herz y distancia en Metros.
	radio = 20
	intensidad = 3
	intensidad = intensidad/radio**2
	celdas = 2
	colmena = pkcel.Celdas(celdas, radio, distribucion=("ppp", intensidad))
	print(colmena.cluster[0].distancias)
	print(colmena.cluster[1].distancias)
	colmena.ver_celdas()
	colmena.ver_usuarios()
	colmena.ver_estaciones_base()
	plt.figure(2)
	plt.bar(np.arange(len(colmena.cluster[0].distancias)),colmena.cluster[0].distancias)
	#plt.axis("equal")
	plt.grid(True)
	plt.show()
	

#las funciones nuevas deben ser creadas de arriba hacia abajo. Abajo las mas nuevas.
def pruebas_modelo_canal_umi():
	frecuencia = 28000000000
	frecuenciaGHz= frecuencia/1000000000
	sigma= 4
	PerdidasProp=0
	Sigma_Xn=4
	alpha_n=3
	PerdidasProp=0
	PerdidasPropi=0
	Ppl=[]
	for d in colmena.cluster[0].distancias:
		PerdidasPropi=cim.modeloci(alpha_n,d,Sigma_Xn,frecuencia)
		PerdidasProp=np.add(PerdidasPropi)
		#print(PerdidasProp.shape)
		#np.array(len(colmena.cluster[0].distancias),)
		#print(PerdidasProp)
	#disarray=np.arange(len(distanciaU))
	print(PerdidasProp)
	#print("oleee ". disarray)
	#plt.bar(np.arange(len(colmena.cluster[0].distancias)),colmena.cluster[0].distancias)
	plt.figure(3)
	plt.bar(np.arange(len(PerdidasProp)),PerdidasProp)
	ptl.grid(True)
	plt.show()


def prueba_perdidas_propagacion(radio,frecuencia,distancias):
	'''Funcion de prueba para crear las perdidas basicas (espacio libre)'''
	#pasos:
	#1.
	#2.
	#3.
	#4.
	PerdidasFSPL = cim.FSPL(frecuencia) #el nombre de la ecuacion debe ser mas especica: free_space_loss()
	print("PERDIDAS ESPACIO LIBRE : ",PerdidasFSPL)

if __name__=="__main__":
	#REGLAS:
	#0 [critico]. Las pruebas en if name, deben ir comentadas por prueba 1., prueba 2., ..., prueba n.
		#0.1 Si se necesitan hacer mas de una prueba con la funcion, pasar de 1 a 1.1 a 1.2, etc.
		#en el numeral de la prueba
		
	#1. LAS FUNCIONES DE PRUEBA NO RECIBEN PARAMETROS, Excepto en el siguiente caso:
		#Que la funcion sea definida con parametros y al llamarla sea explicito los
		#parametros y los valores que reciben
		# funcion(parametro=valor1, parametro2=valor, etc)
		#ver prueba 1.
	#2. LAS VARIABLES VAN EN MINUSCULA
	#3. LOS NOMBRE DE FUNCIONES, MINUSCULA
	#4. LAS INSTANCIAS DE CLASE, MINUSCULA
	#5. LOS NOMBRES DEBEN SER ESPECIFICOS Y SEPARADOS POR: _ así:
		#EjemploDeFUNCION ---> x , ejemplo_de_funcion ---> bieeeen
		#fdp ----------------> x , funcion_de_prueba ----> mega bieeeen
		#etc.

	
	#Prototipos:
	#prueba 1.
	# prueba_pk_dispositivos(celdas=2,radio=20,intensidad=5)
	
	#prueba 2.
	# pkcel.modulo_coordenadas.coordenadas_nceldas(3,4)
	
	#prueba 3.
	#prueba_guardar_datos()
	
	#prueba 4.
	prueba_distancia_celdas()

	#prueba 5. 
	#prueba_Perdidas_propagacion(12,28,500)
	#prueba 5.1
	#prueba_Perdidas_propagacion(radio,frecuencia)
	
	#prueba 6.
	#

else:
	print("Modulo <escribir_nombre> importado")
