#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.humanize.templatetags.humanize import intcomma

def currency(dollars):
    dollars = round(float(dollars), 2)
    return "R$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

FONTE = (('0','Caixa'),('1','Unibanco'),('2','Banco do Brasil'))
TIPO_MOVIMENTO = (('0','Estoque Inicial'),('1','Quebra/Perda'))
TIPO_PESSOA = (('0', 'Cliente'),('1','Fornecedor'),('2','Outros'))
STATUS_PEDIDO = (('0', u"Orçamento"),('1', u"Em Produção"),('2', u"Eliminado"),('3',u"Concluído"))
STATUS_ITEM_PEDIDO =(('0',u"Orçamento"),('1',u"Em Produção"),('2',u"Eliminado"),('3',u"Concluído"))
STATUS_DUPLICATA = (('0', u"Orçamento"),('1', u"Confirmada"),('3',u"Entregue"))
TIPO_PAGAMENTO =(('0',u"Dinheiro"),('1',u"Cheque"),('2',u"Depósito"),('3',u"Outro"))
PAGAMENTO =(('0',u"Total"),('1',u"Entrada"),('2',u"Parcela"))

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100,blank='True',help_text='Deixar em branco se empresa')
    email = models.EmailField(max_length=200,verbose_name='E-mail')
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    tipo = models.CharField(max_length=1, choices=TIPO_PESSOA, default='2')
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
    familia = models.CharField(max_length=30, verbose_name='Família')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Família'
        verbose_name_plural = 'Famílias'
        ordering = ['familia']
    def __unicode__(self):
        return self.familia
    def __str__(self):
        return self.familia
class Produto(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_fornecedor = models.CharField(max_length=20, verbose_name='Código Fornecedor', blank=True)
    descricao_fornecedor = models.CharField(max_length=50, verbose_name='Descrição Fornecedor',blank=True)
    descricao = models.CharField(max_length=50, verbose_name='Descrição', unique=True)
    familia = models.ForeignKey(Familia)
    fornecedor = models.ForeignKey(Pessoa)
    data_criacao = models.DateTimeField(auto_now_add=True, editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True, editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['familia__familia','descricao']
    def estoque(self):
        c = 0
        for i in self.item_duplicata_set.all():
            if i.duplicata.status == '3':
                c = c + i.qtd
        for i in self.item_pedido_set.all():
            if i.status not in ('0','2'):
                c = c - i.qtd
        for i in self.movimento_estoque_set.all():
                if i.tipo_movimento in ('0'):
                    c = c + i.qtd
                else:
                    c = c - i.qtd
        return c
    estoque.short_description = 'Qtd Estoque'
    estoque.boolean = False
    estoque.admin_order_field = 'descrizione'
    def estoque_producao(self):
        c = 0
        for i in self.item_pedido_set.all():
            if i.status == '1':
                c = c + i.qtd
        return c
    estoque_producao.short_description = 'Qtd Em Produção'
    estoque_producao.boolean = False
    estoque_producao.admin_order_field = 'descrizione'
    def estoque_confirmado(self):
        c = 0
        for i in self.item_duplicata_set.all():
            if i.duplicata.status == '2':
                c = c + i.qtd
        return c
    estoque_confirmado.short_description = 'Qtd à entregar'
    estoque_confirmado.boolean = False
    estoque_confirmado.admin_order_field = 'descrizione'
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
    codigo = models.AutoField(primary_key=True)
    pessoa = models.ForeignKey(Pessoa)
    aprovado = models.BooleanField(default=False)
    data_entrega = models.DateTimeField(verbose_name='Data Entrega', default=timezone.now())
    data_pagamento = models.DateField(verbose_name='Data Pagamento', default=timezone.now())
    data_pagamento.filtro_vencido = True
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
                t = t + (p.preco * p.qtd)
        else:
            return t
    total = property(total)
    def string_total(self):
        return currency(self.total)
    string_total.short_description = 'Total'
    string_total.boolean = False
    string_total.admin_order_field = '-codigo'
    def total_pago(self):
        t = 0
        for p in self.pagamento_pedido_set.all():
                t = t + p.valor
        else:
            return t
    total_pago = property(total_pago)
    def string_total_pago(self):
        return currency(self.total_pago)
    string_total_pago.short_description = 'Total Pago'
    string_total_pago.boolean = False
    string_total_pago.admin_order_field = '-codigo'
    def lista_items(self):
        t = ''
        for i in self.item_pedido_set.all():
            if t == '':
                t = '%s%s' % (t, i.__unicode__())
            else:
                t = '%s, %s' % (t, i.__unicode__())
        else:
            return t
    lista_items.short_description = 'Lista Items'
    lista_items.boolean = False
    lista_items.admin_order_field = '-codigo'
    def __unicode__(self):
        return 'Pe%s-%s-%s-%s' % (self.codigo, STATUS_PEDIDO[int(self.status)][1], self.pessoa.nome_completo, self.string_total())
    def __str__(self):
        return 'Pe%s-%s-%s-%s' % (self.codigo, STATUS_PEDIDO[int(self.status)][1], self.pessoa.nome_completo, self.string_total())
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
class Item_Pedido(models.Model):
    produto = models.ForeignKey(Produto)
    pedido = models.ForeignKey(Pedido)
    modelo = models.ForeignKey(Modelo)
    status = models.CharField(max_length=1, choices=STATUS_ITEM_PEDIDO, default='0')
    qtd = models.DecimalField(decimal_places=2,max_digits=7,verbose_name=u"Quantidade",default=1)
    preco = models.DecimalField(decimal_places=2,max_digits=7,verbose_name=u"Preço Venda",default=0,blank=True)
    #todo-me ultimo preço como default
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    def string_preco(self):
        return currency(self.preco)
    string_preco.short_description = 'Preço Venda'
    string_preco.boolean = False
    string_preco.admin_order_field = 'produto__descricao'
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
    class Meta:
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Items Pedido'
        ordering = ['produto__familia','produto__descricao']
    def __unicode__(self):
        return "%s - %s" % (self.produto.descricao, self.string_preco())
    def __str__(self):
        return "%s - %s" % (self.produto.descricao, self.string_preco())
class Duplicata(models.Model):
    codigo = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=20, blank=True, verbose_name=u"Número")
    pessoa = models.ForeignKey(Pessoa)
    data_entrega = models.DateField(verbose_name='Data Entrega', default=timezone.now())
    data_vencimento = models.DateField(verbose_name='Data Vencimento', default=timezone.now())
    data_vencimento.filtro_vencido = True
    status = models.CharField(max_length=1, choices=STATUS_DUPLICATA, default='0')
    items = models.ManyToManyField(Produto, through='Item_Duplicata')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Duplicata'
        verbose_name_plural = 'Duplicatas'
        ordering = ['-codigo']
    def total(self):
        t = 0
        for p in self.item_duplicata_set.all():
                t = t + (p.preco * p.qtd)
        else:
            return t
    total = property(total)
    def string_total(self):
        return currency(self.total)
    string_total.short_description = 'Total'
    string_total.boolean = False
    string_total.admin_order_field = '-codigo'
    def total_pago(self):
        t = 0
        for p in self.pagamento_duplicata_set.all():
            t = t + p.valor
        else:
            return t
    total_pago = property(total_pago)
    def string_total_pago(self):
        return currency(self.total_pago)
    string_total_pago.short_description = 'Total Pago'
    string_total_pago.boolean = False
    string_total_pago.admin_order_field = '-codigo'
    def lista_items(self):
        t = ''
        for i in self.item_duplicata_set.all():
            if t == '':
                t = '%s%s' % (t, i.__unicode__())
            else:
                t = '%s, %s' % (t, i.__unicode__())
        else:
            return t
    lista_items.short_description = 'Lista Items'
    lista_items.boolean = False
    lista_items.admin_order_field = '-codigo'
    def __unicode__(self):
        return 'Du%s-%s-%s-%s-%s' % (self.codigo, self.data_entrega, STATUS_DUPLICATA[int(self.status)][1], self.pessoa.nome_completo, self.string_total())
    def __str__(self):
        return 'Du%s-%s-%s-%s-%s' % (self.codigo, self.data_entrega, STATUS_DUPLICATA[int(self.status)][1], self.pessoa.nome_completo, self.string_total())
class Item_Duplicata(models.Model):
    produto = models.ForeignKey(Produto)
    duplicata = models.ForeignKey(Duplicata)
    #modelo = models.ForeignKey(Modelo)
    qtd = models.DecimalField(decimal_places=2,max_digits=7,verbose_name=u"Quantidade",default=1)
    preco = models.DecimalField(decimal_places=2,max_digits=7,verbose_name=u"Preço Compra",default=0,blank=True)
    #todo-me ultimo preço como default
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    def string_preco(self):
        return currency(self.preco)
    string_preco.short_description = 'Preço Venda'
    string_preco.boolean = False
    string_preco.admin_order_field = 'produto__descricao'
    class Meta:
        verbose_name = 'Item Duplicata'
        verbose_name_plural = 'Items Duplicata'
        ordering = ['produto__familia','produto__descricao']
    def __unicode__(self):
        return "Du%s-%s-%s-%s" % (self.duplicata.codigo, self.produto.descricao, self.qtd, self.string_preco())
    def __str__(self):
        return "Du%s-%s-%s-%s" % (self.duplicata.codigo, self.produto.descricao, self.qtd, self.string_preco())
class Pagamento(models.Model):
    codigo = models.AutoField(primary_key=True)
    data = models.DateField(verbose_name='Data', default=timezone.now())
    fonte = models.CharField(choices=FONTE,max_length=1, default='0',verbose_name='Fonte')
    tipo_pagamento = models.CharField(choices=TIPO_PAGAMENTO,max_length=1, default='0',verbose_name='Tipo Pagamento')
    pagamento = models.CharField(choices=PAGAMENTO,max_length=1, default='0')
    pagamentos_pedido = models.ManyToManyField(Pedido, through='Pagamento_Pedido')
    pagamentos_duplicata = models.ManyToManyField(Duplicata, through='Pagamento_Duplicata')
    texto_extrato = models.CharField(max_length=30, verbose_name='Texto Extrato', blank=True)
    verificado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data', 'fonte', 'tipo_pagamento', 'pagamento']
    def total(self):
        t = 0
        for p in self.pagamento_pedido_set.all():
            t = t + p.valor
        for p in self.pagamento_duplicata_set.all():
            t = t - p.valor
        for p in self.despesa_set.all():
            t = t - p.valor
        return t
    total = property(total)
    def string_total(self):
        return currency(self.total)
    string_total.short_description = 'Total'
    string_total.boolean = False
    string_total.admin_order_field = '-data'
    def items(self):
        t = ''
        for i in self.pagamento_duplicata_set.all():
            if t == '':
                t = '%sDu%s-%s-%s' % (t, i.duplicata.codigo, i.duplicata.pessoa.nome, i.string_valor)
            else:
                t = '%s, Du%s-%s-%s' % (t, i.duplicata.codigo, i.duplicata.pessoa.nome, i.string_valor)
        for i in self.pagamento_pedido_set.all():
            if t == '':
                t = '%sPe%s-%s-%s' % (t, i.pedido.codigo, i.pedido.pessoa.nome, i.string_valor)
            else:
                t = '%s, Pe%s-%s-%s' % (t, i.pedido.codigo, i.pedido.pessoa.nome, i.string_valor)
        for i in self.despesa_set.all():
            if t == '':
                t = '%sDe%s-%s-%s' % (t, i.codigo, i.pessoa.nome, i.string_valor)
            else:
                t = '%s, De%s-%s-%s' % (t, i.codigo, i.pessoa.nome, i.string_valor)
        return t
    items = property(items)
    def __unicode__(self):
        return 'Pa%s-%s-%s-%s' % (self.codigo, self.data, TIPO_PAGAMENTO[int(self.tipo_pagamento)][1], self.items)
    def __str__(self):
        return 'Pa%s-%s-%s-%s' % (self.codigo, self.data, TIPO_PAGAMENTO[int(self.tipo_pagamento)][1], self.items)
class Pagamento_Pedido(models.Model):
    pedido = models.ForeignKey(Pedido)
    pagamento = models.ForeignKey(Pagamento)
    valor = models.DecimalField(decimal_places=2,max_digits=7,verbose_name='Valor')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Pagamento Pedido'
        verbose_name_plural = 'Pagamentos Pedido'
        ordering = ['pedido']
    def string_valor(self):
        return currency(self.valor)
    string_valor =property(string_valor)
    def __unicode__(self):
        return 'Pe%s-%s-%s' % (self.pedido.codigo, self.pedido.pessoa.nome, self.string_valor)
    def __str__(self):
        return 'Pe%s-%s-%s' % (self.pedido.codigo, self.pedido.pessoa.nome, self.string_valor)
class Pagamento_Duplicata(models.Model):
    duplicata = models.ForeignKey(Duplicata)
    pagamento = models.ForeignKey(Pagamento)
    valor = models.DecimalField(decimal_places=2,max_digits=7,verbose_name='Valor')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Pagamento Duplicata'
        verbose_name_plural = 'Pagamentos Duplicata'
        ordering = ['duplicata']
    def string_valor(self):
        return currency(self.valor)
    string_valor =property(string_valor)
    def __unicode__(self):
        return 'Pe%s-%s-%s' % (self.duplicata.codigo, self.duplicata.pessoa.nome, self.string_valor)
    def __str__(self):
        return 'Pe%s-%s-%s' % (self.duplicata.codigo, self.duplicata.pessoa.nome, self.string_valor)
class Tipo_Despesa(models.Model):
    descricao = models.CharField(max_length=30, verbose_name='Descrição')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Tipo Despesa'
        verbose_name_plural = 'Tipos Despesa'
        ordering = ['descricao']
    def __unicode__(self):
        return self.descricao
    def __str__(self):
        return self.descricao
class Despesa(models.Model):
    codigo = models.AutoField(primary_key=True)
    pagamento = models.ForeignKey(Pagamento)
    pessoa = models.ForeignKey(Pessoa, blank=True)
    tipo_despesa = models.ForeignKey(Tipo_Despesa)
    valor = models.DecimalField(decimal_places=2,max_digits=7,verbose_name='Valor')
    descricao = models.CharField(max_length=30,blank=True, verbose_name='Descrição')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
        ordering = ['-pagamento__data', 'tipo_despesa', '-valor']
    def data(self):
        return self.pagamento.data
    data.short_description = 'Data'
    data.boolean = False
    data.admin_order_field = '-pagamento__data'
    def string_valor(self):
        return currency(self.valor)
    string_valor =property(string_valor)
    def __unicode__(self):
        return 'Pe%s-%s-%s' % (self.codigo, self.pessoa.nome, self.string_valor)
    def __str__(self):
        return 'Pe%s-%s-%s' % (self.codigo, self.pessoa.nome, self.string_valor)
class Movimento_Estoque(models.Model):
    codigo = models.AutoField(primary_key=True)
    tipo_movimento = models.CharField(max_length=1, choices=TIPO_MOVIMENTO, default='1',verbose_name='Tipo Movimento')
    data = models.DateField(verbose_name=u"Data", default=timezone.now())
    produto = models.ForeignKey(Produto)
    qtd = models.DecimalField(decimal_places=2,max_digits=7,verbose_name=u"Quantidade",default=1)
    descricao = models.CharField(max_length=30, blank=True, verbose_name='Descrição')
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Movimento Estoque'
        verbose_name_plural = 'Movimentos Estoque'
        ordering = ['-data', 'tipo_movimento', 'produto']
    def __unicode__(self):
        return 'Es%s-%s-%s-%s' % (self.codigo, self.data, TIPO_MOVIMENTO[int(self.tipo_movimento)][1], self.produto.descricao)
    def __str__(self):
        return 'Es%s-%s-%s-%s' % (self.codigo, self.data, TIPO_MOVIMENTO[int(self.tipo_movimento)][1], self.produto.descricao)
class Transferencia(models.Model):
    numero = models.CharField(max_length=20, blank=True, verbose_name=u"Número")
    data = models.DateField(verbose_name=u"Data", default=timezone.now())
    de = models.CharField(choices=FONTE,max_length=1, default='0',verbose_name='De')
    a = models.CharField(choices=FONTE,max_length=1, default='0',verbose_name='A')
    valor = models.DecimalField(decimal_places=2,max_digits=7,verbose_name='Valor')
    descricao = models.CharField(max_length=50, blank=True, verbose_name='Descrição')
    texto_extrato = models.CharField(max_length=30, verbose_name='Texto Extrato', blank=True)
    verificado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=u"Data criação")
    data_modificacao = models.DateTimeField(auto_now=True,editable=False,verbose_name=u"Data Modificação")
    class Meta:
        verbose_name = 'Transferência/Depósito'
        verbose_name_plural = 'Transferências/Depósitos'
        ordering = ['-data', 'de', 'a', '-valor']
    def string_valor(self):
        return currency(self.valor)
    string_valor =property(string_valor)
    def clean(self):
        if self.de == self.a:
            raise ValidationError('Fonte De não pode ser igual a fonte A')
    def __unicode__(self):
        return 'Tr%s-%s-%s-%s' % (self.data, FONTE[int(self.de)][1], FONTE[int(self.a)][1], self.descricao)
    def __str__(self):
        return 'Tr%s-%s-%s-%s' % (self.data, FONTE[int(self.de)][1], FONTE[int(self.a)][1], self.descricao)














