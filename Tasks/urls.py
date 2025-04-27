from django.urls import path
from .views import *


urlpatterns = [
    path("", Home , name="home"),
    path('login/', SAGPNLoginView.as_view(), name='login'),
    path('logout/', SAGPNLogoutView.as_view(), name='logout'),
    path('solicitar_account', solicitar_account, name='solicitar_account'),
    path('access_denied', access_denied, name='access_denied'),
    
    path('new_ticket/', new_ticket, name='new_ticket'),
    path('list_all_tickets/', list_all_tickets, name='list_all_tickets'),
    path('list_complete_tickets/', list_complete_tickets, name='list_complete_tickets'),
    path('list_my_tickets/', list_my_tickets, name='list_my_tickets'),
    path('list_link_tickets/', list_all_tickets, name='list_link_tickets'),
    path('view_tickets/<int:id>', view_tickets, name='view_tickets'),
    path('update_tickets/<int:id>', update_tickets, name='update_tickets'),
    path('delete_tickets/<int:id>', delete_tickets, name='delete_tickets'),
    
    path('reporte_general', reporte_general, name='reporte_general'),
    path('new_tecnico', new_tecnico, name='new_tecnico'),
    path('solicitudes_accounts', solicitudes_accounts, name='solicitudes_accounts'),
    path('list_accounts', list_accounts, name='list_accounts'),
    path('list_tecnicos', list_tecnicos, name='list_tecnicos'),
    path('view_user/<int:id>', view_user, name='view_user'),
    path('list_clientes', list_clientes, name='list_clientes'),
    path('asignar_tickets', asignar_tickets, name='asignar_tickets'),
    
    
    path('cambiar_estado_account/<int:id_user>_<str:estado>', cambiar_estado_account, name='cambiar_estado_account'),
    path('delete_account/<int:id_user>', delete_account, name='delete_account'),
    path('search_ticket', search_ticket, name='search_ticket'),
    path('search_ticket_id/<int:id>', search_ticket_id, name='search_ticket_id'),
    path('search_ticket_own', search_ticket_own, name='search_ticket_own'),
    path('asignacion_ticket/<int:id_ticket>/<int:id_usuario>', asignacion_ticket, name='asignacion_ticket'),
]