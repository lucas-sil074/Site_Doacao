from django.shortcuts import render, redirect # type: ignore
from .models import Doador, Paciente
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.shortcuts import render # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore


# Página Inicial
def home(request):
    return render(request, 'home.html')

# Cadastro de Doador
def cadastro_doador(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        tipo_sanguineo = request.POST['tipo_sanguineo']
        data_nascimento = request.POST['data_nascimento']
        Doador.objects.create(nome=nome, email=email, tipo_sanguineo=tipo_sanguineo, data_nascimento=data_nascimento)
        return redirect('home')
    return render(request, 'cadastro_doador.html')

# Cadastro de Paciente
def cadastro_paciente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        tipo_sanguineo = request.POST['tipo_sanguineo']
        necessidade = request.POST['necessidade']
        Paciente.objects.create(nome=nome, tipo_sanguineo=tipo_sanguineo, necessidade=necessidade)
        return redirect('home')
    return render(request, 'cadastro_paciente.html')

# Edição de Paciente
def editar_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    if request.method == 'POST':
        paciente.nome = request.POST.get('nome')
        paciente.tipo_sanguineo = request.POST.get('tipo_sanguineo')
        paciente.necessidade = request.POST.get('necessidade')
        paciente.save()
        return redirect('gerenciar')
    return render(request, 'editar_paciente.html', {'paciente': paciente})

# Edição de Doador
def editar_doador(request, id):
    doador = Doador.objects.get(id=id)
    if request.method == 'POST':
        doador.nome = request.POST.get('nome')
        doador.email = request.POST.get('email')
        doador.tipo_sanguineo = request.POST.get('tipo_sanguineo')
        doador.data_nascimento = request.POST.get('data_nascimento')
        doador.save()
        return redirect('gerenciar')
    return render(request, 'editar_doador.html', {'doador': doador})

# Função de Busca
def busca(request):
    pacientes = []
    doadores_compatíveis = {}

    if request.method == "POST":
        nome_paciente = request.POST.get('nome_paciente', '').strip()
        
        # Verifique se o nome do paciente não está vazio
        if nome_paciente:
            pacientes = Paciente.objects.filter(nome__icontains=nome_paciente)

            # Tabela de compatibilidade sanguínea
            compatibilidade = {
                "O+": ["O+", "O-"],
                "O-": ["O-"],
                "A+": ["A+", "A-", "O+", "O-"],
                "A-": ["A-", "O-"],
                "B+": ["B+", "B-", "O+", "O-"],
                "B-": ["B-", "O-"],
                "AB+": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
                "AB-": ["A-", "B-", "O-", "AB-"]
            }

            # Processar compatibilidade para cada paciente encontrado
            for paciente in pacientes:
                tipos_compatíveis = compatibilidade.get(paciente.tipo_sanguineo, [])
                
                if tipos_compatíveis:
                    # Consultar doadores compatíveis
                    doadores = Doador.objects.filter(tipo_sanguineo__in=tipos_compatíveis)
                    # Mapear doadores compatíveis para cada paciente
                    doadores_compatíveis[paciente.id] = doadores

    return render(request, 'busca.html', {
        'pacientes': pacientes,
        'doadores_compatíveis': doadores_compatíveis
    })

# Página de Gerenciamento de Pacientes e Doadores
@login_required
def gerenciar(request):
    pacientes = Paciente.objects.all()
    doadores = Doador.objects.all()
    return render(request, 'gerenciar.html', {'pacientes': pacientes, 'doadores': doadores})

def home(request):
    return render(request, 'home.html')

# Deletar Paciente
def deletar_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    paciente.delete()
    return redirect('gerenciar')

# Deletar Doador
def deletar_doador(request, id):
    doador = Doador.objects.get(id=id)
    doador.delete()
    return redirect('gerenciar')

# Login do Administrador

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('gerenciar')  # Redireciona para a página de gerenciamento
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

# Logout do Administrador
def logout_view(request):
    logout(request)
    return redirect('login')
