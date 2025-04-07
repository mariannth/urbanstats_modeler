# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Evita archivos pyc y mejora logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Copia y actualiza pip, luego instala dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del proyecto al contenedor
COPY . /app/

# Recolecta archivos estáticos (evita errores si no hay)
RUN python manage.py collectstatic --noinput || true

# Expone el puerto donde correrá gunicorn
EXPOSE 8000

# Comando para ejecutar la app usando gunicorn
CMD ["gunicorn", "mi_proyecto.wsgi:application", "--bind", "0.0.0.0:8000"]
