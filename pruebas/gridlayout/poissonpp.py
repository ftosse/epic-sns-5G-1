#Implemtenado por Michael phikubo. 
#Script para generar puntos que simulan la posición de UEs en el espacio, mediante el proceso Poisson (Point Processs Poisson)
#El script, presenta dos tipos de pruebas: se generan puntos con la libreŕia scipy y con numpy. Los resultados no difieren.
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import math
import time

'''
Phikubo says-> No todos los comentarios pertenecen a la receta. Algunos comentarios en ingles fueron puestos por Phikubo para pruebas y documentación.
Estado: En proceso.
recipe: https://hpaulkeeler.com/simulating-a-poisson-point-process-on-a-disk/, https://stackoverflow.com/questions/31778995/how-to-generate-a-homogeneous-poisson-point-process-in-a-circle
https://en.wikipedia.org/wiki/Poisson_point_process, https://hpaulkeeler.com/poisson-point-process/
recomendations from recipe:

Resultados:
	
'''

def maint(r, xx0, yy0, lambda0):
	print("ppp")
	#Simulation window parameters
	#r=1;  #radius of disk
	#centre of disk
	areaTotal=np.pi*r**2; #area of disk
	
	#Point process parameters
	#lambda0=1; #intensity (ie mean density) of the Poisson process
	print("lambda: ", lambda0)
	
	#Simulate Poisson point process. Este proceso debe ser independiente de maint si se desea que sea el mismo número de puntos.
	numbPoints = np.random.poisson(lambda0*areaTotal);#Poisson number of points
	print("Numero de points: ", numbPoints)
	theta=2*np.pi*np.random.uniform(0,1,numbPoints); #angular coordinates 
	rho=r*np.sqrt(np.random.uniform(0,1,numbPoints)); #radial coordinates 
	
	#Convert from polar to Cartesian coordinates
	xx = rho * np.cos(theta);
	yy = rho * np.sin(theta);
	
	#Shift centre of disk to (xx0,yy0) 
	xx=xx+xx0; yy=yy+yy0;
	
	#Plotting
	#plt.scatter(xx,yy, edgecolor='b', facecolor='none', alpha=0.5 );
	#plt.xlabel("x"); plt.ylabel("y");
	#plt.axis('equal');
	#plt.grid(True)
	#plt.savefig("test2.png")
	return xx,yy
	#plt.show()
	#
	'''

    tamano=1000
    y_axis=10
    #t = np.linspace(0.0, 10.0, N, endpoint=False)
    pppx=np.random.poisson(y_axis,tamano)
    pppy=np.random.poisson(y_axis,tamano)
    x=tamano*np.random.random(tamano)
    #
    plt.plot(pppx, pppy, '.')
    
    plt.xlabel("Prueba de Puntos con distribución Poisson")
    plt.ylabel("y(t)")
    plt.title('Poisson Process Point', fontsize=16, color='r')
    plt.grid(True)
    plt.show()'''
    

if __name__ == "__main__":
	print("ppp fix function")
	radio=1 
	x=5;y=10
	 
	#requisite: create n disk or radius r.
	#radio: radius of disk. origen: coordinates.  
	maint(radio, x,y, intensity)
else:
    print("importado:ppp")
