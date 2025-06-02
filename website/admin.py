from django.contrib import admin

# Register your models here.

from . models import Record
from . models import Agencia, Cliente, Veiculo, Categoria

admin.site.register(Record)
admin.site.register(Agencia)
admin.site.register(Cliente)
admin.site.register(Veiculo)
admin.site.register(Categoria)