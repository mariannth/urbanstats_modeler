from django.urls import path
from . import views 
from .views import login_view, register_view, logout_view, lista_mensajes

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('noticias/', views.noticias, name='noticias'),
    path('contacto/', views.contacto, name='contacto'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('informacion/', views.informacion, name='informacion'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/admin/', views.dashboard_admin, name='admin_dashboard'),
    path('dashboard/usuario/', views.dashboard_usuario, name='user_dashboard'),
    path('dashboard/tablas/', views.tablas, name='tablas'),
    path('dashboard/graficas/', views.graficas, name='graficas'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('admin/mensajes/', lista_mensajes, name="admin_mensajes"),

]
