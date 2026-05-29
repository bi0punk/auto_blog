import json
import locale
from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from .models import Post


def post_list(request):
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except locale.Error:
            pass

    ahora = datetime.now()
    fecha_formateada = ahora.strftime("%A, %d de %B de %Y")

    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    latest = posts_list.first()
    if latest:
        last_event = {
            'place': latest.location or latest.title,
            'mag': latest.magnitude,
            'depth_km': latest.depth_km,
            'lat': latest.latitude,
            'lon': latest.longitude,
            'time_utc': latest.utc_time,
            'source': 'sismologia.cl',
            'url': 'https://www.sismologia.cl',
        }
    else:
        last_event = None

    depth_series = [
        {
            'time': p.utc_time.isoformat() if p.utc_time else '',
            'depth_km': p.depth_km,
            'mag': p.magnitude,
            'place': p.location or p.title,
        }
        for p in posts_list
        if p.depth_km is not None
    ]
    depth_series_json = json.dumps(list(reversed(depth_series)))

    context = {
        'posts': posts,
        'fecha': fecha_formateada,
        'last_event': last_event,
        'depth_series_json': depth_series_json,
    }
    return render(request, 'blog/index.html', context)
