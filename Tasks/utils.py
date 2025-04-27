def initials(value):
    if not value:
        return ""
    parts = value.split()
    return ''.join([part[0].upper() for part in parts if part])

dias = {
    "Monday" : "Lunes",
    "Tuesday" : "Martes",
    "Wednesday" : "Miércoles",
    "Thursday" : "Jueves",
    "Friday" : "Viernes",
    "Saturday" : "Sábado",
    "Sunday" : "Domingo",
}

meses = {
    "January" : "Enero",
    "February" : "Febrero",
    "March" : "Marzo",
    "April" : "Abril",
    "May" : "Mayo",
    "June" : "Junio",
    "July" : "Julio",
    "August" : "Agosto",
    "September" : "Septiembre",
    "October" : "Octubre",
    "November" : "Noviembre",
    "December" : "Diciembre",
}