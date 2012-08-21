#!/usr/bin/python
# -*- coding: utf-8 -*-
from loja.models import \
    Pessoa, \
    Telefone_Tipo, \
    Telefone, \
    Endereco, \
    Familia, \
    Produto, \
    Modelo,\
    Pedido, \
    Item_Pedido, \
    Duplicata, \
    Item_Duplicata,\
    Pagamento, \
    Pagamento_Pedido, \
    Pagamento_Duplicata, \
    Tipo_Despesa, \
    Despesa, \
    Movimento_Estoque, \
    Transferencia
from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter, FieldListFilter
from django.utils.translation import ugettext as _
from datetime import date #,datetime

class FiltroVencido(DateFieldListFilter):
    """
    Filtra se campo vencido ou não
    my_model_field.filtro_vencido = True
    """
    def __init__(self, f, request, params, model, model_admin, **kwargs):
        super(FiltroVencido, self).__init__(f, request, params, model,
            model_admin, **kwargs)
        today = date.today()
        self.links = (
            (_('Qualquer Data'), {}),
            (_(u"Não Vencida"), {'%s__gte' % self.field.name: str(today),
                                }),
            (_('Vencida'), {'%s__lt' % self.field.name: str(today),
                            }))
    def title(self):
        return "Filtro se Data Vencida"
    # registering the filter
FieldListFilter._field_list_filters.insert(0, (lambda f: getattr(f, 'filtro_vencido', False), FiltroVencido))

class TelefonesInline(admin.TabularInline):
    model = Telefone
    extra = 1
    radio_fields = {"tipo": admin.VERTICAL}
    #verbose_name = 'Telefone'
    #verbose_name_plural = 'Telefones'
class EnderecosInline(admin.TabularInline):
    model = Endereco
    extra = 1
class ItemDuplicataInline(admin.TabularInline):
    model = Item_Duplicata
    extra = 1
class ItemPedidoInline(admin.TabularInline):
    model = Item_Pedido
    extra = 1
class PagamentoPedidoInline(admin.TabularInline):
    model = Pagamento_Pedido
    extra = 1
class PagamentoDuplicataInline(admin.TabularInline):
    model = Pagamento_Duplicata
    extra = 1
class DespesaInline(admin.TabularInline):
    model = Despesa
    extra = 1
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'sobrenome', 'email', 'telefones','ativa')
    search_fields = ['nome']
    list_filter = ['ativa']
    list_editable = ['ativa']
    fieldsets = [
        ('Principal', {'fields': ['nome', 'sobrenome', 'email']}),
    ]
    inlines = [TelefonesInline, EnderecosInline]
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'data', 'tipo_despesa', 'pessoa', 'valor', 'descricao')
    search_fields = ['pessoa__nome_completo', 'descricao', 'total']
    list_filter = ['pagamento__data', 'tipo_despesa', 'pessoa']
    #list_editable = ['status']
    fieldsets = [
        ('Principal', {'fields': ['pagamento', 'pessoa', 'tipo_despesa', 'valor', 'descricao']}),
    ]
class TelefoneAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'tipo', 'telefone')
    search_fields = ['pessoa__nome_completo', 'telefone']
    list_filter = ['tipo']
    fieldsets = [
        (None, {'fields': ['pessoa', 'tipo', 'telefone']}),
    ]
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'rua', 'cidade', 'estado', 'cep')
    search_fields = ['pessoa__nome_completo', 'rua', 'cidade', 'estado', 'cep']
    list_filter = ['cidade', 'estado']
    fieldsets = [
        (None, {'fields': ['pessoa', 'rua', 'cidade', 'estado', 'cep']}),
    ]
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'familia', 'fornecedor', 'codigo_fornecedor', 'descricao', 'estoque', 'estoque_producao')
    search_fields = ['familia__familia', 'fornecedor__nome_completo', 'codigo_fornecedor', 'descricao_fornecedor', 'descricao']
    list_filter = ['familia', 'fornecedor']
    #list_editable = ['ativa']
    fieldsets = [
        ('Principal', {'fields': ['familia', 'fornecedor', 'descricao',]}),
        ('Informações Fornecedor', {'fields': ['codigo_fornecedor', 'descricao_fornecedor',]}),
    ]
    inlines = [ItemDuplicataInline]
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'status', 'pessoa', 'data_entrega', 'data_pagamento', 'string_total', 'string_total_pago', 'lista_items')
    search_fields = ['codigo', 'pessoa__nome_completo', 'total']
    list_filter = ['status', 'data_entrega', 'data_pagamento', 'pessoa']
    list_editable = ['status', 'data_entrega', 'data_pagamento']
    fieldsets = [
        ('Principal', {'fields': ['pessoa', 'status', 'aprovado', 'data_entrega', 'data_pagamento']}),
    ]
    inlines = [ItemPedidoInline, PagamentoPedidoInline]
class DuplicataAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'numero', 'status', 'data_entrega', 'data_vencimento', 'pessoa', 'string_total', 'string_total_pago', 'lista_items')
    search_fields = ['codigo', 'pessoa__nome_completo', 'total']
    list_filter = ['status', 'data_entrega', 'data_vencimento', 'pessoa']
    list_editable = ['status', 'data_entrega', 'data_vencimento']
    fieldsets = [
        ('Principal', {'fields': ['numero', 'pessoa', 'status', 'data_entrega', 'data_vencimento']}),
    ]
    inlines = [ItemDuplicataInline, PagamentoDuplicataInline]
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'data', 'total', 'fonte', 'tipo_pagamento', 'pagamento', 'items')
    search_fields = ['codigo','items', 'total']
    list_filter = ['data', 'fonte', 'tipo_pagamento', 'pagamento']
    #list_editable = ['status']
    fieldsets = [
        ('Principal', {'fields': ['data', 'fonte', 'tipo_pagamento', 'pagamento']}),
        ('Banco', {'fields': ['texto_extrato', 'verificado']}),
    ]
    inlines = [PagamentoPedidoInline, PagamentoDuplicataInline, DespesaInline]

admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Telefone_Tipo)
admin.site.register(Telefone, TelefoneAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Familia)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Modelo)
admin.site.register(Pedido, PedidoAdmin)
#admin.site.register(Item_Pedido)
admin.site.register(Duplicata, DuplicataAdmin)
#admin.site.register(Item_Duplicata)
admin.site.register(Pagamento, PagamentoAdmin)
#admin.site.register(Pagamento_Pedido)
#admin.site.register(Pagamento_Duplicata)
admin.site.register(Tipo_Despesa)
#admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Movimento_Estoque)
admin.site.register(Transferencia)





