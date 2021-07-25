from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
#form tools
from formtools.wizard.views import SessionWizardView

#fomularios simulador
from .forms import FormGeneral, FormPropagacion, FormBalanceAntenas,FormAsignacion
from .forms import FormCompacto
#integracion simulador
import os
import json
#
from .static.simulador import top_pruebas
from .static.simulador import simulador as samiv1
from .static.simulador.utilidades import config as cfg


#--------------------------------------
#--------------------------------------
'''Definiciones Globales'''
#--------------------------------------
#--------------------------------------

#--------------------------------------
#--------------------------------------
'''Definiciones Auxiliares'''
#--------------------------------------
#--------------------------------------
def convertir_str_2_bool(check):
    '''Convierte "True" o "False" a True o False'''
    res=False
    if check=="True":
        res=True
    else:
        pass
    return res


def validar_desvanecimiento(check):
    '''Valida el contenido de la variable desvanecimiento y ajusta los parametros'''
    flag=True
    if check=="False":
        flag=False
        tipo="none"
    else:
        flag=True
        tipo=check
    #print(flag,tipo)
    return flag, tipo


#----------------------------END

#--------------------------------------
#--------------------------------------
'''VIEWs'''
#--------------------------------------
#--------------------------------------
# Create your views here.
def home(request):
    '''Index: debe cambiarse a la version del simulador mas reciente'''
    return render(request,'simapp/sami-index.html')


def form_demo_sami_v1(request):
    '''Demostracion de formulario.'''
    return render(request,'simapp/form_demo/sami-demo-v1.html')


def futuro(request):
    '''Para mostrar pagina bajo desarrollo'''
    return render(request,'simapp/sami-futuro.html')


def iniciar_simulacion(request):
    '''Inicia la simulacion''' 
    configuracion=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
    if request.method == 'GET':
        try:
            arr = os.listdir()
            print(arr)
        except Exception as ex:
            print(ex)
        #exists = os.path.isfile('qw2ass<z/path/to/file')
        #print(exists)
        print("GET Metodo")
        
        '''***OPTIMIZACION***
        Anotacion de suma importancia:
        Que ocurre cuando el sistema es grande? es decir, con muchos usuarios y muchas celdas?
        La presimulacion se ejecuta como una simulacion y pierde el sentido de efectuarla. Esto
        ocurre debido a que la presimulacion y la simulacion ocurren al mismo tiempo. En la clase no existe
        ninguna diferencia entre ambas. La presimulacion si es diferente en simulador pues usa funciones internas
        configuradas con ese proposito, mas sin embargo la simulacion y todos los detalles tambien se ejecutan.
        
        Existen dos opciones para optimizar la presimulacion e indpendientemente ejecutar la simulacion que es el comportamiento esperado.
        La primera opcion directa y mas facil consiste en que al ejecutar la presimulacion, los datos para ese escenario (1 iteracion) se usen 
        para obtener estadisticas de muestras de valores (valores de potencia, sinr, estadisticas). Esta presimulacion seria la simulacion 0, cuya 
        utilidad puede o no (dependiendo del disenno) usarse en el compendio de simulacion montecarlo para su estudio. E
        Sin embargo, es de suma importancia comprobar logicamente el flujo de esta operacion, debido que en presimulacion, hasta el modelo del
        canal, los valores originales de distancia y otros se mantienen intactos, luego estos cambian para generar las graficas correspondientes.

        Para comprobar basta con imprimir la informacion de esa presimulacion.

        La segunda opcion es mas compleja e implica tambien cambios profundos de disenno,
        cuya solucion planteada puede agregarse un parametro adicional que indique que la simuacion
        no es una completa sino una con datos custom de pruebas. En este caso, los calculos de potencia, sinr, trhougput no se generan, 
        y la simulacion de montecarlo este parametro se desactiva (o no dependiendo de la logica implementada)
        para que la primera simulacion corresponda.

        Escenario 1:
            simulacion 0
            Hay perdida de datos.
            Se generan estadisticas simples de simulacion (datos: 56%, 40%, 100%, 100/399, etc)

            MONTECARLO: estadisticas complejas (graficas)

        Escenario 1.2:
            imulacion 0 como simulacion 1 de montecarlo.
            No hay perdida de datos.
            Es necesario crear una copia de presim antes de que sea modificada.
        Esecenario 2:
            Separar los calculos, hasta el modelo del canal y no calcular lo sucesivo.
                implica perder los primeros datos (generacion de usuarios)
        '''
        presim=samiv1.Simulador(tipo="presimulacion")
        #limpiar rutas.
        presim.graficas_disponibles_dic={}

        #presim_graphs=presim.graficas_disponibles
        #EN SIMULACION, DESACTIVAR LA GENERACION DE IMAGENES.
    
        #si iteracion>1 and iteracion<5, ejecutar tipo="simulacion"
            #mensaje: no hay suficientes tomas para crear estadisticas.
                #fordward to tablas (datos por simulacion)
        #si iteracion>=5, ejecutar tipo="montecarlo"
        iteracion=configuracion["cfg_simulador"]["params_general"]["iteracion"]
        if iteracion>=1 and iteracion<10:
            print("[view.gui]:Montecarlo no disponible para iteracion<10")
            #go to 
            #sim=samiv1.Simulador(tipo="simulacion")
            
            #step1: en presim, antes del cambio de muestra, 
                #copiar info de simulacion.
            #clean memory
            presim=0
            #presim.info_sinr()
            '''Falta modulo que guarda estos datos, debe almacenarse en una ruta de path'''


        elif iteracion>=10:
            print("[view.gui]:Montecarlo activado, porfavor espere...")
            montecarlo=samiv1.Simulador(tipo="montecarlo")


        
    return render(request,'simapp/sami-iniciar-sim.html')


def ver_parametros(request):
    '''Punto de control: se observan los parametros, se decide iniciar simulacion
    o corregirlos con las opciones disponibles.'''
    configuracion=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")

    config1=configuracion["cfg_simulador"]["params_general"]
    config2=configuracion["cfg_simulador"]["params_propagacion"]
    config3=configuracion["cfg_simulador"]["params_balance"]
    config4=configuracion["cfg_simulador"]["params_antena"]
    config5=configuracion["cfg_simulador"]["params_asignacion"]

    return render(request,'simapp/sami-parametros.html', {"cfg1":config1, 
    "cfg2":config2, "cfg3":config3, "cfg4":config4, "cfg5":config5 })


def ver_presim(request):
    #configuracion=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
    #imagenes_disp=configuracion["cfg_gui"]["presim_graphs"]
    #
    #se separa el archivo de path debido a que genera problemas en modo debug
    configuracion=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_gui")
    imagenes_disp=configuracion["presim_graphs"]
    #print(imagenes_disp)
    return render(request,'simapp/resultados/sami-presim-graficas.html', {"img_disp":imagenes_disp})


def ver_sim(request):
    configuracion=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_gui")
    configuracion_base=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
    iteracion=configuracion_base["cfg_simulador"]["params_general"]["iteracion"]
    imagenes_disp=configuracion["montecarlo_graphs"]
    #cambia a las graficas de simulacion
    #print(imagenes_disp)
    if iteracion >= 1 and iteracion < 10:
        return render(request,'simapp/resultados/sami-sim-graficas-empty.html')
    else:
        return render(request,'simapp/resultados/sami-sim-graficas.html', {"img_disp":imagenes_disp})


#FORMULARIOS V1
def form_a1(request):
    form=FormGeneral()
    if request.method == 'POST':
        form=FormGeneral(request.POST)
        print("\nHA OCURRIDO UN POST")
        if form.is_valid():
            #CONFIGURACION DE VARIABLES
            print("[OK]-Formulario 1 Aceptado")
            contenido=form.cleaned_data

            config=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
            config["cfg_simulador"]["params_general"]["iteracion"]=contenido["iteraciones"]
            config["cfg_simulador"]["params_general"]["n_celdas"]=contenido["n_celdas"]
            config["cfg_simulador"]["params_general"]["portadora"][0]=contenido["portadora"]
            config["cfg_simulador"]["params_general"]["isd"]=contenido["isd"]
            
            config["cfg_simulador"]["params_general"]["geometria"]=contenido["geometria_usuarios"]
            config["cfg_simulador"]["params_general"]["radio_cel"]=contenido["radio_cel"] 

            config["cfg_simulador"]["params_general"]["distribucion"][0]=contenido["tipo_distribucion"]
            config["cfg_simulador"]["params_general"]["distribucion"][1]=float(contenido["densidad"])
                        
            flag_imagen=convertir_str_2_bool(contenido["imagen"])
            config["cfg_simulador"]["params_general"]["imagen"]["display"][0]=flag_imagen
            if flag_imagen:
                print("imagen activado, desactivar iteraciones.")
                #config["cfg_simulador"]["params_general"]["iteracion"]=1
                #NORMALMENTE SE DESACTIVA LAS ITERACIONES. En lugar de eso,
                #SE DESACTIVA LA IMAGEN, PERO EN EL SIMULADOR
            config["cfg_simulador"]["params_general"]["imagen"]["resolucion"]=contenido["pixeles"]
            cfg.guardar_cfg(config, target_path="simapp/static/simulador/base_datos/")
            config=0
        else:
            print("Oops, algo ha fallado. Retornando.")
            return redirect('/sim/')
        #no necesario con validators
        #if int(request.POST["isd"])>1200:
        #    return redirect('/sim')
        #-----------
        #SIGUIENTE
        return redirect('/sim/form_a2')
    #-----------
    #ACTUAL
    return render(request,'simapp/form_v1/sami-form-a1.html', {"form_data":form} )


def form_a2(request):
    form=FormPropagacion()
    if request.method == 'POST':
        form=FormPropagacion(request.POST)
        print("\nHA OCURRIDO UN POST a2 \n")
        if form.is_valid():
            #CONFIGURACION DE VARIABLES
            print("[OK]-Formulario a2 Aceptado")
            contenido=form.cleaned_data
            
            config=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
            config["cfg_simulador"]["params_propagacion"]["modelo_perdidas"]=contenido["modelo_perdidas"]
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][0]=float(contenido["mp1"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][1]=float(contenido["mp2"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][2]=float(contenido["mp3"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][3]=float(contenido["mp4"])

            flag_desv, tipo_desv=validar_desvanecimiento(contenido["params_desv"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["display"]=flag_desv
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["tipo"]=tipo_desv
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][0]=float(contenido["dp1"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][1]=float(contenido["dp2"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][2]=float(contenido["dp3"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][3]=float(contenido["dp4"])

            config["cfg_simulador"]["params_general"]["nf"][0]=float(contenido["nf"])
            config["cfg_simulador"]["params_general"]["ber_sinr"]=float(contenido["ber_sinr"])
            cfg.guardar_cfg(config, target_path="simapp/static/simulador/base_datos/")
            config=0
        else:
            print("Oops, algo ha fallado. Retornando.")
            return redirect('/sim/form_a2')
        #-----------
        #SIGUIENTE
        #return render(request,'simapp/form_v1/sami-form-a3.html')
        return redirect('/sim/form_a3')
    #-----------
    #ACTUAL
    return render(request,'simapp/form_v1/sami-form-a2.html', {"form_data":form} )


def form_a3(request):
    form=FormBalanceAntenas()
    if request.method == 'POST':
        form=FormBalanceAntenas(request.POST)
        print("\nHA OCURRIDO UN POST a3 \n")
        print(form)
        if form.is_valid():
            #CONFIGURACION DE VARIABLES
            contenido=form.cleaned_data
            print("[OK]-Formulario a3 Aceptado")
            print(contenido)
            
            config=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
            config["cfg_simulador"]["params_balance"]["ptx"]=float(contenido["ptx"])
            config["cfg_simulador"]["params_balance"]["gtx"]=float(contenido["gtx"])
            config["cfg_simulador"]["params_balance"]["ltx"]=float(contenido["ltx"])
            config["cfg_simulador"]["params_balance"]["lrx"]=float(contenido["lrx"])
            config["cfg_simulador"]["params_balance"]["grx"]=float(contenido["grx"])
            config["cfg_simulador"]["params_balance"]["sensibilidad"]=float(contenido["sensibilidad"])
            config["cfg_simulador"]["params_balance"]["mcl"]=float(contenido["mcl"])
            #antenas
            config["cfg_simulador"]["params_antena"]["tipo"]=contenido["tipo_antena"]
            config["cfg_simulador"]["params_antena"]["hpbw"]=contenido["hpbw"]
            config["cfg_simulador"]["params_antena"]["atmin"]=float(contenido["atmin"])
            config["cfg_simulador"]["params_antena"]["apuntamiento"][0]=int(contenido["apuntamiento"])
            cfg.guardar_cfg(config, target_path="simapp/static/simulador/base_datos/")
            config=0
        else:
            print("Oops, algo ha fallado. Retornando.")
            return redirect('/sim/form_a3')
        #-----------
        #SIGUIENTE
        #return render(request,'simapp/form_v1/sami-form-a4.html')
        return redirect('/sim/form_a4')
    #-----------
    #ACTUAL
    else:
        print("HA OCURRIDO OTRA COSA a3")
    return render(request,'simapp/form_v1/sami-form-a3.html', {"form_data":form} )


def form_a4(request):
    form=FormAsignacion()
    if request.method == 'POST':
        form=FormAsignacion(request.POST)
        print("\nHA OCURRIDO UN POST a4", request.POST)
        if form.is_valid():
            contenido=form.cleaned_data
            #CONFIGURACION DE VARIABLES
            print("[OK]-Formulario a4 Aceptado")
            print(contenido)
            config=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
            config["cfg_simulador"]["params_asignacion"]["tipo"]=contenido["tipo_asignacion"]
            config["cfg_simulador"]["params_asignacion"]["bw"][0]=int(contenido["bw"])
            config["cfg_simulador"]["params_asignacion"]["numerologia"]=float(contenido["numerologia"])
            config["cfg_simulador"]["params_asignacion"]["bw_guarda"][0]=int(contenido["banda_guarda"])
            config["cfg_simulador"]["params_asignacion"]["sub_ofdm"]=float(contenido["subportadora"])
            config["cfg_simulador"]["params_asignacion"]["trama_total"]=float(contenido["trama"])
            config["cfg_simulador"]["params_asignacion"]["simbolo_ofdm_dl"]=float(contenido["simbolos"])
            config["cfg_simulador"]["params_asignacion"]["frame"]=float(contenido["frame"])
            cfg.guardar_cfg(config, target_path="simapp/static/simulador/base_datos/")
            config=0
        else:
            print("Oops, algo ha fallado. Retornando.")
            return redirect('/sim/form_a4')
            
        #-----------
        #SIGUIENTE
        return redirect('parametros/')
    #-----------
    #ACTUAL
    return render(request,'simapp/form_v1/sami-form-a4.html', {"form_data":form} )


def form_compacto(request):
    '''Implementacion de 4 fases en 1 para agilizar la simulacion.'''
    form=FormCompacto()
    if request.method == 'POST':
        form=FormCompacto(request.POST)
        print("\nHA OCURRIDO UN POST Compacto", request.POST)
        if form.is_valid():
            print("[OK]-Formulario 1 Aceptado")
            contenido=form.cleaned_data
            print("clase django", contenido)

            config=cfg.cargar_variables(target_path="simapp/static/simulador/base_datos/")
            config["cfg_simulador"]["params_general"]["iteracion"]=contenido["iteraciones"]
            config["cfg_simulador"]["params_general"]["n_celdas"]=contenido["n_celdas"]
            config["cfg_simulador"]["params_general"]["portadora"][0]=contenido["portadora"]
            config["cfg_simulador"]["params_general"]["isd"]=contenido["isd"]
            
            config["cfg_simulador"]["params_general"]["geometria"]=contenido["geometria_usuarios"]
            config["cfg_simulador"]["params_general"]["radio_cel"]=contenido["radio_cel"] 

            config["cfg_simulador"]["params_general"]["distribucion"][0]=contenido["tipo_distribucion"]
            config["cfg_simulador"]["params_general"]["distribucion"][1]=float(contenido["densidad"])
                        
            flag_imagen=convertir_str_2_bool(contenido["imagen"])
            config["cfg_simulador"]["params_general"]["imagen"]["display"][0]=flag_imagen
            if flag_imagen:
                print("imagen activado, desactivar iteraciones.")
                #config["cfg_simulador"]["params_general"]["iteracion"]=1
            config["cfg_simulador"]["params_general"]["imagen"]["resolucion"]=contenido["pixeles"]
            #
            #
            config["cfg_simulador"]["params_propagacion"]["modelo_perdidas"]=contenido["modelo_perdidas"]
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][0]=float(contenido["mp1"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][1]=float(contenido["mp2"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][2]=float(contenido["mp3"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][3]=float(contenido["mp4"])

            flag_desv, tipo_desv=validar_desvanecimiento(contenido["params_desv"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["display"]=flag_desv
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["tipo"]=tipo_desv
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][0]=float(contenido["dp1"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][1]=float(contenido["dp2"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][2]=float(contenido["dp3"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][3]=float(contenido["dp4"])

            config["cfg_simulador"]["params_general"]["nf"][0]=float(contenido["nf"])
            config["cfg_simulador"]["params_general"]["ber_sinr"]=float(contenido["ber_sinr"])
            #
            #
            config["cfg_simulador"]["params_balance"]["ptx"]=float(contenido["ptx"])
            config["cfg_simulador"]["params_balance"]["gtx"]=float(contenido["gtx"])
            config["cfg_simulador"]["params_balance"]["ltx"]=float(contenido["ltx"])
            config["cfg_simulador"]["params_balance"]["lrx"]=float(contenido["lrx"])
            config["cfg_simulador"]["params_balance"]["grx"]=float(contenido["grx"])
            config["cfg_simulador"]["params_balance"]["sensibilidad"]=float(contenido["sensibilidad"])
            config["cfg_simulador"]["params_balance"]["mcl"]=float(contenido["mcl"])
            #antenas
            config["cfg_simulador"]["params_antena"]["tipo"]=contenido["tipo_antena"]
            config["cfg_simulador"]["params_antena"]["hpbw"]=contenido["hpbw"]
            config["cfg_simulador"]["params_antena"]["atmin"]=float(contenido["atmin"])
            config["cfg_simulador"]["params_antena"]["apuntamiento"][0]=int(contenido["apuntamiento"])

            #
            #
            config["cfg_simulador"]["params_asignacion"]["tipo"]=contenido["tipo_asignacion"]
            config["cfg_simulador"]["params_asignacion"]["bw"][0]=int(contenido["bw"])
            config["cfg_simulador"]["params_asignacion"]["numerologia"]=float(contenido["numerologia"])
            config["cfg_simulador"]["params_asignacion"]["bw_guarda"][0]=int(contenido["banda_guarda"])
            config["cfg_simulador"]["params_asignacion"]["sub_ofdm"]=float(contenido["subportadora"])
            config["cfg_simulador"]["params_asignacion"]["trama_total"]=float(contenido["trama"])
            config["cfg_simulador"]["params_asignacion"]["simbolo_ofdm_dl"]=float(contenido["simbolos"])
            config["cfg_simulador"]["params_asignacion"]["frame"]=float(contenido["frame"])
            cfg.guardar_cfg(config, target_path="simapp/static/simulador/base_datos/")
            
        return redirect('parametros/')
    return render(request,'simapp/form_v1/sami-form-compacto.html', {"form_data":form})
    #return render(request,'simapp/form_v1/sami-form-a4.html', {"form_data":form} )


#AUXILIAR Y PRUEBAS
