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
    Pagamento_Pedido, \
    Pagamento_Duplicata, \
    Tipo_Despesa, \
    Despesa, \
    Movimento_Estoque, \
    Transferencia, \
    Contas, \
    Ajuste_Conta,\
    Transacao

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

class EnderecosInline(admin.TabularInline):
    model = Endereco
    extra = 1

class ItemDuplicataInline(admin.TabularInline):
    model = Item_Duplicata
    extra = 1
class ItemDuplicataInline0(admin.TabularInline):
    model = Item_Duplicata
    extra = 1

class ItemPedidoInline(admin.TabularInline):
    model = Item_Pedido
    extra = 1
class ItemPedidoInline0(admin.TabularInline):
    model = Item_Pedido
    extra = 0

class PagamentoPedidoInline(admin.TabularInline):
    model = Pagamento_Pedido
    extra = 1
class PagamentoPedidoInline0(admin.TabularInline):
    model = Pagamento_Pedido
    extra = 0

class PagamentoDuplicataInline(admin.TabularInline):
    model = Pagamento_Duplicata
    extra = 1
class PagamentoDuplicataInline0(admin.TabularInline):
    model = Pagamento_Duplicata
    extra = 0

class DespesaInline(admin.TabularInline):
    model = Despesa
    extra = 1
class DespesaInline0(admin.TabularInline):
    model = Despesa
    extra = 0

class TransferenciaInline(admin.TabularInline):
    model = Transferencia
    fk_name = 'fonte'
    extra = 1
    verbose_name = 'Transferência/Depósito Em saída'
    verbose_name_plural = 'Transferências/Depósitos Em saída'
class TransferenciaInline0(admin.TabularInline):
    model = Transferencia
    fk_name = 'fonte'
    extra = 0
    verbose_name = 'Transferência/Depósito Em saída'
    verbose_name_plural = 'Transferências/Depósitos Em saída'

class TransferenciaTransacaoInline(admin.TabularInline):
    model = Transferencia
    extra = 1
    verbose_name = 'Transferência/Depósito'
    verbose_name_plural = 'Transferências/Depósitos'
class TransferenciaTransacaoInline0(admin.TabularInline):
    model = Transferencia
    extra = 0
    verbose_name = 'Transferência/Depósito'
    verbose_name_plural = 'Transferências/Depósitos'

class TransferenciaInlineDestino(admin.TabularInline):
    model = Transferencia
    fk_name = 'destino'
    extra = 1
    verbose_name = 'Transferência/Depósito Em entrada'
    verbose_name_plural = 'Transferências/Depósitos Em entrada'
class TransferenciaInlineDestino0(admin.TabularInline):
    model = Transferencia
    fk_name = 'destino'
    extra = 0
    verbose_name = 'Transferência/Depósito Em entrada'
    verbose_name_plural = 'Transferências/Depósitos Em entrada'

class AjusteContaInline(admin.TabularInline):
    model = Ajuste_Conta
    extra = 1
class AjusteContaInline0(admin.TabularInline):
    model = Ajuste_Conta
    extra = 0

class PessoaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('nome_completo', 'sobrenome', 'email', 'telefones','ativa')
    search_fields = ['nome']
    list_filter = ['ativa']
    list_editable = ['ativa']
    fieldsets = [
        ('Principal', {'fields': ['nome', 'sobrenome', 'email']}),
    ]
    inlines = [TelefonesInline, EnderecosInline]

class DespesaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('cod', 'data_transacao', 'fonte', 'tipo_despesa', 'tipo_pagamento', 'valor', 'pessoa', 'descricao')
    search_fields = ['pessoa__nome_completo', 'descricao', 'total']
    list_filter = ['tipo_despesa', 'tipo_pagamento', 'pessoa']
    list_editable = [ 'data_transacao', 'fonte', 'tipo_despesa', 'tipo_pagamento', 'valor', 'pessoa',  'descricao']
    fieldsets = [
        ('Base', {'fields': ['data_transacao', 'fonte', 'tipo_pagamento', 'valor', ]}),
        ('Despesa', {'fields': ['tipo_despesa', 'pessoa', 'descricao']}),
        ('Banco', {'fields': ['texto_extrato', 'verificado',]}),
    ]

class TelefoneAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('pessoa', 'tipo', 'telefone')
    search_fields = ['pessoa__nome_completo', 'telefone']
    list_filter = ['tipo']
    fieldsets = [
        (None, {'fields': ['pessoa', 'tipo', 'telefone']}),
    ]
class EnderecoAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('pessoa', 'rua', 'cidade', 'estado', 'cep')
    search_fields = ['pessoa__nome_completo', 'rua', 'cidade', 'estado', 'cep']
    list_filter = ['cidade', 'estado']
    fieldsets = [
        (None, {'fields': ['pessoa', 'rua', 'cidade', 'estado', 'cep']}),
    ]
class ProdutoAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('codigo', 'familia', 'fornecedor', 'codigo_fornecedor', 'descricao', 'estoque', 'estoque_producao')
    search_fields = ['familia__familia', 'fornecedor__nome_completo', 'codigo_fornecedor', 'descricao_fornecedor', 'descricao']
    list_filter = ['familia', 'fornecedor']
    #list_editable = ['ativa']
    fieldsets = [
        ('Principal', {'fields': ['familia', 'fornecedor', 'descricao',]}),
        ('Informações Fornecedor', {'fields': ['codigo_fornecedor', 'descricao_fornecedor',]}),
    ]
    inlines = [ItemDuplicataInline0]
class PedidoAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('codigo', 'status', 'pessoa', 'data_entrega', 'data_pagamento', 'string_total', 'string_total_pago', 'lista_items')
    search_fields = ['codigo', 'pessoa__nome_completo', 'total']
    list_filter = ['status', 'data_entrega', 'data_pagamento', 'pessoa']
    list_editable = ['status', 'data_entrega', 'data_pagamento']
    fieldsets = [
        ('Principal', {'fields': ['pessoa', 'status', 'aprovado', 'data_entrega', 'data_pagamento']}),
    ]
    inlines = [ItemPedidoInline]
class DuplicataAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('codigo', 'numero', 'status', 'data_entrega', 'data_vencimento', 'pessoa', 'string_total', 'string_total_pago', 'lista_items')
    search_fields = ['codigo', 'pessoa__nome_completo', 'total']
    list_filter = ['status', 'data_entrega', 'data_vencimento', 'pessoa']
    list_editable = ['status', 'data_entrega', 'data_vencimento']
    fieldsets = [
        ('Principal', {'fields': ['numero', 'pessoa', 'status', 'data_entrega', 'data_vencimento']}),
    ]
    inlines = [ItemDuplicataInline]
class ContasAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['codigo', 'nome', 'string_saldo_atual']
    inlines = [DespesaInline0, PagamentoPedidoInline0, PagamentoDuplicataInline0, TransferenciaInline0, TransferenciaInlineDestino0, AjusteContaInline0]

class TransacaoAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['data_transacao', 'fonte', 'tipo', 'string_valor' ]
    fieldsets = [
        ('Principal', {'classes': ('collapse',), 'fields': []}),
    ]
    def has_add_permission(self, request):
        return False
    inlines = [DespesaInline0, PagamentoPedidoInline0, PagamentoDuplicataInline0, TransferenciaTransacaoInline0, AjusteContaInline0]

admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Telefone_Tipo)
admin.site.register(Telefone, TelefoneAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Familia)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Modelo)
admin.site.register(Pedido, PedidoAdmin)
#admin.site.register(Item_Pedido)
#todo Lista items pedidos com filtro por status
admin.site.register(Duplicata, DuplicataAdmin)
#admin.site.register(Item_Duplicata)
admin.site.register(Pagamento_Pedido)
admin.site.register(Pagamento_Duplicata)
admin.site.register(Tipo_Despesa)
admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Movimento_Estoque)
admin.site.register(Transferencia)
admin.site.register(Contas, ContasAdmin)
admin.site.register(Transacao, TransacaoAdmin)






