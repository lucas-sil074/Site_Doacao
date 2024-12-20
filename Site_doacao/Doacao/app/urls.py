from django.urls import path # type: ignore
from django.contrib.auth import logout # type: ignore
from . import views

def logout_view(request):
    logout(request)
    return redirect('login') # type: ignore

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('home/', views.home, name='home'),  # Alias para a página inicial
    path('cadastro_doador/', views.cadastro_doador, name='cadastro_doador'),
    path('cadastro_paciente/', views.cadastro_paciente, name='cadastro_paciente'),
    path('gerenciar/', views.gerenciar, name='gerenciar'),
    path('editar_paciente/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('editar_doador/<int:id>/', views.editar_doador, name='editar_doador'),
    path('deletar_paciente/<int:id>/', views.deletar_paciente, name='deletar_paciente'),
    path('deletar_doador/<int:id>/', views.deletar_doador, name='deletar_doador'),
    path('busca/', views.busca, name='busca'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
