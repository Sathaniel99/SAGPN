from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .utils import initials, meses
from django.utils.timezone import now
from django.db.models import Q, Count
from datetime import datetime
from .models import Ticket
from .decorators import *
from .forms import *

from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta


# VISTA PRINCIPAL
def Home(request):
    user = request.user
    if user.is_authenticated:
        rol = user.rol
        if rol == "Gestor de Tareas":
            return redirect('reporte_general')
        context = {
            "title_page" : user.rol,
            'tickets_asignados' : Ticket.objects.filter(tecnico = user.id).filter(realizada=False).__len__
            }
        
        if not user.img:
            context["initials"] = initials(request.user.first_name)
            
        return render(request, 'pages/main.html', context)
    
    else:
        return render(request, 'pages/home.html', {"title_page" : "Página Principal" , 'year' : datetime.now().year})

###############################################################
# AUTENTICACION
class SAGPNLoginView(LoginView):
    template_name = 'pages/auth/login.html'
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Autenticación'
        
        return context

class SAGPNLogoutView(LogoutView):
    template_name = 'pages/auth/logged_out.html'
    next_page = '/'
###############################################################
# CREAR UN TICKET
@login_required
@combined_role_required('Cliente', 'Técnico', 'Gestor de Tareas')
def new_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, user=request.user)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.fecha_ini = datetime.now()
            ticket.save()
            return redirect('new_ticket')
    
    form = TicketForm(user=request.user)
    
    context = {"title_page" : "Crear Ticket" , 'form' : form , 'last_url' : '/'}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)
    
    if request.user.rol == 'Gestor de Tareas':
        return render(request, 'pages/modules/gestor_modules/new_ticket.html', context)

    return render(request, 'pages/modules/new_ticket.html', context)

# VISUALIZAR LOS TICKETs COMPLETADOS
@login_required
@combined_role_required('Técnico', 'Gestor de Tareas')
def list_complete_tickets(request):
    tickets = Ticket.objects.filter(realizada = True)
    
    context = {"title_page" : "Tickets Completados" , 'tickets' : tickets, 'last_url' : '/'}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)

    if request.user.rol == 'Gestor de Tareas':
        return render(request, 'pages/modules/gestor_modules/list_all_tickets.html', context)

    return render(request, 'pages/modules/list_all_tickets.html', context)

# VISUALIZAR TODOS LOS TICKETs
@login_required
@combined_role_required('Técnico', 'Gestor de Tareas')
def list_all_tickets(request):
    tickets = Ticket.objects.all()
    
    context = {"title_page" : "Total de Ticket" , 'tickets' : tickets, 'last_url' : '/'}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)

    if request.user.rol == 'Gestor de Tareas':
        return render(request, 'pages/modules/gestor_modules/list_all_tickets.html', context)
    
    return render(request, 'pages/modules/list_all_tickets.html', context)

# VISUALIZAR UN TICKET ESPECIFICO
@login_required
@combined_role_required('Cliente', 'Técnico', 'Gestor de Tareas')
def view_tickets(request, id):
    tickets = Ticket.objects.get(pk=id)
    
    context = {"title_page" : f"Ticket #{id}" , 'tickets' : tickets , 'last_url' : '/'}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)

    return render(request, 'pages/modules/view_tickets.html', context)

# ACTUALIZAR LOS CAMPOS DE UN TICKET
@login_required
@combined_role_required('Cliente', 'Técnico', 'Gestor de Tareas')
def update_tickets(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket_instance = form.save(commit=False)
            ticket_instance.fecha_fin = now().date()
            ticket_instance.save()
            return redirect('update_tickets', id=ticket.id)  

    # Crear una instancia del formulario con los datos actuales del ticket
    form = TicketForm(instance=ticket)
    
    context = {"title_page" : f"Actualizar Ticket #{id}" , 'form' : form , 'last_url' : '/'}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)

    return render(request, 'pages/modules/update_tickets.html', context)

# ELIMINAR UN TICKET
@login_required
@combined_role_required('Cliente', 'Técnico', 'Gestor de Tareas')
def delete_tickets(id):
    get_object_or_404(Ticket, pk=id).delete()
    return redirect('/list_my_tickets/')
    
# LISTAR TICKETS DEL USUARIO AUTENTICADO
# EN CASO DE SER CLIENTE SE MUESTRAN LOS CREADOS POR SI MISMO
# EN CASO DE SER TECNICO SE MUESTRAN LOS ASIGNADOS PARA SI MISMO
@login_required
@combined_role_required('Cliente', 'Técnico')
def list_my_tickets(request):
    if request.user.rol == 'Cliente':
        tickets = Ticket.objects.filter(cliente = request.user.id).filter(realizada=False)
    else:
        tickets = Ticket.objects.filter(tecnico = request.user.id).filter(realizada=False)
    
    context = {"title_page" : "Total de Ticket" , 'tickets' : tickets, 'last_url' : '/'}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)

    return render(request, 'pages/modules/list_all_tickets.html', context)

# TICKETS ASIGNADOS Y/O COMPLETADOS DE UN TECNICO *************************    PROBAR    *************************    PROBAR    *************************
@login_required
@gestor_required
def list_link_tickets(request, id_tecnico):
    tickets = Ticket.objects.filter(tecnico=id_tecnico)
    
    context = {"title_page" : f"Tickets de {Usuario.objects.get(pk=id_tecnico).first_name}" , 'tickets' : tickets, 'last_url' : '/'}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)
    
    return render(request, 'pages/modules/list_all_tickets.html', context)

# ERROR 404 *************************    IMPLEMENTAR    *************************    IMPLEMENTAR    *************************
def error_404(request, exception=None):
    context = {"title_page" : "Error 404"}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)
    return render(request, 'pages/auth/error_404.html', context, status=404)

# ACCESO DENEGADO
def access_denied(request):
    context = {"title_page" : "Acceso denegado"}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)
    
    return render(request, 'pages/auth/access_denied.html', context)

################################################################################################################################################
##############################                               MODULO GESTOR DE TAREAS                              ##############################
################################################################################################################################################
@login_required
@gestor_required
def reporte_general(request):
    # cantidad de usuario, clientes y tecnicos
    users = Usuario.objects.all()
    
    # total de usuarios
    total_usuarios = users.exclude(is_superuser = True).count()
    # total de clientes
    total_clientes = users.filter(rol='Cliente').count()
    # total de tecnicos
    total_tecnicos = users.filter(rol='Técnico').count()
    # total de GESTORES
    total_gestores = users.filter(rol='Gestor de Tareas').count()
    
    # tickets de la BD
    tickets = Ticket.objects.all()
    
    # TICKETS TOTAL DE USUARIOS
    tickets_por_usuarios = tickets.exclude(cliente__is_superuser = True).count()
    
    # TICKETS CREADOS POR CLIENTES
    tickets_clientes = tickets.filter(cliente__rol = 'Cliente').count()
    
    # TICKETS CREADOS POR TECNICOS O GESTORES
    tickets_tecnicos_gestores = tickets.filter(cliente__rol__in=['Técnico', 'Gestor de Tareas']).count()
    
    # tickets de este mes
    tickets_mes = tickets.filter(fecha_ini__month=datetime.now().month, fecha_ini__year=datetime.now().year).count()
    
    ##################################################################################################################################################################
    # Obtener la fecha actual
    today = timezone.now().date()

    # Primer día del mes actual
    first_day_of_month = today.replace(day=1)

    # Último día del mes actual
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Función para calcular la semana relativa al mes
    def week_of_month(date):
        # Calcula el número de semana dentro del mes
        return (date.day - 1) // 7 + 1

    # Anotar cada ticket con su semana relativa al mes
    tickets_por_semana = (
        tickets.filter(fecha_ini__range=(first_day_of_month, last_day_of_month))
        .annotate(
            week_relative=TruncDate("fecha_ini")  # Extraer solo la fecha
        )
        .values("week_relative")  # Agrupar por fecha truncada
        .annotate(
            count=Count("id"),  # Contar tickets por semana
        )
        .order_by("week_relative")
    )

    # Crear un diccionario para almacenar el conteo de tickets creados por semana
    semanas_tickets_creados = {}
    for ticket in tickets_por_semana:
        fecha = ticket["week_relative"]
        semana = week_of_month(fecha)
        if semana not in semanas_tickets_creados:
            semanas_tickets_creados[semana] = 0
        semanas_tickets_creados[semana] += ticket["count"]

    # Preparar los datos para el gráfico de tickets creados
    tickets_creados_semana = [semanas_tickets_creados.get(week, 0) for week in range(1, 5)]  # Asumimos máximo 4 semanas

    # Filtrar tickets finalizados (realizada=True) y agruparlos por semana
    tickets_finalizados_por_semana = (
        tickets.filter(fecha_fin__range=(first_day_of_month, last_day_of_month), realizada=True)
        .annotate(
            week_relative=TruncDate("fecha_fin")  # Extraer solo la fecha
        )
        .values("week_relative")  # Agrupar por fecha truncada
        .annotate(
            count=Count("id"),  # Contar tickets por semana
        )
        .order_by("week_relative")
    )

    # Crear un diccionario para almacenar el conteo de tickets finalizados por semana
    semanas_tickets_finalizados = {}
    for ticket in tickets_finalizados_por_semana:
        fecha = ticket["week_relative"]
        semana = week_of_month(fecha)
        if semana not in semanas_tickets_finalizados:
            semanas_tickets_finalizados[semana] = 0
        semanas_tickets_finalizados[semana] += ticket["count"]

    # Preparar los datos para el gráfico de tickets finalizados
    tickets_finalizados_semana = [semanas_tickets_finalizados.get(week, 0) for week in range(1, 5)]  # Asumimos máximo 4 semanas
    ##################################################################################################################################################################

    # cantida de tickets
    cantidad_tickets = tickets.count()
    
    # cantida de tickets asignados
    tickets_asignados = tickets.exclude(tecnico = None).count()
    
    # tickets completados
    tickets_completados = tickets.filter(realizada = True).count()
    
    # tickets pendientes
    tickets_pendientes = cantidad_tickets - tickets_completados
        
    context = {
        "title_page" : "Reporte general",
        'last_url' : '/',
        'total_usuarios' : total_usuarios,
        'total_clientes' : total_clientes,
        'total_tecnicos' : total_tecnicos,
        'total_gestores' : total_gestores,
        'tickets_por_usuarios' : tickets_por_usuarios,
        'tickets_clientes' : tickets_clientes,
        'tickets_tecnicos_gestores' : tickets_tecnicos_gestores,
        'cantidad_tickets' : cantidad_tickets,
        'tickets_asignados' : tickets_asignados,
        'tickets_completados' : tickets_completados,
        'tickets_pendientes' : tickets_pendientes,
        'tickets_mes' : tickets_mes,
        'fecha' : f"{datetime.now().day}/{meses.get(datetime.now().strftime('%B'))}/{datetime.now().year}",
        'tickets_creados_semana' : tickets_creados_semana,
        'tickets_finalizados_semana' : tickets_finalizados_semana,
    }
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)
    
    return render(request, 'pages/modules/gestor_modules/reporte_general.html', context)

@login_required
@gestor_required
def new_tecnico(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST, rol="Técnico")
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('reporte_general')
    
    form = TecnicoForm(rol="Técnico")

    context = {
        "title_page": "Crear Técnico",
        'last_url': '/reporte_general',
        'fecha' : f"{datetime.now().day}/{meses.get(datetime.now().strftime('%B'))}/{datetime.now().year}",
        'form': form,
    }
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)

    return render(request, 'pages/modules/gestor_modules/new_tecnico.html', context)

@login_required
@gestor_required
def asignar_tickets(request):
    tickets = Ticket.objects.filter(tecnico = None)
    tecnicos = Usuario.objects.filter(rol = 'Técnico')
    
    context = {
        "title_page" : "Asignar Tickets",
        'last_url' : '/reporte_general',
        'fecha' : f"{datetime.now().day}/{meses.get(datetime.now().strftime('%B'))}/{datetime.now().year}",
        'tickets' : tickets,
        'tecnicos' : tecnicos
        }
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)
    
    return render(request, 'pages/modules/gestor_modules/asignar_tickets.html', context)

######################################################################################
################################### LISTAR CUENTAS ###################################
######################################################################################
def list_acc_type(request, users, title):
    context = {
        "title_page" : title,
        'last_url' : '/reporte_general',
        'fecha' : f"{datetime.now().day}/{meses.get(datetime.now().strftime('%B'))}/{datetime.now().year}",
        'users' : users,
        }
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)
    
    return render(request, 'pages/modules/gestor_modules/list_accounts.html', context)

@login_required
@gestor_required
def list_accounts(request):
    users = Usuario.objects.exclude(is_superuser=True).exclude(rol='Gestor de Tareas')
    return list_acc_type(request, users, "Listar Cuentas")

@login_required
@gestor_required
def list_tecnicos(request):
    users = Usuario.objects.filter(rol='Técnico')
    return list_acc_type(request, users, "Listar Técnicos")

# VISUALIZAR TECNICO
@login_required
@gestor_required
def view_user(request, id):
    usuario = Usuario.objects.get(pk = id)
    context = {
        'usuario' : usuario,
        'last_url' : '/',
        'fecha' : f"{datetime.now().day}/{meses.get(datetime.now().strftime('%B'))}/{datetime.now().year}"
        }
    
    if usuario.rol == "Técnico":
        context["title_page"] = f"Técnico #{id}"
    else:
        context["title_page"] = f"Cliente #{id}"
    
    
    
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)

    return render(request, 'pages/modules/gestor_modules/view_user.html', context)

# VISUALIZAR UN TICKET ESPECIFICO
@login_required
@combined_role_required('Cliente', 'Técnico', 'Gestor de Tareas')
def view_tickets(request, id):
    tickets = Ticket.objects.get(pk=id)
    
    context = {"title_page" : f"Ticket #{id}" , 'tickets' : tickets , 'last_url' : '/'}
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)

    return render(request, 'pages/modules/view_tickets.html', context)

@login_required
@gestor_required
def list_clientes(request):
    users = Usuario.objects.filter(rol='Cliente')
    return list_acc_type(request, users, "Listar Clientes")
###############################################################################################################################################
###############################################################################################################################################

def solicitar_account(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST, rol="Cliente")
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('/')
    form = TecnicoForm(rol="Cliente")

    context = {
        "title_page": "Solicitar cuenta",
        'last_url': '/',
        'form': form,
    }
    return render(request, 'pages/auth/solicitar_account.html', context)
    
def solicitudes_accounts(request):
    users = Usuario.objects.filter(is_active = False)
    
    context = {
        "title_page" : "Solicitudes de Cuenta",
        'last_url' : '/reporte_general',
        'fecha' : f"{datetime.now().day}/{meses.get(datetime.now().strftime('%B'))}/{datetime.now().year}",
        'users' : users,
        }
    if not request.user.img:
        context["initials"] = initials(request.user.first_name)
    
    return render(request, 'pages/modules/gestor_modules/solicitudes_accounts.html', context)


@login_required
@gestor_required
def asignacion_ticket(request, id_ticket, id_usuario):
    ticket = Ticket.objects.get(pk = id_ticket)
    ticket.tecnico = Usuario.objects.get(pk = id_usuario)
    ticket.save()
    return redirect('asignar_tickets')

@login_required
@gestor_required
def delete_account(id):
    get_object_or_404(Usuario, pk=id).delete()
    return redirect('/list_my_tickets/')

@login_required
@gestor_required
def cambiar_estado_account(id_user, estado):
    if estado == 'True':
        ax = True
    else:
        ax = False
    account = Usuario.objects.get(id = id_user)
    account.is_active = ax
    account.save()
    
    return redirect('/solicitudes_accounts')
    

################################################################################################################################################
#################################                                VISTAS ENDPOINTS                               ################################
################################################################################################################################################
# ENDPOINT PARA OBTENER TODOS LOS TICKETS POR UN STRING
def search_ticket(request):
    ax = request.GET.get("search-input")
    tickets = Ticket.objects.filter(
            Q(cliente__first_name__icontains=ax) | Q(tecnico__first_name__icontains=ax) |
            Q(situacion__icontains=ax) | Q(area__icontains=ax) | 
            Q(descripcion__icontains=ax) | Q(prioridad__icontains=ax)
        )
    html = render(request, 'includes/cards_tickets_list_template.html', {'tickets' : tickets})
    
    return HttpResponse(html)

# ENDPOINT PARA OBTENER UN TICKETS POR UN ID
def search_ticket_id(request,id):
    ticket = Ticket.objects.filter(pk = id)
    html = render(request, 'includes/consultar_ticket_template_modal.html', {'tickets' : ticket})
    return HttpResponse(html)


# ENDPOINT PARA OBTENER TODOS LOS TICKETS DE UN USUARIO POR UN STRING
# EN CASO DE SER CLIENTE SE MUESTRAN LOS CREADOS POR SI MISMO
# EN CASO DE SER TECNICO SE MUESTRAN LOS ASIGNADOS PARA SI MISMO
def search_ticket_own(request):
    ax = request.GET.get("search-input")
    user = request.user
    
    tickets = Ticket.objects.filter(
            Q(cliente__first_name__icontains=ax) | Q(tecnico__first_name__icontains=ax) |
            Q(situacion__icontains=ax) | Q(area__icontains=ax) | 
            Q(descripcion__icontains=ax) | Q(prioridad__icontains=ax)
        )
    if user.rol == 'Cliente':
        tickets = tickets.filter(cliente = user.id)
    else:
        tickets = tickets.filter(tecnico = user.id)
    
    html = render(request, 'includes/cards_tickets_list_template.html', {'tickets' : tickets})
    
    return HttpResponse(html)

