import numpy as np
import os

class Planificador:
	'''Clase: asigna prb por usuario, calcula matriz de interferencia.'''
	def __init__(self, params_cfg, params_cfg_gen, params, upgrade):
		self.cfg_plan=params_cfg
		self.cfg_gen=params_cfg_gen
		if upgrade:
			self.mapa_asignacion=params[0]
			self.dim_mapa=params[1]
			self.loc_max_pot=params[2]
			self.pr_maximo_dB_=params[3]
			self.mapa_conexion_usuario_binario=np.ones(self.mapa_asignacion.shape)
			self.mapa_conexion_celda=[]
			for i in range(self.cfg_gen["n_celdas"]):
				self.mapa_conexion_celda.append(np.count_nonzero(self.mapa_asignacion==i))
			self.mapa_interf_distribuida=np.ones(params[1])
			
		else:
			self.mapa_asignacion=params[0]
			self.dim_mapa=params[1]
			self.mapa_usuarios=params[2]
			self.mapa_margen_descon=np.stack(params[3])
			self.mapa_usr_descon=params[4]
			self.mapa_estacion_descon=params[5]
			self.max_usuario=max(self.mapa_asignacion)
			self.max_usuario_descon=max(self.mapa_estacion_descon)
			#self.dim_pot_r=params[1]
			self.mapa_interf_distribuida=np.ones(params[1])
		#output:
		self.asignacion=0
		self.one_resource_block=0
		self.nrb_usuario=0 #por usuario
		self.nrb_total_por_celda=0
		#self.nrb_total_por_celda=24
		self.estadistica_nrb_sobrante=0
		self.nrb_con_PBCH=0
		self.contador=0
		self.mapa_nrb=[]
		self.lista_distribucion=[]
		self.mapa_estado=[]
		self.mapa_interferencia=[]
		self.estado=0
		self.info_variables=[]
		#
		#self.mapa_conexion_desconexion=[]
		self.sensiblidad_receptor=[]
		self.margen_dB=[]
		#
		self.nrbs=0
		self.nrb_sobrantes=0
		self.numerologia=0
		self.resource_grid=0
		self.delta_bw_khz=0
		#self.calcular_tipo_asignacion()
		self.calcular_nrbs_celda()
		'''
		self.calcular_nrbs_usuarios()
		self.configurar_mapa_nrb()
		'''
		self.calcular_nrbs_usuarios_upgrade()
		#self.configurar_mapa_nrb()
		self.calcular_desconexion_upgrade()
		self.configurar_mapa_interferencia_nrb_upgrade()


	def to_khz(self,target):
		'''return variable in khz'''
		return target*10**3

	def to_mhz(self,target):
		'''return variable in Mhz'''
		return target*10**6


	def set_numerologia(self, bw):
		'''Calcula la numerologia dado un ancho de banda que depende de la frecuencia a utilizar'''
		if bw==50:
			self.nrbs=270
			self.numerologia=0
		elif bw==100:
			self.nrbs=273 
			self.numerologia=1
		elif bw==200:
			self.nrbs=264
			self.numerologia=2
		elif bw==400:
			self.nrbs=264
			self.numerologia=3
		else:
			print("Ancho de banda no es valido")



	def calcular_nrbs_celda(self):
		'''Calcula el numero de prbs por cada celda, de acuerdo a numerologia y ancho de banda'''
		#http://www.techplayon.com/nr-resource-block-definition-and-rbs-calculation/
		#https://www.rfwireless-world.com/calculators/5G-NR-maximum-throughput-calculator.html
		#https://5g-tools.com/5g-nr-throughput-calculator/
		#https://apkpure.com/nr-5g-prb-and-data-rate-calculator/com.instinctcoder.nr5gthecal
		#https://www.rfwireless-world.com/calculators/5G-NR-TBS-Calculation.html
		#print("POR QUE ES: 2*mu*15khz y no 2**mu*15khz") En realidad es: (2**mu)*15khz
		#calcula nrbs y numerologia.
		
		self.set_numerologia(self.cfg_plan["bw"][0])
		self.delta_bw_khz=(2**self.numerologia)*15
		self.delta_bw_hz=(2**self.numerologia)*self.to_khz(15)
		self.resource_grid=self.nrbs*self.cfg_plan["simbolo_ofdm_dl"]*(2**self.numerologia)
		self.nrb_total_por_celda=self.resource_grid


		'''
		SI SE REDUCE EL ANCHO DE BANDA TOTAL POR LA BANDA DE GUARDA, O EL CAMBIO SE APLICA PARA CADA ANCHO DE BANDA REPARTIDO
		delta_bw=(2**self.cfg_plan["numerologia"]*self.to_khz(15))
		#print("dleta",delta_bw)
		#15khz es lo minimo.
		self.one_resource_block=self.cfg_plan["sub_ofdm"]*delta_bw
		#print("one:" ,self.one_resource_block)
		nrb_sin_gbw=self.to_mhz(self.cfg_plan["bw"][0])-2*self.to_khz(self.cfg_plan["bw_guarda"][0])
		nrb=np.floor(nrb_sin_gbw/self.one_resource_block)
		#print("nrb", nrb)
		if self.cfg_plan["pbch"]:
			self.nrb_con_PBCH=nrb-22
			self.nrb_total_por_celda=self.nrb_con_PBCH*self.cfg_plan["trama_total"]
		else:
			self.nrb_total_por_celda=nrb*self.cfg_plan["trama_total"]
		print('planificador.py\nnrb_total disponibles', self.nrb_total_por_celda)
		'''




	def calcular_nrbs_usuarios(self):
		'''Funcion que asigna ancho de banda representado en prb, a partir de la
		frecuencia portadora y otros parametros adicionales.
		
		'''
		total_recursos_celda=0
		#self.max_usuario_descon
		if self.cfg_plan["tipo"]=="rr":
			#para usuarios sin deconexion.
			#ress=self.nrb_total_por_celda%self.max_usuario
			ress=self.nrb_total_por_celda%self.max_usuario_descon
			if ress!=0:
				self.nrb_total_por_celda=self.nrb_total_por_celda-ress
			else:
				pass
			#para usuarios sin deconexion.
			#self.nrb_usuario=self.nrb_total_por_celda/self.max_usuario
			self.nrb_usuario=self.nrb_total_por_celda/self.max_usuario_descon
			self.asignacion=self.nrb_usuario*self.one_resource_block*self.mapa_margen_descon
			self.asignacion=np.where(self.asignacion==0,0.0001,self.asignacion)

		elif self.cfg_plan["tipo"]=="estatico":
			self.nrb_usuario=self.cfg_plan["bw"][0]
		elif self.cfg_plan["tipo"]=="arreglo":
				#procesa arreglos, gestiona pesos.
				#this
				pass
		elif self.cfg_plan["tipo"]=="futuro":
			pass
		else:
			pass


	def calcular_nrbs_usuarios_upgrade(self):
		'''Funcion que asigna ancho de banda representado en prb, a partir de la
		frecuencia portadora y otros parametros adicionales.
		
		Si el numero de celdas es impar y el numero de usuarios tambien, la distribucion rr no es equitativa 
		pues sobran recursos. Estos deben asignarse al usuario cuya potencia sea la mayor
		
		Es mejor almacenar la informacion de cuantos recursos tiene  cada uisario en self.nrb_usuario, que hacer la operacion mas adelante.
		
		otra opcion es agrandar el bloque de recurso maximo 276 * num_cel. luego repartir este numero a todos los usuarios.'''
		#self.max_usuario_descon
		
		if self.cfg_plan["tipo"]=="rr":
			#verificar si la distribucion es exacta
			self.nrb_sobrantes=self.nrb_total_por_celda%np.array(self.mapa_conexion_celda)
			self.nrb_usuario=np.floor(self.nrb_total_por_celda/np.array(self.mapa_conexion_celda))
			for indx, recursos in enumerate(self.nrb_usuario):
				self.asignacion=np.where(self.mapa_asignacion==indx, recursos, self.asignacion)

			self.asignacion_bw=self.asignacion*self.delta_bw_hz

		elif self.cfg_plan["tipo"]=="estatico":
			self.nrb_usuario=self.cfg_plan["bw"][0]
		elif self.cfg_plan["tipo"]=="arreglo":
				#procesa arreglos, gestiona pesos.
				pass
		elif self.cfg_plan["tipo"]=="futuro":
			pass
		elif self.cfg_plan["tipo"]=="rr_hard":
			#verificar si la distribucion es exacta
			#ress=self.nrb_total_por_celda%np.array(self.mapa_conexion_celda)
			max_usuarios=max(self.mapa_conexion_celda)
			particion=np.floor(self.nrb_total_por_celda/max_usuarios)
			en_uso=particion*max_usuarios
			self.nrb_usuario=particion*np.ones(np.shape(self.mapa_asignacion))
			self.nrb_sobrantes=self.nrb_total_por_celda-particion*np.array(self.mapa_conexion_celda)

			self.estadistica_nrb_sobrante=np.round(100*self.nrb_sobrantes/self.nrb_total_por_celda,4)
			#cambio dimension
			for indx, recursos in enumerate(self.nrb_usuario):
				self.asignacion=np.where(self.mapa_asignacion==indx, recursos, self.asignacion)
			self.asignacion_bw=self.asignacion*self.delta_bw_hz

		elif self.cfg_plan["tipo"]=="rr_soft":
			pass
		else:
			pass


	def calcular_desconexion_upgrade(self):
		'''calcula un mapa de desconexion y conexion a partir de una snr objetivo y un calculo inicial de frecuencia'''
		nf=self.cfg_gen["nf"][0]
		ktb=-174+10*np.log10(self.asignacion_bw)
		sinr_objetivo=self.cfg_gen["ber_sinr"]
		self.sensiblidad_receptor=nf+ktb+sinr_objetivo
		self.margen_dB=np.vstack(self.pr_maximo_dB_)-self.sensiblidad_receptor
		self.mapa_conexion_usuario_binario=np.where(self.margen_dB<0, 0, self.mapa_conexion_usuario_binario)

	def configurar_mapa_interferencia_nrb_upgrade(self):
		'''Calcula matriz interferente, para ello reparte recursos (bloques de ancho de banda) C_{i}, de acuerdo al mapa de conexion de celdas.
		C_{i}, i={1,2,3,...,n_cel}, representa cada bloque de nrb entregado a cada
		usuario, de esta forma si se entrega a cada usuario 364 nrbs, C1 representa
		el bloque nrb 0-363 hz, C2 representa el bloque nrb 364-2*363 hz y asi sucesivamente '''
		#el estado debe cambiar solo cuando el indice cambia.
		self.contador=[0 for i in range(len(self.mapa_conexion_celda))]
		#convierto a numpy para aprovechar multiplicacion elemento a elemnto.
		self.contador=np.array(self.contador)
		self.estado=[0 for i in range(len(self.mapa_conexion_celda))]
		#convierto a numpy para aprovechar multiplicacion elemento a elemnto.
		self.estado=np.array(self.estado)
		for indd, celda in enumerate(self.mapa_asignacion):
			if self.mapa_conexion_usuario_binario[indd]==0:
				self.estado[celda[0]]=0
			else:
				#si diferente de 0, sum
				self.contador[celda[0]]=self.contador[celda[0]]+1
				self.estado[celda[0]]=1
			'''indice, celda de conexion, conexion, contador, estado, nrb asignado'''
			mostrar="{}	{}	{}		{}	{}	nrb_{}".format(indd,celda,
				self.mapa_conexion_usuario_binario[indd],self.contador, self.estado, sum(self.contador*self.estado))
			'''
			print("[planificador.configurar_mapa_interferencia, ", mostrar)
			'''
			self.mapa_estado.append(self.estado.copy())
			nrb_actual=sum(self.contador*self.estado)
			self.mapa_nrb.append(nrb_actual)
			self.estado[celda[0]]=0
		
		'''Funciona por que originalmente la matriz de estados interferentes es cero y a medida
		que se generan la distribucion se rellena, como la matriz de distribucion solo es
		repartida a los usuarios cuyos indices se encuentran mapeados, los indices no mapeados
		corresponden a los indices donde no ha habido conexion desde un principio'''
		self.mapa_nrb=np.array(self.mapa_nrb)
		self.mapa_estado=np.stack(self.mapa_estado).reshape(self.dim_mapa)
		start=1 #si empieza en cero se cuenta un potencial nrb0

		for indx, mapa in enumerate(range(start,int(np.max(self.mapa_nrb))+1)):
			arreglo=np.where(self.mapa_nrb==mapa)
			#esta nueva lista de distribucion cuenta donde ha habido nrb,
			#y los reparte a la lista, por lo que el ciclo esta completo.
			self.lista_distribucion.append(arreglo[0])
			mapa_semilla=[0 for i in range(len(self.mapa_conexion_celda))]
			for indxx in arreglo[0]:
				mapa_semilla=self.mapa_estado[indxx] + mapa_semilla
			self.mapa_interferencia.append(mapa_semilla)
		self.mapa_interferencia=np.stack(self.mapa_interferencia)
		for lista, mapa_dist in zip(self.lista_distribucion, self.mapa_interferencia):
			for indx_interf in lista:
				self.mapa_interf_distribuida[indx_interf]=mapa_dist



	def configurar_mapa_nrb(self):
		'''Reparte recursos (bloques de ancho de banda) C_{i}, de acuerdo al mapa de conexion de celdas.
		C_{i}, i={1,2,3,...,n_cel}, representa cada bloque de nrb entregado a cada
		usuario, de esta forma si se entrega a cada usuario 364 nrbs, C1 representa
		el bloque nrb 0-363 hz, C2 representa el bloque nrb 364-2*363 hz y asi sucesivamente.'''
		#el estado debe cambiar solo cuando el indice cambia.
		self.contador=[0 for i in range(len(self.mapa_asignacion))]
		#convierto a numpy para aprovechar multiplicacion elemento a elemnto.
		self.contador=np.array(self.contador)
		self.estado=[0 for i in range(len(self.mapa_asignacion))]
		#convierto a numpy para aprovechar multiplicacion elemento a elemnto.
		self.estado=np.array(self.estado)

		########################print("indice	descon	cel_descon	celda	contador	estado		nrb")
		for indd, celda in enumerate(self.mapa_usuarios):
			#celda[0], porque al ser numpy, genera un array[] y para acceder al
				#array, es necesario acecder al valor [0]
			if self.mapa_margen_descon[indd]==0:
				self.estado[celda[0]]=0
			else:
				#si diferente de 0, sum
				self.contador[celda[0]]=self.contador[celda[0]]+1
				self.estado[celda[0]]=1
			#self.contador[celda[0]]=self.contador[celda[0]]+1
			#uno donde ha habido cambio. el estado es por cada celda
				#para indicar donde ha habido cambio.
			#self.estado[celda[0]]=1
			#cambio de indice.
				#sum(self.contador*self.estado) es el valor del nrb1.

			#print(indd,self.mapa_usuarios[indd],self.contador, self.estado, "nrb_{}".format(sum(self.contador*self.estado)))
			mostrar="{}	{}	{}		{}	{}	{}	nrb_{}".format(indd,self.mapa_margen_descon[indd], self.mapa_usr_descon[indd],
				self.mapa_usuarios[indd],self.contador, self.estado, sum(self.contador*self.estado))
			self.info_variables.append(mostrar)

			self.mapa_estado.append(self.estado.copy())
			#if bandera conexion==0:
				#apend -1 en esa posicion. [ok]
				#sino:
					#pass a mapa_nrb. [ok]
			#posible error: [ok]
				#se salta el recurso, por que igual hay menos usuarios.
				#revisar el mapa de conexion, debe considerar menos usuarios tambien.
				#como realizar el descuento?
			nrb_actual=sum(self.contador*self.estado)
			self.mapa_nrb.append(nrb_actual)
			self.estado[celda[0]]=0
		#convertir a numpy
		self.mapa_nrb=np.array(self.mapa_nrb)
		self.mapa_estado=np.stack(self.mapa_estado).reshape(self.dim_mapa)

		#primero es el max de cada celda incluyendo desconxion, el otro es el original que no la tiene en cuenta.
		'''Funciona por que originalmente la matriz de estados interferentes es cero y a medida
		que se generan la distribucion se rellena, como la matriz de distribucion solo es
		repartida a los usuarios cuyos indices se encuentran mapeados, los indices no mapeados
		corresponden a los indices donde no ha habido conexion desde un principio'''
		for indx, mapa in enumerate(range(0,self.max_usuario_descon+1)):
			arreglo=np.where(self.mapa_nrb==mapa)
			#esta nueva lista de distribucion cuenta donde ha habido nrb0,
			#y los reparte a la lista, por lo que el ciclo esta completo.
			self.lista_distribucion.append(arreglo[0])
			mapa_semilla=[0 for i in range(len(self.mapa_asignacion))]

			for indxx in arreglo[0]:
				mapa_semilla=self.mapa_estado[indxx] + mapa_semilla
			self.mapa_interferencia.append(mapa_semilla)
		self.mapa_interferencia=np.stack(self.mapa_interferencia)

		for lista, mapa_dist in zip(self.lista_distribucion, self.mapa_interferencia):
			for indx_interf in lista:
				self.mapa_interf_distribuida[indx_interf]=mapa_dist



def prueba_asignar100():
	#@@ -163,11 +124,7 @@
	print(prueba2)
	print("-----------------------------------------------Numero de bloques de recursos 400MHz ---------------")
	print("-----------------------------------------------(Cantidad de bloques de recuros , ancho de banda por RB) ---------------")
	print("test3",prueba3)

def prueba_asignar():
	"""Comprueba implementacion de funciones asignar 100,200,400 segun parametros"""
	prueba=Planificador.asignar_100mhz()


def lista_rb():
	#lista=append
	print("-----------------------------------------------(distribucion bloques de recursos por numero de usuario) ---------------")
	print(m_rb)
	#

if __name__=="__main__":
	#Prototipo:
	print("planificador")

	#plan=Planificador(params_cfg, 17)
	#Planificador.asignar_100mhz()
	#REALIZAR PRUEBA DE F1,F2,F3
	prueba_asignar100()
	#lista_rb()
	#prueba_asignar()
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
