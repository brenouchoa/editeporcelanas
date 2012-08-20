#!/usr/bin/python
# -*- coding: utf-8 -*-
from loja.models import Pessoa, Telefone_Tipo, Telefone, Endereco, Familia, Produto, Modelo, Item_Pedido, Pedido
from django.contrib import admin

class TelefonesInline(admin.TabularInline):
    model = Telefone
    extra = 1
    radio_fields = {"tipo": admin.VERTICAL}
    #verbose_name = 'Telefone'
    #verbose_name_plural = 'Telefones'

class EnderecosInline(admin.TabularInline):
    model = Endereco
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

admin.site.register(Pessoa, PessoaAdmin)

class TelefoneAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'tipo', 'telefone')
    search_fields = ['pessoa__nome_completo', 'telefone']
    list_filter = ['tipo']
    fieldsets = [
        (None, {'fields': ['pessoa', 'tipo', 'telefone']}),
    ]

admin.site.register(Telefone, TelefoneAdmin)

class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'rua', 'cidade', 'estado', 'cep')
    search_fields = ['pessoa__nome_completo', 'rua', 'cidade', 'estado', 'cep']
    list_filter = ['cidade', 'estado']
    fieldsets = [
        (None, {'fields': ['pessoa', 'rua', 'cidade', 'estado', 'cep']}),
    ]

admin.site.register(Endereco, EnderecoAdmin)

admin.site.register(Telefone_Tipo)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'familia', 'fornecedor', 'descricao')
    search_fields = ['familia__familia', 'fornecedor__nome_completo', 'descricao']
    list_filter = ['familia', 'fornecedor']
    #list_editable = ['ativa']
    fieldsets = [
        ('Principal', {'fields': ['familia', 'fornecedor', 'descricao']}),
    ]

admin.site.register(Produto, ProdutoAdmin)

admin.site.register(Familia)

admin.site.register(Modelo)

admin.site.register(Item_Pedido)

class ItemPedidoInline(admin.TabularInline):
    model = Item_Pedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'status', 'cliente', 'string_total')
    search_fields = ['codigo', 'cliente__nome_completo', 'total']
    list_filter = ['status', 'data_entrega', 'cliente']
    list_editable = ['status']
    fieldsets = [
        ('Principal', {'fields': ['cliente', 'status', 'aprovado', 'data_entrega', ]}),
    ]
    inlines = [ItemPedidoInline]


admin.site.register(Pedido, PedidoAdmin)





