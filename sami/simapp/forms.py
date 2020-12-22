from django import forms
#from .simulador_v1.utilidades import config as cfg
#https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
class FormStepOne(forms.Form):
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1)
    nombre= forms.CharField(max_length=100,initial="name")
    Apellido = forms.CharField(max_length=100,initial="last")
    Telefono  = forms.CharField(max_length=100,initial="number")
    otro  = forms.CharField(max_length=100,initial="number")
    otro2  = forms.CharField(max_length=100,initial="number")
    otro3  = forms.CharField(max_length=100,initial="number")
    otro4  = forms.CharField(max_length=100,initial="number")
    otro5  = forms.CharField(max_length=100,initial="number")

class FormStepTwo(forms.Form):
    job = forms.CharField(max_length=100,initial="name")
    salary = forms.CharField(max_length=100,initial="name")
    job_description = forms.CharField(widget=forms.Textarea,initial="name")

#------------------------------SIMAPP
#seleccion
geometria_choices=(
        ('autoajustable', 'Radio proporcional a ISD'),
        ('manual', 'Radio Customizado'),  
    )

distribucion_choices=(
        ('ppp', 'Proceso Puntual Poissson'),
        ('rand', 'Aleatorio'),
        ('fijo', 'Fijo'),
    )

densidad_choices=(
        (0.000002, 'Baja'),
        (0.000005, 'Media'),
        (0.000009, 'Moderada'),
        (0.00009, 'Alta [!]'),
        (0.00001, 'Masivo [!!]'),
        (0.0009, 'Ultra [!!!]'),
    )

imagen_choices=(
        (False, 'Desactivado'),
        (True, 'Activado'),

    )

#---------------------------------
modelo_perdidas_choices=(
        ('okumura_hata', 'Modelo Okumura Hata'),
        ('uma_3gpp', 'Modelo 3GPP UMa'),
        ('umi_ci', 'Modelo CI-UMi'),
        ('umi_abg', 'Modelo ABG-UMi'),
        
    )

desvancimiento_choices=(
        (False, 'Desactivado'),
        ('normal', 'Normal'),
        ('rayl', 'Rayleight'),
        ('mixto', 'Normal+Rayleight'),
        
    )

#----------------------------------------------
antena_choices=(
        ('4g', '38942 Trisectorizada'),
        ('5g', 'Futuro*'),
        ('futuro', 'Futuro**'), 
    )


asignacion_choices=(
        ('rr', 'Round Robin'),
        ('f1', 'Futuro*'),
        ('f2', 'Futuro**'), 
    )

bw_choices=(
        (10, '10'),
        (20, '20'),
        (40, '40'),
        (100, '100'), 
        (200, '200'), 
        (400, '400'),  
    )

#----------------------------------------------
#end
class FormGeneral(forms.Form):
    '''Formulario inicial. Configura parametros globales'''
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1, min_value=1)
    n_celdas=forms.IntegerField(label='Cantidad de Celdas',initial=1, max_value=19, min_value=1)
    portadora=forms.IntegerField(label='Frecuencia Portadora [Mhz, Ghz]',initial=900, min_value=200, max_value=75000,)
    isd=forms.IntegerField(label='Distancia Entre Celdas [m]',initial=1000, min_value=10)
    geometria_usuarios=forms.ChoiceField(label='Distribución de Usuarios',choices=geometria_choices)
    radio_cel=forms.IntegerField(initial=1000, min_value=5)
    tipo_distribucion=forms.ChoiceField(label='Tipo de Despliegue de Usuarios',choices=distribucion_choices)
    densidad=forms.ChoiceField(label='Densidad de Población',choices=densidad_choices)
    imagen=forms.ChoiceField(required=False,label='Imagen de Potencia Recibida',choices=imagen_choices)
    pixeles=forms.IntegerField(required=False,initial=1000, max_value=2000, min_value=10) 



class FormPropagacion(forms.Form):
    '''Formulario para configurar variables relacionadas al modelo de perdidas de propagación'''
    modelo_perdidas=forms.ChoiceField(label='Modelo de Pérdidas de Propagación',choices=modelo_perdidas_choices)
    #floats
    mp1=forms.DecimalField(label='Parámero 1',initial=30, min_value=0, max_digits=5, decimal_places=2)
    mp2=forms.DecimalField(label='Parámero 2',initial=0, min_value=0, max_digits=5, decimal_places=2)
    mp3=forms.DecimalField(label='Parámero 3',initial=1.5, min_value=0, max_digits=5, decimal_places=2)
    mp4=forms.DecimalField(label='Parámero 4',initial=0, min_value=0, max_digits=5, decimal_places=2)

    params_desv=forms.ChoiceField(label='Tipo de Desvanecimiento',choices=desvancimiento_choices)
    #flats
    dp1=forms.DecimalField(label='Parámero 1',initial=3.1, min_value=0, max_digits=5, decimal_places=2)
    dp2=forms.DecimalField(label='Parámero 2',initial=8.1, min_value=0, max_digits=5, decimal_places=2)
    dp3=forms.DecimalField(label='Parámero 3',initial=0, min_value=0, max_digits=5, decimal_places=2)
    dp4=forms.DecimalField(label='Parámero 4',initial=0, min_value=0, max_digits=5, decimal_places=2)

    ber_sinr=forms.DecimalField(label='BER Objetivo [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    nf=forms.DecimalField(label='Figura de Ruido [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)


class FormBalanceAntenas(forms.Form):
    '''Formulario para configurar variables relacionadas al balance del enlace y las antenas'''
    ptx=forms.DecimalField(label='Potencia en Transmisión [dBm]',initial=28, min_value=1, max_digits=5, decimal_places=2)
    gtx=forms.DecimalField(label='Ganancia en Transmisión [dB]',initial=15, min_value=1, max_digits=5, decimal_places=2)
    ltx=forms.DecimalField(label='Pérdidas en Transmisión [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    lrx=forms.DecimalField(label='Pérdidas en Recepción [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    grx=forms.DecimalField(label='Ganancia en Recepción [dB]',initial=8, min_value=1, max_digits=5, decimal_places=2)
    sensibilidad=forms.DecimalField(label='Sensibilidad en Recepción',initial=-110, max_digits=5, decimal_places=2)
    mcl=forms.DecimalField(label='MCL',initial=70, min_value=1, max_digits=5, decimal_places=2)
    #antenas
    tipo_antena=forms.ChoiceField(label='Tipo Antena',choices=antena_choices)
    hpbw=forms.IntegerField(label='Ancho de Haz',initial=65, min_value=1)
    atmin=forms.DecimalField(label='Atenuación Mínima',initial=20, min_value=1, max_digits=5, decimal_places=2)
    

class FormAntenas(forms.Form):
    '''Formulario para configurar variables relacionadas a las antenas. Fue Combinado en Balance.'''
    pass

class FormAsignacion(forms.Form):
    '''Formulario para configurar variables relacionadas a la asignación de recursos radio.'''
    tipo_asignacion=forms.ChoiceField(label='Tipo de Asignación',choices=asignacion_choices)
    #bw=forms.IntegerField(label='Ancho de Banda Usuario [Mhz]',initial=20, min_value=10)
    bw=forms.ChoiceField(label='Ancho de Banda del Sistema [Mhz]',choices=bw_choices)
    numerologia=forms.IntegerField(label='Numerología',initial=1, min_value=1)
    banda_guarda=forms.IntegerField(label='Banda de Guarda [Khz]',initial=845, min_value=1)
    subportadora=forms.IntegerField(label='Suportadora [u]',initial=12, min_value=1)
    trama=forms.IntegerField(label='Trama Total [u]',initial=12,min_value=1)
    simbolos=forms.IntegerField(label='Símbolos OFDM [u]',initial=10, min_value=1)
    frame=forms.IntegerField(label='Frame',initial=10, min_value=1)
    #
    futuro1=forms.IntegerField(label='Futuro*',initial=0, min_value=0)
    futuro2=forms.IntegerField(label='Futuro**',initial=0, min_value=0)
    
    
