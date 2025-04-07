from django.shortcuts import render, redirect
import random  # Solo para generar algunos datos de ejemplo para las gráficas
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required, user_passes_test
import openai
from django.conf import settings
from django.http import JsonResponse
import pandas as pd
from django.conf import settings
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
import seaborn as sns
import io
import urllib
import base64
from django.http import HttpResponse

openai.api_key = settings.OPENAI_API_KEY
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        
        # Llamar a la API de OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",  # O el modelo que elijas
            prompt=user_message,
            max_tokens=150
        )

        chatbot_reply = response.choices[0].text.strip()
        
        # Devolver la respuesta del chatbot
        return JsonResponse({'response': chatbot_reply})
    
    return render(request, 'chatbot.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirige al admin
            else:
                return redirect('user_dashboard')  # Redirige al usuario normal
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # o la página a la que quieras redirigir después
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_admin(request):
    return render(request, 'admin_dashboard.html')

@login_required
def dashboard_usuario(request):
    if request.user.is_superuser:
        return redirect('dashboard_admin')
    return render(request, 'user_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required
# def dashboard_admin(request):
#     return render(request, 'admin_dashboard.html')

# @login_required
# def dashboard_usuario(request):
#     return render(request, 'user_dashboard.html')

def inicio(request):
    return render(request, 'inicio.html')
def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def noticias(request):
    return render(request, 'noticias.html')

def contacto(request):
    return render(request, 'contacto.html')

def newsletter(request):
    return render(request, 'newsletter.html')

def informacion(request):
    return render(request, 'informacion.html')


@login_required
def dashboard_usuario(request):
    return render(request, 'user_dashboard.html')

@login_required
def tablas(request):
    return render(request, 'tablas.html')

@login_required
def graficas(request):
    return render(request, 'graficas.html')

# @login_required
# def pagina3(request):
#     return render(request, 'pagina3.html')

# ----------------------------------------
#
#               TABLAS
#
# ----------------------------------------


def tablas(request):
    # Ruta del archivo CSV
    csv_path = os.path.join(settings.BASE_DIR, 'principal', 'static', 'csv', 'archivo_combinado.csv')
    
    # Cargar solo las primeras 100 filas del archivo CSV
    try:
        df = pd.read_csv(csv_path, nrows=100)
    except FileNotFoundError:
        # Manejo de error si el archivo no se encuentra
        return render(request, 'tablas.html', {'error': 'El archivo CSV no se pudo encontrar.'})
    
    # Convertir el DataFrame a HTML
    tabla_html = df.to_html(classes='table table-bordered table-striped', index=False)

    # Pasar la tabla a la plantilla
    return render(request, 'tablas.html', {'tabla': tabla_html})


# ----------------------------------------
#
#               GRÁFICAS
#
# ----------------------------------------

# Función para cargar el CSV y generar la gráfica
def generar_grafica():
    csv_path = os.path.join(settings.BASE_DIR, 'principal', 'static', 'csv', 'archivo_combinado.csv')

    # Cargar el CSV
    df = pd.read_csv(csv_path, nrows=100)  # Solo cargamos las primeras 100 filas para rendimiento

    # Verificar que haya datos suficientes para graficar
    if df.shape[1] < 2:
        return None

    # Crear la gráfica con Seaborn
    plt.figure(figsize=(8, 5))
    sns.barplot(x=df.iloc[:, 0], y=df.iloc[:, 1])  # Primera columna en X y segunda en Y
    plt.xticks(rotation=90)  # Rotar etiquetas del eje X
    plt.title("Ejemplo de Gráfica de Barras")
    plt.xlabel(df.columns[0])
    plt.ylabel(df.columns[1])

    # Guardar la gráfica en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)

    # Convertir la imagen a base64 para enviarla a la plantilla
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return image_base64

# Vista para la página de gráficas
def graficas(request):
    grafica_base64 = generar_grafica()

    return render(request, 'graficas.html', {'grafica': grafica_base64})


# ----------------------------------------
#
#               CONTACTO
#
# ----------------------------------------
from django.contrib import messages
from .forms import ContactoForm
from django.contrib.auth.decorators import login_required
from .models import MensajeContacto


def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu mensaje se ha enviado correctamente. ¡Gracias por contactarnos!")
            return redirect('contacto')  # Redirige a la misma página para limpiar el formulario
    else:
        form = ContactoForm()
    
    return render(request, 'contacto.html', {'form': form})

@login_required
def lista_mensajes(request):
    mensajes = MensajeContacto.objects.all().order_by('-fecha')
    return render(request, 'admin_mensajes.html', {'mensajes': mensajes})

