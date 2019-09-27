#import


#x+y+z=0
def patron_dado_xy(x,y):
	#x+y=-z
	return -1*(x+y)
def patron_dado_yz(y,z):
	#y+z=-x
	return -1*(y+z)
def patron_dado_zx(z,x):
	#z+x=-y
	return -1*(z+x)
	
def patron_dado_ab(a,b):
	#funcion que resume las anteriores
	return -1*(a+b)
#		
def patron_circular(nivel):
	'''Prueba de concepto. Genera las coordenadas axiales de acuerdo a patron encontrado'''
	#no implementado
	origen=[0,0,0]
	total_celdas=nivel*6
	patron=[[0,0,0] for i in range(total_celdas)]
	#permite cambiar el slicing de cada for para ajustar al nivel deseado, y conformar una sola funcion
	
	#how to generate this dinamicaly?
	if nivel == 1:
		inicio=[0, nivel+1, 3*nivel+1]
		final =[nivel+1,	3*nivel+1, len(patron)]
	elif nivel==2:
		inicio=[0, nivel+2, 3*nivel+2]
		final =[nivel+1, 3*nivel+1, len(patron)+1]

	print("start of experimento circular grid")
	#output should be: [1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0]
	if nivel == 4:
		for y,p in zip(range(nivel+1), patron[0:nivel+1]):
			#print(-nivel)
			#print(y)
			#p corresponde al item [a,b,c] dentro de la lista de patron(total_celdas)
			#print(p)
			#0,1,2 corresponden a: a,b,c respectivamente
			p[1]=y
			p[2]=-nivel
			p[0]=patron_dado_ab(p[1],p[2])
			#resultados
			#print(p)
			#print(patron)
			
		for z,p in zip(range(nivel+1), patron[nivel+1:3*nivel+1]):
			#print(-nivel)
			p[2]=z
			p[0]=-nivel
			p[1]=patron_dado_ab(p[2],p[0])
			#print(p)
			#print(patron)

		for x,p in zip(range(nivel+1),patron[3*nivel+1:len(patron)]):
			#print(x)
			p[0]=x
			p[1]=-nivel
			p[2]=patron_dado_ab(p[0],p[1])
		print(patron)
	#output should be: 
	#[1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0]
	#[],[],[],[],[],[],[],[],[],[],[],[]
	'''Para que las inserciones sean dinámicas más allá de 2, debe incluirse en un for el bloque de inserción'''
	if nivel > 0:
		#inicializo variables para obtener el estado final al término de cada ciclo for.
		y=0
		x=0
		z=0
		ultima_variable=0
		#star of
		for y,p in zip(range(nivel+1), patron[inicio[0]:final[0]]):
			#print(-nivel)
			#print(y)
			#p corresponde al item [a,b,c] dentro de la lista de patron(total_celdas)
			#print(p)
			#0,1,2 corresponden a: a,b,c respectivamente
			p[1]=y
			p[2]=-nivel
			p[0]=patron_dado_ab(p[1],p[2])
			ultima_variable=p[0]
			#resultados
			#print(p)
			#print(patron)
			#patron[nivel+1]=y
		if nivel == 1:
			pass
		else:
			print("test 1", patron[nivel+1])
			patron[nivel+1][1]=y
			patron[nivel+1][0]=ultima_variable-1
			patron[nivel+1][2]=patron_dado_ab(patron[nivel+1][1],patron[nivel+1][0])
			print("y: ",y)	
			print("y test", patron[nivel+1])
		#start of
		for z,p in zip(range(nivel+1), patron[inicio[1]:final[1]]):
			#print(-nivel)
			p[2]=z
			p[0]=-nivel
			p[1]=patron_dado_yz(p[2],p[0])
			ultima_variable=p[1]
			print(ultima_variable)
			#print(p)
			#print(patron)
		if nivel == 1:
			pass
		else:
			print("test 2", patron[3*nivel+1])
			patron[3*nivel+1][2]=z
			patron[3*nivel+1][1]=ultima_variable-1
			patron[3*nivel+1][0]=patron_dado_ab(patron[3*nivel+1][2],patron[3*nivel+1][1])
			print("z: ",z)	
			print("z test", patron[3*nivel+1])

		for x,p in zip(range(nivel+1),patron[inicio[2]:final[2]]):#atencion, patron+1?
			#print(x)
			p[0]=x
			p[1]=-nivel
			p[2]=patron_dado_ab(p[0],p[1])
			ultima_variable=p[2]
		
		if nivel == 1:
			pass
		else:
			print("test", patron[len(patron)-1])
			patron[len(patron)-1][0]=x
			patron[len(patron)-1][2]=ultima_variable-1
			patron[len(patron)-1][1]=patron_dado_ab(patron[len(patron)-1][0],patron[len(patron)-1][2])
			print("x: ",x)	
			print("x test", patron[len(patron)-1])
			
		
		print(patron)



def patron_circular_final(nivel):
	'''Funcion. Genera dinamicamente el conjunto de coordenadas [a,b,c] axiales, 
	de acuerdo al nivel deseado. Solo genera un conjunto. Las coordenadas se obtiene siguiendo contramanecillas del reloj
	en cada nivel y siguiendo un patron reconocido en una coordenada especifica que aumenta y:0,1,2,..., la siguiente
	coordenada es el nivel negativo y se calcula la variable faltante. Luego se inserta celda:
	copia coordenada faltante, copia variable especifica en su estado final; pasa a Z y luego a X con el 
	mismo patron.'''
	total_celdas=nivel*6
	print("celdas a dibujar: ",total_celdas)
	patron=[[0,0,0] for i in range(total_celdas)]
	#permite cambiar el slicing de cada for para ajustar al nivel deseado, y conformar una sola funcion

	#how to generate this dinamicaly?
	if nivel == 1:
		inicio=[0, nivel+1, 3*nivel+1]
		final =[nivel+1,	3*nivel+1, len(patron)]
	elif nivel==2:
		inicio=[0, nivel+2, 3*nivel+2]
		final =[nivel+1, 3*nivel+1, len(patron)+1]

	#output should be: [1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0]
	#si el nivel es > 0, es decir {1,2}, se genera coordenada axial a coordenada axial 
	# de esquina superior derecha, hacia esquina superior izquierda, en el orden contramanecillas del reloj
	if nivel > 0:
		#inicializo variables para obtener el estado final al término de cada ciclo for.
		#p corresponde al item [a,b,c] dentro de la lista de patron(total_celdas)
		#0,1,2 corresponden a: a,b,c respectivamente
		y=0
		x=0
		z=0
		ultima_variable=0
		#patron[params]: params es un slicing de la lista, se mueve por cada nivel.
		#se obtiene un par de un conjunto {h,i,j}, con el par se calcula la coordenada faltante.
		for y,p in zip(range(nivel+1), patron[inicio[0]:final[0]]):
			p[1]=y
			p[2]=-nivel
			p[0]=patron_dado_ab(p[1],p[2])
			ultima_variable=p[0]
		#se inserta una celda 
		if nivel == 1:
			pass
		else:
			patron[nivel+1][1]=y
			patron[nivel+1][0]=ultima_variable-1
			patron[nivel+1][2]=patron_dado_ab(patron[nivel+1][1],patron[nivel+1][0])

		#start of
		for z,p in zip(range(nivel+1), patron[inicio[1]:final[1]]):
			p[2]=z
			p[0]=-nivel
			p[1]=patron_dado_yz(p[2],p[0])
			ultima_variable=p[1]

		if nivel == 1:
			pass
		else:
			patron[3*nivel+1][2]=z
			patron[3*nivel+1][1]=ultima_variable-1
			patron[3*nivel+1][0]=patron_dado_ab(patron[3*nivel+1][2],patron[3*nivel+1][1])

		for x,p in zip(range(nivel+1),patron[inicio[2]:final[2]]):#atencion, patron+1?
			p[0]=x
			p[1]=-nivel
			p[2]=patron_dado_ab(p[0],p[1])
			ultima_variable=p[2]
		
		if nivel == 1:
			pass
		else:
			patron[len(patron)-1][0]=x
			patron[len(patron)-1][2]=ultima_variable-1
			patron[len(patron)-1][1]=patron_dado_ab(patron[len(patron)-1][0],patron[len(patron)-1][2])
	elif nivel == 0:
		return [[0,0,0]]
		
	return(patron)

def ensamblar(nivel):
	'''Funcion. Genera una sola lista que junta los n niveles, n={0,1,2,3,..}'''
	if nivel > 2:
		print("Aun no implementado")
	else:
		pat_cir=[]
		for nvl in range(nivel+1):
			pat_cir.append(patron_circular_final(nvl))
		return pat_cir

if __name__=="__main__":
	#Prototipo:
	patron_cir=[]
	#nivel=1
	#a=patron_circular_final(nivel)
	mi_nivel=2
	#b=patron_circular_final(nivel)

	print(len(ensamblar(mi_nivel)))

	#patron_circular(nivel)
else:
	print("Modulo <patron_hexagonal> importado")


