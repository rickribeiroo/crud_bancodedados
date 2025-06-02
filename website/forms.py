from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.db import connection

from .models import Aluguel, Record
from .models import Agencia, Cliente


class AddRecordForm(forms.ModelForm):
    name    = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Nome", "class": "form-control"}),label="")
    phone   = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Telefone", "class": "form-control"}),label="")
    zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "CEP", "class": "form-control"}),label="")
    road    = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Rua", "class": "form-control"}),label="")
    city    = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Cidade", "class": "form-control"}),label="")
    state   = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Estado", "class": "form-control"}),label="")

    class Meta:
        model = Record
        #fields = ['name', 'phone', 'zipcode', 'road', 'city', 'state']
        exclude = ("user",)

class AddAgenciaForm(forms.Form):
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome da agência...'
        })
    )
    
    telefone = forms.CharField(
        max_length=11,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(__) _ ____-____'
        })
    )
    
    cep = forms.CharField(
        max_length=8,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '_____-___'
        })
    )
    
    rua = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o logradouro...'
        })
    )
    
    cidade = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da cidade...'
        })
    )
    
    estado = forms.CharField(
        max_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'UF'
        })
    )
    
    complemento = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Detalhes adicionais...',
            'rows': 3
        })
    )   

    estado = forms.CharField(
        max_length=2,
        validators=[RegexValidator(
            regex='^[A-Z]{2}$',
            message='Digite a sigla do estado com 2 letras maiúsculas'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'UF',
            'style': 'text-transform:uppercase;'
        })
    )

class AddClienteForm(forms.Form):
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome completo do cliente...'
        })
    )
    
    cpf = forms.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex='^\d{11}$',
            message='CPF deve conter 11 dígitos numéricos'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00'
        })
    )
    
    cnh = forms.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex='^\d{11}$',
            message='CNH deve conter 11 dígitos numéricos'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número da CNH...'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemplo@email.com'
        })
    )
    
    telefone = forms.CharField(
        max_length=11,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(__) _ ____-____'
        })
    )
    
    # Campos de endereço
    cep = forms.CharField(
        max_length=8,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00000-000'
        })
    )
    
    rua = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rua, Avenida, etc...'
        })
    )
    
    cidade = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cidade...'
        })
    )
    
    estado = forms.CharField(
        max_length=2,
        validators=[RegexValidator(
            regex='^[A-Z]{2}$',
            message='Sigla do estado com 2 letras maiúsculas'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'UF',
            'style': 'text-transform:uppercase;'
        })
    )
    
    complemento = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Complemento...',
            'rows': 2
        })
    )

class AddCategoriaForm(forms.Form):
    nome = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Econômico'
        })
    )
    
    descricao = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Descrição detalhada da categoria...',
            'rows': 3
        })
    )
    
    preco_diaria_base = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'R$ 0,00'
        })
    )

class AddVeiculoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome FROM crud_locadora.agencia")
            self.fields['agencia'].choices = [(row[0], row[1]) for row in cursor.fetchall()]
            
            cursor.execute("SELECT id, nome FROM crud_locadora.categoria")
            self.fields['categoria'].choices = [(row[0], row[1]) for row in cursor.fetchall()]

    agencia = forms.ChoiceField(
        label="Agência",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    categoria = forms.ChoiceField(
        label="Categoria",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    placa = forms.CharField(
        max_length=8,
        validators=[RegexValidator(
             # Aceita ABC-1D23, ABC 1D23 ou ABC1D23
            message='Formato inválido. Use: AAA-1A23 ou AAA1A23'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'AAA-1A23'
        })
    )
    
    marca = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Ford'
        })
    )
    
    modelo = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Fiesta'
        })
    )
    
    ano = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '2023'
        })
    )
    
    cor = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Prata'
        })
    )
    
    tipo_combustivel = forms.ChoiceField(
        choices=[
            ('', 'Selecione...'),
            ('Gasolina', 'Gasolina'),
            ('Etanol', 'Etanol'),
            ('Diesel', 'Diesel'),
            ('Flex', 'Flex'),
            ('Elétrico', 'Elétrico')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    quilometragem = forms.IntegerField(
        initial=0,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    
    disponivel = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class AddManutencaoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, placa, marca, modelo FROM crud_locadora.veiculo")
            self.fields['veiculo'].choices = [
                (row[0], f"{row[1]} - {row[2]} {row[3]}") for row in cursor.fetchall()
            ]

    veiculo = forms.ChoiceField(
        label="Veículo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    data_entrada = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    data_saida = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    tipo_problema = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descreva o problema identificado...'
        })
    )
    
    custo = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    status = forms.ChoiceField(
        choices=[
            ('Em andamento', 'Em andamento'),
            ('Concluída', 'Concluída'),
            ('Aguardando peças', 'Aguardando peças'),
            ('Cancelada', 'Cancelada')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class AddAluguelForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with connection.cursor() as cursor:
            # Carregar clientes
            cursor.execute("SELECT id, nome, cpf FROM crud_locadora.cliente")
            self.fields['cliente'].choices = [
                (row[0], f"{row[1]} (CPF: {row[2]})") for row in cursor.fetchall()
            ]
            
            # Carregar veículos disponíveis com preço da categoria
            cursor.execute("""
                SELECT v.id, v.placa, v.marca, v.modelo, c.preco_diaria_base 
                FROM crud_locadora.veiculo v
                JOIN crud_locadora.categoria c ON v.id_categoria = c.id
                WHERE v.disponivel = TRUE
            """)
            self.fields['veiculo'].choices = [
                (row[0], f"{row[1]} - {row[2]} {row[3]} (R$ {row[4]}/dia)") 
                for row in cursor.fetchall()
            ]

    cliente = forms.ChoiceField(
        label="Cliente",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    veiculo = forms.ChoiceField(
        label="Veículo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    data_retirada = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }))
    
    data_dev_prev = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }))
    
    status = forms.ChoiceField(
        choices=Aluguel.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}))