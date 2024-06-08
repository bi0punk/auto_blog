# blog/views.py
from django.shortcuts import render
from .models import Post
from datetime import datetime
import locale

def post_list(request):
    # Configura la localización a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    ahora = datetime.now()
    fecha_formateada = ahora.strftime("%A, %d de %B de %Y")
    posts = Post.objects.all()
    
    # Renderiza la plantilla con los posts y la fecha formateada
    return render(request, 'blog/index.html', {'posts': posts, 'fecha': fecha_formateada})
