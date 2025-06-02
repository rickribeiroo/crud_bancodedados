from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('record/<int:pk>', views.record_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),

    path('agencias/', views.lista_agencias, name='lista_agencias'),
    path('agencias/editar/<int:id>/', views.edit_agencia, name='edit_agencia'),
    path('agencias/add_agencia/', views.add_agencia, name='add_agencia'),
    path('agencias/excluir/<int:id>/', views.delete_agencia, name='delete_agencia'),

    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.add_cliente, name='add_cliente'),
    path('clientes/editar/<int:id>/', views.edit_cliente, name='edit_cliente'),
    path('clientes/excluir/<int:id>/', views.delete_cliente, name='delete_cliente'),

    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/novo/', views.add_categoria, name='add_categoria'),
    path('categorias/editar/<int:id>/', views.edit_categoria, name='edit_categoria'),
    path('categorias/excluir/<int:id>/', views.delete_categoria, name='delete_categoria'),

    path('veiculos/', views.lista_veiculos, name='lista_veiculos'),
    path('veiculos/novo/', views.add_veiculo, name='add_veiculo'),
    path('veiculos/editar/<int:id>/', views.edit_veiculo, name='edit_veiculo'),
    path('veiculos/excluir/<int:id>/', views.delete_veiculo, name='delete_veiculo'),

    path('manutencoes/', views.lista_manutencoes, name='lista_manutencoes'),
    path('manutencoes/novo/', views.add_manutencao, name='add_manutencao'),
    path('manutencoes/editar/<int:id>/', views.edit_manutencao, name='edit_manutencao'),
    path('manutencoes/excluir/<int:id>/', views.delete_manutencao, name='delete_manutencao'),

    path('alugueis/', views.lista_alugueis, name='lista_alugueis'),
    path('alugueis/novo/', views.add_aluguel, name='add_aluguel'),
    path('alugueis/finalizar/<int:id>/', views.finalizar_aluguel, name='finalizar_aluguel'),
    path('alugueis/editar/<int:id>/', views.edit_aluguel, name='edit_aluguel'),
    path('alugueis/cancelar/<int:id>/', views.cancelar_aluguel, name='cancelar_aluguel'),
]
