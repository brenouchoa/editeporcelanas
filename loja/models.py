#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.contrib.humanize.templatetags.humanize import intcomma

def currency(dollars):
    dollars = round(float(dollars), 2)
    return "R$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

class Pessoa(models.Model):
    #TIPO_PESSOA = (('C', 'Cliente'),('F','Fornecedor'))
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100,blank='True',help_text='Deixar em branco se empresa')
    email = models.EmailField(max_length=200,verbose_name='E-mail')
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    #tipo = models.CharField(max_length=1, choices=TIPO_PESSOA)
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['nome']
    def telefones(self):
        t = ''
        for i in self.telefone_set.all():
            if t == '':
                t = '%s%s:%s' % (t, i.tipo.tipo, i.telefone)
            else:
                t = '%s, %s:%s' % (t, i.tipo.tipo, i.telefone)
        else:
            return t
    def nome_completo(self):
        return self.nome + ' ' + self.sobrenome
    nome_completo = property(nome_completo)
    telefones = property(telefones)
    def __unicode__(self):
        return self.nome_completo
    def __str__(self):
        return self.nome_completo

class Telefone_Tipo(models.Model):
    tipo = models.CharField(max_length=3)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Tipo Telefone'
        verbose_name_plural = 'Tipos Telefone'
        ordering = ['tipo']
    def __unicode__(self):
        return self.tipo
    def __str__(self):
        return self.tipo

class Telefone(models.Model):
    tipo = models.ForeignKey(Telefone_Tipo)
    telefone = models.CharField(max_length=20)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'
        ordering = ['telefone']
        #order_with_respect_to = 'pessoa'
    def __unicode__(self):
        return '%s - %s:%s' % (self.pessoa.nome_completo, self.tipo.tipo, self.telefone)
    def __str__(self):
        return '%s - %s:%s' % (self.pessoa.nome_completo, self.tipo.tipo, self.telefone)

class Endereco(models.Model):
    rua = models.CharField(max_length=100,help_text=u"Rua e número")
    cidade = models.CharField(max_length=100,default='Belo Horizonte')
    estado = models.CharField(max_length=2,help_text='Formato: XX',default='MG')
    cep = models.CharField(max_length=100,blank='True',help_text='Formato: XXXXX-XXX')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['rua']
        #order_with_respect_to = 'pessoa'
    def __unicode__(self):
        return '%s - %s - %s/%s - %s' % (self.pessoa, self.rua, self.cidade, self.estado, self.cep)
    def __str__(self):
        return '%s - %s - %s/%s - %s' % (self.pessoa, self.rua, self.cidade, self.estado, self.cep)

class Familia(models.Model):
    familia = models.CharField(max_length=30)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'
        ordering = ['familia']
    def __unicode__(self):
        return self.familia
    def __str__(self):
        return self.familia

class Produto(models.Model):
    codigo = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=50)
    familia = models.ForeignKey(Familia)
    fornecedor = models.ForeignKey(Pessoa)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['familia__familia','descricao']
    def __unicode__(self):
        return self.descricao
    def __str__(self):
        return self.descricao

class Modelo(models.Model):
    modelo = models.CharField(max_length=30)
    multiplicador = models.DecimalField(decimal_places=4,max_digits=7,help_text='Utilizado para indicar Preço de Venda')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        ordering = ['modelo']
    def __unicode__(self):
        return self.modelo
    def __str__(self):
        return self.modelo

class Pedido(models.Model):
    STATUS_PEDIDO = (('0', u"Orçamento"),('1', u"Em Produção"),('2', u"Eliminado"),('3',u"Concluído"))
    codigo = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Pessoa)
    aprovado = models.BooleanField(default=False)
    data_entrega = models.DateTimeField(verbose_name='Data Entrega', default=timezone.now())
    status = models.CharField(max_length=1, choices=STATUS_PEDIDO, default='0')
    items = models.ManyToManyField(Produto, through='Item_Pedido')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-codigo']

    def total(self):
        t = 0
        for p in self.item_pedido_set.all():
            if p.status <> '2':
                t = t + p.preco_venda
        else:
            return t
    total = property(total)
    def string_total(self):
        return currency(self.total)
    string_total.short_description = 'Total'
    string_total.boolean = False
    string_total.admin_order_field = '-codigo'
    def __unicode__(self):
        return '%s - %s - %s' % (self.codigo, self.cliente.nome_completo, self.string_total())
    def __str__(self):
        return '%s - %s - %s' % (self.codigo, self.cliente.nome_completo, self.string_total())
    def clean(self):
        if self.status == '0':
            if self.aprovado:
                raise ValidationError('Pedido aprovado, mudar o status para Em Produção ou desaprove o pedido')
        if self.status == '1':
            if not self.aprovado:
                raise ValidationError('Pedido ainda não aprovado, mudar o status para Orçamento ou aprove o pedido')
        if self.status == '3':
            if not self.aprovado:
                raise ValidationError('Pedido ainda não aprovado, mudar o status para Orçamento ou aprove o pedido')

            #    def save(self, *args, **kwargs):
#        super(Pedido, self).save(*args, **kwargs)
#        self.clean()


    #    if self.status <> self._original_state['status']:
    #        self._reset_state()
    #        raise 'Errore'
    #    else:
    #    # Call parent's ``save`` function
            #super(Pedido, self).save(*args, **kwargs)




class Item_Pedido(models.Model):
    STATUS_ITEM =(('0',u"Orçamento"),('1',u"Em Produção"),('2',u"Eliminado"),('3',u"Concluído"))
    produto = models.ForeignKey(Produto)
    pedido = models.ForeignKey(Pedido)
    modelo = models.ForeignKey(Modelo)
    status = models.CharField(max_length=1, choices=STATUS_ITEM, default='0')
    preco_venda = models.DecimalField(decimal_places=2,max_digits=7,verbose_name=u"Preço Venda",default=0,blank=True)
    #todo-me ultimo preço como default
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    def string_preco_venda(self):
        return currency(self.preco_venda)
    string_preco_venda.short_description = 'Preço Venda'
    string_preco_venda.boolean = False
    string_preco_venda.admin_order_field = 'produto__descricao'
    def clean(self):
        if self.pedido.status == '0':
            if self.status <> '0':
                raise ValidationError('Pedido ainda em orçamento, não é possivel iniciar a produção do item, mudar para Orçamento')
        if self.pedido.status == '1':
            if self.status == '0':
                raise ValidationError('Pedido já em produção, não é possivel selecionar o item como Orçamento')
#            c = 0
#            for i in self.pedido.item_pedido_set.all():
#                if i.status not in ('0', '2'):
#                    c += c + 1
#            if not c:
#                raise ValidationError('Nenhum item valido para o Pedido, eliminar o Pedido ou adicionar um item valido')
        if self.pedido.status == '2':
            if self.status <> '2':
                raise ValidationError('Pedido eliminado, selecionar também os items como eliminados')
        if self.pedido.status == '3':
            if self.status == '0':
                raise ValidationError('Pedido já concluído, não é possivel selecionar o item como Orçamento')
            if self.status == '1':
                raise ValidationError('Pedido já concluído, não é possivel selecionar o item como Em Produção')
#            c = 0
#            for i in self.pedido.item_pedido_set.all():
#                if i.status not in ('0', '2'):
#                    c += c + 1
#            if not c:
#                raise ValidationError('Nenhum item valido para o Pedido, eliminar o Pedido ou adicionar um item valido')

    class Meta:
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Items Pedido'
        ordering = ['produto__familia','produto__descricao']
    def __unicode__(self):
        return "%s - %s" % (self.produto.descricao, self.string_preco_venda())
    def __str__(self):
        return "%s - %s" % (self.produto.descricao, self.string_preco_venda())









