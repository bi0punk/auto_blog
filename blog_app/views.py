from django.views.generic import ListView
from django.http import HttpResponse
from .models import Category, Post
import plotly.graph_objects as go
import plotly.offline as opy

def test_html(request):
    planetas = ['Mercurio', 'Venus', 'Tierra', 'Marte', 'Júpiter', 'Saturno', 'Urano', 'Neptuno']
    distancias_au = [0.38709893, 0.72333199, 1, 1.52366231, 5.20336301, 9.53707032, 19.19126393, 30.06896348]

    fig = go.Figure(data=[go.Scatter3d(
        x=distancias_au,
        y=[0] * len(planetas),
        z=list(range(len(planetas))),
        mode='markers+text',
        marker=dict(size=12, color=distancias_au, colorscale='Viridis', opacity=0.8),
        text=planetas,
        textposition="bottom center"
    )])

    fig.update_layout(
        title="Posición de los Planetas en el Sistema Solar",
        title_x=0.5,
        margin=dict(l=0, r=0, b=0, t=30),
        scene=dict(xaxis_title='Distancia al Sol (UA)', yaxis_title='Eje Y', zaxis_title='Eje Z')
    )

    div = opy.plot(fig, auto_open=False, output_type='div')
    return HttpResponse(div)

class PostListView(ListView):
    model = Post
    paginate_by = 3

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
            return self.model.objects.filter(categories__in=[int(category_id)])
        return self.model.objects.all()

class CategoryListView(ListView):
    model = Category

