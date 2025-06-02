from .models import Agencia
import os
import django

# Configure o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()
# Criar um registro (usando a sequence do PostgreSQL)
nova_agencia = Agencia.objects.create(
    nome="Agência Central",
    telefone="11999999999",
    cep="12345678",
    rua="Rua Principal",
    cidade="São Paulo",
    estado="SP",
    complemento="Sala 101"
)

# Consultar registros
agencias = Agencia.objects.all()
print(agencias)