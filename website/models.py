from django.db import models
# Create your models here.

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=100)
    phone   = models.CharField(max_length=11) # 63981476921
    zipcode = models.CharField(max_length=8)
    road    = models.CharField(max_length=100)
    city    = models.CharField(max_length=50)
    state   = models.CharField(max_length=2)

    def __str__(self):
        return (f"{self.name} {self.phone} {self.city} {self.state}")
    
class Agencia(models.Model):
    # Mapeando campos da tabela existente
    id_agencia = models.AutoField(primary_key=True,db_column='id')

    nome = models.CharField(max_length=100, db_column='nome')
    telefone = models.CharField(max_length=11, blank=True, null=True, db_column='telefone')

    # Campos do tipo composto "Endereço" (serão armazenados em colunas separadas)
    endereco = models.JSONField(db_column='endereco')
    
    #cep = models.CharField(max_length=8, db_column='endereco->cep')  # Acesso via JSONField (PostgreSQL)
    #rua = models.CharField(max_length=100, db_column='endereco->rua')
    #cidade = models.CharField(max_length=50, db_column='endereco->cidade')
    #estado = models.CharField(max_length=2, db_column='endereco->estado')
    #complemento = models.TextField(blank=True, null=True, db_column='endereco->complemento')
    
    class Meta:
        managed = False  # Impede o Django de criar/mods a tabela
        db_table = 'crud_locadora.agencia'  # Nome da tabela existente

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    cnh = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, unique=True)
    telefone = models.CharField(max_length=11, blank=True, null=True)
      # Para armazenar o tipo composto como JSON
    endereco = models.JSONField(db_column='endereco')
    class Meta:
        managed = False
        db_table = 'crud_locadora"."cliente'  # Schema + tabela
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome
    
class Categoria(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    nome = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)
    preco_diaria_base = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'crud_locadora"."categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome
    
class Veiculo(models.Model):
    id = models.AutoField(primary_key=True)
    agencia = models.ForeignKey('Agencia', on_delete=models.CASCADE, db_column='id_agencia')
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, db_column='id_categoria')
    placa = models.CharField(max_length=8)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField(blank=True, null=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    tipo_combustivel = models.CharField(max_length=30, blank=True, null=True)
    quilometragem = models.IntegerField(default=0)
    disponivel = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'crud_locadora"."veiculo'
        
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}" 

class Manutencao(models.Model):
    id = models.AutoField(primary_key=True)
    veiculo = models.ForeignKey('Veiculo', on_delete=models.CASCADE, db_column='id_veiculo')
    data_entrada = models.DateField()
    data_saida = models.DateField(null=True, blank=True)
    tipo_problema = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'crud_locadora"."manutencao'
        
    def __str__(self):
        return f"Manutenção #{self.id} - {self.veiculo.placa}"
    
class Aluguel(models.Model):
    STATUS_CHOICES = [
        ('Reservado', 'Reservado'),
        ('Em Curso', 'Em Curso'),
        ('Concluído', 'Concluído'),
        ('Atrasado', 'Atrasado'),
        ('Cancelado', 'Cancelado')
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, db_column='id_cliente')
    veiculo = models.ForeignKey('Veiculo', on_delete=models.CASCADE, db_column='id_veiculo')
    data_retirada = models.DateField()
    data_dev_prev = models.DateField()
    data_dev_real = models.DateField(null=True, blank=True)
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    class Meta:
        managed = False
        db_table = 'crud_locadora"."aluguel'
        
    def __str__(self):
        return f"Aluguel #{self.id} - {self.cliente.nome}"