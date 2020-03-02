#Implemtenado por Michael phikubo. 
#Script para generar puntos que simulan la posición de UEs en el espacio, mediante el proceso Poisson (Point Processs Poisson)
#El script, presenta dos tipos de pruebas: se generan puntos con la libreŕia scipy y con numpy. Los resultados no difieren.
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import math
import time

def distribuir_en_sector():
	'''Funcion. Distribuye usuarios en un sector. Retorna una matriz por celda mas no por sector.'''
	pass

def distribuir_en_celdas(r, x_origen, y_origen, intensidad):
	'''Funcion principal. Distribuye un conjunto de usuarios en un conjunto de celdas. El resultado
	es las coordenadas de usuarios por celda, empaquetados en una matriz. Con esta matriz se 
	calcula la distancia. Retorna una matriz de matrices (matriz de celda).'''

	area_total=np.pi*r**2
	cantidad_de_puntos = np.random.poisson(intensidad*area_total) 
	#de esta forma todas las celdas tiene el mismo numero de usuarios.
	#llamar funcion
	print("ppp: puntos de entrada ", len(x_origen))
	
	'''Recordar que x_origen y y_origen de esta funcion tiene un formato dinamico
	esto debe ser tenido en cuenta como se hizo para la sectorizacion.(revisar si 
	lo dicho anterior, es verdad. parece que no)'''
	lista_x=[]
	lista_y=[]

	for x,y in zip(x_origen,y_origen):
		#print(x,y)
		coordenada_x, coordenada_y = distribuir_usuarios(r, cantidad_de_puntos) #genera puntos en un circulo de origen 0,0
		###################para trasladar el circullo a un lugar deseado, se suman los puntos cartesianos x,y a los del circulo
		###########Ademas se hace dentro del for, para que genere puntos distintos en cada iteracion.
		#print("antes: ", coordenada_x, "sumando ", x)
		coordenada_x=coordenada_x + x 
		
		lista_x.append(coordenada_x)
		#print("dapues: ", coordenada_x)
		coordenada_y=coordenada_y + y
		lista_y.append(coordenada_y)
	#e.g., para celdas=19, hay cantidad_de_puntos distribuidos con ppp.
	
	#convierto la lista de array en array de listas #issue: no sirve .shape
	'''Por cada coordenada x,y, existen n usuarios de coordenadas cordenada_x,cordenada_y'''
	coordenada_np_x=np.asarray(lista_x)
	coordenada_np_y=np.asarray(lista_y)
	return coordenada_np_x, coordenada_np_y


def distribuir_usuarios(r, cantidad_puntos):
	'''Funcion secundaria a principal. Copia el comportamiento de distribuir_circuo, pero en una forma modular'''
	#calcular theta y rho en esta funcion, garantiza que sean distintos.
	try:
		theta=2*np.pi*np.random.uniform(0,1,cantidad_puntos)
		rho=r*np.sqrt(np.random.uniform(0,1,cantidad_puntos))
		coord_x = rho * np.cos(theta)
		coord_y = rho * np.sin(theta)
	except Exception as ex:
		print(ex)
	return coord_x, coord_y



def distribuir_circulo(r, x_origen, y_origen, intensidad):
	'''Funcion. Genera las coordenadas de un conjunto de usuarios confinados
	en un espacio deseado (circulo) y de intensidad (densidad) intensidad, y ubicados en un origen'''

	#Simulation window parameters
	#r=1;  #radius of disk
	#centre of disk
	area_total=np.pi*r**2; #area of disk
	
	#Point process parameters
	#intensidad=1; #intensity (ie mean density) of the Poisson process
	#print("lambda: ", intensidad)
	
	#Simulate Poisson point process. Este proceso debe ser independiente de maint si se desea que sea el mismo número de puntos.
	numero_de_puntos = np.random.poisson(intensidad*area_total);#Poisson number of points
	print("Numero de points: ", numero_de_puntos)
	theta=2*np.pi*np.random.uniform(0,1,numero_de_puntos); #angular coordinates 
	rho=r*np.sqrt(np.random.uniform(0,1,numero_de_puntos)); #radial coordinates 
	
	#Convert from polar to Cartesian coordinates
	coordenada_x = rho * np.cos(theta);
	coordenada_y = rho * np.sin(theta);
	
	#Shift centre of disk to (x_origen,y_origen) 
	coordenada_x=coordenada_x+x_origen; coordenada_y=coordenada_y+y_origen;
	
	#Plotting
	#plt.scatter(coordenada_x,coordenada_y, edgecolor='b', facecolor='none', alpha=0.5 );
	#plt.xlabel("x"); plt.ylabel("y");
	#plt.axis('equal');
	#plt.grid(True)
	#plt.savefig("test2.png")
	return coordenada_x,coordenada_y

   
def prueba1():
	x=5;y=10
	intensity=100/radio**2
	x,y=distribuir_circulo(radio, x,y, intensity)
	plt.plot(x,y,"ro")

def prueba2():
	pass

if __name__ == "__main__":
	print("ppp fix function")
	radio=100 
	
	 
	#requisite: create n disk or radius r.
	#radio: radius of disk. origen: coordinates.  
	prueba1()
	
	plt.show()

else:
    print("importado:ppp")
