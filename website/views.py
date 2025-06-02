import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection

from .forms import AddRecordForm, AddAgenciaForm, AddClienteForm, AddCategoriaForm, AddVeiculoForm, AddManutencaoForm, AddAluguelForm
from .models import Aluguel, Cliente, Record

# Create your views here.

def home(request): 
    records = Record.objects.all()
    clientes = Cliente.objects.all()

    return render(request, "home.html",{'records': records}) 


def record_record(request, pk):
    obj_record= Record.objects.get(id=pk)
    return render(request, 'record.html', {'obj_record':obj_record})


def delete_record(request, pk):
    delete_obj = Record.objects.get(id=pk)
    delete_obj.delete()
    #messages.success(request,"Item deletado!")
    return redirect('home')

    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid(): 
            add_record = form.save()
            messages.success(request, "Registro Adicionado!")
            return redirect('home')
    return render(request, 'add_record.html', {'form':form})
    
    #messages.success(request, "Registro NÃO Adicionado...")
    #return redirect('home') 


def update_record(request, pk):
    current_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request, "Registro Alterado!")
        return redirect('home')
    return render(request, 'update_record.html', {'form':form})

def lista_agencias(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id, 
                nome, 
                telefone, 
                (endereco).cep, 
                (endereco).rua, 
                (endereco).cidade, 
                (endereco).estado 
            FROM crud_locadora.agencia
        """)
        agencias = cursor.fetchall()

    return render(request, 'lista_agencias.html', {'agencias': agencias})

def add_agencia(request):
    if request.method == 'POST':
        # Capturar dados do formulário
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        complemento = request.POST.get('complemento')

        # Inserir usando o tipo composto do PostgreSQL
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO crud_locadora.agencia (nome, telefone, endereco)
                VALUES (%s, %s, ROW(%s, %s, %s, %s, %s)::crud_locadora.endereco)
            """, [nome, telefone, cep, rua, cidade, estado, complemento])
        
        return redirect('lista_agencias')
    
    # Se for GET, mostrar formulário vazio
    form = AddAgenciaForm()
    return render(request, 'add_agencia.html', {'form': form})

def edit_agencia(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id,
                nome,
                telefone,
                (endereco).cep,
                (endereco).rua,
                (endereco).cidade,
                (endereco).estado,
                (endereco).complemento
            FROM crud_locadora.agencia
            WHERE id = %s
        """, [id])
        agencia = cursor.fetchone()

    if not agencia:
        return redirect('lista_agencias')

    if request.method == 'POST':
        form = AddAgenciaForm(request.POST)
        if form.is_valid():
            # Extrair dados do formulário
            dados = form.cleaned_data
            
            # Atualizar registro via SQL
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE crud_locadora.agencia SET
                        nome = %s,
                        telefone = %s,
                        endereco = ROW(%s, %s, %s, %s, %s)::crud_locadora.endereco
                    WHERE id = %s
                """, [
                    dados['nome'],
                    dados['telefone'],
                    dados['cep'],
                    dados['rua'],
                    dados['cidade'],
                    dados['estado'],
                    dados['complemento'],
                    id
                ])
            return redirect('lista_agencias')
    else:
        # Preencher formulário com dados existentes
        initial_data = {
            'nome': agencia[1],
            'telefone': agencia[2],
            'cep': agencia[3],
            'rua': agencia[4],
            'cidade': agencia[5],
            'estado': agencia[6],
            'complemento': agencia[7]
        }
        form = AddAgenciaForm(initial=initial_data)

    return render(request, 'edit_agencia.html', {
        'form': form,
        'agencia_id': id
    })

def delete_agencia(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Verifica se a agência existe
                cursor.execute("SELECT id FROM crud_locadora.agencia WHERE id = %s", [id])
                if not cursor.fetchone():
                    messages.error(request, 'Agência não encontrada!')
                    return redirect('agencias')
                
                # Executa a exclusão
                cursor.execute("DELETE FROM agencia WHERE id = %s", [id])
                messages.success(request, 'Agência excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir agência: {str(e)}')
        
        return redirect('lista_agencias')
    
    # Bloqueia acesso via GET
    messages.warning(request, 'Método não permitido!')
    return redirect('lista_agencias')



def add_cliente(request):
    if request.method == 'POST':
        form = AddClienteForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO crud_locadora.cliente 
                    (nome, cpf, cnh, email, telefone, endereco)
                    VALUES (%s, %s, %s, %s, %s, ROW(%s, %s, %s, %s, %s)::crud_locadora.endereco)
                """, [
                    form.cleaned_data['nome'],
                    form.cleaned_data['cpf'],
                    form.cleaned_data['cnh'],
                    form.cleaned_data['email'],
                    form.cleaned_data['telefone'],
                    form.cleaned_data['cep'],
                    form.cleaned_data['rua'],
                    form.cleaned_data['cidade'],
                    form.cleaned_data['estado'],
                    form.cleaned_data['complemento']
                ])
            return redirect('lista_clientes')
    else:
        form = AddClienteForm()
    return render(request, 'add_cliente.html', {'form': form})

def lista_clientes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id,
                nome,
                cpf,
                cnh,
                email,
                telefone,
                (endereco).cep AS cep,
                (endereco).rua AS rua,
                (endereco).cidade AS cidade,
                (endereco).estado AS estado,
                (endereco).complemento AS complemento
            FROM crud_locadora.cliente
        """)
        clientes = [
            {
                'id': row[0],
                'nome': row[1],
                'cpf': row[2],
                'cnh': row[3],
                'email': row[4],
                'telefone': row[5],
                'endereco': {
                    'cep': row[6],
                    'rua': row[7],
                    'cidade': row[8],
                    'estado': row[9],
                    'complemento': row[10]
                }
            }
            for row in cursor.fetchall()
        ]
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def delete_cliente(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM crud_locadora.cliente WHERE id = %s", [id])
        except Exception as e:
            pass  # Tratar erro adequadamente
    return redirect('lista_clientes')

def edit_cliente(request, id):
    # Buscar dados atuais do cliente
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id,
                nome,
                cpf,
                cnh,
                email,
                telefone,
                (endereco).cep,
                (endereco).rua,
                (endereco).cidade,
                (endereco).estado,
                (endereco).complemento
            FROM crud_locadora.cliente
            WHERE id = %s
        """, [id])
        cliente = cursor.fetchone()

    if not cliente:
        return redirect('lista_clientes')

    if request.method == 'POST':
        form = AddClienteForm(request.POST)
        if form.is_valid():
            # Extrair dados do formulário
            dados = form.cleaned_data
            
            # Atualizar registro via SQL
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE crud_locadora.cliente SET
                        nome = %s,
                        cpf = %s,
                        cnh = %s,
                        email = %s,
                        telefone = %s,
                        endereco = ROW(%s, %s, %s, %s, %s)::crud_locadora.endereco
                    WHERE id = %s
                """, [
                    dados['nome'],
                    dados['cpf'],
                    dados['cnh'],
                    dados['email'],
                    dados['telefone'],
                    dados['cep'],
                    dados['rua'],
                    dados['cidade'],
                    dados['estado'],
                    dados['complemento'],
                    id
                ])
            return redirect('lista_clientes')
    else:
        # Preencher formulário com dados existentes
        initial_data = {
            'nome': cliente[1],
            'cpf': cliente[2],
            'cnh': cliente[3],
            'email': cliente[4],
            'telefone': cliente[5],
            'cep': cliente[6],
            'rua': cliente[7],
            'cidade': cliente[8],
            'estado': cliente[9],
            'complemento': cliente[10]
        }
        form = AddClienteForm(initial=initial_data)

    return render(request, 'edit_cliente.html', {
        'form': form,
        'cliente_id': id
    })



def lista_categorias(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM crud_locadora.categoria")
        columns = [col[0] for col in cursor.description]
        categorias = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def add_categoria(request):
    if request.method == 'POST':
        form = AddCategoriaForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO crud_locadora.categoria 
                    (nome, descricao, preco_diaria_base)
                    VALUES (%s, %s, %s)
                """, [
                    form.cleaned_data['nome'],
                    form.cleaned_data['descricao'],
                    form.cleaned_data['preco_diaria_base']
                ])
            return redirect('lista_categorias')
    else:
        form = AddCategoriaForm()
    return render(request, 'add_categoria.html', {'form': form})

def edit_categoria(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM crud_locadora.categoria WHERE id = %s", [id])
        categoria = cursor.fetchone()

    if not categoria:
        return redirect('lista_categorias')

    if request.method == 'POST':
        form = AddCategoriaForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE crud_locadora.categoria SET
                        nome = %s,
                        descricao = %s,
                        preco_diaria_base = %s
                    WHERE id = %s
                """, [
                    form.cleaned_data['nome'],
                    form.cleaned_data['descricao'],
                    form.cleaned_data['preco_diaria_base'],
                    id
                ])
            return redirect('lista_categorias')
    else:
        initial_data = {
            'nome': categoria[1],
            'descricao': categoria[2],
            'preco_diaria_base': categoria[3]
        }
        form = AddCategoriaForm(initial=initial_data)

    return render(request, 'edit_categoria.html', {
        'form': form,
        'categoria_id': id
    })

def delete_categoria(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM crud_locadora.categoria WHERE id = %s", [id])
    return redirect('lista_categorias')


def lista_veiculos(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.id, 
                   a.nome AS agencia_nome,  -- Alias diferente para agência
                   c.nome AS categoria_nome, -- Alias diferente para categoria
                   v.placa, v.marca, v.modelo, 
                   v.ano, v.disponivel, v.quilometragem
            FROM crud_locadora.veiculo v
            JOIN crud_locadora.agencia a ON v.id_agencia = a.id
            JOIN crud_locadora.categoria c ON v.id_categoria = c.id
        """)
        columns = [col[0] for col in cursor.description]
        veiculos = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'lista_veiculos.html', {'veiculos': veiculos})

def add_veiculo(request):
    if request.method == 'POST':
        form = AddVeiculoForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO crud_locadora.veiculo (
                        id_agencia, id_categoria, placa, marca, modelo,
                        ano, cor, tipo_combustivel, quilometragem, disponivel
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    form.cleaned_data['agencia'],
                    form.cleaned_data['categoria'],
                    form.cleaned_data['placa'],
                    form.cleaned_data['marca'],
                    form.cleaned_data['modelo'],
                    form.cleaned_data['ano'],
                    form.cleaned_data['cor'],
                    form.cleaned_data['tipo_combustivel'],
                    form.cleaned_data['quilometragem'],
                    form.cleaned_data.get('disponivel', False)
                ])
            return redirect('lista_veiculos')
    else:
        form = AddVeiculoForm()
    return render(request, 'add_veiculo.html', {'form': form})

def edit_veiculo(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM crud_locadora.veiculo WHERE id = %s", [id])
        veiculo = cursor.fetchone()

    if not veiculo:
        return redirect('lista_veiculos')

    if request.method == 'POST':
        form = AddVeiculoForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE crud_locadora.veiculo SET
                        id_agencia = %s,
                        id_categoria = %s,
                        placa = %s,
                        marca = %s,
                        modelo = %s,
                        ano = %s,
                        cor = %s,
                        tipo_combustivel = %s,
                        quilometragem = %s,
                        disponivel = %s
                    WHERE id = %s
                """, [
                    form.cleaned_data['agencia'],
                    form.cleaned_data['categoria'],
                    form.cleaned_data['placa'],
                    form.cleaned_data['marca'],
                    form.cleaned_data['modelo'],
                    form.cleaned_data['ano'],
                    form.cleaned_data['cor'],
                    form.cleaned_data['tipo_combustivel'],
                    form.cleaned_data['quilometragem'],
                    form.cleaned_data.get('disponivel', False),
                    id
                ])
            return redirect('lista_veiculos')
    else:
        initial_data = {
            'agencia': veiculo[1],
            'categoria': veiculo[2],
            'placa': veiculo[3],
            'marca': veiculo[4],
            'modelo': veiculo[5],
            'ano': veiculo[6],
            'cor': veiculo[7],
            'tipo_combustivel': veiculo[8],
            'quilometragem': veiculo[9],
            'disponivel': veiculo[10]
        }
        form = AddVeiculoForm(initial=initial_data)
    
    return render(request, 'edit_veiculo.html', {
        'form': form,
        'veiculo_id': id
    })

def delete_veiculo(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM crud_locadora.veiculo WHERE id = %s", [id])
    return redirect('lista_veiculos')

def lista_manutencoes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.id, v.placa, m.data_entrada, m.data_saida, 
                   m.tipo_problema, m.custo, m.status
            FROM crud_locadora.manutencao m
            JOIN crud_locadora.veiculo v ON m.id_veiculo = v.id
            ORDER BY m.data_entrada DESC
        """)
        columns = [col[0] for col in cursor.description]
        manutencoes = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'lista_manutencoes.html', {'manutencoes': manutencoes})

def add_manutencao(request):
    if request.method == 'POST':
        form = AddManutencaoForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO crud_locadora.manutencao (
                        id_veiculo, data_entrada, data_saida,
                        tipo_problema, custo, status
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, [
                    form.cleaned_data['veiculo'],
                    form.cleaned_data['data_entrada'],
                    form.cleaned_data['data_saida'],
                    form.cleaned_data['tipo_problema'],
                    form.cleaned_data['custo'],
                    form.cleaned_data['status']
                ])
            return redirect('lista_manutencoes')
    else:
        form = AddManutencaoForm()
    return render(request, 'add_manutencao.html', {'form': form})

def edit_manutencao(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM crud_locadora.manutencao 
            WHERE id = %s
        """, [id])
        manutencao = cursor.fetchone()

    if not manutencao:
        return redirect('lista_manutencoes')

    if request.method == 'POST':
        form = AddManutencaoForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE crud_locadora.manutencao SET
                        id_veiculo = %s,
                        data_entrada = %s,
                        data_saida = %s,
                        tipo_problema = %s,
                        custo = %s,
                        status = %s
                    WHERE id = %s
                """, [
                    form.cleaned_data['veiculo'],
                    form.cleaned_data['data_entrada'],
                    form.cleaned_data['data_saida'],
                    form.cleaned_data['tipo_problema'],
                    form.cleaned_data['custo'],
                    form.cleaned_data['status'],
                    id
                ])
            return redirect('lista_manutencoes')
    else:
        initial_data = {
            'veiculo': manutencao[1],
            'data_entrada': manutencao[2],
            'data_saida': manutencao[3],
            'tipo_problema': manutencao[4],
            'custo': manutencao[5],
            'status': manutencao[6]
        }
        form = AddManutencaoForm(initial=initial_data)
    
    return render(request, 'edit_manutencao.html', {
        'form': form,
        'manutencao_id': id
    })

def delete_manutencao(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM crud_locadora.manutencao WHERE id = %s", [id])
    return redirect('lista_manutencoes')

def lista_alugueis(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id, c.nome, v.placa, a.data_retirada, 
                   a.data_dev_prev, a.status, a.valor_total
            FROM crud_locadora.aluguel a
            JOIN crud_locadora.cliente c ON a.id_cliente = c.id
            JOIN crud_locadora.veiculo v ON a.id_veiculo = v.id
            ORDER BY a.data_retirada DESC
        """)
        columns = [col[0] for col in cursor.description]
        alugueis = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'lista_alugueis.html', {'alugueis': alugueis})

def add_aluguel(request):
    if request.method == 'POST':
        form = AddAluguelForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                # Obter preço da diária da categoria do veículo
                cursor.execute("""
                    SELECT c.preco_diaria_base 
                    FROM crud_locadora.veiculo v
                    JOIN crud_locadora.categoria c ON v.id_categoria = c.id
                    WHERE v.id = %s
                """, [form.cleaned_data['veiculo']])
                preco_diaria = cursor.fetchone()[0]

                # Calcular dias e valor total
                data_retirada = form.cleaned_data['data_retirada']
                data_dev_prev = form.cleaned_data['data_dev_prev']
                dias = (data_dev_prev - data_retirada).days
                valor_total = dias * preco_diaria

                # Inserir aluguel
                cursor.execute("""
                    INSERT INTO crud_locadora.aluguel (
                        id_cliente, id_veiculo, data_retirada, data_dev_prev,
                        valor_diaria, valor_total, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [
                    form.cleaned_data['cliente'],
                    form.cleaned_data['veiculo'],
                    data_retirada,
                    data_dev_prev,
                    preco_diaria,
                    valor_total,
                    form.cleaned_data['status']
                ])

                # Atualizar status do veículo
                cursor.execute("""
                    UPDATE crud_locadora.veiculo
                    SET disponivel = FALSE
                    WHERE id = %s
                """, [form.cleaned_data['veiculo']])
                
            return redirect('lista_alugueis')
    else:
        form = AddAluguelForm()
    return render(request, 'add_aluguel.html', {'form': form})

def finalizar_aluguel(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Obter dados essenciais
            cursor.execute("""
                SELECT a.data_retirada, a.valor_diaria, v.id 
                FROM crud_locadora.aluguel a
                JOIN crud_locadora.veiculo v ON a.id_veiculo = v.id
                WHERE a.id = %s
            """, [id])
            aluguel = cursor.fetchone()
            
            data_retirada = aluguel[0]
            valor_diaria = float(aluguel[1])
            data_dev_real = datetime.date.today()
            
            # Cálculo correto dos dias
            dias = (data_dev_real - data_retirada).days
            dias = max(dias, 1)
            valor_total = dias * valor_diaria
            
            # Verificar atraso
            status = 'Concluído'
            cursor.execute("SELECT data_dev_prev FROM crud_locadora.aluguel WHERE id = %s", [id])
            data_dev_prev = cursor.fetchone()[0]
            if data_dev_real > data_dev_prev:
                status = 'Atrasado'
                # (Adicione cálculo de multa aqui se necessário)
            
            # Atualizar aluguel
            cursor.execute("""
                UPDATE crud_locadora.aluguel SET
                    data_dev_real = %s,
                    valor_total = %s,
                    status = %s
                WHERE id = %s
            """, [data_dev_real, valor_total, status, id])
            
            # Liberar veículo
            cursor.execute("""
                UPDATE crud_locadora.veiculo
                SET disponivel = TRUE
                WHERE id = %s
            """, [aluguel[2]])
            
        return redirect('lista_alugueis')

def cancelar_aluguel(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE crud_locadora.aluguel 
                SET status = 'Cancelado' 
                WHERE id = %s
            """, [id])
            
            cursor.execute("""
                UPDATE crud_locadora.veiculo v
                SET disponivel = TRUE
                FROM crud_locadora.aluguel a
                WHERE v.id = a.id_veiculo AND a.id = %s
            """, [id])
            
        return redirect('lista_alugueis')
    
def edit_aluguel(request, id):
    with connection.cursor() as cursor:
        # Buscar dados do aluguel e veículo/categoria
        cursor.execute("""
            SELECT a.id_cliente, a.id_veiculo, a.data_retirada, 
                   a.data_dev_prev, a.valor_diaria, a.status,
                   c.preco_diaria_base
            FROM crud_locadora.aluguel a
            JOIN crud_locadora.veiculo v ON a.id_veiculo = v.id
            JOIN crud_locadora.categoria c ON v.id_categoria = c.id
            WHERE a.id = %s
        """, [id])
        aluguel = cursor.fetchone()

    if not aluguel:
        return redirect('lista_alugueis')

    if request.method == 'POST':
        form = AddAluguelForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                # Obter dados do formulário
                novo_veiculo_id = form.cleaned_data['veiculo']
                data_retirada = form.cleaned_data['data_retirada']
                data_dev_prev = form.cleaned_data['data_dev_prev']
                valor_diaria = form.cleaned_data['valor_diaria']
                status = form.cleaned_data['status']
                
                # Calcular novo valor total
                dias = (data_dev_prev - data_retirada).days
                dias = max(dias, 1)
                valor_total = dias * float(valor_diaria)

                # Liberar veículo antigo se necessário
                if novo_veiculo_id != aluguel[1]:
                    cursor.execute("""
                        UPDATE crud_locadora.veiculo
                        SET disponivel = TRUE
                        WHERE id = %s
                    """, [aluguel[1]])

                # Atualizar aluguel
                cursor.execute("""
                    UPDATE crud_locadora.aluguel SET
                        id_cliente = %s,
                        id_veiculo = %s,
                        data_retirada = %s,
                        data_dev_prev = %s,
                        valor_diaria = %s,
                        valor_total = %s,
                        status = %s
                    WHERE id = %s
                """, [
                    form.cleaned_data['cliente'],
                    novo_veiculo_id,
                    data_retirada,
                    data_dev_prev,
                    valor_diaria,
                    valor_total,
                    status,
                    id
                ])

                # Atualizar disponibilidade do novo veículo
                cursor.execute("""
                    UPDATE crud_locadora.veiculo
                    SET disponivel = FALSE
                    WHERE id = %s
                """, [novo_veiculo_id])

                return redirect('lista_alugueis')
    else:
        # Carregar dados iniciais
        initial_data = {
            'cliente': aluguel[0],
            'veiculo': aluguel[1],
            'data_retirada': aluguel[2],
            'data_dev_prev': aluguel[3],
            'valor_diaria': aluguel[4],
            'status': aluguel[5]
        }
        form = AddAluguelForm(initial=initial_data)

    return render(request, 'edit_aluguel.html', {
        'form': form,
        'aluguel_id': id,
        'preco_diaria_original': aluguel[6]
    })