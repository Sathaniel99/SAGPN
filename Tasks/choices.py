from django.db import models

class Choices_Prioridades(models.TextChoices):
    BAJA = 'Baja'
    MEDIA = 'Media'
    ALTA = 'Alta'
    
class Choices_Rol(models.TextChoices):
    CLIENTE = 'Cliente'
    TECNICO = 'Técnico'
    GESTOR = 'Gestor de Tareas'
    ADMIN = 'Administrador del Sitio'

# AREAS DE EJEMPLOS POR AHORA
class Choices_Areas(models.TextChoices):
    CATASTRO = 'Catastro'
    RELACIONES_INTERNACIONALES = 'Relaciones Internacionales'
    ECONOMIA = 'Economia'
    UNIDAD_ASEGURAMIENTO = 'Unidad de Aseguramiento'
    GESTION_PLANEAMIENTO = 'Gestion del Planeamiento'
    ORDENAMIENTO = 'Ordenamiento'
    URBANISMO = 'Urbanismo'
    JURIDICO = 'Juridico'
    CUADROS = 'Cuadros'
    ESQUEMA_Y_PLANES = 'Esquema y Planes'
    COMUNICACION_INSTITUCIONAL = 'Comunicacion Institucional'
    CIENCIA_Y_TECNICA = 'Ciencia y Técnica'
    RECURSOS_HUMANOS = 'Recursos Humanos'
    SEGURIDAD_PROTECCION = 'Seguridad y Protección'
    SERVICIOS_GENERALES = 'Servicios Generales'
    ATENCION_A_LA_POBLACION = 'Atención a la población'
    
    
