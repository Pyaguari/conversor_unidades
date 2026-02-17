from django.urls import path
from . import views

app_name = "conversor"

urlpatterns = [
    path("", views.seleccionar_magnitud, name="seleccionar_magnitud"),
    path("convertir/<int:magnitud_id>/", views.convertir_view, name="convertir"),
    path('debug/<int:magnitud_id>/', views.debug_magnitud, name='debug'),  # ← Temporal
   
]