from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MensajeContacto

class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha')

admin.site.register(MensajeContacto, MensajeContactoAdmin)

@login_required
def ver_mensajes(request):
    mensajes = MensajeContacto.objects.all().order_by('-fecha')
    return render(request, 'admin_mensajes.html', {'mensajes': mensajes})

# 🔹 Definir correctamente `get_urls()` evitando recursión infinita
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()  # 🔹 Llamamos a las URLs originales
        custom_urls = [
            path('mensajes/', self.admin_view(ver_mensajes), name="admin_mensajes"),
        ]
        return custom_urls + urls  # 🔹 Agregamos las nuevas URLs sin recursión infinita

# Reemplazamos el admin.site predeterminado por nuestro custom admin
admin.site = CustomAdminSite()
